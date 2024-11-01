import os
import fitz  # pip install PyMuPDF

def pdf_to_image(pdf_path, output_image_dir_path, target_dpi=300):
    # 计算缩放因子, PDF 的默认分辨率是 72 DPI
    zoom = target_dpi / 72.0

    # 打开 PDF 文件
    pdf_document = fitz.open(pdf_path)

    file_name_without_ext = os.path.basename(pdf_path).split(".")[0]

    for page_number in range(len(pdf_document)):
        # 获取每一页
        page = pdf_document[page_number]

        # 创建缩放矩阵
        mat = fitz.Matrix(zoom, zoom)

        # 将页面转换为图像（pixmap），应用缩放矩阵
        pix = page.get_pixmap(matrix=mat)

        # 保存图像
        output_image_path = os.path.join(
            output_image_dir_path, f"{file_name_without_ext}-P{page_number + 1}.png"
        )
        pix.save(output_image_path)
        print(f"Saved: {output_image_path}")

    # 关闭 PDF 文档
    pdf_document.close()