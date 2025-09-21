# ml/generate_workers.py

import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()

# PARAMETERS
NUM_WORKERS = 800
NUM_ZONES = 4
CITY_CENTERS = [
    (52.3728, 4.8936),  # Centrum
    (52.3400, 4.8885),  # Zuid
    (52.4000, 4.9166),  # Noord
    (52.3870, 4.8357),  # Sloterdijk
]

SKILL_POOL = ["Welding", "Assembly", "Packaging", "Logistics", "Admin", "QA", "Forklift"]

def generate_worker(i):
    gender = random.choice(["Male", "Female"])
    name = fake.name_male() if gender == "Male" else fake.name_female()

    # Choose a base location (cluster center) and add noise
    base_lat, base_lon = random.choice(CITY_CENTERS)
    lat = base_lat + np.random.normal(0, 0.01)
    lon = base_lon + np.random.normal(0, 0.01)

    # Select 2-3 skills
    skills = random.sample(SKILL_POOL, k=random.randint(2, 3))

    # Availability: 0 or 1 for each weekday (Mon–Sun)
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

def generate_workers(n=NUM_WORKERS):
    return pd.DataFrame([generate_worker(i) for i in range(n)])

if __name__ == "__main__":
    OUTPUT_DIR = "data"		# share file with the host
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = generate_workers()
    df.to_csv(f"{OUTPUT_DIR}/workers.csv", index=False)
    print("✅ workers.csv generated with", len(df), "entries.")

