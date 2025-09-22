# ml/optimize_schedule.py

import pandas as pd
import numpy as np
import os
from ortools.sat.python import cp_model

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load datasets
workers = pd.read_csv("data/workers.csv")
drivers = pd.read_csv("data/drivers.csv")
workplaces = pd.read_csv("data/workplaces.csv")
shifts = pd.read_csv("data/shifts.csv")

print("✅ Data loaded")

# Small sample for prototype (to keep solver light)
workers = workers.sample(50, random_state=42).reset_index(drop=True)
drivers = drivers.sample(10, random_state=42).reset_index(drop=True)
workplaces = workplaces.sample(5, random_state=42).reset_index(drop=True)
shifts = shifts.sample(5, random_state=42).reset_index(drop=True)


print(f"Using {len(workers)} workers, {len(drivers)} drivers, {len(workplaces)} workplaces, {len(shifts)} shifts")

# 2. Distance function (approximate)
def distance(lat1, lon1, lat2, lon2):
    return np.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

# Precompute distances worker → workplace
dist_matrix = {}
for i, w in workers.iterrows():
    for j, wp in workplaces.iterrows():
        dist_matrix[(i, j)] = distance(w["Latitude"], w["Longitude"], wp["Latitude"], wp["Longitude"])

# 3. Optimization model
model = cp_model.CpModel()

# Variables: assign worker i to workplace j in shift s with driver d
assign = {}
for wi in range(len(workers)):
    for di in range(len(drivers)):
        for wpi in range(len(workplaces)):
            for si in range(len(shifts)):
                assign[(wi, di, wpi, si)] = model.NewBoolVar(f"assign_w{wi}_d{di}_wp{wpi}_s{si}")

# 4. Constraints

# Each worker can only be assigned once per shift
for wi in range(len(workers)):
    for si in range(len(shifts)):
        model.Add(sum(assign[(wi, di, wpi, si)] for di in range(len(drivers)) for wpi in range(len(workplaces))) <= 1)

# Driver capacity respected per shift
for di, driver in drivers.iterrows():
    for si in range(len(shifts)):
        model.Add(sum(assign[(wi, di, wpi, si)] for wi in range(len(workers)) for wpi in range(len(workplaces)))
                  <= driver["VehicleCapacity"])

# Cada shift debe tener al menos un worker asignado
for si in range(len(shifts)):
    model.Add(sum(assign[(wi, di, wpi, si)] 
                  for wi in range(len(workers)) 
                  for di in range(len(drivers)) 
                  for wpi in range(len(workplaces))) >= 1)

# Cada driver debe llevar al menos un trabajador en total (para que no queden todos vacíos)
for di in range(len(drivers)):
    model.Add(sum(assign[(wi, di, wpi, si)] 
                  for wi in range(len(workers)) 
                  for wpi in range(len(workplaces)) 
                  for si in range(len(shifts))) >= 1)
    
# 5. Objective: minimize total distance
objective_terms = []
for wi, worker in workers.iterrows():
    for di in range(len(drivers)):
        for wpi, wp in workplaces.iterrows():
            for si in range(len(shifts)):
                objective_terms.append(assign[(wi, di, wpi, si)] * int(dist_matrix[(wi, wpi)] * 1000))

model.Minimize(sum(objective_terms))

# 6. Solve
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 15
status = solver.Solve(model)

# 7. Collect results
rows = []
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for wi, worker in workers.iterrows():
        for di, driver in drivers.iterrows():
            for wpi, wp in workplaces.iterrows():
                for si, shift in shifts.iterrows():
                    if solver.Value(assign[(wi, di, wpi, si)]) == 1:
                        rows.append({
                            "WorkerID": worker["WorkerID"],
                            "DriverID": driver["DriverID"],
                            "WorkplaceID": wp["WorkplaceID"],
                            "ShiftID": shift["ShiftID"],
                            "Distance": round(dist_matrix[(wi, wpi)], 4)
                        })

    if rows:
        df_result = pd.DataFrame(rows)
        df_result.to_csv(f"{OUTPUT_DIR}/optimized_assignments.csv", index=False)
        print(f"✅ Optimized assignments saved to {OUTPUT_DIR}/optimized_assignments.csv with {len(df_result)} rows")
    else:
        print("⚠️ Solver found a solution but no assignments were made.")
else:
    print("❌ No feasible solution found.")

