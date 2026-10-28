
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Body

# Initialize FastAPI
app = FastAPI(
    title="Student Performance Prediction API",
    description="Predict student exam scores using a trained ML model",
    version="1.0.0"
)

# Load the trained model
MODEL_PATH = Path(__file__).parent / "student_performance_model.joblib"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}"
    )

saved = joblib.load(MODEL_PATH)

model = saved["model"]
features = saved["features"]


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Student Performance Prediction API is running",
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": True
    }


# Prediction endpoint
@app.post("/predict")
def predict(student: dict = Body(...)):
    try:
        # Check that all required input features are present
        missing = [feature for feature in features if feature not in student]

        if missing:
            raise HTTPException(
                status_code=422,
                detail={"missing_features": missing}
            )

        # Keep only the expected features in the correct order
        row = pd.DataFrame(
            [{feature: student[feature] for feature in features}],
            columns=features
        )

        # Predict exam score
        score = model.predict(row)[0]

        return {
            "predicted_exam_score": round(float(score), 2)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
