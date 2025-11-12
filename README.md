# Spatial Data Optimization System for Disaster Response (Himachal Pradesh)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python) ![FastAPI](https://img.shields.io/badge/FastAPI-0.103-green?logo=fastapi) ![PostGIS](https://img.shields.io/badge/PostGIS-3.4-blue?logo=postgresql) ![Leaflet](https://img.shields.io/badge/Leaflet-1.9-green?logo=leaflet)

A high-performance backend API and dashboard to find optimal routes for emergency services in geographically complex regions. This system calculates the nearest available resources (hospitals, rescue teams) while actively avoiding real-time hazard zones like landslides and floods.

This prototype is populated with realistic data for the Himachal Pradesh, India, region (Mandi, Shimla, Kullu).

---

## Core Features

* **Real-time Asset Tracking:** Manages the locations of hospitals, police stations, and fire stations.
* **Dynamic Hazard Zones:** Models real-world dangers like landslides and flood plains as polygons.
* **Nearest Neighbor Search:** Instantly finds the closest *k*-nearest resources to an incident.
* **Safe Route Prioritization:** A powerful query that finds assets *within* a radius but *outside* any danger zone.
* **Interactive Map Dashboard:** A simple Leaflet.js frontend visualizes all assets, incidents, and zones in real-time.


## Tech Stack

* **Database:** **PostgreSQL** with the **PostGIS** extension (for all spatial data types and queries).
* **Backend API:** **FastAPI (Python)** for its high performance and asynchronous capabilities.
* **Frontend:** **Leaflet.js** (a lightweight, open-source mapping library).
* **Data Format:** **GeoJSON** (the web standard for geographic data).

---

## How to Run This Project

### 1. Prerequisites

* **Python 3.9+**
* **PostgreSQL** (v12+ recommended)
* **PostGIS Extension:** (Must be installed *for* your PostgreSQL instance)

### 2. Database Setup

1.  Open `pgAdmin` or `psql` and create a new database.
    ```sql
    CREATE DATABASE disaster_db;
    ```
2.  Connect to your new database and **enable the PostGIS extension**. This is a critical step.
    ```sql
    -- Connect to disaster_db
    \c disaster_db

    CREATE EXTENSION postgis;
    ```

### 3. Backend (FastAPI)

1.  Clone this repository:
    ```bash
    git clone [https://github.com/Commander-Kunal/YOUR-REPO-NAME.git](https://github.com/Commander-Kunal/YOUR-REPO-NAME.git)
    cd YOUR-REPO-NAME
    ```
2.  (Recommended) Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```
3.  Install the required libraries:
    ```bash
    pip install fastapi uvicorn psycopg[binary]
    ```
4.  **Edit `main.py`:** Update the `DB_DSN` string with your PostgreSQL username, password, and database name.
    ```python
    DB_DSN = "postgresql://postgres:YOUR_PASSWORD_HERE@127.0.0.1/disaster_db"
    ```
5.  Run the API server:
    ```bash
    python -m uvicorn main:app --reload
    ```
    The server is now running at `http://127.0.0.1:8000`.

### 4. Frontend (Leaflet)

1.  **No setup required!**
2.  Simply open the `index.html` file in any web browser.
3.  The map will automatically fetch data from your running FastAPI server (`http://127.0.0.1:8000`).

---

## API Endpoints

The API serves standard GeoJSON `FeatureCollection` objects.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root endpoint, confirms the API is running. |
| `GET` | `/api/resources` | Returns all available resources (hospitals, police, etc.) as points. |
| `GET` | `/api/zones` | Returns all active disaster zones (landslides, etc.) as polygons. |
| `GET` | `/api/incidents` | Returns all active incidents (accidents, fires, etc.) as points. |
