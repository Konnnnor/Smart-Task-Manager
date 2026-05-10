from datetime import datetime


from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.core.database import Base
from app.models.projects import ProjectModel

from app.dependencies.Enums import Priority, Status


class TodoModel(Base):
    __tablename__ = "todos"

    id:Mapped[int]= mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id:Mapped[int]= mapped_column(Integer, ForeignKey("projects.id"))
    title:Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, nullable=False, default=Status.todo)
    priority: Mapped[str] = mapped_column(String, nullable=False, default=Priority.medium)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    labels:Mapped[str] = mapped_column(String, nullable=False, index=True)

    projects:Mapped["ProjectModel"]= relationship("ProjectModel", back_populates="todos")

    def __repr__(self):
        return f"<TodoModel = (id= {self.id}, project_id= {self.project_id}, title= {self.title})>"