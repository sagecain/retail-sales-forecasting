🛒 Retail Sales Forecasting

This project applies time series forecasting to retail sales data (UCI Online Retail dataset). The goal is to model monthly sales trends and predict future demand using SARIMA.

📊 Dataset

Source: UCI Online Retail Dataset

Filtered to monthly aggregates of sales revenue.

Data prepared in data/Online Retail.xlsx.

⚙️ Workflow

Data Cleaning & Aggregation

Converted invoice dates to monthly periods

Removed returns/cancellations

Aggregated by monthly sales

Exploratory Analysis

Monthly sales trend visualization (monthly_sales.png)

Train/Test Split

80/20 split into training vs. test set

Visualization saved as train_test_plot.png

Modeling (SARIMA)

Candidate SARIMA models fit with statsmodels

Best model selected via lowest AIC

Forecasting

Predictions vs. actual values exported to forecast_vs_actual.csv

📉 Results

Forecasts generally capture the overall sales trend.

Small dataset length limits model complexity.

Output files:

results/monthly_sales.png – historical sales

results/train_test_plot.png – train/test split

results/forecast_vs_actual.csv – numerical results

🔍 Diagnostics

Because the dataset slice used here had only 11 months of sales history, the standard SARIMA diagnostic routine (res.plot_diagnostics) could not be applied — it requires longer time series to validate assumptions.

Instead, a custom lightweight diagnostic visualization was created and saved as:

results/custom_diagnostics.png


This diagnostic includes:

Residuals over time (check for patterns)

Residual histogram (check approximate normality)

Residual autocorrelation function (ACF), trimmed to the available data

While limited, these diagnostics still provide a basic check on model fit. For larger datasets (e.g., multiple years or all countries), the full SARIMA diagnostics can be run without modification.

🚀 Next Steps

Extend analysis with longer sales history

Compare SARIMA with Prophet, XGBoost, and LSTM

Deploy forecasts in an interactive dashboard (e.g., Power BI or Streamlit)
