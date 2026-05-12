from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.core.database import Base



class ProjectModel(Base):
    __tablename__ = "projects"

    id:Mapped[int] = mapped_column(Integer,index=True, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String, index=True, nullable=False)
    users_creator_id:Mapped[str] = mapped_column(ForeignKey('users.id'), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    users:Mapped["UserModel"] = relationship("UserModel", back_populates="projects", )
    todos:Mapped[list["TodoModel"]]= relationship("TodoModel", back_populates="projects", lazy="selectin")


    def __repr__(self) -> str:
        return f"<ProjectModel (id= {self.id}, name= {self.name}, users_creator_id= {self.users_creator_id})>"