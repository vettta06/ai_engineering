import json
import joblib
import logging
from pathlib import Path

from fastapi import HTTPException

logger = logging.getLogger(__name__)


class ModelService:
    """Service responsible for loading and managing the ML model."""

    def __init__(self):
        self.model = None
        self.scaler = None
        self.config = None
        self.loaded = False

    def initialize(self, project_root: Path):
        """Load configuration and model artifacts."""
        if self.loaded:
            return

        config_path = project_root / "configs" / "model_config.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")

        with open(config_path, "r") as f:
            self.config = json.load(f)

        artifacts_path = project_root / "artifacts"
        model_path = artifacts_path / self.config["model_file"]
        scaler_path = artifacts_path / self.config["scaler_file"]

        if not model_path.exists() or not scaler_path.exists():
            raise FileNotFoundError("Model artifacts missing.")

        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.loaded = True
        logger.info("Model service initialized successfully.")

    def predict(self, features):
        """Predict risk based on input features."""
        if not self.loaded:
            raise HTTPException(status_code=500, detail="Model not loaded.")

        scaled_features = self.scaler.transform(features)

        prediction = self.model.predict(scaled_features)[0]
        probabilities = self.model.predict_proba(scaled_features)[0]

        return {"prediction": int(prediction), "probabilities": probabilities.tolist()}


model_service = ModelService()
