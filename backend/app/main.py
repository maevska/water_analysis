from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.api.auth import router as auth_router
from app.api.routes import router as api_router
from app.api.users import router as users_router
from app.database.database import init_db
from app.database.migrations.run_migrations import run_migrations
import logging
import sys
import os


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Water Quality Analysis API")

os.makedirs("profile_photos", exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/profile_photos", StaticFiles(directory="profile_photos"), name="profile_photos")

app.include_router(auth_router)
app.include_router(api_router, prefix="/api")
app.include_router(users_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.on_event("startup")
async def startup_event():
    init_db()
    try:
        run_migrations()
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Error running migrations: {str(e)}")
        raise
    
    logger.info("=== Registered Routes ===")
    for route in app.routes:
        if hasattr(route, "methods"):
            logger.info(f"Path: {route.path}")
            logger.info(f"Methods: {route.methods}")
            logger.info(f"Name: {route.name}")
            logger.info("---")
    logger.info("=======================")

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"} 