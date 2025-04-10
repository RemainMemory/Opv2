import os
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
from tqdm import tqdm
import paddle
from chapters import chapters  # 导入章节数据

def ocr_processing(pdf_path, chapters, output_root, dpi=300):
    """
    对指定章节的 PDF 内容进行 OCR 识别并保存到指定文件夹

    :param pdf_path: PDF 文件路径
    :param chapters: 章节数据（列表）
    :param output_root: 输出根目录
    :param dpi: PDF 转图片的分辨率，默认 300
    """
    # 自动判断是否使用 GPU
    use_gpu = paddle.is_compiled_with_cuda()
    print(f"🚀 正在使用 {'GPU' if use_gpu else 'CPU'} 模式运行 PaddleOCR")

    # 初始化 PaddleOCR 模型
    ocr_model = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=use_gpu)

    # 创建输出根目录
    os.makedirs(output_root, exist_ok=True)

    # 遍历章节并进行 OCR 处理
    for chapter in tqdm(chapters, desc="📘 正在处理所有章节"):
        chapter_title = chapter['title']
        chapter_dir = os.path.join(output_root, chapter_title)
        os.makedirs(chapter_dir, exist_ok=True)

        for section in chapter['sections']:
            section_title = section['title']
            start_page = section['start']
            end_page = section['end']
            output_path = os.path.join(chapter_dir, f"{section_title}.txt")

            print(f"\n📖 开始处理：{chapter_title} / {section_title}（第 {start_page}~{end_page} 页）")
            pages = convert_from_path(pdf_path, dpi=dpi, first_page=start_page, last_page=end_page)

            # 逐页处理 OCR
            for i, img in enumerate(pages):
                page_num = start_page + i
                img_path = f"temp_page_{page_num}.png"
                img.save(img_path)

                print(f"🔍 OCR 第 {page_num} 页...", end=" ")
                result = ocr_model.ocr(img_path, cls=True)
                os.remove(img_path)

                page_text = "\n".join([line[1][0] for line in result[0]])
                print("✓")

                # ✅ 确保输出文件夹存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # 追加写入结果到文件
                with open(output_path, "a", encoding="utf-8") as f:
                    f.write(f"\n\n--- Page {page_num} ---\n{page_text}")

            print(f"✅ 完成节内容保存：{output_path}")

    print("\n🎉 全部章节识别完成！结果保存在", output_root)


# === 示例：调用 OCR 处理函数 ===
if __name__ == "__main__":
    pdf_path = "data/pdfs/计算机操作系统.pdf"  # 你的 PDF 文件路径
    output_root = "data/raw_text"  # 输出目录
    
    # 调用 OCR 处理函数
    ocr_processing(pdf_path, chapters, output_root)
