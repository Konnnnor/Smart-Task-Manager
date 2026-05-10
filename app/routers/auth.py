import jwt
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.crud.user import create_user, get_user_by_email
from app.schemas.Token import Token
from app.schemas.userSchemas import UserSchemas, UserSchemasResponse

router = APIRouter()


@router.post("/registration", response_model=UserSchemasResponse,
                                    status_code=status.HTTP_201_CREATED,
                                    tags=["auth"], description="User registration")
async def get_registration(user_create: UserSchemas, db:AsyncSession= Depends(get_db)):
   return await create_user(user_create, db)

@router.post("/login", response_model=Token,
                            status_code=status.HTTP_200_OK,
                            tags=["auth"], description="User login")
async def login(form_data: OAuth2PasswordRequestForm= Depends(), db:AsyncSession= Depends(get_db)) :

    user=await get_user_by_email(db, form_data.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect email or password")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")

    access_token=create_access_token(data={"sub":user.email})
    return {"access_token":access_token, "token_type":"bearer" }
