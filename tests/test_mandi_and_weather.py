import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

def test_mandi_prices_labeled_as_sample():
    with TestClient(app) as client:
        response = client.get("/api/v1/mandi-prices")
        assert response.status_code == 200
        data = response.json()
        assert data["data_type"] == "sample"
        assert data["api_available"] is False
        assert len(data["prices"]) > 0
        first_price = data["prices"][0]
        assert "min_price" in first_price
        assert "max_price" in first_price
        assert "modal_price" in first_price

def test_weather_labeled_as_sample():
    with TestClient(app) as client:
        response = client.get("/api/v1/weather?location=Karnal")
        assert response.status_code == 200
        data = response.json()
        assert data["data_type"] == "sample"
        assert "current" in data
        assert "forecast" in data
        assert data["location"] == "Karnal"

