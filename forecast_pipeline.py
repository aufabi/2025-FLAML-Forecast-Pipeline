from prefect import flow, task
import pandas as pd
import joblib
from datetime import timedelta
from flaml import AutoML


# ----------------------------
# Shared tasks
# ----------------------------
@task
def preprocess(df, target_col):
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df = df[["date", target_col]]
    df = df.set_index("date").resample("D").mean().fillna(method="ffill").reset_index()
    return df

@task
def train_forecast(df, target_col, model_path):
    automl = AutoML()
    settings = {
        "time_budget": 600,
        "metric": "mape",
        "task": "ts_forecast",
        "log_file_name": f"training_{target_col}.log",
        "eval_method": "auto",
        "seed": 7654321,
    }
    automl.fit(dataframe=df, label=target_col, period=180, **settings)
    joblib.dump(automl, model_path)
    print(f"Model for {target_col} saved at {model_path}")
    return automl

@task
def forecast_next(automl, df, horizon=180, save_path="forecast.csv"):
    last_date = df["date"].max()
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=horizon, freq="D")
    y_pred = automl.predict(future_dates.to_frame(name="date"))
    forecast_df = pd.DataFrame({"date": future_dates, "forecast": y_pred})
    forecast_df.to_csv(save_path, index=False)
    print(f"Forecast saved at {save_path}")
    return forecast_df


# ----------------------------
# Full Pipeline
# ----------------------------
@flow(name="Cashflow Forecasting Pipeline")
def run_pipeline(data_path="customer0001_cashflow.csv"):
    print("Starting pipeline...")
    data = pd.read_csv(data_path)

    # Inflow tasks
    inflow_df_future = preprocess.submit(data, "cash_inflow")
    inflow_model_future = train_forecast.submit(inflow_df_future, "cash_inflow", "inflow_model.pkl")
    inflow_forecast_future = forecast_next.submit(inflow_model_future, inflow_df_future, save_path="inflow_forecast.csv")

    # Outflow tasks
    outflow_df_future = preprocess.submit(data, "cash_outflow")
    outflow_model_future = train_forecast.submit(outflow_df_future, "cash_outflow", "outflow_model.pkl")
    outflow_forecast_future = forecast_next.submit(outflow_model_future, outflow_df_future, save_path="outflow_forecast.csv")

    # Wait for completion
    inflow_result = inflow_forecast_future.result()
    outflow_result = outflow_forecast_future.result()

    print("Pipeline completed.")
    return inflow_result, outflow_result


if __name__ == "__main__":
    run_pipeline()
