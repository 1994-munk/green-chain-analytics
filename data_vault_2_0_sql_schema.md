-- GreenChain Analytics: Data Vault 2.0 Database Schema
-- Simple, clean tables for tracking shipments and carbon emissions

-- 1. HUBS (Business Keys)
-- Stores unique shipment IDs
CREATE TABLE IF NOT EXISTS hub_shipment (
    hk_shipment CHAR(64) PRIMARY KEY, -- MD5/SHA256 Hash of shipment_id
    shipment_id VARCHAR(50) NOT NULL UNIQUE,
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_source VARCHAR(100) NOT NULL
);

-- Stores unique carrier company codes
CREATE TABLE IF NOT EXISTS hub_carrier (
    hk_carrier CHAR(64) PRIMARY KEY, -- Hash of carrier_code
    carrier_code VARCHAR(50) NOT NULL UNIQUE,
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_source VARCHAR(100) NOT NULL
);

-- 2. LINKS (Relationships between Hubs)
-- Connects a shipment to its carrier
CREATE TABLE IF NOT EXISTS link_shipment_carrier (
    hk_shipment_carrier CHAR(64) PRIMARY KEY,
    hk_shipment CHAR(64) NOT NULL REFERENCES hub_shipment(hk_shipment),
    hk_carrier CHAR(64) NOT NULL REFERENCES hub_carrier(hk_carrier),
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_source VARCHAR(100) NOT NULL
);

-- 3. SATELLITES (Descriptive Data & Point-in-time metrics)
-- Stores emissions and distance measurements over time
CREATE TABLE IF NOT EXISTS sat_shipment_metrics (
    hk_shipment CHAR(64) NOT NULL REFERENCES hub_shipment(hk_shipment),
    load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    distance_km NUMERIC(10, 2) NOT NULL,
    fuel_used_liters NUMERIC(10, 2) NOT NULL,
    carbon_emitted_kg NUMERIC(10, 2) NOT NULL,
    record_source VARCHAR(100) NOT NULL,
    PRIMARY KEY (hk_shipment, load_date)
);