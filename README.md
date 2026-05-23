# 🚀 AI Network Intrusion Detection System (NIDS)

A beginner-friendly, real-time Intrusion Detection System powered by Machine Learning (Random Forest, SVM, XGBoost) with a beautiful interactive Streamlit dashboard.

---

## 🌟 Why This Project is Great for Beginners

We built this project with **simplicity and clarity** in mind. Network security and machine learning can be incredibly complex, so we intentionally designed this project to be easy to understand, easy to run, and easy to modify:

- **Clear Architecture:** The code is cleanly separated into machine learning training (`src/models/train.py`), live packet capture (`live_ids.py`), and a frontend dashboard (`dashboard.py`).
- **Interactive UI:** Instead of staring at terminal logs, our Streamlit dashboard provides beautiful, real-time graphs showing exactly what the ML models are detecting.
- **Easy Simulation:** Don't want to wait for a real hacker? We've included a `simulate_attacks.py` script that safely generates fake attack traffic so you can see the system working instantly.
- **Standard Libraries:** We rely on industry-standard, well-documented Python libraries (Scikit-Learn, Pandas, Scapy, Streamlit).

---

## 🛠️ Quick Installation Guide

If you just cloned this repository, follow these simple steps to get the project running on your local machine.

### 1. Prerequisites
- **Python 3.9+** installed on your system.
- *(Windows Only)* If you want to capture real live packets, install [Npcap](https://npcap.com/) with "WinPcap API-compatible Mode" enabled (Scapy requires this).

### 2. Create a Virtual Environment (Recommended)
It's always best to install Python packages in a virtual environment to avoid conflicts.

```bash
# Open your terminal/command prompt inside the project folder
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
Install all required libraries with one command:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Project

> **⚠️ Note on Cloud Deployment**
> This project is designed to be run **locally** rather than hosted on a public cloud platform. While static monitoring (uploading a dataset) works perfectly on hosted projects, **dynamic live monitoring is blocked by cloud services**. Cloud providers strictly prohibit the packet sniffing required by our Scapy code. Because we send simulated live attacks over the local network (due to the lack of open-source IP addresses for safe live testing), the full features of this project are best experienced on a local machine.

You can run the project in two ways: **Real-Time Capture** or **Simulated Demo**.

### Option A: The Full Practical Demo (Recommended for Presentations)

We've provided a simulation script that generates fake attack traffic so you can easily demonstrate the dashboard's capabilities.

**Terminal 1:** Run the dashboard
```bash
streamlit run dashboard.py
```
*(Login with Username: `admin` | Password: `admin123`)*

**Terminal 2:** Run the simulation generator
```bash
python simulate_attacks.py
```
*Switch back to your browser. You will immediately see the dashboard light up with detected attacks!*

### Option B: Real-Time Network Monitoring

Want to monitor your actual Wi-Fi or Ethernet traffic?

**Terminal 1:** Run the live packet capturer (requires Admin/Sudo privileges)
```bash
python live_ids.py
```

**Terminal 2:** Run the dashboard
```bash
streamlit run dashboard.py
```

---

## 🧰 How to Train the ML Models Yourself

If you want to re-train the models (Random Forest, SVM, XGBoost) on your own dataset:

1. Place your preprocessed CSV dataset at `data/preprocess/preprocessed_data.csv`
2. Run the training script:
```bash
python src/models/train.py
```
*This will train the models, save the best one as `IDS.joblib`, and output performance metrics into a JSON file that the dashboard reads to display the Model Performance graphs.*

---

## 📂 Project Structure

- `dashboard.py` — The interactive Streamlit frontend web app.
- `live_ids.py` — Captures live network packets using Scapy and uses the ML model to predict attacks.
- `simulate_attacks.py` — Generates simulated attack logs for easy demonstrations.
- `src/models/train.py` — Trains the Machine Learning models.
- `src/models/output/` — Where the trained `.joblib` models and performance `.json` data are stored.
- `logs/live_traffic.csv` — The live log file where incoming traffic is recorded and read by the dashboard.