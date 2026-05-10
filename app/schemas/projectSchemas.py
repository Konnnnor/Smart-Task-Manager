from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict,Field

from app.schemas.todoSchemas import TodoSchemasResponse


class ProjectSchemas(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    users_creator_id: int
    model_config = ConfigDict(from_attributes=True)


class ProjectSchemasCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    model_config = ConfigDict(from_attributes=True)

class ProjectSchemasResponse(BaseModel):
    id:int
    name: str
    users_creator_id: int
    created_at: datetime
    todos: list[TodoSchemasResponse]


    model_config = ConfigDict(from_attributes=True)

class ProjectSchemasUpdate(BaseModel):
    name: Optional[str]=Field(min_length=1, max_length=50)
    users_creator_id:Optional[int]=None


    model_config = ConfigDict(from_attributes=True)
