import os
import joblib
import pandas as pd
from datetime import timedelta
from flaml import AutoML
from prefect import flow, task

# ----------------------------
# Step 1: Preprocessing
# ----------------------------
@task
def preprocess(df, target_col):
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df = df[["date", target_col]]

    # Ensure daily frequency
    df = df.set_index("date").resample("D").mean().fillna(method="ffill").reset_index()
    return df


# ----------------------------
# Step 2: Train FLAML Forecasting Model
# ----------------------------
@task
def train_forecast(df, target_col, model_path):
    automl = AutoML()
    settings = {
        "time_budget": 600,
        "metric": "mape",
        "task": "ts_forecast",
        "log_file_name": "training_forecast.log",
        "eval_method": "auto",
        "seed": 7654321, 
    }
    
    automl.fit(dataframe=df, label=target_col, period=180, **settings)
    joblib.dump(automl, model_path)
    print(f"✅ Model for {target_col} saved at {model_path}")
    return automl


# ----------------------------
# Step 3: Batch Prediction
# ----------------------------
@task
def forecast_next(automl, df, horizon=180):
    last_date = df["date"].max()
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=horizon, freq="D")

    y_pred = automl.predict(future_dates.to_frame(name="date"))
    forecast_df = pd.DataFrame({"date": future_dates, "forecast": y_pred})
    return forecast_df


# ----------------------------
# Step 4: Full Pipeline
# ----------------------------
@flow(name="Cashflow Forecasting Pipeline")
def run_pipeline(data_path="customer0001_cashflow.csv"):
    print("🚀 Starting pipeline...")

    data = pd.read_csv(data_path)

    # Inflow
    inflow_df = preprocess(data, "cash_inflow")
    inflow_model = train_forecast(inflow_df, "cash_inflow", "inflow_model.pkl")
    inflow_forecast = forecast_next(inflow_model, inflow_df)
    inflow_forecast.to_csv("inflow_forecast.csv", index=False)
    print("📈 Inflow forecast saved.")

    # Outflow
    outflow_df = preprocess(data, "cash_outflow")
    outflow_model = train_forecast(outflow_df, "cash_outflow", "outflow_model.pkl")
    outflow_forecast = forecast_next(outflow_model, outflow_df)
    outflow_forecast.to_csv("outflow_forecast.csv", index=False)
    print("📉 Outflow forecast saved.")

    print("✅ Pipeline completed.\n")


if __name__ == "__main__":
    run_pipeline()