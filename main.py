
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from services.predict import predict_risk
from services.advisory_engine import get_advisory


app = FastAPI(
    title="White Root Rot Prediction & Advisory API",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=(
        r"http://localhost:\d+|https://.*\.azurestaticapps\.net"
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SensorData(BaseModel):
    Soil_pH: float
    Soil_Moisture_VWC: float
    Soil_Temp_C: float
    language: Literal["en", "si", "ta"] = "en"


def normalize_risk_level(raw_level: str) -> str:
    key = raw_level.strip().lower().replace(" risk", "")

    if key == "critical":
        return "High"

    if key in ("low", "medium", "high"):
        return key.capitalize()

    return "Medium"


def normalize_probabilities(raw_probs: dict) -> dict:
    merged = {
        "Low": 0.0,
        "Medium": 0.0,
        "High": 0.0,
    }

    for label, prob in raw_probs.items():
        key = label.strip().lower().replace(" risk", "")

        if key == "critical":
            key = "high"

        if key in ("low", "medium", "high"):
            merged[key.capitalize()] += float(prob)

    return {
        key: round(value, 3)
        for key, value in merged.items()
    }


@app.get("/")
def home():
    return {
        "message": "White Root Disease API Running",
        "supported_languages": ["en", "si", "ta"],
    }


def build_prediction_response(data: SensorData):
    result = predict_risk(
        data.Soil_pH,
        data.Soil_Moisture_VWC,
        data.Soil_Temp_C,
    )

    normalized_risk = normalize_risk_level(result["level"])

    probabilities = normalize_probabilities(
        result["probabilities"]
    )

    advisory_report = get_advisory(
        ph=data.Soil_pH,
        moisture=data.Soil_Moisture_VWC,
        temp=data.Soil_Temp_C,
        risk=normalized_risk.lower(),
        confidence=result["confidence"] / 100,
        language=data.language,
    )

    return {
        "prediction": {
            "risk_level": normalized_risk,
            "confidence": result["confidence"],
            "probabilities": probabilities,
        },
        "advisory": advisory_report,
    }


@app.post("/predict")
def predict(data: SensorData):
    return build_prediction_response(data)


@app.post("/advisory")
def advisory(data: SensorData):
    return build_prediction_response(data)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": True,
        "supported_languages": ["en", "si", "ta"],
    }
