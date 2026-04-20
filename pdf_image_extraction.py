import fitz  # PyMuPDF
import os
import time
import argparse

def extract_images_from_pdf(pdf_path, output_dir):
    """
    从 PDF 文件中提取所有图片。
    针对大文件和大量图片进行了优化。
    """
    # 如果输出目录不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 打开 PDF 文件
    try:
        pdf_document = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return

    total_pages = len(pdf_document)
    print(f"Opened PDF with {total_pages} pages.")

    image_count = 0
    start_time = time.time()

    # 通过 xref 跟踪已提取的图片，避免重复提取
    extracted_xrefs = set()

    for page_index in range(total_pages):
        # 使用 yield 或分步加载以节省内存
        page = pdf_document.load_page(page_index)
        image_list = page.get_images(full=True)

        if image_list:
            for img_index, img in enumerate(image_list, start=1):
                xref = img[0]
                
                if xref in extracted_xrefs:
                    continue
                
                extracted_xrefs.add(xref)
                
                try:
                    # 提取图片
                    # 直接获取图像数据通常比 Pixmap 更快且更节省内存（对于原始格式）
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # 生成文件名
                    image_filename = f"img_{image_count+1:05d}_xref{xref}.{image_ext}"
                    image_path = os.path.join(output_dir, image_filename)
                    
                    # 保存图片
                    with open(image_path, "wb") as f:
                        f.write(image_bytes)
                    
                    image_count += 1
                    
                    # 定期打印进度
                    if image_count % 1000 == 0:
                        elapsed = time.time() - start_time
                        print(f"已提取 {image_count} 张唯一图片... (耗时 {elapsed:.2f} 秒)")
                    
                except Exception as e:
                    print(f"Error extracting image at page {page_index+1}, xref {xref}: {e}")

        # 每页处理完后释放页面内存
        page = None

    pdf_document.close()
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n提取完成!")
    print(f"总共提取了 {image_count} 张唯一图片。")
    print(f"总耗时: {duration:.2f} 秒")
    if duration > 0:
        print(f"平均速度: {image_count / duration:.2f} 张/秒")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从 PDF 文件中高效提取图片")
    parser.add_argument("-i", "--input", help="输入的 PDF 文件路径", default="梧桐币1000.pdf")
    parser.add_argument("-o", "--output", help="输出图片的目录", default="extracted_images")
    
    args = parser.parse_args()
    
    pdf_file = args.input
    output_folder = args.output
    
    if os.path.exists(pdf_file):
        extract_images_from_pdf(pdf_file, output_folder)
    else:
        # 搜索当前目录下所有 PDF
        pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
        if pdf_files:
            print(f"未找到指定文件 '{pdf_file}'，将尝试提取: {pdf_files[0]}")
            extract_images_from_pdf(pdf_files[0], output_folder)
        else:
            print(f"错误: 找不到 PDF 文件 '{pdf_file}'，且当前目录下没有其他 PDF 文件。")
