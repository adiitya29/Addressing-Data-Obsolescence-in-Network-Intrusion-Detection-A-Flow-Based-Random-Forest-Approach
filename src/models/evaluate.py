import os
import joblib
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import logging
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# =========================
# Configuration
# =========================
MODEL_PATH = "src/models/output/IDS.joblib"
DATA_PATH = "data/preprocess/preprocessed_data.csv"
TARGET_COL = "attack_detected"
OUTPUT_DIR = "src/models/output"

# =========================
# Logger Setup
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("evaluate.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# =========================
# Loaders
# =========================
def load_data(data_path):
    """
    Load the preprocessed dataset from a CSV file,
    and separate features and target column.
    """
    logger.info(f"Loading preprocessed data from '{data_path}'")
    df = pd.read_csv(data_path)
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]
    logger.info(f"Data loaded: {df.shape[0]} samples, {df.shape[1]} columns (including target)")
    return X, y

def load_model(model_path):
    """
    Load the trained ML model from disk.
    """
    logger.info(f"Loading trained model from '{model_path}'")
    model = joblib.load(model_path)
    logger.info("Model loaded successfully")
    return model

# =========================
# Evaluation
# =========================
def evaluate_model(model, X, y):
    """
    Evaluate the model on the dataset,
    print classification report and save confusion matrix.
    """
    logger.info("Starting model evaluation...")
    y_pred = model.predict(X)

    report = classification_report(y, y_pred)
    acc = accuracy_score(y, y_pred)
    cm = confusion_matrix(y, y_pred)

    logger.info("\nClassification Report:\n" + report)
    logger.info(f"Accuracy: {acc:.4f}")

    # Confusion matrix plot
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.tight_layout()

    cm_path = os.path.join(OUTPUT_DIR, "confusion_matrix.png")
    plt.savefig(cm_path)
    plt.close()
    logger.info(f"Confusion matrix saved to: {cm_path}")

# =========================
# SHAP Explainability
# =========================
def explain_with_shap(model, X):
    """
    Generate SHAP explainability plots to visualize feature importance.
    Handles both default Explainer and TreeExplainer fallback.
    Only SHAP summary plot is generated (bar plot removed).
    """
    logger.info("Generating SHAP explanation...")

    try:
        explainer = shap.Explainer(model, X)
        shap_values = explainer(X, check_additivity=False)
        is_tree_explainer = False
    except Exception as e:
        logger.warning(f"Default SHAP Explainer failed: {e}. Trying TreeExplainer...")
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X, check_additivity=False)
        is_tree_explainer = True

    # SHAP summary plot only
    try:
        plt.figure()
        if is_tree_explainer and isinstance(shap_values, list):
            shap.summary_plot(shap_values[1], X, show=False)  # class 1
        else:
            shap.summary_plot(shap_values, X, show=False)

        summary_path = os.path.join(OUTPUT_DIR, "shap_summary.png")
        plt.savefig(summary_path, bbox_inches='tight')
        plt.close()
        logger.info(f"SHAP summary plot saved to: {summary_path}")
    except Exception as e:
        logger.warning(f"SHAP summary plot failed: {e}")

# =========================
# Main Entry Point
# =========================
def main():
    """
    Main function to run model evaluation and explainability.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    X, y = load_data(DATA_PATH)
    model = load_model(MODEL_PATH)

    evaluate_model(model, X, y)

    # SAMPLE DATA FOR FASTER SHAP
    X_sample = X.sample(n=500, random_state=42)  # You can adjust n as needed
    explain_with_shap(model, X_sample)

    logger.info("Evaluation and explainability complete.")

if __name__ == "__main__":
    main()
