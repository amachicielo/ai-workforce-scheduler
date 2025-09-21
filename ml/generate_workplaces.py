# ml/generate_workplaces.py

import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()

# PARAMETERS
NUM_WORKPLACES = 15
TYPES = ["Factory", "Office", "Warehouse", "Construction"]

# Amsterdam clusters (same as workers)
CITY_CENTERS = [
    (52.3728, 4.8936),  # Centrum
    (52.3400, 4.8885),  # Zuid
    (52.4000, 4.9166),  # Noord
    (52.3870, 4.8357),  # Sloterdijk
]

def generate_workplace(i):
    base_lat, base_lon = random.choice(CITY_CENTERS)
    lat = base_lat + np.random.normal(0, 0.01)
    lon = base_lon + np.random.normal(0, 0.01)

    return {
        "WorkplaceID": f"WP{i:03d}",
        "Name": fake.company(),
        "Type": random.choice(TYPES),
        "Latitude": round(lat, 6),
        "Longitude": round(lon, 6)
    }

def generate_workplaces(n=NUM_WORKPLACES):
    return pd.DataFrame([generate_workplace(i) for i in range(n)])

if __name__ == "__main__":
    OUTPUT_DIR = "data"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = generate_workplaces()
    df.to_csv(f"{OUTPUT_DIR}/workplaces.csv", index=False)
    print("✅ workplaces.csv generated with", len(df), "entries.")
