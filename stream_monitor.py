import pandas as pd
import joblib
import time
import csv
from datetime import datetime
import os

# ===============================
# Paths
# ===============================
MODEL_PATH = "src/models/output/IDS.joblib"
DATA_PATH = "data/preprocess/preprocessed_data.csv"
LOG_FILE = "logs/attack_log.csv"

# Create logs folder if not exists
os.makedirs("logs", exist_ok=True)

# ===============================
# Load Model & Data
# ===============================
model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

# ===============================
# Counters
# ===============================
attack_count = 0
normal_count = 0

print("\nStarting simulated live intrusion detection...\n")

# ===============================
# Function to log attacks
# ===============================
def log_attack():

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Attack Detected"
        ])

# ===============================
# Live Detection Loop
# ===============================
for i in range(len(df)):

    row = df.iloc[i:i+1].drop(columns=["attack_detected"])

    prediction = model.predict(row)[0]

    current_time = datetime.now().strftime("%H:%M:%S")

    if prediction == 1:
        attack_count += 1
        print(f"[{current_time}] ⚠️ Attack Detected")
        log_attack()

    else:
        normal_count += 1
        print(f"[{current_time}] Normal Traffic")

    print(f"Total Attacks: {attack_count} | Normal: {normal_count}\n")

    time.sleep(1)

print("Monitoring finished.")