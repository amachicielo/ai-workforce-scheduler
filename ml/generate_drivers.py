# ml/generate_drivers.py

import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()

# PARAMETERS
NUM_DRIVERS = 50
VEHICLE_CAPACITY_RANGE = (4, 15)
HOURS_RANGE = (6, 10)
ZONES = ["Centrum", "Zuid", "Noord", "Sloterdijk"]

def generate_driver(i):
    name = fake.name()
    capacity = random.randint(*VEHICLE_CAPACITY_RANGE)
    hours = random.randint(*HOURS_RANGE)
    preferred_zone = random.choice(ZONES)

    return {
        "DriverID": f"D{i:03d}",
        "Name": name,
        "VehicleCapacity": capacity,
        "MaxHoursPerDay": hours,
        "PreferredZone": preferred_zone
    }

def generate_drivers(n=NUM_DRIVERS):
    return pd.DataFrame([generate_driver(i) for i in range(n)])

if __name__ == "__main__":
    OUTPUT_DIR = "data"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = generate_drivers()
    df.to_csv(f"{OUTPUT_DIR}/drivers.csv", index=False)
    print("✅ drivers.csv generated with", len(df), "entries.")
