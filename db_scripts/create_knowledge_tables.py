from db_connection import create_connection, close_connection

def create_tables():
    """创建表格"""
    # SQL 查询语句：创建表
    create_table_query = """
    CREATE TABLE IF NOT EXISTS chapters (
        id SERIAL PRIMARY KEY,
        title_1 TEXT,
        title_2 TEXT,
        title_3 TEXT,
        content TEXT,
        title_1_embedding vector(768),
        title_2_embedding vector(768),
        title_3_embedding vector(768),
        content_embedding vector(768),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # 创建数据库连接
    conn = create_connection()
    if conn is not None:
        try:
            # 创建游标对象
            cur = conn.cursor()
            # 执行创建表的 SQL 语句
            cur.execute(create_table_query)
            conn.commit()
            print("表格创建成功！")
            cur.close()
        except Exception as e:
            print(f"创建表失败: {e}")
        finally:
            # 关闭数据库连接
            close_connection(conn)

if __name__ == "__main__":
    create_tables()
