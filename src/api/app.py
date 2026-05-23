from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import joblib
import io

app = FastAPI(
    title="Network Intrusion Detection API",
    description="API to predict intrusions from uploaded network traffic CSV files",
    version="1.0"
)

MODEL_PATH = "src/models/output/IDS.joblib"

# Load your model once at startup
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV file: {e}")

    try:
        # Make predictions
        preds = model.predict(df)
        # If model supports probabilities, include them
        probs = model.predict_proba(df).tolist() if hasattr(model, "predict_proba") else None

        results = []
        for i, pred in enumerate(preds):
            res = {"prediction": int(pred)}
            if probs:
                res["probability"] = probs[i]
            results.append(res)

        return JSONResponse(content={"results": results})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
