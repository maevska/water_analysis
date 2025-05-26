import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем абсолютный путь к директории backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Путь к файлу базы данных
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'sql_app.db')}"

logger.info(f"Database URL: {DATABASE_URL}")

# Создаем движок базы данных с дополнительными настройками
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30  # Увеличиваем таймаут
    },
    echo=True  # Включаем логирование SQL-запросов
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Отключаем автоматическое истечение срока действия объектов
)

# Создаем базовый класс для моделей
Base = declarative_base()

def get_db():
    """
    Функция-зависимость для получения сессии базы данных.
    Гарантирует закрытие сессии после использования.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Инициализация базы данных - создание всех таблиц.
    """
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

# Экспортируем URL базы данных для миграций
SQLALCHEMY_DATABASE_URL = DATABASE_URL 