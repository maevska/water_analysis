from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.database.database import get_db
from app.database.models.user import User
from app.schemas.user import Token, UserCreate, User as UserSchema
import logging
import traceback
from app.core.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    try:
        body = await request.body()
        logger.info(f"Received registration request with body: {body.decode()}")
        
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            firstName=user.firstName,
            lastName=user.lastName,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User registered successfully: {user.username}")
        return db_user
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/token", response_model=Token)
@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        logger.info(f"User logged in successfully: {user.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        logger.error(f"HTTPException during login: {repr(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error during login: {repr(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/all-users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all() 

@router.get("/auth/verify")
async def verify_token(current_user = Depends(get_current_user)):
    return {"status": "valid"}