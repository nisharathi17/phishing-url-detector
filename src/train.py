import pandas as pd
from feature_extractor import extract_features
from sklearn.model_selection import train_test_split
df = pd.read_csv("data/urls.csv")
features = []
for url in df["url"]:
    features.append(extract_features(url))
X = pd.DataFrame(features)
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, predictions)

from sklearn.metrics import classification_report
print(classification_report(y_test, predictions))
print("Accuracy:", accuracy)

for feature, importance in zip(
    X.columns,
    model.feature_importances_
):
    print(f"{feature}: {importance:.4f}")