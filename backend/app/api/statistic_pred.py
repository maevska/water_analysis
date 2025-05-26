from fastapi import APIRouter, Depends, HTTPException
from services.historypred import PredictionService
from schemas.statistic import UserStats, PredictionResponse
from typing import List

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.get("/user/{user_id}/stats", response_model=UserStats)
async def get_user_stats(
    user_id: int,
    prediction_service: PredictionService = Depends()
):
    return prediction_service.get_user_stats(user_id)

@router.get("/user/{user_id}/predictions", response_model=List[PredictionResponse])
async def get_user_predictions(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    prediction_service: PredictionService = Depends()
):
    return prediction_service.get_user_predictions(user_id, skip, limit)