# ml/predict_absences.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
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
# - Gender (categorical)
# - Skills (multi-label → one-hot expand)
# - Availability (numeric)
features = pd.DataFrame()

# Encode gender
features["Gender"] = data["Gender"]

# Expand availability
availability_cols = [c for c in data.columns if "Available_" in c]
features[availability_cols] = data[availability_cols]

# Expand skills (split by comma)
skills_expanded = data["Skills"].str.get_dummies(sep=",")
features = pd.concat([features, skills_expanded], axis=1)

# 5. One-hot encode categorical
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
gender_encoded = encoder.fit_transform(features[["Gender"]])
gender_df = pd.DataFrame(gender_encoded, columns=encoder.get_feature_names_out(["Gender"]))
features = pd.concat([features.drop(columns=["Gender"]).reset_index(drop=True),
                      gender_df], axis=1)

# 6. Split data
X = features
y = data["AbsentFlag"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 7. Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 8. Evaluate
y_pred = model.predict(X_test)
print("\n--- Classification Report ---")
print(classification_report(y_test, y_pred))

# 9. Save model
joblib.dump(model, f"{OUTPUT_DIR}/absence_model.pkl")
print(f"✅ Model saved to {OUTPUT_DIR}/absence_model.pkl")
