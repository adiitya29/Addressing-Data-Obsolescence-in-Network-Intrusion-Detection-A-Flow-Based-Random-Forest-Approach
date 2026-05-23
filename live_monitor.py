from scapy.all import sniff
import pandas as pd
import joblib

model = joblib.load("src/models/output/IDS.joblib")

def process_packet(packet):

    # Example feature extraction (basic)
    data = {
        "packet_length": len(packet),
        "protocol": packet.proto if hasattr(packet, "proto") else 0
    }

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    if prediction[0] == 1:
        print("⚠️ Attack detected!")
    else:
        print("Normal traffic")


print("Starting live intrusion detection...")

sniff(prn=process_packet, store=False)