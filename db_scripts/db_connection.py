import psycopg2
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def create_connection():
    """创建 PostgreSQL 数据库连接"""
    try:
        # 创建连接
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("数据库连接成功！")
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None


def close_connection(conn):
    """关闭数据库连接"""
    if conn:
        conn.close()
        print("数据库连接已关闭。")
