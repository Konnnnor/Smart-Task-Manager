from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db

from app.dependencies.depends import get_current_user
from app.models.users import UserModel

from app.schemas.userSchemas import UserSchemasResponse, UserSchemasUpdate
from app.crud.user import update_user

router= APIRouter()

@router.get("/me", response_model=UserSchemasResponse, status_code=status.HTTP_200_OK, tags=["user"])
async def get_user(current_user: UserModel=Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserSchemasResponse, status_code=status.HTTP_202_ACCEPTED, tags=["user"])
async def update_me(user_in: UserSchemasUpdate,
                      db:AsyncSession= Depends(get_db),
                      current_user: UserModel=Depends(get_current_user)):
    return await update_user(current_user.email, user_in, db)

