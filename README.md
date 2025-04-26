# 🧠 操作系统智能问答系统

本项目基于 **FastAPI + Vue 3 + Vite + 本地 BERT + DeepSeek 大模型**，构建了一个支持关键词与向量混合检索（Hybrid RAG）的智能问答系统，适用于操作系统课程答疑、知识回顾与教学辅助。

---

## 📁 项目结构

```
Opv2/
├── backend/                   # 后端 FastAPI 服务
│   ├── main.py                # FastAPI 启动入口
│   ├── routers/               # API 路由模块
│   │   └── query_router.py    # 主问答逻辑路由
│   ├── services/              # 服务模块：关键词提取、嵌入生成、数据库检索
│   │   ├── embedding.py
│   │   ├── keyword_extractor.py
│   │   └── db_query.py
│   └── config.py              # 配置项和日志设置
│
├── db_scripts/
│   ├── db_connection.py       # 数据库连接管理
│   └── init_db.sql            # 创建表结构的 SQL 脚本
│
├── os-chat-frontend/          # 前端 Vue 3 + Vite 项目
│   ├── src/
│   │   ├── views/ChatView.vue
│   │   ├── components/Sidebar.vue
│   │   ├── components/ChatPanel.vue
│   │   └── api/index.js
│   └── vite.config.js
│
├── database/                  # 数据导入、embedding 脚本等
├── app.log                    # 运行日志
└── README.md
```

---

## 🚀 后端部署指南（FastAPI）

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动服务

```bash
uvicorn backend.main:app --reload
```

访问接口文档：

- ✅ 接口主页：http://127.0.0.1:8000
- ✅ 文档页面：http://127.0.0.1:8000/docs

---

## 🌐 前端部署指南（Vue 3 + Vite）

### 1. 安装依赖

```bash
cd os-chat-frontend
npm install
```

### 2. 启动前端开发服务器

```bash
npm run dev
```

浏览器访问：http://localhost:5173

---

## 🧮 数据库相关

### 创建 PostgreSQL 数据表

```sql
CREATE TABLE IF NOT EXISTS chapters (
    id SERIAL PRIMARY KEY,
    title_1 TEXT,
    title_2 TEXT,
    title_3 TEXT,
    content TEXT,
    title_1_embedding TEXT,
    title_2_embedding TEXT,
    title_3_embedding TEXT,
    content_embedding TEXT
);
```

### 数据库连接配置

数据库连接逻辑位于 `db_scripts/db_connection.py` 中，使用 `psycopg2` 进行连接。

### 查看数据示例（进入 psql）

```bash
sudo -u postgres psql
\c knowledge
SELECT * FROM chapters LIMIT 5;
```

---

## 🔑 API 示例说明

### 关键词提取 + 查询 + 回答一体化接口

```http
POST /api/query

Body:
{
  "query": "进程控制块和线程的关系是什么？"
}

返回：
{
  "answer": "（LLM生成的操作系统回答）"
}
```

---

## 💡 项目亮点

- ✅ 支持本地 BERT 向量生成，结合 DeepSeek 高质量回答
- ✅ 支持关键词 + 向量混合检索（Hybrid RAG）
- ✅ 支持 Markdown 渲染、深色模式、历史问答记录
- ✅ 模块解耦、日志管理、可扩展 API

---

## 📈 后续优化方向

- 支持用户注册 / 登录 / 收藏
- 加入上下文多轮对话
- 支持知识图谱融合增强问答（KG-RAG）
- 响应速度优化：引入异步/缓存机制、预加载嵌入

---

## 🧑‍💻 作者 & 致谢

作者：`@Ferry Chen`  
技术栈：`FastAPI` `Vue 3` `Transformers` `PostgreSQL`  
鸣谢：感谢 DeepSeek 开源模型提供强大支持！