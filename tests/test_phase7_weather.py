"""
Tests for Phase 7 — Weather-Based Farming Guidance (IMD Agromet Advisory Integration)
"""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services import weather_service

def test_weather_locations_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/v1/weather/locations")
        assert res.status_code == 200
        data = res.json()
        assert "locations" in data
        assert data["total"] >= 10
        assert data["data_type"] == "sample"
        # Check pilot states present
        states = {loc["state"] for loc in data["locations"]}
        assert "Haryana" in states
        assert "Punjab" in states
        assert "Uttar Pradesh" in states
        assert "Rajasthan" in states
        assert "Himachal Pradesh" in states
        assert "Uttarakhand" in states

def test_weather_status_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/v1/weather/status")
        assert res.status_code == 200
        data = res.json()
        assert data["provider"] == "India Meteorological Department (IMD)"
        assert "written permission" in data["commercial_use"].lower()
        assert data["data_type_in_use"] == "sample"
        assert "mausam.imd.gov.in" in data["weather_portal"]
        assert "agromet.imd.gov.in" in data["agromet_portal"]

def test_weather_parameters_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/v1/weather/parameters")
        assert res.status_code == 200
        data = res.json()
        assert "parameters" in data
        assert data["total"] >= 5
        param_names = [p["parameter"] for p in data["parameters"]]
        assert "rainfall" in param_names
        assert "temperature_max" in param_names
        assert "wind_speed" in param_names

def test_weather_karnal_sample_data():
    with TestClient(app) as client:
        res = client.get("/api/v1/weather?location=Karnal")
        assert res.status_code == 200
        data = res.json()
        assert data["location"] == "Karnal"
        assert data["state"] == "Haryana"
        assert data["data_type"] == "sample"
        assert "IMD" in data["data_source"]
        assert len(data["forecast"]) == 5
        assert "spray_advisory" in data
        assert "irrigation_advisory" in data
        assert "harvest_advisory" in data
        # Check computed property
        assert "current" in data
        assert data["current"]["temperature"] == data["temperature"]
        assert len(data["farm_advisories"]) == 3

def test_weather_spray_advisory_logic():
    # Low wind condition (<10 km/h) -> should be 'good'
    spray_good = weather_service.compute_spray_advisory(wind_speed=7.5, rainfall_prob=10, humidity=50)
    assert spray_good["status"] == "good"

    # High wind condition (>15 km/h) -> should be 'danger'
    spray_danger = weather_service.compute_spray_advisory(wind_speed=18.0, rainfall_prob=5, humidity=40)
    assert spray_danger["status"] == "danger"
    assert "न करें" in spray_danger["message_hi"]

    # Caution condition (10-15 km/h)
    spray_caution = weather_service.compute_spray_advisory(wind_speed=12.5, rainfall_prob=10, humidity=50)
    assert spray_caution["status"] == "caution"

def test_weather_dedicated_advisory_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/v1/weather/advisory?location=Ludhiana")
        assert res.status_code == 200
        data = res.json()
        assert data["location"] == "Ludhiana"
        assert data["data_type"] == "sample"
        assert "spray_advisory" in data
        assert "irrigation_advisory" in data
        assert "harvest_advisory" in data

def test_weather_invalid_location_fallback():
    with TestClient(app) as client:
        res = client.get("/api/v1/weather?location=UnknownVillage999")
        assert res.status_code == 200
        data = res.json()
        assert data["data_type"] == "sample"
        # Falls back to default station
        assert data["resolved_station"] == "default"
        assert data["location"] == "Northern Plain Zone"

