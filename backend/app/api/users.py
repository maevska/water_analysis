from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models.user import User
from app.database.models.statistic_history import Prediction
from app.schemas.user import User as UserSchema
from app.core.security import get_current_user
import os
import shutil
from datetime import datetime

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

PROFILE_PHOTOS_DIR = "profile_photos"
os.makedirs(PROFILE_PHOTOS_DIR, exist_ok=True)

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/me/photo")
async def upload_profile_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл должен быть изображением"
        )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{current_user.username}_{timestamp}{file_extension}"
    file_path = os.path.join(PROFILE_PHOTOS_DIR, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        if current_user.profile_photo:
            old_photo_path = os.path.join(PROFILE_PHOTOS_DIR, os.path.basename(current_user.profile_photo))
            if os.path.exists(old_photo_path):
                os.remove(old_photo_path)
        
        current_user.profile_photo = file_path
        db.commit()
        
        return {
            "message": "Фото профиля успешно загружено",
            "photo_path": file_path
        }
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при загрузке фото: {str(e)}"
        )

@router.get("/{user_id}/stats")
async def get_user_stats(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    

    predictions = db.query(Prediction).filter(Prediction.user_id == user_id).all()
    
    total_predictions = len(predictions)
    completed_predictions = len([p for p in predictions if p.status == "completed"])
    error_predictions = len([p for p in predictions if p.status == "error"])
    
    last_prediction = db.query(Prediction)\
        .filter(Prediction.user_id == user_id)\
        .order_by(Prediction.created_at.desc())\
        .first()
    
    quality_classes = [
        p.water_quality_class.get('class', 0) 
        for p in predictions 
        if p.status == "completed" and p.water_quality_class
    ]
    avg_quality_class = sum(quality_classes) / len(quality_classes) if quality_classes else 0
    
    stats = {
        "user_id": user.id,
        "username": user.username,
        "total_predictions": total_predictions,
        "completed_predictions": completed_predictions,
        "error_predictions": error_predictions,
        "last_prediction_date": last_prediction.created_at if last_prediction else None,
        "average_quality_class": round(avg_quality_class, 2)
    }
    
    return stats

@router.get("/{user_id}/predictions")
async def get_user_predictions(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    predictions = db.query(Prediction)\
        .filter(Prediction.user_id == user_id)\
        .order_by(Prediction.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return predictions 