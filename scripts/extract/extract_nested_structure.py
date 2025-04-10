import os
import re
import json
import pandas as pd

def clean_title(title):
    """
    仅去掉标题中的 '_cleaned' 后缀，保留数字和英文部分。
    """
    title = re.sub(r"_cleaned$", "", title)  # 仅去除结尾的 '_cleaned' 后缀
    return title.strip()

def extract_structured_json_and_excel(input_root, output_dir):
    """
    提取嵌套结构（一级 > 二级 > 三级 > 正文），确保每一层的内容都嵌套在前一层，
    并生成 JSON 和 Excel 文件，每个章节一个文件。确保正文不重复。
    """
    os.makedirs(output_dir, exist_ok=True)

    # 遍历每个章节目录
    for chapter_dir, _, files in os.walk(input_root):
        if not files:
            continue

        chapter_name = os.path.basename(chapter_dir)
        chapter_data = {
            "一级标题": chapter_name,
            "二级内容": []
        }

        excel_data = []
        seen_body = set()  # 用来存储已经处理过的正文内容，防止重复

        # 遍历章节文件
        for file in sorted(files):
            if not file.endswith(".txt"):
                continue

            second_level = clean_title(file.replace(".txt", ""))
            filepath = os.path.join(chapter_dir, file)

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            second_level_data = {
                "二级标题": second_level,
                "三级内容": []
            }

            # === 提取三级标题块 ===
            third_blocks = re.split(r"\n(?=\d+\.\d+\.\d+\s*[^\d])", text)
            for block in third_blocks:
                block = block.strip()
                if not block:
                    continue

                # 提取三级标题
                third_match = re.match(r"^(\d+\.\d+\.\d+)\s*([^\n]*)", block)
                if not third_match:
                    continue

                third_num = third_match.group(1)
                third_title = third_match.group(2).strip()
                third_full_title = f"{third_num} {third_title}"
                third_body = block[len(third_match.group(0)):].strip()

                # 检查正文是否已出现过，避免重复
                if third_body not in seen_body:
                    seen_body.add(third_body)

                    # 在三级内容下添加正文
                    third_level_data = {
                        "三级标题": third_full_title,
                        "正文": third_body.strip(),
                    }

                    second_level_data["三级内容"].append(third_level_data)

                    # 为Excel文件准备数据
                    excel_data.append({
                        "一级标题": chapter_name,
                        "二级标题": second_level,
                        "三级标题": third_full_title,
                        "正文": third_body.strip(),
                    })

            chapter_data["二级内容"].append(second_level_data)

        # === 保存 JSON ===
        json_path = os.path.join(output_dir, f"{chapter_name}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([chapter_data], f, ensure_ascii=False, indent=2)

        # === 保存 Excel ===
        excel_path = os.path.join(output_dir, f"{chapter_name}.xlsx")
        df = pd.DataFrame(excel_data)
        df.to_excel(excel_path, index=False)

        print(f"✅ 已保存：{json_path} 和 {excel_path}")


# ✅ 示例调用
if __name__ == "__main__":
    input_root = "your/input/directory"  # 自定义输入路径
    output_dir = "your/output/directory"  # 自定义输出路径
    extract_structured_json_and_excel(input_root, output_dir)
