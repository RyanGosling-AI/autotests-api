from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    """
    Описание модели GET User запроса
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias='lastName')
    first_name: str = Field(alias='firstName')
    middle_name: str = Field(alias='middleName')


class UserCreate(BaseModel):
    """
    Описание модели создания пользователя
    """
    email: EmailStr
    password: str
    last_name: str = Field(alias='lastName')
    first_name: str = Field(alias='firstName')
    middle_name: str = Field(alias='middleName')


class CreateUserResponseSchema(BaseModel):
    """
    Описание модели ответа GET User
    """
    user: UserSchema
