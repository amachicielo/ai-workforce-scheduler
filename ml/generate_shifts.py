# ml/generate_shifts.py

import pandas as pd
import os

# PARAMETERS
NUM_WEEKS = 2   # you can increase this (e.g., 4 or 8)
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SHIFTS = {
    "Morning": ("06:00", "14:00"),
    "Evening": ("14:00", "22:00"),
    "Night": ("22:00", "06:00")
}

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

if __name__ == "__main__":
    OUTPUT_DIR = "data"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = generate_shifts()
    df.to_csv(f"{OUTPUT_DIR}/shifts.csv", index=False)
    print("✅ shifts.csv generated with", len(df), "entries.")
