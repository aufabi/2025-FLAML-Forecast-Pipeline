# 🏦 Cashflow Forecasting Pipeline with Prefect & FLAML

This project implements an **automated cashflow forecasting pipeline** using:

- [FLAML](https://microsoft.github.io/FLAML/) for lightweight AutoML forecasting  
- [Prefect](https://docs.prefect.io/) for orchestration and task/flow management  
- [Joblib](https://joblib.readthedocs.io/) for model saving  
- [Pandas](https://pandas.pydata.org/) for data preprocessing  

The pipeline performs:
1. Preprocessing of raw cashflow data  
2. Training separate inflow & outflow forecasting models  
3. Generating **batch predictions** for the next 180 days  
4. Saving both models and forecast outputs to disk  

---

## ⚙️ Installation

Clone the repository:

```
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

Create a virtual environment (recommended):

```
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

Install dependencies:

```
pip install -r requirements.txt
```

Or install them manually:

```
pip install pandas joblib flaml prefect

```

---

# 🚀 Usage
## 1. Run the Pipeline Locally

You can run the full pipeline with:

```
python cashflow_pipeline.py
```

This will:
- Preprocess the input customer0001_cashflow.csv
- Train models for cash_inflow and cash_outflow
- Save models (inflow_model.pkl, outflow_model.pkl)
- Save predictions (inflow_forecast.csv, outflow_forecast.csv)

## 2. Using Prefect
**Install Prefect**

Prefect is already in the requirements, but if not:
```
pip install prefect
```

**Run Prefect Flow**

The code is written using Prefect's @flow and @task decorators. To run:
```
python cashflow_pipeline.py
```

You’ll see Prefect manage the execution of each step in the flow.

**Monitor with Prefect Orion UI**

Prefect comes with a built-in UI:
```
prefect orion start
```

---

# 📊 Example Output

- **Inflow Forecast (inflow_forecast.csv)**
```csv
date,cash_inflow
2025-09-13,12345.67
2025-09-14,12012.34
...
```

- **Outflow Forecast (outflow_forecast.csv)**
```csv
date,cash_outflow
2025-09-13,9876.54
2025-09-14,10023.45
...
```

---

# 🛠️ Customization

- Change input file:
```
run_pipeline(data_path="your_file.csv")
```

- Adjust forecast horizon (default 180 days):
```
forecast_next(inflow_model, inflow_df, horizon=90)
```

---

# 📌 Requirements

- Python 3.8+
- Pandas
- Joblib
- FLAML
- Prefect
