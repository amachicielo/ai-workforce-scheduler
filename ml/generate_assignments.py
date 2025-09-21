# ml/generate_assignments.py

import pandas as pd
import random
import os

# PARAMETERS
WORKERS_PER_SHIFT = (5, 15)   # min-max
ABSENCE_RATE = 0.1

def generate_assignments():
    # Load datasets
    workers = pd.read_csv("data/workers.csv")
    drivers = pd.read_csv("data/drivers.csv")
    workplaces = pd.read_csv("data/workplaces.csv")
    shifts = pd.read_csv("data/shifts.csv")

    rows = []
    assignment_id = 1

    for _, shift in shifts.iterrows():
        # pick a random workplace
        workplace = workplaces.sample(1).iloc[0]

        # pick random workers
        n_workers = random.randint(*WORKERS_PER_SHIFT)
        selected_workers = workers.sample(n_workers)

        # pick driver(s) according to capacity
        driver = drivers.sample(1).iloc[0]
        capacity = driver["VehicleCapacity"]

        # split workers into vehicle loads
        for i, (_, worker) in enumerate(selected_workers.iterrows()):
            status = "Assigned"
            if random.random() < ABSENCE_RATE:
                status = "Absent"

            rows.append({
                "AssignmentID": f"A{assignment_id:05d}",
                "WorkerID": worker["WorkerID"],
                "DriverID": driver["DriverID"],
                "WorkplaceID": workplace["WorkplaceID"],
                "ShiftID": shift["ShiftID"],
                "Status": status
            })
            assignment_id += 1

    return pd.DataFrame(rows)

if __name__ == "__main__":
    OUTPUT_DIR = "data"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = generate_assignments()
    df.to_csv(f"{OUTPUT_DIR}/assignments.csv", index=False)
    print("✅ assignments.csv generated with", len(df), "entries.")
