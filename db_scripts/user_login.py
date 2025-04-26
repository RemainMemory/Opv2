import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_scripts.db_connection import create_connection, close_connection

def validate_login(username: str, password: str) -> bool:
    conn = create_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = %s",
            (username,)
        )
        row = cursor.fetchone()
        if row and row[0] == password:
            print("✅ 登录成功")
            return True
        else:
            print("❌ 用户名或密码错误")
            return False
    except Exception as e:
        print(f"登录验证失败: {e}")
        return False
    finally:
        close_connection(conn)

# 示例调用
if __name__ == "__main__":
    validate_login("admin", "admin123")
