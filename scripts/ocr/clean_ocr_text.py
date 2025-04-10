import os
import re

def is_new_paragraph(line: str) -> bool:
    """
    判断一行是否是段落编号开头
    支持：1.、1.2.3、1.1.1.1、(1)、（1）、一、
    """
    line = line.strip()
    patterns = [
        r"^\d+(\.\d+)*[\s．、.]",           # 数字编号如 1.、1.2.3
        r"^[（(]\d{1,2}[）)]",              # 完整括号 (1)、（2）
        r"^[一二三四五六七八九十百]{1,3}[、.．\s]",  # 中文编号如 一、 二.
    ]
    return any(re.match(p, line) for p in patterns)

def clean_ocr_text(text: str) -> str:
    """
    清洗 OCR 文本：
    - 删除页码标记（--- Page N ---）
    - 删除前一行仅为数字的页脚
    - 按段落编号判断是否换段
    """
    lines = text.splitlines()
    cleaned = []

    for i in range(len(lines)):
        line = lines[i].strip()

        # 跳过页码标记
        if re.fullmatch(r"--- Page \d+ ---", line):
            if cleaned and re.fullmatch(r"\d{1,4}", cleaned[-1].strip()):
                cleaned.pop()
            continue

        cleaned.append(line)

    # 合并文本，遇段落编号开头换段
    merged = ""
    for line in cleaned:
        if is_new_paragraph(line):
            merged += "\n\n" + line
        else:
            merged += " " + line.strip()

    return merged.strip()

def clean_all_txt_files_recursive():
    """
    递归处理文件夹中的所有 `.txt` 文件，进行 OCR 文本清洗
    """
    input_root = "data/raw_text"  # 输入的原始文本文件夹
    output_root = "data/cleaned_text"  # 输出的清洗后文本文件夹
    print(f"📂 递归清洗目录：{input_root}")

    # 遍历目录和子目录中的所有文件
    for dirpath, _, filenames in os.walk(input_root):
        rel_path = os.path.relpath(dirpath, input_root)
        output_dir = os.path.join(output_root, rel_path)
        os.makedirs(output_dir, exist_ok=True)

        # 处理每个 .txt 文件
        for fname in filenames:
            if not fname.endswith(".txt"):
                continue

            in_path = os.path.join(dirpath, fname)
            out_path = os.path.join(output_dir, fname.replace(".txt", "_cleaned.txt"))

            with open(in_path, "r", encoding="utf-8") as f:
                raw = f.read()

            # 调用清洗函数
            cleaned = clean_ocr_text(raw)

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(cleaned)

            print(f"✅ {in_path} → {out_path}")


# === 主入口 ===
if __name__ == "__main__":
    clean_all_txt_files_recursive()
