"""
Attack Traffic Simulator for IDS Demo
======================================
Injects simulated attack entries into live_traffic.csv so the dashboard
shows real-time attack detection during a practical demo.

Run this in a SEPARATE terminal alongside live_ids.py and dashboard.
Usage:
    python simulate_attacks.py
"""

import csv
import time
import random
import datetime
import os

LOG_FILE = "logs/live_traffic.csv"

os.makedirs("logs", exist_ok=True)

# Create file with header if missing
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "source_ip", "destination_ip", "status", "attack_type"])

# ----------------------------------------
# Simulated attacker and victim IPs
# ----------------------------------------
ATTACKER_IPS = [
    "10.0.0.50",
    "172.16.0.100",
    "185.220.101.45",
    "45.33.32.156",
    "198.51.100.77",
    "203.0.113.42",
    "91.108.56.130",
    "77.88.55.70",
]

TARGET_IPS = [
    "192.168.1.7",
    "192.168.1.10",
    "192.168.1.20",
    "192.168.1.100",
]

NORMAL_PAIRS = [
    ("192.168.1.7", "35.237.69.59"),
    ("35.237.69.59", "192.168.1.7"),
    ("192.168.1.7", "142.250.82.219"),
    ("192.168.1.7", "192.168.1.1"),
    ("192.168.1.1", "192.168.1.7"),
    ("192.168.1.7", "34.54.84.110"),
]

ATTACK_SCENARIOS = [
    ("SSH Brute Force", [
        ("185.220.101.45", "192.168.1.7"),
        ("185.220.101.45", "192.168.1.10"),
        ("91.108.56.130", "192.168.1.7"),
    ]),
    ("HTTP Flood",  [
        ("45.33.32.156",  "192.168.1.7"),
        ("77.88.55.70",   "192.168.1.20"),
        ("203.0.113.42",  "192.168.1.100"),
    ]),
    ("DNS Attack", [
        ("10.0.0.50",      "192.168.1.7"),
        ("172.16.0.100",   "192.168.1.10"),
    ]),
    ("Port Scan", [
        ("198.51.100.77", "192.168.1.7"),
        ("45.33.32.156",  "192.168.1.20"),
    ]),
    ("FTP Attack", [
        ("203.0.113.42",  "192.168.1.100"),
        ("91.108.56.130", "192.168.1.10"),
    ]),
    ("RDP Attack", [
        ("77.88.55.70",   "192.168.1.7"),
        ("10.0.0.50",     "192.168.1.20"),
    ]),
]


def write_row(src, dst, status, attack_type):
    ts = datetime.datetime.now()
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([ts, src, dst, status, attack_type])


def burst_normal(n=3):
    for _ in range(n):
        src, dst = random.choice(NORMAL_PAIRS)
        write_row(src, dst, "Normal", "None")
        print(f"  ✅ Normal  | {src} -> {dst}")


def burst_attack(scenario_name, pairs, n=4):
    for _ in range(n):
        src, dst = random.choice(pairs)
        write_row(src, dst, "Attack", scenario_name)
        print(f"  ⚠️  {scenario_name} | {src} -> {dst}")


if __name__ == "__main__":
    print("=" * 58)
    print("  ATTACK TRAFFIC SIMULATOR — IDS Demo")
    print("=" * 58)
    print("Simulating attacks into logs/live_traffic.csv")
    print("Dashboard auto-refreshes every 2 seconds.")
    print("Press Ctrl+C to stop.\n")

    cycle = 0
    try:
        while True:
            cycle += 1
            print(f"\n─── Cycle {cycle} ───────────────────────────────────")

            # Phase 1: Normal traffic (short)
            burst_normal(random.randint(2, 4))

            # Phase 2: Attack burst (heavier — ensures CRITICAL threat level)
            attack_name, attack_pairs = random.choice(ATTACK_SCENARIOS)
            burst_attack(attack_name, attack_pairs, n=random.randint(5, 10))

            # Phase 3: More normal
            burst_normal(random.randint(1, 3))

            # Phase 4: Second attack type for variety
            attack_name2, attack_pairs2 = random.choice(ATTACK_SCENARIOS)
            if attack_name2 != attack_name:
                burst_attack(attack_name2, attack_pairs2, n=random.randint(3, 6))

            time.sleep(1.5)

    except KeyboardInterrupt:
        print("\n\nSimulation stopped.")
