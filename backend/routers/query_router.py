import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.keyword_extractor import extract_keywords_from_deepseek
from services.embedding import get_embedding_from_text
from services.db_query import query_data_from_db_using_keywords_and_embeddings
from config import logger, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL_NAME
from openai import OpenAI

router = APIRouter()

# 创建 OpenAI 客户端
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

class QueryRequest(BaseModel):
    query: str


@router.post("/get_answer")
def get_answer(request: QueryRequest):
    query_text = request.query

    # ① 提取关键词
    keywords_set = extract_keywords_from_deepseek(query_text)
    if not keywords_set:
        raise HTTPException(status_code=400, detail="关键词提取失败")

    logger.info(f"提取关键词: {keywords_set}")

    # ② 批量生成 embedding
    embeddings = get_embedding_from_text(list(keywords_set))
    if isinstance(embeddings, np.ndarray):  # 如果只有一个关键词
        embeddings = [embeddings]

    # ③ 多关键词查询并聚合
    all_results = []
    for keyword, embedding in zip(keywords_set, embeddings):
        results = query_data_from_db_using_keywords_and_embeddings(keyword, embedding)
        if results:
            all_results.append((keyword, results))

    if not all_results:
        return {"answer": "未找到相关内容"}

    # ④ 构建 prompt
    prompt = "你是一个操作系统知识问答助手，请根据以下与关键词相关的内容回答用户问题。\n"
    for keyword, entries in all_results:
        prompt += f"\n【关键词】：{keyword}\n【相关内容】:\n"
        for result in entries:
            prompt += f"- 一级标题: {result[1]}；二级标题: {result[2]}；三级标题: {result[3]}\n  内容摘要: {result[4]}\n"
    prompt += f"\n【用户问题】：{query_text}\n请结合上面内容，条理清晰地回答。若无直接答案，请合理补充。"

    # ⑤ 请求模型
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个专业的操作系统问答助手。"},
                {"role": "user", "content": prompt},
            ],
        )
        answer = response.choices[0].message.content
        logger.info("模型回答成功")
        return {"answer": answer}
    except Exception as e:
        logger.error(f"模型调用失败: {e}")
        raise HTTPException(status_code=500, detail="模型调用失败")
