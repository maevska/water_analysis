from pydantic import BaseModel
from typing import Dict, Optional

class WaterData(BaseModel):
    waterName: str
    coordinates: Dict[str, float]
    parameters: Dict[str, float]

class WaterQualityClass(BaseModel):
    raw: str
    label: str

class PredictionResponse(BaseModel):
    predictions: Dict[str, float]
    waterQualityClass: WaterQualityClass
    plot: Optional[str] = None

class WaterReportData(BaseModel):
    waterName: str
    coordinates: Dict[str, float]
    predictions: Dict[str, float]
    waterQualityClass: Dict[str, str]
    plot: Optional[str] = None
    parameters: Dict[str, float] 