import uvicorn
from fastapi import FastAPI


from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.project import router as project_router
from app.routers.todo import router as todo_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(project_router, prefix="/project")
app.include_router(todo_router, prefix="/todo")


if __name__ =="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
