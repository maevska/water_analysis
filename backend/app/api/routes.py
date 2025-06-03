from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.schemas.water import WaterData, WaterReportData, PredictionResponse, CSVUploadResponse
from app.services.ml_service import MLService
from app.services.report_service import ReportService
from app.core.exceptions import WaterQualityException
from app.database.database import get_db
from app.database.models.statistic_history import Prediction
from app.core.security import get_current_user
from sqlalchemy.orm import Session
import pandas as pd
import io

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

@router.post("/upload-csv", response_model=CSVUploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Файл должен быть в формате CSV"
        )

    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        required_columns = ['water_name', 'temp_water', 'temp_air', 'precipitation', 
                    'water_level', 'ph', 'turbidity', 'oxygen', 'nitrates', 'ammonia']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}"
            )


        row = df.iloc[0]
        
        water_name = str(row['water_name'])
        parameters = {
            'temp_water': float(row['temp_water']),
            'temp_air': float(row['temp_air']),
            'precipitation': float(row['precipitation']),
            'water_level': float(row['water_level']),
            'ph': float(row['ph']),
            'turbidity': float(row['turbidity']),
            'oxygen': float(row['oxygen']),
            'nitrates': float(row['nitrates']),
            'ammonia': float(row['ammonia'])
        }

        return CSVUploadResponse(
            waterName=water_name,
            parameters=parameters,
            message="CSV файл успешно обработан"
        )

    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=400,
            detail="CSV файл пуст"
        )
    except pd.errors.ParserError:
        raise HTTPException(
            status_code=400,
            detail="Ошибка при чтении CSV файла"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка в данных: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обработке файла: {str(e)}"
        )

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