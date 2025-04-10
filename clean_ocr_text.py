import os
import re

def clean_ocr_text(text: str) -> str:
    """
    清洗 OCR 文本：
    - 删除页码标记（--- Page N ---）
    - 删除其上方单独一行仅包含数字的段落（页脚页码）
    - 合并 OCR 断裂的行（非标点结尾接上）
    """
    lines = text.splitlines()
    cleaned = []

    for i in range(len(lines)):
        line = lines[i].strip()

        # 跳过页码标记
        if re.fullmatch(r"--- Page \d+ ---", line):
            # 同时删除前一行纯数字页脚
            if cleaned and re.fullmatch(r"\d{1,4}", cleaned[-1].strip()):
                cleaned.pop()
            continue

        cleaned.append(line)

    # 合并断裂句
    merged = ""
    for line in cleaned:
        if merged and not merged.endswith(("。", "？", "！", "：", "；", "…", "”", ".", "!", "?", ":")):
            merged += line
        else:
            merged += "\n" + line

    return merged.strip()


def clean_all_txt_files_in_folder():
    input_folder = "/your/folder/path"  # <<< ✅ 修改为你自己的路径
    print(f"📂 正在清洗文件夹：{input_folder}")

    if not os.path.exists(input_folder):
        print(f"❌ 路径不存在：{input_folder}")
        return

    txt_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]

    for fname in txt_files:
        in_path = os.path.join(input_folder, fname)
        out_path = os.path.join(input_folder, fname.replace(".txt", "_cleaned.txt"))

        with open(in_path, "r", encoding="utf-8") as f:
            raw = f.read()

        cleaned = clean_ocr_text(raw)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

        print(f"✅ 已处理: {fname} -> {os.path.basename(out_path)}")

# === ✅ 执行入口 ===
if __name__ == "__main__":
    clean_all_txt_files_in_folder()
