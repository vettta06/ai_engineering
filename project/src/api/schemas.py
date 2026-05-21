from pydantic import BaseModel, Field


class CreditApplication(BaseModel):
    """Credit application input data."""

    age: int = Field(..., ge=18, le=100)
    income: float = Field(..., gt=0)
    employment_years: int = Field(..., ge=0, le=50)
    loan_amount: float = Field(..., gt=0)
    credit_score: int = Field(..., ge=300, le=850)


class PredictionResponse(BaseModel):
    """Prediction response with risk assessment."""

    prediction: int
    prediction_label: str
    probability_high_risk: float
    probability_low_risk: float
    risk_category: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    model_name: str
    model_version: str
    ready: bool
