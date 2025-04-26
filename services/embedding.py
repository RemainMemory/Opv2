import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from config import MODEL_NAME, MODEL_CACHE_DIR, MAX_LENGTH, logger

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载 tokenizer 和 BERT 模型
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME, cache_dir=MODEL_CACHE_DIR)
model = BertModel.from_pretrained(MODEL_NAME, cache_dir=MODEL_CACHE_DIR)
model.to(device)
model.eval()


def get_embedding_from_text(texts):
    """
    获取单个或多个文本的 embedding（支持列表）
    使用 mean pooling 聚合 token 表示
    :param texts: str 或 List[str]
    :return: 单个 numpy 向量 或 向量列表
    """
    if isinstance(texts, str):
        texts = [texts]

    try:
        inputs = tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=MAX_LENGTH,
        ).to(device)

        with torch.no_grad():
            outputs = model(**inputs)
            last_hidden = outputs.last_hidden_state  # (batch_size, seq_len, hidden_size)
            attention_mask = inputs["attention_mask"].unsqueeze(-1)  # (batch_size, seq_len, 1)

            # mean pooling
            masked_hidden = last_hidden * attention_mask
            sum_hidden = masked_hidden.sum(dim=1)
            lengths = attention_mask.sum(dim=1)
            embeddings = sum_hidden / lengths

        embeddings = embeddings.cpu().numpy()
        return embeddings[0] if len(texts) == 1 else embeddings.tolist()

    except Exception as e:
        logger.error(f"生成 embedding 时出错: {e}")
        return np.zeros((model.config.hidden_size,))
