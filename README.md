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

## 📂 Project Structure

├── cashflow_pipeline.py # Main pipeline code
├── customer0001_cashflow.csv # Example input data
├── inflow_forecast.csv # Generated forecast (inflow)
├── outflow_forecast.csv # Generated forecast (outflow)
└── README.md # Project documentation


---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

Create a virtual environment (recommended):
