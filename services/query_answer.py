# services/query_answer.py
from config import DEEPSEEK_MODEL_NAME, logger, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL
from openai import OpenAI
from services.keyword_extractor import extract_keywords_from_deepseek
from services.embedding import get_embedding_from_text
from services.db_query import hybrid_query_from_db

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

def query_answer_for_question(query_text: str, top_k: int = 5):
    keywords_set = extract_keywords_from_deepseek(query_text)
    if not keywords_set:
        logger.warning("未能提取关键词")
        return "未能从问题中提取关键词，无法查询。"

    all_results = []
    for keyword in keywords_set:
        query_embedding = get_embedding_from_text(keyword)
        top_k_results = hybrid_query_from_db(keyword, query_embedding, top_k=top_k)
        if top_k_results:
            all_results.append((keyword, top_k_results))

    if not all_results:
        return "未能在数据库中找到与问题相关的内容。"

    final_prompt = ""
    for keyword, results in all_results:
        final_prompt += f"\n与关键词 '{keyword}' 相关的内容：\n"
        for result in results:
            final_prompt += f"标题1: {result[1]}, 标题2: {result[2]}, 标题3: {result[3]}, 内容: {result[4]}\n"

    final_prompt += f"\n问题: {query_text}\n请根据上述内容回答，若内容不全请补充。"

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个帮助用户的助手"},
                {"role": "user", "content": final_prompt},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"生成答案失败: {e}")
        return "生成答案时出错。"

        