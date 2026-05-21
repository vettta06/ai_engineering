import logging
from datetime import datetime

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException

from .dependencies import ModelService, model_service
from .schemas import CreditApplication, HealthResponse, PredictionResponse

logger = logging.getLogger(__name__)
router = APIRouter()


def get_model_service() -> ModelService:
    """Return the singleton model service instance."""
    return model_service


@router.get("/health", response_model=HealthResponse)
async def health_check(service: ModelService = Depends(get_model_service)):
    """Return service health status."""
    return HealthResponse(
        status="healthy",
        model_name="Random Forest",
        model_version="1.0.0",
        ready=service.loaded,
    )


@router.post("/predict", response_model=PredictionResponse)
async def predict_risk(
    application: CreditApplication, service: ModelService = Depends(get_model_service)
):
    """Predict credit risk for a given application."""
    try:
        df = pd.DataFrame([application.model_dump()])
        features = df[service.config["features"]]

        result = service.predict(features)
        prob_high = result["probabilities"][1]
        prob_low = result["probabilities"][0]

        thresholds = service.config["risk_thresholds"]
        if prob_high >= thresholds["high"]:
            category = "HIGH"
        elif prob_high >= thresholds["low"]:
            category = "MEDIUM"
        else:
            category = "LOW"

        return PredictionResponse(
            prediction=result["prediction"],
            prediction_label="High Risk" if result["prediction"] == 1 else "Low Risk",
            probability_high_risk=round(prob_high, 4),
            probability_low_risk=round(prob_low, 4),
            risk_category=category,
        )
    except Exception as e:
        logger.error("Prediction failed: %s", e)
        raise HTTPException(status_code=500, detail="Internal prediction error.") from e


@router.get("/metrics")
async def get_metrics():
    """Return basic service metrics."""
    return {"timestamp": datetime.utcnow().isoformat(), "status": "ok"}
