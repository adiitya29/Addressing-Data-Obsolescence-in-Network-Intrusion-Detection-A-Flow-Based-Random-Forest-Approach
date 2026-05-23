import os
import json
import pandas as pd
import numpy as np
import logging
import datetime
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, auc, precision_recall_curve
)
from joblib import dump


# =========================
# Logger Setup
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("logs/train.log"), logging.StreamHandler()],
)

logger = logging.getLogger()

os.makedirs("logs", exist_ok=True)
os.makedirs("src/models/output", exist_ok=True)


# =========================
# Constants
# =========================
DATA_PATH = "data/preprocess/preprocessed_data.csv"
MODEL_PATH = "src/models/output/IDS.joblib"
METRICS_PATH = "src/models/output/model_metrics.json"
TARGET_COLUMN = "attack_detected"


# =========================
# Load Data
# =========================
def load_data(path: str) -> pd.DataFrame:

    if not os.path.exists(path):
        logger.error(f"Data file not found {path}")
        raise FileNotFoundError(f"Data file not found {path}")

    logger.info(f"Loading data from {path}")
    df = pd.read_csv(path)

    logger.info(f"Data loaded successfully with shape: {df.shape}")

    return df


# =========================
# Train Models
# =========================
def train_models(X_train, X_test, y_train, y_test):

    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            class_weight="balanced",
            random_state=42
        ),

        "SVM": SVC(
            kernel="rbf",
            probability=True
        ),

        "XGBoost": XGBClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=6,
            eval_metric="logloss"
        )
    }

    best_model = None
    best_accuracy = 0
    best_model_name = ""
    all_metrics = {}

    for name, model in models.items():

        logger.info(f"Training {name} model...")

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)

        # ROC curve data
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        roc_auc = auc(fpr, tpr)

        # Precision-Recall curve data
        pr_precision, pr_recall, _ = precision_recall_curve(y_test, y_proba)

        all_metrics[name] = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "confusion_matrix": cm.tolist(),
            "roc_fpr": [round(x, 4) for x in fpr[::max(1, len(fpr)//50)]],
            "roc_tpr": [round(x, 4) for x in tpr[::max(1, len(tpr)//50)]],
            "roc_auc": round(roc_auc, 4),
            "pr_precision": [round(x, 4) for x in pr_precision[::max(1, len(pr_precision)//50)]],
            "pr_recall": [round(x, 4) for x in pr_recall[::max(1, len(pr_recall)//50)]]
        }

        logger.info(f"{name} — Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f}")

        if acc > best_accuracy:

            best_accuracy = acc
            best_model = model
            best_model_name = name

    # Save all metrics to JSON
    with open(METRICS_PATH, "w") as f:
        json.dump(all_metrics, f, indent=2)
    logger.info(f"All model metrics saved to {METRICS_PATH}")

    logger.info(f"Best Model: {best_model_name} with accuracy {best_accuracy:.4f}")

    return best_model


# =========================
# Save Model
# =========================
def save_model(model):

    if os.path.exists(MODEL_PATH):
        logger.warning("Model already exists. Overwriting...")

    dump(model, MODEL_PATH)

    logger.info(f"Model saved to {MODEL_PATH}")

    # Save versioned model
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    version_path = f"src/models/output/model_{timestamp}.joblib"

    dump(model, version_path)

    logger.info(f"Backup model saved to {version_path}")


# =========================
# Main Pipeline
# =========================
def main():

    logger.info("IDS model training started...")

    try:

        df = load_data(DATA_PATH)

        if TARGET_COLUMN not in df.columns:
            raise ValueError(f"Target column '{TARGET_COLUMN}' not found.")

        X = df.drop(columns=[TARGET_COLUMN])
        y = df[TARGET_COLUMN]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            stratify=y,
            random_state=42
        )

        best_model = train_models(X_train, X_test, y_train, y_test)

        save_model(best_model)

    except Exception as e:

        logger.exception(f"Training pipeline failed: {e}")

    logger.info("IDS training pipeline completed.")


if __name__ == "__main__":
    main()