import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_scripts.db_connection import create_connection, close_connection

def register_user(username: str, password: str) -> bool:
    conn = create_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print("❌ 用户名已存在")
            return False

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        print("✅ 用户注册成功")
        return True
    except Exception as e:
        print(f"注册失败: {e}")
        return False
    finally:
        close_connection(conn)

# 示例调用
if __name__ == "__main__":
    register_user("admin", "admin123")
