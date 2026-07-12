import joblib
import pandas as pd
from pathlib import Path

from feature_extractor import extract_features

# -----------------------------
# Load trained model
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "random_forest.pkl"

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!\n")

# -----------------------------
# Get URL from user
# -----------------------------
url = input("Enter URL: ").strip()

if not url:
    print("Error: URL cannot be empty.")
    exit()

# Remove protocol for consistency with training data
url = url.replace("https://", "").replace("http://", "")

# -----------------------------
# Extract features
# -----------------------------
features = extract_features(url)

# Convert dictionary to DataFrame
X = pd.DataFrame([features])

# -----------------------------
# Predict
# -----------------------------
prediction = model.predict(X)[0]

# Prediction confidence
probabilities = model.predict_proba(X)[0]
confidence = max(probabilities) * 100

# -----------------------------
# Display results
# -----------------------------
print("\n==============================")
print("Prediction Results")
print("==============================")
print(f"URL         : {url}")
print(f"Prediction  : {prediction}")
print(f"Confidence  : {confidence:.2f}%")