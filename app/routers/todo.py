from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db

from app.dependencies.depends import  project_permission, create_one_todo, todo_permission, \
    update_one_todo, delete_one_todo


from app.schemas.projectSchemas import ProjectSchemasResponse
from app.schemas.todoSchemas import TodoSchemasResponse, TodoSchemasUpdate,  TodoSchemasCreate

router= APIRouter()




@router.post("/todo", response_model=TodoSchemasResponse,
                                status_code=status.HTTP_200_OK,
                                tags=["todos"])
async def create_todo(todo_in:TodoSchemasCreate,
                            project: ProjectSchemasResponse=Depends(project_permission),
                            db:AsyncSession=Depends(get_db)):
    return await create_one_todo(todo_in, project,db)

# @router.get("/todo/{todo_id}", response_model=TodoSchemasResponse,
#                                             status_code=status.HTTP_202_ACCEPTED,
#                                             tags=["todos"])
# async def get_one_todo(todo=Depends(todo_permission)):
#     return todo
#
#
@router.patch("/todo/{todo_id}", response_model=TodoSchemasResponse,
                                            status_code=status.HTTP_202_ACCEPTED,
                                            tags=["todos"])
async def update_todo(todo_in:TodoSchemasUpdate,
                             todo: TodoSchemasResponse=Depends(todo_permission),
                             db:AsyncSession=Depends(get_db)):
    return update_one_todo(todo_in,todo.id, db)

@router.delete("/todo/{todo_id}",
                                            status_code=status.HTTP_202_ACCEPTED,
                                            tags=["todos"])
async def delete_todo(todo=Depends(todo_permission),
                            db:AsyncSession=Depends(get_db)):
    return delete_one_todo(todo.id,db)

