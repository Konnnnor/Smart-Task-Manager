from dns.e164 import query
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.todos import TodoModel


from app.schemas.todoSchemas import  TodoSchemasUpdate, TodoSchemasCreate


async def create_todo(todo_in: TodoSchemasCreate, project_id:int, db: AsyncSession):
    todo = TodoModel(**todo_in.model_dump(), project_id=project_id)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def get_todo(todo_id: int, db: AsyncSession):
    todo = await db.execute(select(TodoModel).where(TodoModel.id == todo_id))
    return todo.scalars().one_or_none()

async def get_todos_with_filters(project_id: int, filters: dict, sort: dict, db: AsyncSession):
    query= select(TodoModel).where(TodoModel.project_id == project_id)
    FILTERS_MAP = {
        "status": TodoModel.status,
        "priority": TodoModel.priority,
        "deadline": TodoModel.deadline,
        "labels": TodoModel.labels,
    }

    SORT_MAP = {
        "deadline": TodoModel.deadline,
        "priority": TodoModel.priority,
    }
    for filter_key, filter_value in filters.items():
        if filter_value is not None and filter_key in FILTERS_MAP:
            query = query.where(FILTERS_MAP[filter_key] == filter_value)


    sort_by= sort.get("sort_by")
    is_asc= sort.get("is_asc",True)
    if sort_by in SORT_MAP:
        column=SORT_MAP[sort_by]
        if is_asc:
            query= query.order_by(column.asc())
        else:
            query= query.order_by(column.desc())

    result = await db.execute(query)
    return result.scalars().all()



async def get_todo_by_project_id(project_id: int, db: AsyncSession):
    todos = await db.execute(select(TodoModel).where(TodoModel.project_id == project_id))
    return todos.scalars().all()


async def update_todo(todo_in: TodoSchemasUpdate, todo_id: int, db: AsyncSession):
    result = await db.execute(select(TodoModel).where(TodoModel.id == todo_id))
    todo = result.scalars().one_or_none()
    todo_data = todo_in.model_dump(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(todo, key, value)

    await db.commit()
    await db.refresh(todo)
    return todo

async def delete_todo(todo_id: int, db: AsyncSession):
    result = await db.execute(select(TodoModel).where(TodoModel.id == todo_id))
    todo = result.scalars().first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task with whis id not found.")
    await db.delete(todo)
    await db.commit()
    return {"Task_id": todo_id, "Status": "deleted"}

async def delete_todos_by_project(project_id: int, db: AsyncSession):
    result = await db.execute(select(TodoModel).where(TodoModel.project_id == project_id))
    todo= result.scalars().all()
    if todo is None:
        return None
    for td in todo:
        await db.delete(td)
    await db.commit()
    return todo

