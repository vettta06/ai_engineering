import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.api.dependencies import model_service, ModelService


@pytest.fixture
def mock_service():
    """Create a mocked ModelService instance."""
    mock = ModelService()
    mock.loaded = True
    mock.config = {
        "features": [
            "age",
            "income",
            "employment_years",
            "loan_amount",
            "credit_score",
        ],
        "risk_thresholds": {"low": 0.4, "high": 0.7},
        "model_file": "final_model_random_forest.pkl",
        "scaler_file": "scaler.pkl",
    }

    # Мокаем scaler.transform
    class MockScaler:
        def transform(self, x):
            return x

    mock.scaler = MockScaler()
    # Мокаем predict
    mock.predict = lambda x: {"prediction": 0, "probabilities": [0.85, 0.15]}
    return mock


@pytest.fixture
def client(mock_service):
    """Create test client with overridden dependency."""

    def override_get_service():
        return mock_service

    app.dependency_overrides[model_service.__class__] = override_get_service
    # Также нужно переопределить функцию get_model_service если она используется
    from src.api import endpoints

    app.dependency_overrides[endpoints.get_model_service] = lambda: mock_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_root_endpoint(client):
    """Test the root endpoint returns correct info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Credit Scoring API"
    assert "version" in data


def test_health_endpoint(client, mock_service):
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_name"] == "Random Forest"
    assert data["ready"] is True


def test_predict_valid_request(client, mock_service):
    """Test prediction with valid input data."""
    payload = {
        "age": 35,
        "income": 75000,
        "employment_years": 10,
        "loan_amount": 25000,
        "credit_score": 720,
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability_high_risk" in data
    assert "risk_category" in data
    assert data["risk_category"] in ["LOW", "MEDIUM", "HIGH"]


def test_predict_invalid_request(client):
    """Test prediction with invalid input data."""
    payload = {
        "age": 15,
        "income": 75000,
        "employment_years": 10,
        "loan_amount": 25000,
        "credit_score": 720,
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 422
