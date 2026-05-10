from datetime import datetime


from sqlalchemy import Integer, String, DateTime, Null
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.core.database import Base



class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String , nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True,)

    projects: Mapped[list['ProjectModel']]=relationship("ProjectModel", back_populates="users", lazy="selectin")

    def __repr__(self) -> str:
        return f"<UserModel (id= {self.id}, username= {self.username})>"
