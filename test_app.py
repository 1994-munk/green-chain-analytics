import pytest
from fastapi.testclient import TestClient
from app import app

# Create a test client using FastAPI's built-in testing utilities
client = TestClient(app)


def test_health_check():
    """Verify that the health check endpoint returns a 200 OK status."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"
    assert response.json()["project"] == "GreenChain Analytics"


def test_predict_emissions_valid_data():
    """Test emission prediction with valid shipment input."""
    payload = {
        "shipment_id": "SHP_12345",
        "distance_km": 150.0,
        "cargo_weight_kg": 2500.0,
        "vehicle_type": "truck"
    }
    
    response = client.post("/predict", json=payload)
    
    # Assert successful response
    assert response.status_code == 200
    
    data = response.json()
    assert data["shipment_id"] == "SHP_12345"
    assert "estimated_carbon_kg" in data
    assert data["estimated_carbon_kg"] > 0
    assert data["data_vault_hash"] is not None


def test_predict_emissions_invalid_distance():
    """Test validation error when distance is zero or negative."""
    payload = {
        "shipment_id": "SHP_99999",
        "distance_km": -50.0,  # Invalid distance
        "cargo_weight_kg": 1000.0,
        "vehicle_type": "truck"
    }
    
    response = client.post("/predict", json=payload)
    
    # FastApi/Pydantic should intercept this with a 422 Unprocessable Entity
    assert response.status_code == 422