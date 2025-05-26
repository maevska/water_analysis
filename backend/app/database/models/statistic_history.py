from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base
from app.database.models.user import User

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    water_name = Column(String)
    parameters = Column(JSON)
    results = Column(JSON)
    water_quality_class = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # "completed" или "error"
    
    user = relationship("User", back_populates="predictions")