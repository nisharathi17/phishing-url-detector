from fastapi import FastAPI
from pydantic import BaseModel

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
    return {
        "received_url": request.url
    }