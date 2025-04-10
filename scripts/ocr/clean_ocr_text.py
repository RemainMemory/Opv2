import os
import re

def clean_ocr_text(text: str) -> str:
    lines = text.splitlines()
    cleaned = []

    for i in range(len(lines)):
        line = lines[i].strip()
        if re.fullmatch(r"--- Page \d+ ---", line):
            if cleaned and re.fullmatch(r"\d{1,4}", cleaned[-1].strip()):
                cleaned.pop()
            continue
        cleaned.append(line)

    merged = ""
    for line in cleaned:
        if merged and not merged.endswith(("。", "？", "！", "：", "；", "…", "”", ".", "!", "?", ":")):
            merged += line
        else:
            merged += "\n" + line

    return merged.strip()


def clean_all_txt_files_recursive():
    input_root = "data/raw_text"
    output_root = "data/cleaned_text"
    print(f"📂 递归清洗目录：{input_root}")

    for dirpath, _, filenames in os.walk(input_root):
        rel_path = os.path.relpath(dirpath, input_root)
        output_dir = os.path.join(output_root, rel_path)
        os.makedirs(output_dir, exist_ok=True)

        for fname in filenames:
            if not fname.endswith(".txt"):
                continue

            in_path = os.path.join(dirpath, fname)
            out_path = os.path.join(output_dir, fname.replace(".txt", "_cleaned.txt"))

            with open(in_path, "r", encoding="utf-8") as f:
                raw = f.read()

            cleaned = clean_ocr_text(raw)

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(cleaned)

            print(f"✅ {in_path} → {out_path}")


# ✅ 主入口
if __name__ == "__main__":
    clean_all_txt_files_recursive()
