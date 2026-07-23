import joblib
import pandas as pd

from feature_extractor import extract_features

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import train_test_split

# Load dataset


df = pd.read_csv("data/urls.csv")

# Feature Extraction

features = []

for url in df["url"]:
    features.append(extract_features(url))

X = pd.DataFrame(features)
y = df["label"]

# Train/Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions

predictions = model.predict(X_test)


# Evaluation


accuracy = accuracy_score(y_test, predictions)

print("\nClassification Report\n")
print(classification_report(y_test, predictions))

print("Accuracy:", accuracy)


# -------------------------------
# Confusion Matrix
# -------------------------------

print("\nConfusion Matrix\n")

cm = confusion_matrix(y_test, predictions)

print(cm)


# -------------------------------
# Feature Importances
# -------------------------------

print("\nFeature Importances\n")

feature_importance = sorted(
    zip(X.columns, model.feature_importances_),
    key=lambda x: x[1],
    reverse=True
)

for feature, importance in feature_importance:
    print(f"{feature:25} {importance:.4f}")


# -------------------------------
# Save Model
# -------------------------------

joblib.dump(
    model,
    "models/random_forest.pkl"
)

print("\nModel saved successfully!")