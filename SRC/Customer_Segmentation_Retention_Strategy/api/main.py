from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import uvicorn
from pathlib import Path

app = FastAPI(title="Customer Churn Prediction App API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])



def load_model():
    project_root = Path(__file__).parent.parent.parent.parent  
    model_path = project_root / "model" / "model.joblib"

    model_dict = joblib.load(model_path)
    return model_dict['model']


class CustomerFeatures(BaseModel):
    Frequency: float
    Monetary: float
    Total_Products_Purchased: int
    Unique_Products_Purchased: int
    Avg_Transaction_Value: float
    Customer_Tenure_Days: int
    Revenue_Per_Product: float
    Avg_Days_Between_Purchases: float
    Purchase_Regularity: float
    Top_Product_Concentration: float
    Category_Diversity: float
    Quarterly_Spending_Trend: float
    Price_Sensitivity: float
    Spending_Trend: float
    Cancellation_Rate: float
    Is_UK: int


@app.post("/predict/churn")
async def predict_churn(features: CustomerFeatures):

    input_df = pd.DataFrame([features.dict()])

    model = load_model()
    prediction = model.predict(input_df)[0]
    churn_label = "Churn" if prediction == 1 else "Not Churn"

    return {
        "prediction": int(prediction),
        "label": churn_label
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)