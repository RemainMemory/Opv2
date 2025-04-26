import json
import numpy as np
from db_scripts.db_connection import create_connection, close_connection
from config import logger


def cosine_similarity(vec1, vec2):
    """
    计算两个向量的余弦相似度
    """
    try:
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    except Exception as e:
        logger.error(f"余弦相似度计算失败: {e}")
        return 0


def query_data_from_db_using_keywords_and_embeddings(keywords: set, embeddings: list, top_k=5):
    """
    混合关键词+embedding进行数据库检索（RAG方式）
    :param keywords: 提取的关键词集合
    :param embeddings: 每个关键词的embedding列表（与keywords一一对应）
    :param top_k: 返回最相关结果数
    :return: 排序后的top_k结果
    """
    conn = create_connection()
    if not conn:
        logger.error("数据库连接失败")
        return []

    try:
        cursor = conn.cursor()

        # 构建SQL查询，拼接关键词条件
        keyword_conditions = " OR ".join(["title_1 LIKE %s OR title_2 LIKE %s OR title_3 LIKE %s OR content LIKE %s" for _ in keywords])
        sql = f"""
        SELECT id, title_1, title_2, title_3, content,
               title_1_embedding, title_2_embedding, title_3_embedding, content_embedding
        FROM chapters
        WHERE {keyword_conditions}
        """

        # 构造参数（每个关键词四次like）
        params = []
        for word in keywords:
            params.extend([f"%{word}%"] * 4)

        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()

        if not rows:
            logger.warning("数据库未匹配到任何记录")
            return []

        similarities = []
        for row in rows:
            try:
                (
                    id, title_1, title_2, title_3, content,
                    title_1_emb, title_2_emb, title_3_emb, content_emb
                ) = row

                content_vec = np.array(json.loads(content_emb))

                # 计算每个关键词embedding与当前记录内容的相似度
                sim_list = [
                    cosine_similarity(np.array(embed), content_vec)
                    for embed in embeddings
                ]

                mean_similarity = np.mean(sim_list)
                similarities.append((id, title_1, title_2, title_3, content, mean_similarity))

            except Exception as e:
                logger.warning(f"处理记录失败: {e}")
                continue

        # 相似度排序
        similarities.sort(key=lambda x: x[5], reverse=True)
        return similarities[:top_k]

    except Exception as e:
        logger.error(f"查询失败: {e}")
        return []

    finally:
        close_connection(conn)
        logger.info("数据库连接已关闭")
