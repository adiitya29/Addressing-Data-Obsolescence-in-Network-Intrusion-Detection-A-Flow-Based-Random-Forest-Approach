import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000/predict"

st.set_page_config(
    page_title="Intrusion Detection System",
    page_icon="🚨",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Header ---
st.markdown(
    """
    <h1 style='text-align: center; color: #d62728;'>🚨 Network Intrusion Detection System (NIDS)</h1>
    <p style='text-align: center; font-size: 18px; color: #6c757d;'>
    Upload your network traffic data (.csv) to detect potential intrusions using ML-powered backend.
    </p>
    """,
    unsafe_allow_html=True
)

# File uploader with clear label
uploaded_file = st.file_uploader(
    label="Choose a CSV file containing network traffic data",
    type=["csv"],
    help="File size limit: 200MB. The file should include all required features for prediction."
)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.markdown("### 🔍 Sample of uploaded data")
        st.dataframe(df.head(), use_container_width=True)

        if st.button("Run Intrusion Detection"):
            results = []
            with st.spinner("🔍 Detecting intrusions, please wait..."):
                for idx, row in df.iterrows():
                    data = row.to_dict()
                    response = requests.post(API_URL, json=data)
                    if response.status_code == 200:
                        pred = response.json().get("prediction")
                        results.append(pred)
                    else:
                        st.error(f"API error at row {idx}: {response.status_code} - {response.text}")
                        results.append(None)

            df['Prediction'] = results

            st.markdown("### ✅ Prediction Results")
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")

else:
    st.info("Please upload a CSV file to start the intrusion detection process.")

# Footer or additional info
st.markdown(
    """
    <hr>
    <p style='text-align: center; font-size: 14px; color: #888;'>
    Powered by FastAPI & Streamlit &nbsp;&bull;&nbsp; © 2025 Your Company Name
    </p>
    """,
    unsafe_allow_html=True
)
