# 🌿 GreenChain Analytics: Data Vault 2.0 & AI-Powered Carbon Optimization

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Data Vault](https://img.shields.io/badge/Architecture-Data_Vault_2.0-003B5C?style=for-the-badge)](https://datavaultalliance.com)
[![Docker](https://img.shields.io/badge/Docker-24.0+-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

An enterprise-grade, end-to-end data science & data engineering platform that integrates **Data Vault 2.0 architecture**, **strict schema validation**, and **predictive machine learning** to forecast carbon emissions, optimize freight logistics, and automate sustainability compliance reporting.

---

## 💡 Quick Overview & Architecture

```
                       [ Multi-Source Logistics Telemetry ]
                                       │
                                       ▼
                       [ Ingestion & Pandera Schema Guard ]
                                       │
                                       ▼
                     ┌──────────────────────────────────┐
                     │     Data Vault 2.0 Core Layer    │
                     │  (Hubs | Links | Satellites)     │
                     └──────────────────────────────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
      [ Feature Store / dbt Marts ]          [ ML Model Training Engine ]
                    │                                     │
                    └──────────────────┬──────────────────┘
                                       ▼
                        [ FastAPI + RAG Query Agent ]
```

---

## ✨ Key Features

- **🛡️ Strict Schema Guardrails**: Incoming raw streams validated using `Pydantic` and `Pandera` before reaching staging tables.
- **🏛️ Data Vault 2.0 Core**: High-concurrency relational modeling split into immutable **Hubs** (business keys), **Links** (relationships), and **Satellites** (context & point-in-time metrics).
- **🔮 Predictive Emissions Engine**: Automated XGBoost regression and time-series models for route delay forecasting and fuel burn reduction.
- **⚡ Async FastAPI REST API**: Containerized, low-latency microservice exposing prediction endpoints, metrics, and automated API documentation.

---


### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure VS Code Settings
1. Open VS Code Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`).
2. Type **Python: Select Interpreter** and select your active `./venv/bin/python`.
3. Recommended VS Code extensions:
   - **Python** (`ms-python.python`)
   - **Pylance** (`ms-python.vscode-pylance`)
   - **Docker** (`ms-azuretools.vscode-docker`)
   - **SQLTools** (`mtxr.sqltools`)

---

## 🚀 Running the Application

### Launch with Docker Compose
```bash
docker-compose up --build -d
```

### Access API Documentation
Once running, navigate to:
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Viewer**: `http://localhost:8000/redoc`

---

## 📊 Data Vault 2.0 Schema Overview

| Entity Type | Entity Name | Business Key / Hash Key |
| :--- | :--- | :--- |
| **Hub** | `hub_shipment` | `hk_shipment` (`shipment_id`) |
| **Hub** | `hub_carrier` | `hk_carrier` (`carrier_code`) |
| **Link** | `link_shipment_carrier` | `hk_shipment_carrier` |
| **Satellite** | `sat_shipment_emissions` | `hk_shipment` + `load_date` |

---

## 👤 Author

- **GitHub**: [@1994-munk](https://github.com/1994-munk)
