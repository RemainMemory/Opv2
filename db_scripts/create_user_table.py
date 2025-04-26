import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_scripts.db_connection import create_connection, close_connection


def create_users_table():
    conn = create_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        conn.commit()
        print("✅ 用户表创建成功（或已存在）")
    except Exception as e:
        print(f"创建用户表失败: {e}")
    finally:
        close_connection(conn)

if __name__ == "__main__":
    create_users_table()
