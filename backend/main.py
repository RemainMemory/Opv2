from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import query_router
from backend.routers import auth
import os

app = FastAPI(title="操作系统问答系统 API")

# 允许跨域，供前端调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 注册原有问答接口
app.include_router(query_router.router, prefix="/api", tags=["问答接口"])

# ✅ 注册新增的用户认证接口（登录/注册）
app.include_router(auth.router, prefix="/api", tags=["用户接口"])

@app.get("/")
def root():
    return {"message": "欢迎使用操作系统问答系统！访问 /docs 查看 API 文档。"}
