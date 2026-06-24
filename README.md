# AI-Powered Phishing & Malicious URL Classifier
## Project Overview
This project aims to detect and classify malicious URLs using Machine Learning. The objective is to identify whether a URL belongs to one of the following categories:

* Benign
* Phishing
* Malware
* Defacement

The project uses URL-based feature engineering and a Random Forest classifier to learn patterns associated with malicious websites.

## Current Progress

### Completed

* Dataset exploration and analysis
* URL feature extraction pipeline
* Random Forest model training
* Model evaluation and performance analysis
* Feature importance analysis

### In Progress

* Model persistence using Joblib
* URL prediction script
* FastAPI integration
* Threat intelligence integration (VirusTotal)

---

## Project Structure

phishing-url-detector/
│
├── data/
├── notebooks/
│   └── data_exploration.ipynb
│
├── src/
│   ├── feature_extractor.py
│   └── train.py
│
├── models/
├── requirements.txt
└── README.md


---

## Dataset Exploration

Initial analysis was performed in `data_exploration.ipynb`.

Observations:

* URL length varies significantly across classes.
* Malicious URLs tend to contain more special characters.
* Suspicious keywords appear frequently in phishing URLs.
* Certain dataset formatting patterns may influence classification performance.

---

## Features Used

Current model uses the following handcrafted URL features:

* URL length
* Dot count
* Hyphen count
* Digit count
* Slash count
* Question mark count
* Equal sign count
* @ symbol count
* Underscore count
* Suspicious keyword count
* HTTP prefix indicator

---

## Model

Algorithm:

* Random Forest Classifier

Training Pipeline:

1. Extract numerical features from URLs.
2. Convert features into a DataFrame.
3. Split dataset into training and testing sets.
4. Train Random Forest model.
5. Evaluate model performance.

---

## Current Results

Classification Performance:

* Accuracy: 92.87%
* Phishing Precision: 79%
* Phishing Recall: 73%
* Phishing F1 Score: 76%

These results were achieved using handcrafted URL features without external threat intelligence sources.

---

## Key Learning Outcomes

Through this project, I learned:

* Feature engineering for cybersecurity datasets
* Exploratory Data Analysis (EDA)
* Classification using Random Forests
* Model evaluation using Precision, Recall, and F1 Score
* Interpreting feature importance

---

## Next Steps

* Save trained model using Joblib
* Build prediction workflow
* Add domain-based features
* Add WHOIS and SSL-based features
* Integrate VirusTotal API
* Develop FastAPI endpoint
* Deploy the model as a web service

```
```







Feature: starts_with_http
Observation:
The starts_with_http feature has unusually high importance.
This may reflect dataset formatting differences rather than intrinsic URL maliciousness.
Future versions should validate this feature on independent datasets.

Note:
This feature may partially reflect dataset formatting rather than intrinsic URL characteristics. It should be re-evaluated when using other datasets.