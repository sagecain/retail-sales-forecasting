# -*- coding: utf-8 -*-
"""
Retail Sales Forecasting (UCI Online Retail)
- Loads Excel from data/
- Cleans & aggregates monthly revenue
- Trains seasonal SARIMAX
- Forecasts Test period
- Saves plots + CSV into results/
"""

import os, warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings("ignore")
plt.rcParams["figure.figsize"] = (10, 5)

# ========= USER SETTINGS =========
# Path to Excel file inside data/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "Online Retail.xlsx")

# Optional: filter by country, e.g. "United Kingdom". Use "" for all.
COUNTRY = "United Kingdom"

# Model settings
ORDER = (1, 1, 1)
SEASONAL_ORDER = (1, 1, 1, 12)

# Output folder (relative to script)
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)
# =================================


def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at: {path}")
    df = pd.read_excel(path, engine="openpyxl")
    return df


def clean_and_aggregate(df: pd.DataFrame, country: str = "") -> pd.DataFrame:
    df = df.dropna(subset=["InvoiceNo", "StockCode", "Description",
                           "Quantity", "InvoiceDate", "UnitPrice"])

    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    if country and "Country" in df.columns:
        df = df[df["Country"] == country]

    monthly = (df.set_index("InvoiceDate")
                 .resample("MS")["Revenue"]
                 .sum()
                 .to_frame("Revenue"))
    monthly = monthly.loc[monthly["Revenue"] > 0]

    if monthly.empty:
        raise ValueError("Monthly revenue series is empty after cleaning.")
    return monthly


def time_split(series: pd.Series, test_ratio: float = 0.2):
    n = len(series)
    split_idx = max(1, int(n * (1 - test_ratio)))
    return series.iloc[:split_idx], series.iloc[split_idx:]


def fit_sarimax(train: pd.Series, order, seasonal_order):
    model = SARIMAX(train,
                    order=order,
                    seasonal_order=seasonal_order,
                    enforce_stationarity=False,
                    enforce_invertibility=False)
    return model.fit(disp=False)


def evaluate_and_plot(train, test, pred):
    mae = mean_absolute_error(test, pred)
    rmse = mean_squared_error(test, pred, squared=False)

    # Train/Test plot
    ax = train.plot(label="Train")
    test.plot(ax=ax, label="Test")
    ax.set_title("Monthly Revenue (Train/Test)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "train_test_plot.png"), dpi=150)
    plt.close()

    # Forecast vs Actual
    ax = train.plot(label="Train")
    test.plot(ax=ax, label="Actual")
    pred.plot(ax=ax, label="Forecast")
    ax.set_title(f"Forecast vs Actual | MAE={mae:,.0f} RMSE={rmse:,.0f}")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "monthly_sales.png"), dpi=150)
    plt.close()

    return mae, rmse


def residual_diagnostics(res):
    res.plot_diagnostics(figsize=(12, 8))
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "sarimax_diagnostics.png"), dpi=150)
    plt.close()


def main():
    print("Loading data...")
    df = load_data(DATA_PATH)
    print(f"Raw rows: {len(df):,}")

    print("Cleaning & aggregating...")
    monthly = clean_and_aggregate(df, country=COUNTRY)
    print(f"Monthly periods: {len(monthly)} "
          f"({monthly.index.min().date()} → {monthly.index.max().date()})")

    train, test = time_split(monthly["Revenue"], test_ratio=0.2)
    print(f"Train size: {len(train)}, Test size: {len(test)}")

    print("Fitting SARIMAX...")
    res = fit_sarimax(train, ORDER, SEASONAL_ORDER)
    print(res.summary())

    fc = res.get_forecast(steps=len(test))
    pred = fc.predicted_mean
    pred.index = test.index

    mae, rmse = evaluate_and_plot(train, test, pred)
    print(f"MAE: {mae:,.2f}, RMSE: {rmse:,.2f}")

    residual_diagnostics(res)

    out = pd.DataFrame({"actual": test, "forecast": pred})
    out.to_csv(os.path.join(RESULTS_DIR, "forecast_vs_actual.csv"))
    print(f"Results saved to {RESULTS_DIR}")

    print("\nTop 5 months by revenue:")
    print(monthly.sort_values("Revenue", ascending=False).head(5))

    print("\nMonthly revenue stats:")
    print(monthly["Revenue"].describe().round(2))


if __name__ == "__main__":
    main()
