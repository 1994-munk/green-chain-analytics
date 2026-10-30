"""
GreenChain Analytics API
Repository: green-chain-analytics

A clean, human-readable Python microservice that:
- validates shipment telemetry using Pydantic schema guardrails,
- generates Data Vault 2.0 MD5 hash keys,
- predicts fuel consumption and CO2 emissions with a lightweight scikit-learn model.
"""

import hashlib
import os
import sqlite3
from datetime import datetime, timezone

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.linear_model import LinearRegression


# Application initialization
app = FastAPI(
    title="GreenChain Analytics",
    description="Data Vault 2.0 & Carbon Footprint Machine Learning API",
    version="1.0.0",
)


# Input and output models
class ShipmentInput(BaseModel):
    shipment_id: str = Field(
        ..., example="SHP_10045", description="Unique shipment identifier"
    )
    carrier_code: str = Field(
        ..., example="DHL_EXPRESS", description="Unique carrier code"
    )
    distance_km: float = Field(
        ..., gt=0, example=450.5, description="Total transit distance in kilometers"
    )
    weight_kg: float = Field(
        ..., gt=0, example=1200.0, description="Total cargo weight in kilograms"
    )


class PredictionResponse(BaseModel):
    shipment_id: str
    hk_shipment: str
    hk_carrier: str
    estimated_fuel_liters: float
    estimated_carbon_kg: float
    status: str
    processed_at: datetime


# Data Vault 2.0 hash generator and ML model setup

def generate_vault_hash(business_key: str) -> str:
    """Create a standard MD5 hash for a business key in a Data Vault 2.0 model."""
    cleaned_key = business_key.strip().upper()
    return hashlib.md5(cleaned_key.encode("utf-8")).hexdigest()


# A lightweight regression model for demonstration.
# Features: [Distance (km), Weight (kg)] -> Target: Fuel Consumption (Liters)
X_train = np.array(
    [
        [100, 500],
        [200, 1000],
        [500, 2500],
        [1000, 5000],
    ]
)
y_train_fuel = np.array([13.0, 26.0, 65.0, 130.0])

ml_model = LinearRegression()
ml_model.fit(X_train, y_train_fuel)

DB_PATH = os.path.join(os.path.dirname(__file__), "greenchain.db")


def get_db_connection() -> sqlite3.Connection:
    """Open a SQLite connection for the app's Data Vault tables."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    """Create the local SQLite tables used by the service."""
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS hub_shipment (
                hk_shipment TEXT PRIMARY KEY,
                shipment_id TEXT NOT NULL UNIQUE,
                load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                record_source TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS hub_carrier (
                hk_carrier TEXT PRIMARY KEY,
                carrier_code TEXT NOT NULL UNIQUE,
                load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                record_source TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS link_shipment_carrier (
                hk_shipment_carrier TEXT PRIMARY KEY,
                hk_shipment TEXT NOT NULL,
                hk_carrier TEXT NOT NULL,
                load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                record_source TEXT NOT NULL,
                UNIQUE (hk_shipment, hk_carrier),
                FOREIGN KEY (hk_shipment) REFERENCES hub_shipment(hk_shipment),
                FOREIGN KEY (hk_carrier) REFERENCES hub_carrier(hk_carrier)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sat_shipment_metrics (
                hk_shipment TEXT NOT NULL,
                load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                distance_km REAL NOT NULL,
                fuel_used_liters REAL NOT NULL,
                carbon_emitted_kg REAL NOT NULL,
                record_source TEXT NOT NULL,
                PRIMARY KEY (hk_shipment, load_date),
                FOREIGN KEY (hk_shipment) REFERENCES hub_shipment(hk_shipment)
            )
            """
        )
        connection.commit()


def persist_prediction(payload: ShipmentInput, predicted_fuel: float, predicted_carbon: float) -> None:
    """Save the prediction into the local Data Vault tables."""
    now = datetime.now(timezone.utc).isoformat()
    hk_shipment = generate_vault_hash(payload.shipment_id)
    hk_carrier = generate_vault_hash(payload.carrier_code)

    with get_db_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO hub_shipment (hk_shipment, shipment_id, load_date, record_source)
            VALUES (?, ?, ?, 'greenchain-api')
            """,
            (hk_shipment, payload.shipment_id, now),
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO hub_carrier (hk_carrier, carrier_code, load_date, record_source)
            VALUES (?, ?, ?, 'greenchain-api')
            """,
            (hk_carrier, payload.carrier_code, now),
        )
        hk_link = hashlib.md5(f"{hk_shipment}:{hk_carrier}".encode("utf-8")).hexdigest()
        connection.execute(
            """
            INSERT OR IGNORE INTO link_shipment_carrier (
                hk_shipment_carrier, hk_shipment, hk_carrier, load_date, record_source
            ) VALUES (?, ?, ?, ?, 'greenchain-api')
            """,
            (hk_link, hk_shipment, hk_carrier, now),
        )
        connection.execute(
            """
            INSERT INTO sat_shipment_metrics (
                hk_shipment, load_date, distance_km, fuel_used_liters, carbon_emitted_kg, record_source
            ) VALUES (?, ?, ?, ?, ?, 'greenchain-api')
            ON CONFLICT(hk_shipment, load_date) DO UPDATE SET
                distance_km = excluded.distance_km,
                fuel_used_liters = excluded.fuel_used_liters,
                carbon_emitted_kg = excluded.carbon_emitted_kg,
                record_source = excluded.record_source
            """,
            (
                hk_shipment,
                now,
                payload.distance_km,
                predicted_fuel,
                predicted_carbon,
            ),
        )
        connection.commit()


init_db()


# API endpoints
@app.get("/")
def home():
    """Health check endpoint confirming API status."""
    return {
        "project": "green-chain-analytics",
        "status": "online",
        "message": "Welcome to GreenChain Analytics API!",
    }


@app.post("/predict-emissions", response_model=PredictionResponse)
def predict_emissions(data: ShipmentInput):
    """
    Receive shipment telemetry, generate Data Vault 2.0 hash keys,
    and predict the shipment's fuel use and CO2 emissions.
    """
    try:
        # 1. Generate Data Vault 2.0 hash keys
        hk_shipment = generate_vault_hash(data.shipment_id)
        hk_carrier = generate_vault_hash(data.carrier_code)

        # 2. Predict fuel consumption using the ML model
        input_features = np.array([[data.distance_km, data.weight_kg]])
        predicted_fuel = float(ml_model.predict(input_features)[0])

        # 3. Calculate emissions using a standard diesel conversion factor.
        predicted_carbon = round(predicted_fuel * 2.68, 2)
        predicted_fuel = round(predicted_fuel, 2)

        # 4. Persist the prediction to the local Data Vault SQLite database.
        persist_prediction(data, predicted_fuel, predicted_carbon)

        return PredictionResponse(
            shipment_id=data.shipment_id,
            hk_shipment=hk_shipment,
            hk_carrier=hk_carrier,
            estimated_fuel_liters=predicted_fuel,
            estimated_carbon_kg=predicted_carbon,
            status="SUCCESS",
            processed_at=datetime.now(timezone.utc),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(exc)}") from exc
