from datetime import datetime

import jwt
from fastapi import Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.config import settings
from app.core.database import get_db
from app.crud.project import get_project
from app.crud.todo import get_todo
from app.crud.user import get_user_by_email

from app.models.users import UserModel
from app.schemas.Token import  TokenData

oauth2_schema=OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_schema), db:AsyncSession= Depends(get_db)) ->UserModel:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload= jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        email: str = payload.get("sub")
        if email is None:
            raise  exception
    except:
        raise exception

    user_data = TokenData(email=email)
    user = await get_user_by_email(db, user_data.email)

    if user is None:
        raise exception

    return user



async def project_permission(
    project_id: int=Path(...,ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    project = await get_project(project_id, db)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project.users_creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return project

async def todo_permission(
    todo_id: int=Path(...,ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    todo = await get_todo(todo_id, db)
    project= await get_project(todo.project_id, db)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    if todo.project_id != project.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    if project.users_creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return todo

async def filters(
        status: str | None = None,
        priority: str | None = None,
        deadline: datetime | None = None,
        labels: str | None = None):
    return {
        "status":status,
        "priority":priority,
        "deadline":deadline,
        "labels":labels,
    }

async def sort(
        sort_by: str|None=None,
        is_ASC: bool = True):
    return {
        "sort_by":sort_by,
        "is_asc":is_ASC
    }