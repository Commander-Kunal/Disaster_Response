from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from psycopg.rows import dict_row
import json

app = FastAPI()

# 1. Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Database Connection String (Update with your credentials!)
DB_DSN = "postgresql://postgres:YOUR_PASSWORD_HERE@127.0.0.1/Disaster_db"

def get_db_connection():
    return psycopg.connect(DB_DSN, row_factory=dict_row)

# Helper function to wrap PostGIS results in a standard GeoJSON FeatureCollection
def create_feature_collection(rows):
    features = []
    for row in rows:
        # Load the GeoJSON string from DB into a real Python dict
        geometry = json.loads(row['geojson'])
        # Create standard GeoJSON Feature structure
        feature = {
            "type": "Feature",
            "geometry": geometry,
            "properties": {k: v for k, v in row.items() if k != 'geojson'}
        }
        features.append(feature)
    return {"type": "FeatureCollection", "features": features}

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"message": "Disaster Response API is running"}

@app.get("/api/resources")
def get_resources():
    with get_db_connection() as conn:
        # We use ST_AsGeoJSON(location) to get the geometry ready for the web
        res = conn.execute("SELECT id, name, type, status, ST_AsGeoJSON(location) as geojson FROM resources").fetchall()
        return create_feature_collection(res)

@app.get("/api/zones")
def get_zones():
    with get_db_connection() as conn:
        res = conn.execute("SELECT id, description, severity, ST_AsGeoJSON(area) as geojson FROM disaster_zones").fetchall()
        return create_feature_collection(res)

@app.get("/api/incidents")
def get_incidents():
    with get_db_connection() as conn:
        res = conn.execute("SELECT id, description, ST_AsGeoJSON(location) as geojson FROM incidents").fetchall()
        return create_feature_collection(res)