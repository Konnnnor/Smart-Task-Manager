from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic import EmailStr

from app.schemas.projectSchemas import  ProjectSchemasResponse


class UserSchemas(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: str
    password: str = Field(min_length=8, max_length=25)

    model_config = ConfigDict(from_attributes=True)

class UserSchemasResponse(BaseModel):
    id:int
    username: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    projects: list[ProjectSchemasResponse]

    model_config = ConfigDict(from_attributes=True)

class UserSchemasUpdate(BaseModel):
    username: Optional[str]=Field(min_length=1, max_length=50, default=None)
    password: Optional[str]=Field(min_length=8, max_length=25, default=None)

    model_config = ConfigDict(from_attributes=True)
