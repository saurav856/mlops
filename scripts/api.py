from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI(title="Credit Card Default Prediction API")

model = pickle.load(open("models/best_model.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

class ClientData(BaseModel):
    LIMIT_BAL: float
    SEX: int
    EDUCATION: int
    MARRIAGE: int
    AGE: int
    PAY_0: int
    PAY_2: int
    PAY_3: int
    PAY_4: int
    PAY_5: int
    PAY_6: int
    BILL_AMT1: float
    BILL_AMT2: float
    BILL_AMT3: float
    BILL_AMT4: float
    BILL_AMT5: float
    BILL_AMT6: float
    PAY_AMT1: float
    PAY_AMT2: float
    PAY_AMT3: float
    PAY_AMT4: float
    PAY_AMT5: float
    PAY_AMT6: float

@app.get("/")
def root():
    return {"message": "Credit Card Default Prediction API is running"}

@app.post("/predict")
def predict(data: ClientData):
    features = np.array([[
        data.LIMIT_BAL, data.SEX, data.EDUCATION, data.MARRIAGE,
        data.AGE, data.PAY_0, data.PAY_2, data.PAY_3, data.PAY_4,
        data.PAY_5, data.PAY_6, data.BILL_AMT1, data.BILL_AMT2,
        data.BILL_AMT3, data.BILL_AMT4, data.BILL_AMT5, data.BILL_AMT6,
        data.PAY_AMT1, data.PAY_AMT2, data.PAY_AMT3, data.PAY_AMT4,
        data.PAY_AMT5, data.PAY_AMT6
    ]])
    scaled = scaler.transform(features)
    prediction = model.predict(scaled)[0]
    probability = model.predict_proba(scaled)[0][1]
    return {
        "prediction": int(prediction),
        "probability_of_default": round(float(probability), 4),
        "risk": "HIGH" if prediction == 1 else "LOW"
    }