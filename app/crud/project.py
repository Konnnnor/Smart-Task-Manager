from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud.todo import delete_todos_by_project
from app.models.projects import ProjectModel
from app.schemas.projectSchemas import ProjectSchemas, ProjectSchemasUpdate


async def create_project(project_in:ProjectSchemas, db:AsyncSession):
    project= ProjectModel(**project_in.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

async def get_project(project_id:int, db:AsyncSession):
    project= await db.execute(select(ProjectModel).where(ProjectModel.id == project_id))
    return project.scalars().one_or_none()

async def get_projects_by_userid(user_id:int, db:AsyncSession):
    project= await db.execute(select(ProjectModel).where(ProjectModel.users_creator_id == user_id))
    return project.scalars().all()

async def update_project(project_in:ProjectSchemasUpdate, project_id:int, db:AsyncSession):
    project= await db.execute(select(ProjectModel).where(ProjectModel.id == project_id))

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Project not found")

    project_data = project_in.model_dump(exclude_unset=True)
    for key, value in project_data.items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project_data)
    return project_data


async def delete_project(project_id:int, db:AsyncSession):
    project= await db.execute(select(ProjectModel).where(ProjectModel.id == project_id))
    await delete_todos_by_project(project_id,db)
    await db.delete(project)
    await db.commit()
    await db.refresh(project)
    return project

