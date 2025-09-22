# ml/eda.py

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os

OUTPUT_DIR = "data/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load datasets
workers = pd.read_csv("data/workers.csv")
assignments = pd.read_csv("data/assignments.csv")

print("✅ Workers loaded:", workers.shape)
print("✅ Assignments loaded:", assignments.shape)

# 2. Basic statistics
print("\n--- Gender distribution ---")
print(workers["Gender"].value_counts(normalize=True) * 100)

# Count skills (split by comma)
all_skills = []
for skills in workers["Skills"]:
    all_skills.extend(skills.split(","))
skills_series = pd.Series(all_skills)

print("\n--- Top Skills ---")
print(skills_series.value_counts())

# Availability summary
availability_cols = [col for col in workers.columns if "Available_" in col]
availability_summary = workers[availability_cols].mean() * 100
print("\n--- Availability by day (%) ---")
print(availability_summary)

# 3. Clustering by location
coords = workers[["Latitude", "Longitude"]]
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
workers["Cluster"] = kmeans.fit_predict(coords)

# Save workers with cluster assignment
workers.to_csv("data/workers_clustered.csv", index=False)
print("✅ workers_clustered.csv saved")

# 4. Plot clusters
plt.figure(figsize=(8, 6))
for cluster_id in workers["Cluster"].unique():
    cluster_data = workers[workers["Cluster"] == cluster_id]
    plt.scatter(cluster_data["Longitude"], cluster_data["Latitude"], label=f"Cluster {cluster_id}", alpha=0.6)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Workers Clusters (KMeans)")
plt.legend()
plt.grid(True)
plt.savefig(f"{OUTPUT_DIR}/workers_clusters.png")
print(f"✅ Cluster plot saved at {OUTPUT_DIR}/workers_clusters.png")
