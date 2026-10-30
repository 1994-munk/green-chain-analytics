"""
GreenChain Analytics API
Repository: green-chain-analytics

A clean, human-readable Python microservice that:

Validates incoming shipment telemetry using Pydantic schema guardrails.

Generates Data Vault 2.0 MD5 hash keys for seamless data architecture storage.

Predicts estimated fuel consumption and CO2 emissions using a trained Scikit-Learn regression model.
"""

import hashlib
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import numpy as np
from sklearn.linear_model import LinearRegression



#APPLICATION INITIALIZATION



app = FastAPI(
title="GreenChain Analytics",
description="Data Vault 2.0 & Carbon Footprint Machine Learning API",
version="1.0.0"
)



#2. INPUT & OUTPUT DATA MODELS (Validation Guardrails)



class ShipmentInput(BaseModel):
shipment_id: str = Field(..., example="SHP_10045", description="Unique shipment identifier")
carrier_code: str = Field(..., example="DHL_EXPRESS", description="Unique carrier code")
distance_km: float = Field(..., gt=0, example=450.5, description="Total transit distance in kilometers")
weight_kg: float = Field(..., gt=0, example=1200.0, description="Total cargo weight in kilograms")

class PredictionResponse(BaseModel):
shipment_id: str
hk_shipment: str
hk_carrier: str
estimated_fuel_liters: float
estimated_carbon_kg: float
status: str
processed_at: datetime



#3. DATA VAULT 2.0 HASH GENERATOR & ML MODEL SETUP



def generate_vault_hash(business_key: str) -> str:
"""Creates a standardized MD5 hash key for Data Vault 2.0 entities."""
cleaned_key = business_key.strip().upper()
return hashlib.md5(cleaned_key.encode("utf-8")).hexdigest()

Training a lightweight regression model for demonstration

Features: [Distance (km), Weight (kg)] -> Target: Fuel Consumption (Liters)

X_train = np.array([
[100, 500],
[200, 1000],
[500, 2500],
[1000, 5000]
])
y_train_fuel = np.array([13.0, 26.0, 65.0, 130.0])

ml_model = LinearRegression()
ml_model.fit(X_train, y_train_fuel)



#4. API ENDPOINTS



@app.get("/")
def home():
"""Health check endpoint confirming API status."""
return {
"project": "green-chain-analytics",
"status": "online",
"message": "Welcome to GreenChain Analytics API!"
}

@app.post("/predict-emissions", response_model=PredictionResponse)
def predict_emissions(data: ShipmentInput):
"""
Receives shipment telemetry, calculates Data Vault 2.0 hash keys,
and returns ML-predicted carbon footprint metrics.
"""
try:
# 1. Generate Data Vault 2.0 Business Keys (Hashes)
hk_shipment = generate_vault_hash(data.shipment_id)
hk_carrier = generate_vault_hash(data.carrier_code)

    # 2. Predict fuel consumption using ML Model
    input_features = np.array([[data.distance_km, data.weight_kg]])
    predicted_fuel = float(ml_model.predict(input_features)[0])
    
    # 3. Calculate CO2 emissions (Standard Diesel conversion: ~2.68 kg CO2 per liter)
    predicted_carbon = round(predicted_fuel * 2.68, 2)
    predicted_fuel = round(predicted_fuel, 2)

    return PredictionResponse(
        shipment_id=data.shipment_id,
        hk_shipment=hk_shipment,
        hk_carrier=hk_carrier,
        estimated_fuel_liters=predicted_fuel,
        estimated_carbon_kg=predicted_carbon,
        status="SUCCESS",
        processed_at=datetime.utcnow()
    )
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
