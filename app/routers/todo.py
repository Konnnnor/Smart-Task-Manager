from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db
from app.crud.todo import create_todo, update_todo, delete_todo, get_todos_with_filters
from app.dependencies.depends import project_permission, todo_permission, sort, filters
from app.schemas.projectSchemas import ProjectSchemasResponse
from app.schemas.todoSchemas import TodoSchemasResponse, TodoSchemasUpdate,  TodoSchemasCreate

router= APIRouter()


@router.get("/{project_id}/todos", response_model=list[TodoSchemasResponse], tags=["todos"])
async def get_my_todos(filter: dict = Depends(filters),
                       sorting: dict = Depends(sort),
                       project: ProjectSchemasResponse=Depends(project_permission),
                       db: AsyncSession = Depends(get_db)):
    return await get_todos_with_filters(project.id, filter, sorting, db)

@router.post("/{project_id}/todo", response_model=TodoSchemasResponse,
                                status_code=status.HTTP_200_OK,
                                tags=["todos"])
async def create_my_todo(todo_in:TodoSchemasCreate,
                            project: ProjectSchemasResponse=Depends(project_permission),
                            db:AsyncSession=Depends(get_db)):
    return await create_todo(todo_in, project.id,db)


@router.patch("/todo/{todo_id}", response_model=TodoSchemasResponse,
                                            status_code=status.HTTP_202_ACCEPTED,
                                            tags=["todos"])
async def update_my_todo(todo_in:TodoSchemasUpdate,
                             todo: TodoSchemasResponse=Depends(todo_permission),
                             db:AsyncSession=Depends(get_db)):
    return await update_todo(todo_in,todo.id, db)

@router.delete("/todo/{todo_id}",
                                            status_code=status.HTTP_202_ACCEPTED,
                                            tags=["todos"])
async def delete_my_todo(todo=Depends(todo_permission),
                            db:AsyncSession=Depends(get_db)):
    return await delete_todo(todo.id,db)

