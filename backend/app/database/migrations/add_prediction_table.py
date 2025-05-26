from sqlalchemy import create_engine, Column, String, text
from sqlalchemy.ext.declarative import declarative_base
from app.database.database import SQLALCHEMY_DATABASE_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

def upgrade():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='predictions'"))
            if not result.fetchone():
                logger.info("Creating predictions table")
                conn.execute(text("""
                    CREATE TABLE predictions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        water_name VARCHAR NOT NULL,
                        parameters JSON NOT NULL,
                        results JSON,
                        water_quality_class JSON,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status VARCHAR NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """))

                conn.execute(text("""
                    CREATE INDEX idx_predictions_user_id ON predictions(user_id)
                """))

                conn.commit()
                logger.info("Successfully created predictions table and index")
            else:
                logger.info("Predictions table already exists")
    except Exception as e:
        logger.error(f"Error in migration: {str(e)}")
        raise

def downgrade():
    try:
        with engine.connect() as conn:

            conn.execute(text("DROP INDEX IF EXISTS idx_predictions_user_id"))

            conn.execute(text("DROP TABLE IF EXISTS predictions"))
            
            conn.commit()
            logger.info("Successfully removed predictions table and index")
    except Exception as e:
        logger.error(f"Error in downgrade: {str(e)}")
        raise

if __name__ == "__main__":
    upgrade()