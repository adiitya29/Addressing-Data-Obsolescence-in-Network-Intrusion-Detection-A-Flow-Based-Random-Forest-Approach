from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import joblib
import datetime
import os
import csv

MODEL_PATH = "src/models/output/IDS.joblib"
model = joblib.load(MODEL_PATH)

print("Starting real-time intrusion detection...\n")

# create log folder if missing
if not os.path.exists("logs"):
    os.makedirs("logs")

LOG_FILE = "logs/live_traffic.csv"

# create file header if file doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "source_ip", "destination_ip", "status", "attack_type"])


def classify_attack(src_port, dst_port):
    """Classify attack type based on port heuristics."""
    ports = {src_port, dst_port}

    if 22 in ports:
        return "SSH Brute Force"
    elif 80 in ports or 443 in ports or 8080 in ports:
        return "HTTP Flood"
    elif 53 in ports:
        return "DNS Attack"
    elif 21 in ports or 20 in ports:
        return "FTP Attack"
    elif 25 in ports or 587 in ports:
        return "SMTP Attack"
    elif 23 in ports:
        return "Telnet Attack"
    elif 3389 in ports:
        return "RDP Attack"
    elif dst_port > 1024 and src_port > 1024:
        return "Port Scan"
    else:
        return "Unknown Attack"


def extract_features(packet):

    packet_length = len(packet)

    protocol = 0
    src_port = 0
    dst_port = 0

    if packet.haslayer(IP):

        if packet.haslayer(TCP):
            protocol = 6
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport

        elif packet.haslayer(UDP):
            protocol = 17
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport

    features = {
        "packet_length": packet_length,
        "protocol": protocol,
        "src_port": src_port,
        "dst_port": dst_port
    }

    return features


model_features = model.feature_names_in_


def process_packet(packet):

    if not packet.haslayer(IP):
        return

    try:

        features = extract_features(packet)

        df = pd.DataFrame([features])

        # add missing columns expected by model
        for col in model_features:
            if col not in df.columns:
                df[col] = 0

        df = df[model_features]

        prediction = model.predict(df)[0]

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        timestamp = datetime.datetime.now()

        if prediction == 1:

            attack_type = classify_attack(
                packet[TCP].sport if packet.haslayer(TCP) else (packet[UDP].sport if packet.haslayer(UDP) else 0),
                packet[TCP].dport if packet.haslayer(TCP) else (packet[UDP].dport if packet.haslayer(UDP) else 0)
            )
            status = "Attack"
            print(f"[{timestamp}] ⚠️ {attack_type} Detected | {src_ip} -> {dst_ip}")

        else:

            attack_type = "None"
            status = "Normal"
            print(f"[{timestamp}] Normal Traffic | {src_ip} -> {dst_ip}")

        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, src_ip, dst_ip, status, attack_type])

    except Exception as e:
        print("Processing error:", e)


sniff(prn=process_packet, store=False, filter="ip")