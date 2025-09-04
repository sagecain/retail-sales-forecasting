# 🛒 Retail Sales Forecasting (Python)

This project forecasts **monthly retail revenue** using the [UCI Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online+retail).  
The goal is to demonstrate time series forecasting skills applied to real-world retail sales data.

---

## 📂 Project Structure
retail-sales-forecasting/
├── data/ # Raw dataset (not committed)
├── notebooks/
│ └── retail_forecasting.ipynb # Jupyter notebook (data cleaning, modeling, results)
├── results/ # Saved plots and outputs
│ ├── monthly_sales.png
│ ├── train_test_plot.png
│ └── sarimax_diagnostics.png
└── README.md


---

## 📊 Methods
- Data cleaning: removed returns, negative values, missing IDs  
- Aggregated daily sales into **monthly revenue**  
- Train/test split (chronological 80/20)  
- Seasonal **SARIMAX model** with 12-month seasonality  
- Evaluated using **MAE** and **RMSE**  

---

## 📷 Results
### Forecast vs Actual
![Forecast vs Actual](results/monthly_sales.png)

### Train/Test Split
![Train/Test Split](results/train_test_plot.png)

### Diagnostics
![SARIMAX Diagnostics](results/sarimax_diagnostics.png)

---

## ⚙️ Tools
- Python (pandas, matplotlib, statsmodels)  
- Jupyter Notebook  
- GitHub for version control & portfolio  

---

## 📌 Dataset
- UCI Machine Learning Repository — [Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)  
- Transactions between Dec 2010–Dec 2011 for a UK-based retailer  
- Variables: InvoiceNo, StockCode, Quantity, InvoiceDate, UnitPrice, CustomerID, Country  

---

## 🚀 How to Run
1. Clone the repo:  
   ```bash
   git clone https://github.com/<your-username>/retail-sales-forecasting.git
   cd retail-sales-forecasting
2. Place the dataset in data/Online Retail.xlsx
3. Open the notebook: jupyter notebook notebooks/retail_forecasting.ipynb
4. Run all cells to reproduce results.

Built by Sage Cain (2025)
Portfolio Project – Data Analytics & Forecasting
