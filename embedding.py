import os
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
import pandas as pd
from config import MODEL_NAME, MODEL_CACHE_DIR, MAX_LENGTH

# 检查是否有可用的GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载BERT模型和Tokenizer
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME, cache_dir=MODEL_CACHE_DIR)
model = BertModel.from_pretrained(MODEL_NAME, cache_dir=MODEL_CACHE_DIR).to(device)

# 缓存已处理过的标题和它们的embedding
embedding_cache = {}

def embed_text(text, max_length=MAX_LENGTH):
    """
    对输入文本进行嵌入处理，并返回嵌入向量。
    :param text: 输入文本
    :param max_length: 最大长度，超过该长度时会进行截断或分块
    :return: 嵌入向量
    """
    # 确保输入是字符串
    if not isinstance(text, str):
        text = str(text)
    
    # 检查缓存中是否已存在该文本的embedding
    if text in embedding_cache:
        return embedding_cache[text]

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
    
    # 将数据移到GPU
    inputs = {key: value.to(device) for key, value in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # 获取[CLS]位置的输出作为文本的embedding
    embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()  # 移到CPU以便返回

    # 缓存该文本的embedding
    embedding_cache[text] = embedding

    return embedding

def split_text_with_overlap(text, max_length=MAX_LENGTH, overlap_ratio=0.25):
    """
    将文本分割为多个块，确保每个块最大为max_length，并且每两个块之间有overlap。
    :param text: 输入文本
    :param max_length: 每个块的最大长度
    :param overlap_ratio: 每两个块之间的重叠比例
    :return: 分割后的文本块列表
    """
    # 确保输入是字符串
    if not isinstance(text, str):
        text = str(text)
    
    # Tokenize the text
    tokens = tokenizer.tokenize(text)
    num_tokens = len(tokens)

    # 计算步长（每个块的起始位置偏移量）
    stride = int(max_length * (1 - overlap_ratio))
    
    # 切割文本
    chunks = []
    for start in range(0, num_tokens, stride):
        end = min(start + max_length, num_tokens)
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.convert_tokens_to_string(chunk_tokens)
        chunks.append(chunk_text)
        if end == num_tokens:
            break
    return chunks

def process_excel_file(file_path, max_length=MAX_LENGTH):
    """
    处理Excel文件中的文本，并返回嵌入后的结果。
    :param file_path: 文件路径
    :param max_length: 最大长度，默认为512
    :return: 嵌入结果
    """
    df = pd.read_excel(file_path)
    embeddings = []
    
    # 遍历文件中的每一行，并处理
    for index, row in df.iterrows():
        # 获取标题和正文
        titles = [row['一级标题'], row['二级标题'], row['三级标题']]
        content = row['正文']
        
        # 确保正文是字符串
        if not isinstance(content, str):
            content = str(content)
        
        # 分割正文并生成嵌入
        content_chunks = split_text_with_overlap(content, max_length)
        
        for chunk in content_chunks:
            # 对每一块正文生成embedding
            content_embedding = embed_text(chunk)[0]
            
            # 为每个部分生成嵌入
            embeddings.append({
                "一级标题": row['一级标题'],
                "二级标题": row['二级标题'],
                "三级标题": row['三级标题'],
                "正文": chunk,
                "一级标题embedding": embed_text(row['一级标题'])[0],  # 获取一级标题的嵌入
                "二级标题embedding": embed_text(row['二级标题'])[0],
                "三级标题embedding": embed_text(row['三级标题'])[0],
                "正文embedding": content_embedding,  # 正文的embedding
            })
    
    return embeddings

def save_embeddings_to_excel(embeddings, output_file):
    """
    保存嵌入结果到新的Excel文件
    :param embeddings: 嵌入数据
    :param output_file: 输出文件路径
    """
    # 将嵌入结果转换为DataFrame
    df = pd.DataFrame(embeddings)
    
    # 保存为Excel文件
    df.to_excel(output_file, index=False)
    print(f"✅ 嵌入结果已保存到 {output_file}")

def process_folder_for_embeddings(input_folder, output_folder, max_length=MAX_LENGTH):
    """
    处理文件夹下的所有Excel文件，生成包含嵌入的新的Excel文件
    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    :param max_length: 最大长度，默认为512
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # 遍历文件夹中的每个文件
    for file_name in os.listdir(input_folder):
        if not file_name.endswith(".xlsx"):
            continue
        
        file_path = os.path.join(input_folder, file_name)
        
        # 生成输出文件路径
        output_file_path = os.path.join(output_folder, f"embedded_{file_name}")
        
        print(f"正在处理文件: {file_path}")
        
        # 处理每个Excel文件并生成嵌入结果
        embeddings = process_excel_file(file_path, max_length)
        
        # 保存嵌入结果到Excel
        save_embeddings_to_excel(embeddings, output_file_path)


# 示例调用
if __name__ == "__main__":
    input_folder = "./output/chapters"  # 输入文件夹路径
    output_folder = "./output/test"  # 输出文件夹路径
    process_folder_for_embeddings(input_folder, output_folder)
