# GreenChain Analytics

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![SQLite](https://img.shields.io/badge/DB-SQLite-003B57?style=for-the-badge)](https://www.sqlite.org/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)

A simple but practical sustainability platform for logistics and supply chains.

It helps companies answer a very real question:

> How much fuel and carbon does each shipment produce, and how can we track that in a clean, scalable, analytics-friendly way?

![Carbon footprint and sustainability workflow](https://media0.giphy.com/media/VllZnZs6vnZLQUV0at/giphy.gif)

---

## The problem it solves

Modern freight operations generate a lot of movement data, but that data is usually fragmented across:

- carriers and route systems
- shipment records
- spreadsheets and manual reports
- different operational teams

That makes it hard to:

- estimate emissions consistently
- trace shipment-level carbon impact
- build reliable data pipelines for sustainability reporting
- compare operational performance across routes and carriers

GreenChain Analytics solves this by combining:

- data validation
- Data Vault 2.0-style modeling
- machine learning predictions
- a clean API for shipment analysis

---

## What the project does

This project takes shipment telemetry such as:

- shipment ID
- carrier code
- distance in km
- cargo weight in kg

Then it:

1. validates the incoming data with Pydantic
2. generates a Data Vault hash key for each business entity
3. predicts fuel usage with a lightweight regression model
4. estimates CO2 emissions
5. stores the result in a local SQLite Data Vault-style schema

The result is a simple API that can be used as a base for more advanced supply-chain analytics, ESG reporting, or ML-powered logistics monitoring.

---

## Architecture at a glance

```text
Shipment input
      ↓
Pydantic validation
      ↓
MD5 Data Vault hashes
      ↓
ML fuel prediction
      ↓
CO2 estimation
      ↓
SQLite Data Vault tables
      ↓
FastAPI JSON response
```

---

## Tech stack

- Python 3.11
- FastAPI for the REST API
- Pydantic for schema validation
- SQLite for local persistence
- scikit-learn for fuel prediction
- Docker for containerized deployment
- Data Vault 2.0 concepts for traceable business keys and historical modeling

---

## Project structure

```text
green-chain-analytics/
├── main.py                # FastAPI app and prediction logic
├── schema.sql             # SQLite Data Vault tables
├── Dockerfile             # container config
├── docker-compose.yml     # local runtime config
├── requirements.txt       # Python dependencies
├── greenchain_analytics_readme.md   # project documentation
├── data_vault_2_0_sql_schema.md     # schema notes
└── venv/                  # local environment
```

---

## How to run locally

### 1) Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Start the API

```bash
uvicorn main:app --reload
```

Then open:

- Swagger UI: http://localhost:8000/docs
- API root: http://localhost:8000/

---

## Example prediction request

```bash
curl -X POST "http://localhost:8000/predict-emissions" \
  -H "Content-Type: application/json" \
  -d '{
    "shipment_id": "SHP_10045",
    "carrier_code": "DHL_EXPRESS",
    "distance_km": 450.5,
    "weight_kg": 1200.0
  }'
```

---

## Why this matters

This project is a clean starting point for:

- sustainable logistics analytics
- carbon accounting workflows
- freight visibility dashboards
- data engineering patterns built around Data Vault concepts
- real-world ML APIs for operational decision-making

It is intentionally simple enough to understand quickly, while still showing the right building blocks for a more production-ready solution.

---

## Author

- GitHub: [@1994-munk](https://github.com/1994-munk)

---

## License

This project is intended as an open, extensible starter project for logistics analytics and carbon footprint modeling.






