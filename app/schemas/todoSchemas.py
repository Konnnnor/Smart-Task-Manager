from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.dependencies.Enums import Priority, Status

class TodoSchemas(BaseModel):
    project_id: int
    title: str = Field(min_length=1, max_length=100)
    description: str
    status: Status = Field(default=Status.todo)
    priority: Priority = Field(default=Priority.medium)
    deadline: datetime
    labels: str = Field(min_length=1, max_length=50)
    model_config = ConfigDict(from_attributes=True)

class TodoSchemasCreate(BaseModel):

    title: str = Field(min_length=1, max_length=100)
    description: str
    status: Status = Field(default=Status.todo)
    priority: Priority = Field(default=Priority.medium)
    deadline: datetime
    labels: str = Field(min_length=1, max_length=50)
    model_config = ConfigDict(from_attributes=True)


class TodoSchemasResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    status: Status
    priority: Priority
    deadline: datetime
    labels: str

    model_config = ConfigDict(from_attributes=True)


class TodoSchemasUpdate(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=100, default=None)
    description: Optional[str] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    deadline: Optional[datetime] = None
    labels: Optional[str] = Field(min_length=1, max_length=50, default=None)

    model_config = ConfigDict(from_attributes=True)
