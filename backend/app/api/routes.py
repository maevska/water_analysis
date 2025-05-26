from fastapi import APIRouter, Depends, HTTPException
from app.schemas.water import WaterData, WaterReportData, PredictionResponse
from app.services.ml_service import MLService
from app.services.report_service import ReportService
from app.core.exceptions import WaterQualityException
from app.database.database import get_db
from app.database.models.statistic_history import Prediction
from app.core.security import get_current_user
from sqlalchemy.orm import Session

router = APIRouter()

LABEL_MAPPING = {
    'good': 'Хорошее качество воды',
    'medium': 'Среднее качество воды',
    'bad': 'Плохое качество воды'
}

def get_ml_service():
    return MLService()

def get_report_service():
    return ReportService()

@router.post("/predict", response_model=PredictionResponse)
async def predict(
    data: WaterData,
    ml_service: MLService = Depends(get_ml_service),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        predictions, water_quality_class, plot_data = ml_service.predict(data.parameters)
        
        prediction_record = Prediction(
            user_id=current_user.id,
            water_name=data.waterName,
            parameters=data.parameters,
            results=predictions,
            water_quality_class={
                "raw": water_quality_class,
                "label": LABEL_MAPPING[water_quality_class],
                "class": 1 if water_quality_class == "clean" else (2 if water_quality_class == "medium" else 3)
            },
            status="completed"
        )
        db.add(prediction_record)
        db.commit()
        
        return {
            "predictions": predictions,
            "waterQualityClass": {
                "raw": water_quality_class,
                "label": LABEL_MAPPING[water_quality_class]
            },
            "plot": plot_data
        }
    except Exception as e:
        prediction_record = Prediction(
            user_id=current_user.id,
            water_name=data.waterName,
            parameters=data.parameters,
            status="error"
        )
        db.add(prediction_record)
        db.commit()
        raise e

@router.post("/generate-report")
async def generate_report(
    data: WaterReportData,
    report_service: ReportService = Depends(get_report_service)
):
    return report_service.generate_report(data.dict()) 