# ml/predict_absences.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load datasets
workers = pd.read_csv("data/workers.csv")
assignments = pd.read_csv("data/assignments.csv")

print("✅ Workers loaded:", workers.shape)
print("✅ Assignments loaded:", assignments.shape)

# 2. Merge on WorkerID
data = assignments.merge(workers, on="WorkerID", how="left")

# 3. Prepare target variable
data["AbsentFlag"] = (data["Status"] == "Absent").astype(int)

# 4. Feature engineering
features = pd.DataFrame()

# Gender
features["Gender"] = data["Gender"]

# Availability
availability_cols = [c for c in data.columns if "Available_" in c]
features[availability_cols] = data[availability_cols]

# Skills (expand to one-hot)
skills_expanded = data["Skills"].str.get_dummies(sep=",")
features = pd.concat([features, skills_expanded], axis=1)

# One-hot encode Gender
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
gender_encoded = encoder.fit_transform(features[["Gender"]])
gender_df = pd.DataFrame(gender_encoded, columns=encoder.get_feature_names_out(["Gender"]))
features = pd.concat([features.drop(columns=["Gender"]).reset_index(drop=True),
                      gender_df], axis=1)

# Train/test split
X = features
y = data["AbsentFlag"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

results = []

# 5. Logistic Regression (balanced)
logreg = LogisticRegression(max_iter=1000, class_weight="balanced")
logreg.fit(X_train, y_train)
y_pred_log = logreg.predict(X_test)
report_log = classification_report(y_test, y_pred_log, output_dict=True)
results.append(("Logistic Regression", report_log))
joblib.dump(logreg, f"{OUTPUT_DIR}/absence_model_logreg.pkl")

# 6. Random Forest
rf = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
report_rf = classification_report(y_test, y_pred_rf, output_dict=True)
results.append(("Random Forest", report_rf))
joblib.dump(rf, f"{OUTPUT_DIR}/absence_model_rf.pkl")

# 7. Print & Save metrics
metrics_file = os.path.join(OUTPUT_DIR, "absence_metrics.txt")
with open(metrics_file, "w") as f:
    for name, report in results:
        print(f"\n--- {name} ---")
        print(classification_report(y_test, logreg.predict(X_test) if name=="Logistic Regression" else rf.predict(X_test)))
        f.write(f"--- {name} ---\n")
        f.write(classification_report(y_test, logreg.predict(X_test) if name=="Logistic Regression" else rf.predict(X_test)))
        f.write("\n\n")

print(f"✅ Metrics saved to {metrics_file}")
print("✅ Models saved: absence_model_logreg.pkl, absence_model_rf.pkl")
