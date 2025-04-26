import ast
import numpy as np
import pandas as pd
import json
import os
from db_connection import create_connection, close_connection

# 连接数据库并返回连接对象
def create_db_connection():
    conn = create_connection()
    return conn

# 将嵌入向量从字符串转换为 numpy 数组
def parse_embedding(embedding_str):
    try:
        # 使用 ast.literal_eval 安全地将字符串转换为列表
        return np.array(ast.literal_eval(embedding_str), dtype=float)
    except Exception as e:
        raise ValueError(f"Error parsing embedding: {e}")

# 批量插入数据到数据库
def insert_data_to_db(conn, data):
    cursor = conn.cursor()
    try:
        for row in data:
            # 将 numpy 数组转换为列表
            embedding1_list = row['一级标题embedding'].tolist()
            embedding2_list = row['二级标题embedding'].tolist()
            embedding3_list = row['三级标题embedding'].tolist()
            content_embedding_list = row['正文embedding'].tolist()

            # 将列表转换为 JSON 格式字符串，符合 vector 类型要求
            embedding1_json = json.dumps(embedding1_list)
            embedding2_json = json.dumps(embedding2_list)
            embedding3_json = json.dumps(embedding3_list)
            content_embedding_json = json.dumps(content_embedding_list)

            # 执行插入操作
            query = """
            INSERT INTO chapters (title_1, title_2, title_3, content, 
                title_1_embedding, title_2_embedding, title_3_embedding, content_embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (row['一级标题'], row['二级标题'], row['三级标题'], row['正文'],
                                   embedding1_json, embedding2_json, embedding3_json, content_embedding_json))
        conn.commit()  # 提交所有插入操作
        print("数据已成功插入。")
    except Exception as e:
        print(f"插入数据时发生错误: {e}")
        conn.rollback()  # 如果发生错误，回滚事务
    finally:
        cursor.close()

# 解析并处理 Excel 文件数据
def parse_excel_file(file_path):
    df = pd.read_excel(file_path)

    data = []
    for _, row in df.iterrows():
        # 解析嵌入向量
        try:
            embedding1 = parse_embedding(row['一级标题embedding'])
            embedding2 = parse_embedding(row['二级标题embedding'])
            embedding3 = parse_embedding(row['三级标题embedding'])
            content_embedding = parse_embedding(row['正文embedding'])

            data.append({
                '一级标题': row['一级标题'],
                '二级标题': row['二级标题'],
                '三级标题': row['三级标题'],
                '正文': row['正文'],
                '一级标题embedding': embedding1,
                '二级标题embedding': embedding2,
                '三级标题embedding': embedding3,
                '正文embedding': content_embedding
            })
        except Exception as e:
            print(f"处理文件 {file_path} 时，第 {row.name + 1} 行出错: {e}")

    return data

# 处理文件夹下所有的 Excel 文件
def process_excel_files_in_folder(folder_path):
    conn = create_db_connection()  # 仅在此处创建一次连接
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith('.xlsx'):
                file_path = os.path.join(folder_path, filename)
                print(f"正在处理文件: {file_path}")

                # 解析并插入数据
                data = parse_excel_file(file_path)
                insert_data_to_db(conn, data)

    except Exception as e:
        print(f"处理文件夹时发生错误: {e}")
    finally:
        close_connection(conn)  # 最后关闭连接

# 主程序入口
if __name__ == "__main__":
    folder_path = './output/test'  # 示例文件夹路径
    process_excel_files_in_folder(folder_path)
