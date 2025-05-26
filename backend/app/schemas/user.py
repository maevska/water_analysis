from pydantic import BaseModel, EmailStr, Field, validator
import re

class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        example="user@example.com",
        description="Email пользователя"
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        example="username",
        description="Имя пользователя (3-50 символов)"
    )
    firstName: str = Field(
        ...,
        min_length=2,
        max_length=50,
        example="Иван",
        description="Имя пользователя (2-50 символов)"
    )
    lastName: str = Field(
        ...,
        min_length=2,
        max_length=50,
        example="Иванов",
        description="Фамилия пользователя (2-50 символов)"
    )
    profile_photo: str | None = Field(
        None,
        example="profile_photos/user123.jpg",
        description="Путь к фото профиля"
    )

    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username должен содержать только буквы, цифры и символ подчеркивания')
        return v

    @validator('firstName', 'lastName')
    def name_validation(cls, v):
        if not re.match(r'^[а-яА-Яa-zA-Z\s-]+$', v):
            raise ValueError('Имя и фамилия должны содержать только буквы, пробелы и дефисы')
        return v

class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=6,
        example="password123",
        description="Пароль (минимум 6 символов)"
    )
    confirmPassword: str = Field(
        ...,
        min_length=6,
        example="password123",
        description="Подтверждение пароля"
    )

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError('Пароль должен содержать минимум 6 символов')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r'[a-z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        if not re.search(r'\d', v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v

    @validator('confirmPassword')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "username",
                "firstName": "Иван",
                "lastName": "Иванов",
                "password": "Password123",
                "confirmPassword": "Password123"
            }
        }

class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None 