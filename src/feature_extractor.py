import pandas as pd

df = pd.read_csv("data/urls.csv")

print(df.head())
print(df.shape)
print(df["label"].value_counts())