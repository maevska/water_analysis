import os
import importlib.util
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    # Получаем путь к директории с миграциями
    migrations_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Получаем список всех файлов миграций
    migration_files = [f for f in os.listdir(migrations_dir) 
                    if f.endswith('.py') and f != '__init__.py' and f != 'run_migrations.py']
    
    # Сортируем файлы по имени
    migration_files.sort()
    
    for migration_file in migration_files:
        try:
            # Загружаем модуль миграции
            module_name = os.path.splitext(migration_file)[0]
            file_path = os.path.join(migrations_dir, migration_file)
            
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Запускаем миграцию
            logger.info(f"Running migration: {migration_file}")
            module.upgrade()
            logger.info(f"Successfully applied migration: {migration_file}")
            
        except Exception as e:
            logger.error(f"Error running migration {migration_file}: {str(e)}")
            raise

if __name__ == "__main__":
    run_migrations() 