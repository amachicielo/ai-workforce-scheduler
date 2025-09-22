# ml/visualize_schedule.py

import pandas as pd
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "data/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load datasets
assignments = pd.read_csv("data/optimized_assignments.csv")
workers = pd.read_csv("data/workers.csv")
drivers = pd.read_csv("data/drivers.csv")
workplaces = pd.read_csv("data/workplaces.csv")

print("✅ Data loaded for visualization")

# Merge assignments with coordinates
merged = assignments.merge(workers[["WorkerID", "Latitude", "Longitude"]], on="WorkerID")
merged = merged.merge(workplaces[["WorkplaceID", "Latitude", "Longitude"]], on="WorkplaceID", suffixes=("_worker", "_workplace"))
merged = merged.merge(drivers[["DriverID"]], on="DriverID")

# 2. Plot base
plt.figure(figsize=(8, 6))

# Workers
plt.scatter(workers["Longitude"], workers["Latitude"], c="blue", label="Workers", alpha=0.6, s=20)

# Workplaces
plt.scatter(workplaces["Longitude"], workplaces["Latitude"], c="red", marker="*", label="Workplaces", s=120)

# Drivers (just to show, positions not tracked → random small offset near workers)
plt.scatter(workers.sample(len(drivers), random_state=42)["Longitude"] + 0.001,
            workers.sample(len(drivers), random_state=42)["Latitude"] + 0.001,
            c="green", marker="^", label="Drivers", s=80)

# Connections: worker → workplace
for _, row in merged.iterrows():
    plt.plot([row["Longitude_worker"], row["Longitude_workplace"]],
             [row["Latitude_worker"], row["Latitude_workplace"]],
             c="gray", alpha=0.3, linewidth=0.7)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Optimized Worker Assignments (Workers → Workplaces)")
plt.legend()
plt.grid(True)

# 3. Save plot
plot_path = f"{OUTPUT_DIR}/optimized_routes.png"
plt.savefig(plot_path)
print(f"✅ Visualization saved at {plot_path}")
