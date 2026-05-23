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

## 💻 Tech Stack Used

This project was built using modern, industry-standard tools and libraries:

**Core Language & UI:**
*   **Python 3.9+** – The primary programming language.
*   **Streamlit** – Used to build the beautiful, interactive, real-time frontend dashboard.

**Machine Learning & Data Processing:**
*   **Scikit-Learn** – Used for training the Random Forest and Support Vector Machine (SVM) models.
*   **XGBoost & LightGBM** – Used for advanced, high-performance gradient boosting models.
*   **Pandas & NumPy** – Used for robust data manipulation, preprocessing, and feature engineering.
*   **Joblib** – Used for saving and loading the trained machine learning models efficiently.
*   **SHAP (SHapley Additive exPlanations)** – Used for model explainability to understand feature importance.

**Networking & Packet Analysis:**
*   **Scapy** – Used for real-time network packet sniffing, crafting, and sending simulated attacks.
*   **Npcap** – Required for Windows environments to allow Scapy to capture raw network traffic.

**Deployment & API (Optional):**
*   **FastAPI & Uvicorn** – Used to create a fast backend REST API for model predictions.
*   **Docker & Docker Compose** – Configured for easy containerization and local deployment.

--

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


## 🖥️ PROJECT OUTPUTS


## Static Monitoring

<img width="2560" height="1430" alt="image" src="https://github.com/user-attachments/assets/c318a3c4-8fa5-4b8c-a75b-da7e6f2a65d6" />

<img width="2560" height="1426" alt="image" src="https://github.com/user-attachments/assets/1bd46b42-4103-4eb6-a4be-974f83a3392d" />


## Confusion Matrix and Performance Metrics

<img width="2560" height="1437" alt="image" src="https://github.com/user-attachments/assets/1e861345-af91-4c91-959b-52b6395ffba5" />

<img width="2560" height="1435" alt="image" src="https://github.com/user-attachments/assets/79c9e5f4-7068-4e55-89d7-3b76dc67f3e9" />

<img width="2560" height="1407" alt="image" src="https://github.com/user-attachments/assets/60775135-29ca-45a7-a36d-553d19b3555b" />


## Training Time and Accuracy

<img width="1656" height="683" alt="image" src="https://github.com/user-attachments/assets/dcb7d2da-5dbd-431f-a3fd-a8cae4c99286" />

<img width="1235" height="441" alt="image" src="https://github.com/user-attachments/assets/543aaf20-57ff-4cfa-8288-e3c6ba69ba2d" />


## SHAP Summary Plot

<img width="496" height="680" alt="image" src="https://github.com/user-attachments/assets/a685b9cf-7bba-421f-8d15-0517d8c568fc" />



## Remaining Outputs

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/46529f6b-c1cd-4522-b71d-8af632abc27c" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/417f860d-8837-4659-a4a6-bd49f0573cf7" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/4df74f93-1d19-4960-82f5-b96097fb861b" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/28fa82f3-2a62-40b8-bee6-134847572654" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/be84dcf9-aa89-491b-b9db-01915e05569a" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/c9221b4b-b35d-4ed4-be03-779309df4703" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/d47b69c8-848f-4289-9a7e-c53792838b83" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/12e34b32-e2fe-488d-9bca-ee0689ad9559" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/597cf2b6-8aed-4f15-a7eb-28ce3359c24a" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/66c31473-3f34-4a30-b0dc-67f2f319a1b8" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/c6ea413a-6e40-47a8-bd93-cb26ed935541" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/eefbef25-2784-42cc-b212-ec1ef2be6863" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/a2b8ee6b-8572-406f-8e07-ce0d40f42e33" />

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/f1357c78-d138-4709-b735-a3d3cef18b7f" />



