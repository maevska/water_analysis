from sqlalchemy import create_engine, Column, String, text
from sqlalchemy.ext.declarative import declarative_base
from app.database.database import SQLALCHEMY_DATABASE_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем движок базы данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

def upgrade():
    try:
        # Проверяем, существует ли колонка
        with engine.connect() as conn:
            # Получаем информацию о таблице
            result = conn.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result.fetchall()]
            
            # Если колонки нет, добавляем её
            if 'profile_photo' not in columns:
                logger.info("Adding profile_photo column to users table")
                conn.execute(text("ALTER TABLE users ADD COLUMN profile_photo VARCHAR"))
                conn.commit()
                logger.info("Successfully added profile_photo column")
            else:
                logger.info("profile_photo column already exists")
    except Exception as e:
        logger.error(f"Error in migration: {str(e)}")
        raise

def downgrade():
    try:
        # SQLite не поддерживает удаление колонок напрямую
        # Вместо этого создаем новую таблицу без колонки и копируем данные
        with engine.connect() as conn:
            # Создаем временную таблицу
            conn.execute(text("""
                CREATE TABLE users_temp (
                    id INTEGER PRIMARY KEY,
                    email VARCHAR NOT NULL UNIQUE,
                    username VARCHAR NOT NULL UNIQUE,
                    firstName VARCHAR NOT NULL,
                    lastName VARCHAR NOT NULL,
                    hashed_password VARCHAR NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            """))
            
            # Копируем данные из старой таблицы
            conn.execute(text("""
                INSERT INTO users_temp 
                SELECT id, email, username, firstName, lastName, hashed_password, 
                is_active, created_at, updated_at 
                FROM users
            """))
            
            # Удаляем старую таблицу
            conn.execute(text("DROP TABLE users"))
            
            # Переименовываем временную таблицу
            conn.execute(text("ALTER TABLE users_temp RENAME TO users"))
            
            conn.commit()
            logger.info("Successfully removed profile_photo column")
    except Exception as e:
        logger.error(f"Error in downgrade: {str(e)}")
        raise

if __name__ == "__main__":
    upgrade() 