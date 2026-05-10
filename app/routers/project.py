from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db
from app.crud.project import get_projects_by_userid
from app.dependencies.depends import get_current_user, project_permission, update_one_project, \
    delete_one_project, create_one_project
from app.models.users import UserModel
from app.schemas.projectSchemas import ProjectSchemasResponse, ProjectSchemasUpdate, ProjectSchemas, \
    ProjectSchemasCreate

router= APIRouter()

@router.get("/projects", response_model=list[ProjectSchemasResponse],
                                status_code=status.HTTP_200_OK,
                                tags=["projects"])
async def get_projects(db:AsyncSession=Depends(get_db), current_user: UserModel=Depends(get_current_user)):
    return await get_projects_by_userid(current_user.id,db)


@router.post("/project", response_model=ProjectSchemasResponse,
                                status_code=status.HTTP_200_OK,
                                tags=["projects"])
async def create_project(project_in:ProjectSchemasCreate,
                            current_user: UserModel=Depends(get_current_user),
                            db:AsyncSession=Depends(get_db)):
    return await create_one_project(project_in, current_user, db)

@router.get("/project/{project_id}", response_model=ProjectSchemasResponse,
                                            status_code=status.HTTP_202_ACCEPTED,
                                            tags=["projects"])
async def get_one_project(project=Depends(project_permission)):
    return project


@router.patch("/project/{project_id}", response_model=ProjectSchemasResponse,
                                            status_code=status.HTTP_202_ACCEPTED,
                                            tags=["projects"])
async def update_project(project_in:ProjectSchemasUpdate,
                             project=Depends(project_permission),
                             db:AsyncSession=Depends(get_db)):
    return update_one_project(project_in,project.id, db)

@router.delete("/project/{project_id}",
                                            status_code=status.HTTP_202_ACCEPTED,
                                            tags=["projects"])
async def delete_project(project=Depends(project_permission),
                             db:AsyncSession=Depends(get_db)):
    return delete_one_project(project,db)

