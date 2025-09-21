# ml/generate_all.py

import os
import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

# ========== PARAMETERS ==========
NUM_WORKERS = 800
NUM_DRIVERS = 50
NUM_WORKPLACES = 15
NUM_WEEKS = 2
WORKERS_PER_SHIFT = (5, 15)
ABSENCE_RATE = 0.1

# Amsterdam clusters
CITY_CENTERS = [
    (52.3728, 4.8936),  # Centrum
    (52.3400, 4.8885),  # Zuid
    (52.4000, 4.9166),  # Noord
    (52.3870, 4.8357),  # Sloterdijk
]

SKILL_POOL = ["Welding", "Assembly", "Packaging", "Logistics", "Admin", "QA", "Forklift"]
WORKPLACE_TYPES = ["Factory", "Office", "Warehouse", "Construction"]
SHIFTS = {
    "Morning": ("06:00", "14:00"),
    "Evening": ("14:00", "22:00"),
    "Night": ("22:00", "06:00")
}
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

OUTPUT_DIR = "data"


# ========== WORKERS ==========
def generate_workers(n=NUM_WORKERS):
    def gen_worker(i):
        gender = random.choice(["Male", "Female"])
        name = fake.name_male() if gender == "Male" else fake.name_female()
        base_lat, base_lon = random.choice(CITY_CENTERS)
        lat = base_lat + np.random.normal(0, 0.01)
        lon = base_lon + np.random.normal(0, 0.01)
        skills = random.sample(SKILL_POOL, k=random.randint(2, 3))
        availability = [random.choice([0, 1]) for _ in range(7)]
        return {
            "WorkerID": f"W{i:04d}",
            "Name": name,
            "Gender": gender,
            "Latitude": round(lat, 6),
            "Longitude": round(lon, 6),
            "Skills": ",".join(skills),
            "Available_Mon": availability[0],
            "Available_Tue": availability[1],
            "Available_Wed": availability[2],
            "Available_Thu": availability[3],
            "Available_Fri": availability[4],
            "Available_Sat": availability[5],
            "Available_Sun": availability[6],
        }

    return pd.DataFrame([gen_worker(i) for i in range(n)])


# ========== DRIVERS ==========
def generate_drivers(n=NUM_DRIVERS):
    def gen_driver(i):
        return {
            "DriverID": f"D{i:03d}",
            "Name": fake.name(),
            "VehicleCapacity": random.randint(4, 15),
            "MaxHoursPerDay": random.randint(6, 10),
            "PreferredZone": random.choice(["Centrum", "Zuid", "Noord", "Sloterdijk"])
        }

    return pd.DataFrame([gen_driver(i) for i in range(n)])


# ========== WORKPLACES ==========
def generate_workplaces(n=NUM_WORKPLACES):
    def gen_workplace(i):
        base_lat, base_lon = random.choice(CITY_CENTERS)
        lat = base_lat + np.random.normal(0, 0.01)
        lon = base_lon + np.random.normal(0, 0.01)
        return {
            "WorkplaceID": f"WP{i:03d}",
            "Name": fake.company(),
            "Type": random.choice(WORKPLACE_TYPES),
            "Latitude": round(lat, 6),
            "Longitude": round(lon, 6)
        }

    return pd.DataFrame([gen_workplace(i) for i in range(n)])


# ========== SHIFTS ==========
def generate_shifts(num_weeks=NUM_WEEKS):
    rows = []
    shift_id = 1
    for week in range(1, num_weeks + 1):
        for day in DAYS:
            for shift_type, (start, end) in SHIFTS.items():
                rows.append({
                    "ShiftID": f"S{shift_id:04d}",
                    "Week": week,
                    "Day": day,
                    "ShiftType": shift_type,
                    "StartTime": start,
                    "EndTime": end
                })
                shift_id += 1
    return pd.DataFrame(rows)


# ========== ASSIGNMENTS ==========
def generate_assignments(workers, drivers, workplaces, shifts):
    rows = []
    assignment_id = 1

    for _, shift in shifts.iterrows():
        workplace = workplaces.sample(1).iloc[0]
        n_workers = random.randint(*WORKERS_PER_SHIFT)
        selected_workers = workers.sample(n_workers)
        driver = drivers.sample(1).iloc[0]

        for _, worker in selected_workers.iterrows():
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


# ========== MAIN ==========
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    workers = generate_workers()
    workers.to_csv(f"{OUTPUT_DIR}/workers.csv", index=False)
    print("✅ workers.csv generated")

    drivers = generate_drivers()
    drivers.to_csv(f"{OUTPUT_DIR}/drivers.csv", index=False)
    print("✅ drivers.csv generated")

    workplaces = generate_workplaces()
    workplaces.to_csv(f"{OUTPUT_DIR}/workplaces.csv", index=False)
    print("✅ workplaces.csv generated")

    shifts = generate_shifts()
    shifts.to_csv(f"{OUTPUT_DIR}/shifts.csv", index=False)
    print("✅ shifts.csv generated")

    assignments = generate_assignments(workers, drivers, workplaces, shifts)
    assignments.to_csv(f"{OUTPUT_DIR}/assignments.csv", index=False)
    print("✅ assignments.csv generated")

    print("🎉 All datasets generated in ./data/")
