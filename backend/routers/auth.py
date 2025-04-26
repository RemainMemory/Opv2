from fastapi import APIRouter
from pydantic import BaseModel
from db_scripts.user_register import register_user
from db_scripts.user_login import validate_login

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: User):
    success = register_user(user.username, user.password)
    if success:
        return {"success": True, "message": "注册成功"}
    else:
        return {"success": False, "message": "用户名已存在"}

@router.post("/login")
def login(user: User):
    success = validate_login(user.username, user.password)
    if success:
        return {"success": True, "token": "mock-token"}
    else:
        return {"success": False, "message": "用户名或密码错误"}
