from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.todos import TodoModel


from app.schemas.todoSchemas import TodoSchemas, TodoSchemasUpdate


async def create_todo(todo_in: TodoSchemas, db: AsyncSession):
    todo = TodoModel(**todo_in.model_dump())
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def get_todo(todo_id: int, db: AsyncSession):
    todo = await db.execute(select(TodoModel).where(TodoModel.id == todo_id))
    return todo.scalars().one_or_none()


async def get_todo_by_project_id(project_id: int, db: AsyncSession):
    todos = await db.execute(select(TodoModel).where(TodoModel.project_id == project_id))
    return todos.scalars().all()


async def update_todo(todo_in: TodoSchemasUpdate, todo_id: int, db: AsyncSession):
    todo = await db.execute(select(TodoModel).where(TodoModel.id == todo_id))

    todo_data = todo_in.model_dump(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(todo, key, value)

    await db.commit()
    await db.refresh(todo)
    return todo


async def delete_todo(todo_id: int, db: AsyncSession):
    todo = await db.execute(select(TodoModel).where(TodoModel.id == todo_id))
    await db.delete(todo)
    await db.commit()
    await db.refresh(todo)
    return todo

async def delete_todos_by_project(project_id: int, db: AsyncSession):
    todo = await db.execute(select(TodoModel).where(TodoModel.project_id == project_id))
    if todo is None:
        return todo
    await db.delete(todo)
    await db.commit()
    await db.refresh(todo)
    return todo

