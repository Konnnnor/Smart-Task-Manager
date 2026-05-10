import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.config import settings
from app.core.database import get_db
from app.crud.project import get_project, update_project, delete_project, create_project
from app.crud.todo import create_todo, get_todo, update_todo, delete_todo
from app.crud.user import get_user_by_email

from app.models.users import UserModel

from app.schemas.Token import  TokenData
from app.schemas.projectSchemas import ProjectSchemasUpdate, ProjectSchemas, ProjectSchemasResponse
from app.schemas.todoSchemas import TodoSchemas, TodoSchemasCreate, TodoSchemasUpdate

oauth2_schema=OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_schema), db:AsyncSession= Depends(get_db)) ->UserModel:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload= jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHMS)
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
    project_id: int,
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
    todo_id: int,
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

    if todo.project_id != project.id and project.users_creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return todo



async def create_one_project(project_in: ProjectSchemas,
                             current_user: UserModel = Depends(get_current_user),
                             db: AsyncSession = Depends(get_db)):

    return await create_project(
        ProjectSchemas(
            **project_in.model_dump(),
            users_creator_id=current_user.id),
        db
    )

async def update_one_project(
                            project_in: ProjectSchemasUpdate,
                            project_id: int,
                            db: AsyncSession = Depends(get_db)):
    project = await update_project(project_in, project_id, db)
    return project

async def delete_one_project(project_in, db: AsyncSession = Depends(get_db)):
    return await delete_project(project_in.id,db)

async def create_one_todo(todo_in:TodoSchemasCreate,
                          project_in: ProjectSchemasResponse,
                          db: AsyncSession = Depends(get_db)):

    return await create_todo(
        TodoSchemas(
            **todo_in.model_dump(),
            project_id=project_in.id),
        db)

async def update_one_todo(todo_in: TodoSchemasUpdate,
                          todo_id: int,
                          db: AsyncSession = Depends(get_db)):
    todo = await update_todo(todo_in, todo_id, db)
    return todo

async def delete_one_todo(todo_id: int,
                          db: AsyncSession = Depends(get_db)):
    todo = await delete_todo(todo_id, db)
    return todo
