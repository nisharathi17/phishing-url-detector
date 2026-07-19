from urllib import request

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path

from src.feature_extractor import extract_features
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "random_forest.pkl"

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")
app = FastAPI()


class URLRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {
        "message": "Welcome to the URL Classifier API!"
    }


@app.post("/predict")
def predict(request: URLRequest):

    features = extract_features(request.url)

    X = pd.DataFrame([features])

    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]

    confidence = float(max(probabilities))

    return {
    "url": request.url,
    "prediction": prediction,
    "confidence": round(confidence * 100, 2)
    }