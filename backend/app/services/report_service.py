import os
from pathlib import Path
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from typing import Dict
from app.core.exceptions import WaterQualityException
from .report_generator import WaterQualityReport

class ReportService:
    def __init__(self):
        self.report_generator = WaterQualityReport()

    def generate_report(self, data: Dict) -> FileResponse:
        try:
            required_fields = ["waterName", "waterQualityClass", "predictions"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                raise WaterQualityException(
                    status_code=400,
                    detail=f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"
                )
            
            if not isinstance(data["waterQualityClass"], dict) or "label" not in data["waterQualityClass"]:
                raise WaterQualityException(
                    status_code=400,
                    detail="Некорректная структура класса качества воды"
                )
            
            if not isinstance(data["predictions"], dict):
                raise WaterQualityException(
                    status_code=400,
                    detail="Некорректная структура предсказаний"
                )

            pdf_path = self.report_generator.generate_report(data)
            
            if not os.path.exists(pdf_path):
                raise WaterQualityException(
                    status_code=500,
                    detail="Файл отчета не был создан"
                )
                
            def cleanup():
                try:
                    os.unlink(pdf_path)
                except Exception:
                    pass
                    
            return FileResponse(
                pdf_path,
                media_type='application/pdf',
                filename=f'water-quality-report-{data["waterName"]}.pdf',
                background=BackgroundTask(cleanup)
            )
            
        except Exception as e:
            if isinstance(e, WaterQualityException):
                raise e
            raise WaterQualityException(
                status_code=500,
                detail=f"Ошибка при создании отчета: {str(e)}"
            ) 