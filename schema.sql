-- GreenChain Analytics: Data Vault 2.0 schema
-- SQLite-compatible schema used by the FastAPI service.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS hub_shipment (
    hk_shipment TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL UNIQUE,
    load_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    record_source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hub_carrier (
    hk_carrier TEXT PRIMARY KEY,
    carrier_code TEXT NOT NULL UNIQUE,
    load_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    record_source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS link_shipment_carrier (
    hk_shipment_carrier TEXT PRIMARY KEY,
    hk_shipment TEXT NOT NULL,
    hk_carrier TEXT NOT NULL,
    load_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    record_source TEXT NOT NULL,
    UNIQUE (hk_shipment, hk_carrier),
    FOREIGN KEY (hk_shipment) REFERENCES hub_shipment(hk_shipment),
    FOREIGN KEY (hk_carrier) REFERENCES hub_carrier(hk_carrier)
);

CREATE TABLE IF NOT EXISTS sat_shipment_metrics (
    hk_shipment TEXT NOT NULL,
    load_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    distance_km REAL NOT NULL CHECK (distance_km > 0),
    fuel_used_liters REAL NOT NULL CHECK (fuel_used_liters >= 0),
    carbon_emitted_kg REAL NOT NULL CHECK (carbon_emitted_kg >= 0),
    record_source TEXT NOT NULL,
    PRIMARY KEY (hk_shipment, load_date),
    FOREIGN KEY (hk_shipment) REFERENCES hub_shipment(hk_shipment)
);

CREATE INDEX IF NOT EXISTS idx_hub_shipment_record_source
    ON hub_shipment(record_source);

CREATE INDEX IF NOT EXISTS idx_hub_carrier_record_source
    ON hub_carrier(record_source);

CREATE INDEX IF NOT EXISTS idx_link_shipment
    ON link_shipment_carrier(hk_shipment);

CREATE INDEX IF NOT EXISTS idx_link_carrier
    ON link_shipment_carrier(hk_carrier);
