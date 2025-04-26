from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL_NAME, logger
import ast

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

def extract_keywords_from_deepseek(query_text: str) -> set:
    prompt = f"""
    请从以下问题中提取操作系统相关的关键词，并将其以集合格式返回，例如：{{'进程控制块', '进程', '线程'}}。
    请确保关键词为实际概念，而不是句子或短语，例如：
    "操作系统的概念是什么？" 应仅提取 {{'操作系统'}}。

    示例：
    - "进程控制块是什么？" -> {{'进程控制块'}}
    - "什么是虚拟内存？" -> {{'虚拟内存'}}
    - "操作系统中的线程管理" -> {{'线程管理'}}

    当前问题："{query_text}"
    """

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个帮助用户的助手"},
                {"role": "user", "content": prompt},
            ]
        )
        result = response.choices[0].message.content.strip()
        logger.info(f"[关键词提取] {query_text} => {result}")
        return ast.literal_eval(result)
    except Exception as e:
        logger.error(f"关键词提取失败: {e}")
        return set()
