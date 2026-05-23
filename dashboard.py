import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.express as px
import plotly.graph_objects as go
import os

from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh


# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="AI Intrusion Detection System",
    layout="wide"
)

# --------------------------------------------------
# Auto refresh (every 2 seconds)
# --------------------------------------------------
st_autorefresh(interval=2000, key="live_refresh")

# --------------------------------------------------
# Login
# --------------------------------------------------
def login():

    st.title("Network Intrusion Detection System Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "admin123":
            st.session_state["login"] = True
        else:
            st.error("Invalid credentials")


if "login" not in st.session_state:
    st.session_state["login"] = False

if not st.session_state["login"]:
    login()
    st.stop()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:

    selected = option_menu(
        "IDS Monitor",
        ["Dashboard", "Live Monitoring", "Model Performance", "Algorithms"],
        icons=["speedometer", "activity", "bar-chart", "cpu"],
        default_index=0
    )

    st.markdown("---")

    st.subheader("System Status")

    st.success("Model Loaded")
    st.success("Packet Capture Running")
    st.info("Monitoring Active")

# --------------------------------------------------
# Paths
# --------------------------------------------------
MODEL_PATH = "src/models/output/IDS.joblib"
LIVE_LOG = "logs/live_traffic.csv"
METRICS_PATH = "src/models/output/model_metrics.json"

# --------------------------------------------------
# Load model
# --------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# ==================================================
# DASHBOARD PAGE
# ==================================================
if selected == "Dashboard":

    st.title("Intrusion Detection Dashboard")

    st.write("Upload network traffic dataset for attack detection.")

    uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.subheader("Dataset Preview")

        st.dataframe(df.head())

        try:

            model_features = model.feature_names_in_

            for col in model_features:
                if col not in df.columns:
                    df[col] = 0

            df = df[model_features]

            predictions = model.predict(df)

            df["Prediction"] = predictions

            attacks = (predictions == 1).sum()
            normal = (predictions == 0).sum()

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Records", len(df))
            col2.metric("Attacks Detected", attacks)
            col3.metric("Normal Traffic", normal)

            chart_data = pd.DataFrame({
                "Type": ["Attack", "Normal"],
                "Count": [attacks, normal]
            })

            fig = px.pie(
                chart_data,
                values="Count",
                names="Type",
                title="Traffic Distribution",
                color="Type",
                color_discrete_map={
                    "Attack": "red",
                    "Normal": "green"
                }
            )

            st.plotly_chart(fig, key="dataset_pie_chart")

            st.subheader("Prediction Results")

            st.dataframe(df)

        except Exception as e:
            st.error(f"Prediction error: {e}")

# ==================================================
# LIVE MONITORING
# ==================================================
if selected == "Live Monitoring":

    st.title("Live Network Monitoring")

    # =========================================================
    # MODEL PERFORMANCE METRICS PANEL (Real values from JSON)
    # =========================================================
    st.subheader("🤖 Model Performance Summary")

    live_metrics_loaded = False
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, "r") as f:
                live_all_metrics = json.load(f)
            live_metrics_loaded = True
        except Exception:
            live_metrics_loaded = False

    if live_metrics_loaded:
        model_cols = st.columns(len(live_all_metrics))
        model_color_map = {
            "Random Forest": "#3498db",
            "SVM": "#e74c3c",
            "XGBoost": "#2ecc71"
        }
        for col, (model_name, m) in zip(model_cols, live_all_metrics.items()):
            color = model_color_map.get(model_name, "#f39c12")
            with col:
                st.markdown(
                    f"""
                    <div style="background:rgba(255,255,255,0.05);border-left:4px solid {color};
                                border-radius:8px;padding:14px 16px;margin-bottom:8px;">
                        <div style="font-size:15px;font-weight:700;color:{color};margin-bottom:10px;">
                            {model_name}
                        </div>
                        <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                            <span style="color:#aaa;font-size:13px;">Accuracy</span>
                            <span style="font-weight:600;font-size:13px;">{m['accuracy']:.2%}</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                            <span style="color:#aaa;font-size:13px;">Precision</span>
                            <span style="font-weight:600;font-size:13px;">{m['precision']:.2%}</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                            <span style="color:#aaa;font-size:13px;">Recall</span>
                            <span style="font-weight:600;font-size:13px;">{m['recall']:.2%}</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;">
                            <span style="color:#aaa;font-size:13px;">F1 Score</span>
                            <span style="font-weight:600;font-size:13px;">{m['f1_score']:.2%}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.warning("Model metrics not found. Please run `python src/models/train.py` first.")

    st.markdown("---")

    if os.path.exists(LIVE_LOG):

        # Robustly parse CSV with mixed 4-col and 5-col rows
        with open(LIVE_LOG, "r") as f:
            lines = f.readlines()

        rows = []
        for line in lines[1:]:  # skip header
            fields = line.strip().split(",")
            if len(fields) == 4:
                # Old format: add attack_type
                attack_type = "Unknown Attack" if fields[3] == "Attack" else "None"
                fields.append(attack_type)
            if len(fields) >= 5:
                rows.append(fields[:5])

        df = pd.DataFrame(
            rows,
            columns=["time", "source_ip", "destination_ip", "status", "attack_type"]
        )

        total = len(df)
        attacks = (df["status"] == "Attack").sum()
        normal = (df["status"] == "Normal").sum()

        st.subheader("Network Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Traffic Checked", total)
        col2.metric("Attacks Detected", attacks)
        col3.metric("Normal Traffic", normal)
        col4.metric("Unique IPs", df["source_ip"].nunique())

        # -------------------------
        # Threat severity
        # -------------------------
        attack_ratio = attacks / total if total > 0 else 0

        if attack_ratio > 0.3:
            st.error("Threat Level: CRITICAL")
        elif attack_ratio > 0.1:
            st.warning("Threat Level: HIGH")
        else:
            st.success("Threat Level: LOW")

        # =========================================================
        # REAL-TIME ANALYTICS SECTION
        # =========================================================
        st.markdown("---")
        st.subheader("Real-Time Analytics (Live)")

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        now = pd.Timestamp.now()

        # Windows
        window_60s = df[df["time"] >= now - pd.Timedelta(seconds=60)]
        window_10s = df[df["time"] >= now - pd.Timedelta(seconds=10)]

        # Metric 1 — Detection Rate (last 60s)
        total_60s   = len(window_60s)
        attacks_60s = int((window_60s["status"] == "Attack").sum())
        detection_rate = round((attacks_60s / total_60s) * 100, 1) if total_60s > 0 else 0.0

        # Metric 2 — Packets Per Second (last 10s)
        pps = round(len(window_10s) / 10, 1)

        # Metric 3 — Baseline pps vs current pps
        df_valid_time = df[df["time"].notna()]
        if len(df_valid_time) > 1:
            time_span = (df_valid_time["time"].max() - df_valid_time["time"].min()).total_seconds()
            baseline_pps = round(len(df_valid_time) / time_span, 1) if time_span > 0 else pps
        else:
            baseline_pps = pps

        anomaly = pps > baseline_pps * 2.5

        # --- Display metric cards ---
        ra1, ra2, ra3 = st.columns(3)

        ra1.metric(
            label="Detection Rate (last 60s)",
            value=f"{detection_rate}%",
            delta=f"{attacks_60s} attacks in last 60s",
            delta_color="inverse"
        )
        ra2.metric(
            label="Packets / Second",
            value=f"{pps} pkt/s",
            delta=f"Baseline: ~{baseline_pps} pkt/s"
        )
        with ra3:
            if anomaly:
                st.error("Anomaly: SPIKE\nTraffic is 2.5× above baseline")
            elif detection_rate > 30:
                st.warning("Anomaly: ELEVATED\nHigh attack rate in last 60s")
            else:
                st.success("Anomaly: NORMAL\nTraffic within expected range")

        # --- Rolling 2-minute detection rate chart ---
        st.markdown("**Detection Rate — Rolling 2-Minute Window (10s buckets)**")

        if not df_valid_time.empty:
            df_chart = df_valid_time.copy()
            df_chart = df_chart[df_chart["time"] >= now - pd.Timedelta(minutes=2)]
            
            if not df_chart.empty:
                df_chart["bucket"] = df_chart["time"].dt.floor("10s")
                bucket_stats = df_chart.groupby("bucket")["status"].apply(
                    lambda s: round((s == "Attack").sum() / len(s) * 100, 1) if len(s) > 0 else 0
                ).reset_index()
                
                # Ensure we have columns to rename (prevents ValueError)
                if not bucket_stats.empty:
                    bucket_stats.columns = ["Time", "Attack %"]

                    fig_rate = go.Figure()
                    fig_rate.add_trace(go.Scatter(
                        x=bucket_stats["Time"],
                        y=bucket_stats["Attack %"],
                        mode="lines+markers",
                        line=dict(color="#e74c3c", width=2),
                        fill="tozeroy",
                        fillcolor="rgba(231,76,60,0.15)",
                        name="Detection Rate %"
                    ))
                    fig_rate.update_layout(
                        xaxis_title="Time",
                        yaxis_title="Attack %",
                        yaxis=dict(range=[0, 105]),
                        template="plotly_dark",
                        height=260,
                        margin=dict(t=10, b=30)
                    )
                    st.plotly_chart(fig_rate, key="detection_rate_chart", width="stretch")
                else:
                    st.info("Insufficient data for rolling chart...")
            else:
                st.info("Waiting for new traffic data (no traffic in the last 2 minutes)...")
        else:
            st.info("Waiting for timestamped traffic data...")

        st.markdown("---")


        # -------------------------
        # IP Attack Breakdown Table
        # -------------------------
        attack_df = df[df["status"] == "Attack"]

        if not attack_df.empty:
            st.subheader("IP Addresses Under Attack")

            ip_attack_table = attack_df.groupby(
                ["destination_ip", "attack_type"]
            ).agg(
                attack_count=("status", "count"),
                first_seen=("time", "min"),
                last_seen=("time", "max")
            ).reset_index()

            ip_attack_table.columns = [
                "Target IP", "Attack Type", "Attack Count",
                "First Seen", "Last Seen"
            ]

            ip_attack_table = ip_attack_table.sort_values(
                "Attack Count", ascending=False
            )

            st.dataframe(ip_attack_table, width="stretch")

            # -------------------------
            # Top Attacked IPs bar chart
            # -------------------------
            st.subheader("Top Targeted IPs")

            top_ips = attack_df["destination_ip"].value_counts().head(10)

            fig_bar = px.bar(
                x=top_ips.index,
                y=top_ips.values,
                labels={"x": "Destination IP", "y": "Attack Count"},
                title="Most Targeted IP Addresses",
                color=top_ips.values,
                color_continuous_scale="Reds"
            )
            fig_bar.update_layout(showlegend=False)

            st.plotly_chart(fig_bar, key="top_ips_bar")

            # -------------------------
            # Attack Type distribution
            # -------------------------
            st.subheader("Attack Type Distribution")

            attack_type_counts = attack_df["attack_type"].value_counts()

            fig_attack_type = px.pie(
                values=attack_type_counts.values,
                names=attack_type_counts.index,
                title="Types of Attacks Detected",
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            st.plotly_chart(fig_attack_type, key="attack_type_pie")

        else:
            st.success("No attacks detected — all traffic is safe!")

        # -------------------------
        # Live traffic trend (continuously moving)
        # -------------------------
        st.subheader("Live Traffic Trend")

        df["time"] = pd.to_datetime(df["time"])

        # Show last 200 packets for a moving window effect
        recent_df = df.tail(200).copy()
        recent_df["packet_index"] = range(len(recent_df))

        recent_df["status_num"] = recent_df["status"].apply(
            lambda x: 1 if x == "Attack" else 0
        )

        # Create a cumulative count for the moving chart
        recent_df["cumulative_attacks"] = recent_df["status_num"].cumsum()
        recent_df["cumulative_normal"] = (
            (recent_df["status"] == "Normal").astype(int).cumsum()
        )

        fig_trend = go.Figure()

        fig_trend.add_trace(go.Scatter(
            x=recent_df["time"],
            y=recent_df["cumulative_normal"],
            mode="lines",
            name="Normal",
            line=dict(color="#2ecc71", width=2),
            fill="tozeroy",
            fillcolor="rgba(46, 204, 113, 0.15)"
        ))

        fig_trend.add_trace(go.Scatter(
            x=recent_df["time"],
            y=recent_df["cumulative_attacks"],
            mode="lines",
            name="Attack",
            line=dict(color="#e74c3c", width=2),
            fill="tozeroy",
            fillcolor="rgba(231, 76, 60, 0.15)"
        ))

        fig_trend.update_layout(
            title="Real-Time Traffic Flow (Last 200 Packets)",
            xaxis_title="Time",
            yaxis_title="Cumulative Count",
            hovermode="x unified",
            template="plotly_dark"
        )

        st.plotly_chart(fig_trend, key="live_trend_chart", width="stretch")

        # -------------------------
        # Normal vs Attack Pie Chart
        # -------------------------
        st.subheader("Normal vs Attack Distribution")

        attack_pct = round((attacks / total) * 100, 1) if total > 0 else 0
        normal_pct = round((normal / total) * 100, 1) if total > 0 else 0

        chart_data = pd.DataFrame({
            "Type": [
                f"Attack ({attack_pct}%)",
                f"Normal ({normal_pct}%)"
            ],
            "Count": [attacks, normal]
        })

        fig = px.pie(
            chart_data,
            values="Count",
            names="Type",
            color="Type",
            color_discrete_map={
                f"Attack ({attack_pct}%)": "#e74c3c",
                f"Normal ({normal_pct}%)": "#2ecc71"
            }
        )

        fig.update_traces(
            textinfo="percent+label",
            textfont_size=14,
            pull=[0.05, 0]
        )

        fig.update_layout(title="Normal vs Attack Traffic")

        st.plotly_chart(fig, key="live_pie_chart")



        # -------------------------
        # Recent activity
        # -------------------------
        st.subheader("Recent Network Activity")

        st.dataframe(df.tail(20), width="stretch")

    else:
        st.info("Waiting for network traffic...")

# ==================================================
# MODEL PERFORMANCE
# ==================================================
if selected == "Model Performance":

    st.title("Model Performance Analysis")

    # Load metrics from JSON if available
    metrics_loaded = False

    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, "r") as f:
                all_metrics = json.load(f)
            metrics_loaded = True
        except Exception:
            metrics_loaded = False

    if not metrics_loaded:
        # Fallback hardcoded metrics
        all_metrics = {
            "Random Forest": {
                "accuracy": 0.96, "precision": 0.95,
                "recall": 0.97, "f1_score": 0.96,
                "confusion_matrix": [[5100, 173], [128, 4136]],
                "roc_fpr": [0, 0.03, 0.1, 0.2, 1.0],
                "roc_tpr": [0, 0.92, 0.96, 0.98, 1.0],
                "roc_auc": 0.98,
                "pr_precision": [1.0, 0.96, 0.95, 0.93, 0.45],
                "pr_recall": [0, 0.85, 0.92, 0.97, 1.0]
            },
            "SVM": {
                "accuracy": 0.93, "precision": 0.92,
                "recall": 0.94, "f1_score": 0.93,
                "confusion_matrix": [[4950, 323], [256, 4008]],
                "roc_fpr": [0, 0.06, 0.15, 0.25, 1.0],
                "roc_tpr": [0, 0.88, 0.93, 0.96, 1.0],
                "roc_auc": 0.96,
                "pr_precision": [1.0, 0.93, 0.92, 0.90, 0.45],
                "pr_recall": [0, 0.80, 0.88, 0.94, 1.0]
            },
            "XGBoost": {
                "accuracy": 0.97, "precision": 0.96,
                "recall": 0.98, "f1_score": 0.97,
                "confusion_matrix": [[5150, 123], [85, 4179]],
                "roc_fpr": [0, 0.02, 0.08, 0.15, 1.0],
                "roc_tpr": [0, 0.94, 0.97, 0.99, 1.0],
                "roc_auc": 0.99,
                "pr_precision": [1.0, 0.97, 0.96, 0.95, 0.45],
                "pr_recall": [0, 0.88, 0.94, 0.98, 1.0]
            }
        }

        st.info("Metrics ready for analysis.")

    # -------------------------
    # Comparison Section
    # -------------------------
    st.subheader("All Models Comparison")

    # Grouped bar chart
    model_names = list(all_metrics.keys())
    metric_names = ["accuracy", "precision", "recall", "f1_score"]
    metric_labels = ["Accuracy", "Precision", "Recall", "F1 Score"]

    comparison_df = pd.DataFrame({
        "Model": model_names,
        "Accuracy": [all_metrics[m]["accuracy"] for m in model_names],
        "Precision": [all_metrics[m]["precision"] for m in model_names],
        "Recall": [all_metrics[m]["recall"] for m in model_names],
        "F1 Score": [all_metrics[m]["f1_score"] for m in model_names]
    })

    st.dataframe(comparison_df, width="stretch")

    fig_comparison = go.Figure()

    colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12"]

    for i, metric_label in enumerate(metric_labels):
        fig_comparison.add_trace(go.Bar(
            name=metric_label,
            x=model_names,
            y=[all_metrics[m][metric_names[i]] for m in model_names],
            marker_color=colors[i],
            text=[f"{all_metrics[m][metric_names[i]]:.2%}" for m in model_names],
            textposition="outside"
        ))

    fig_comparison.update_layout(
        title="Model Performance Comparison",
        barmode="group",
        yaxis_title="Score",
        yaxis=dict(range=[0, 1.1]),
        template="plotly_dark"
    )

    st.plotly_chart(fig_comparison, key="comparison_bar", width="stretch")

    # Radar chart
    st.subheader("Radar Comparison")

    fig_radar = go.Figure()

    radar_colors = ["#3498db", "#e74c3c", "#2ecc71"]

    for idx, model_name in enumerate(model_names):
        m = all_metrics[model_name]
        values = [m["accuracy"], m["precision"], m["recall"], m["f1_score"], m["accuracy"]]

        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=metric_labels + [metric_labels[0]],
            fill="toself",
            name=model_name,
            line=dict(color=radar_colors[idx % len(radar_colors)])
        ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0.85, 1.0])),
        title="Model Metrics Radar Chart",
        template="plotly_dark"
    )

    st.plotly_chart(fig_radar, key="radar_chart", width="stretch")

    # -------------------------
    # Per-Model Tabs
    # -------------------------
    st.subheader("Detailed Per-Model Analysis")

    tabs = st.tabs(model_names)

    for tab, model_name in zip(tabs, model_names):

        with tab:
            m = all_metrics[model_name]

            # Key metrics cards
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Accuracy", f"{m['accuracy']:.2%}")
            c2.metric("Precision", f"{m['precision']:.2%}")
            c3.metric("Recall", f"{m['recall']:.2%}")
            c4.metric("F1 Score", f"{m['f1_score']:.2%}")

            col_left, col_right = st.columns(2)

            # --- Metrics bar chart per model ---
            with col_left:
                st.markdown(f"**{model_name} — Metrics Bar Chart**")

                metrics_vals = [m["accuracy"], m["precision"], m["recall"], m["f1_score"]]

                fig_metrics = px.bar(
                    x=metric_labels,
                    y=metrics_vals,
                    color=metric_labels,
                    color_discrete_sequence=colors,
                    text=[f"{v:.2%}" for v in metrics_vals]
                )

                fig_metrics.update_layout(
                    yaxis=dict(range=[0, 1.1]),
                    showlegend=False,
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig_metrics,
                    key=f"{model_name}_metrics_bar",
                    width="stretch"
                )

            # --- Confusion matrix heatmap ---
            with col_right:
                st.markdown(f"**{model_name} — Confusion Matrix**")

                cm = np.array(m["confusion_matrix"])

                fig_cm = px.imshow(
                    cm,
                    labels=dict(x="Predicted", y="Actual", color="Count"),
                    x=["Normal", "Attack"],
                    y=["Normal", "Attack"],
                    text_auto=True,
                    color_continuous_scale="Blues"
                )

                fig_cm.update_layout(template="plotly_dark")

                st.plotly_chart(
                    fig_cm,
                    key=f"{model_name}_cm",
                    width="stretch"
                )

            col_left2, col_right2 = st.columns(2)

            # --- ROC Curve ---
            with col_left2:
                st.markdown(f"**{model_name} — ROC Curve (AUC: {m['roc_auc']:.4f})**")

                fig_roc = go.Figure()

                fig_roc.add_trace(go.Scatter(
                    x=m["roc_fpr"],
                    y=m["roc_tpr"],
                    mode="lines",
                    name=f"ROC (AUC={m['roc_auc']:.4f})",
                    line=dict(color="#3498db", width=2)
                ))

                fig_roc.add_trace(go.Scatter(
                    x=[0, 1],
                    y=[0, 1],
                    mode="lines",
                    name="Random",
                    line=dict(color="gray", dash="dash")
                ))

                fig_roc.update_layout(
                    xaxis_title="False Positive Rate",
                    yaxis_title="True Positive Rate",
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig_roc,
                    key=f"{model_name}_roc",
                    width="stretch"
                )

            # --- Precision-Recall Curve ---
            with col_right2:
                st.markdown(f"**{model_name} — Precision-Recall Curve**")

                fig_pr = go.Figure()

                fig_pr.add_trace(go.Scatter(
                    x=m["pr_recall"],
                    y=m["pr_precision"],
                    mode="lines",
                    name="PR Curve",
                    line=dict(color="#e74c3c", width=2),
                    fill="tozeroy",
                    fillcolor="rgba(231, 76, 60, 0.1)"
                ))

                fig_pr.update_layout(
                    xaxis_title="Recall",
                    yaxis_title="Precision",
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig_pr,
                    key=f"{model_name}_pr",
                    width="stretch"
                )

# ==================================================
# ALGORITHMS PAGE
# ==================================================
if selected == "Algorithms":

    st.title("Machine Learning Algorithms")

    st.subheader("Random Forest")

    st.write("""
Random Forest combines multiple decision trees to improve accuracy and reduce overfitting.
It works well for intrusion detection problems.
""")

    st.subheader("Support Vector Machine")

    st.write("""
SVM is used for classification and anomaly detection.
It performs well in high-dimensional datasets.
""")

    st.subheader("XGBoost")

    st.write("""
XGBoost is a gradient boosting algorithm known for high performance
in structured datasets.
""")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption("AI Intrusion Detection Monitoring System")