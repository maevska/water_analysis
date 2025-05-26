from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class PredictionCreate(BaseModel):
    water_name: str
    parameters: Dict
    results: Dict
    water_quality_class: Dict
    status: str

class PredictionResponse(BaseModel):
    id: int
    water_name: str
    created_at: datetime
    status: str
    water_quality_class: Dict

    class Config:
        orm_mode = True

class UserStats(BaseModel):
    total_predictions: int
    weekly_predictions: int
    last_activity: Optional[datetime]