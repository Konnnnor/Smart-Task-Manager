from datetime import datetime

from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash

from app.models.users import UserModel
from app.schemas.userSchemas import UserSchemas, UserSchemasUpdate


async def get_user_by_email(db, email):
    user= await db.execute(select(UserModel).where(UserModel.email == email))
    return user.scalars().first()

async def create_user(user_in:UserSchemas, db:AsyncSession):
    hashed_password=  get_password_hash(user_in.password)

    user= UserModel(**user_in.model_dump(exclude={"password"}), password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user(user_email: str,
                      user_in:UserSchemasUpdate,
                      db:AsyncSession):

    user= await get_user_by_email(db,user_email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user_in.model_dump(exclude_unset=True)

    for key, value in user_data.items():
        if key == "password":
            setattr(user, key, get_password_hash(value))
        else:
            setattr(user, key, value)
    user.updated_at= datetime.utcnow()

    await db.commit()
    await db.refresh(user)
    return user

