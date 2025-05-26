from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models.statistic_history import Prediction
from sqlalchemy import func

class PredictionService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_stats(self, user_id: int):
        total = self.db.query(Prediction).filter(
            Prediction.user_id == user_id
        ).count()

        week_ago = datetime.utcnow() - timedelta(days=7)
        weekly = self.db.query(Prediction).filter(
            Prediction.user_id == user_id,
            Prediction.created_at >= week_ago
        ).count()

        last_activity = self.db.query(
            func.max(Prediction.created_at)
        ).filter(Prediction.user_id == user_id).scalar()

        return {
            "total_predictions": total,
            "weekly_predictions": weekly,
            "last_activity": last_activity
        }

    def get_user_predictions(self, user_id: int, skip: int = 0, limit: int = 10):
        return self.db.query(Prediction).filter(
            Prediction.user_id == user_id
        ).order_by(
            Prediction.created_at.desc()
        ).offset(skip).limit(limit).all()