import os
import subprocess
from .pdf2image import pdf_to_image

def ppt_to_image(input_ppt_path, output_image_dir_path,
    start_page_num=None, end_page_num=None):
    file_name_without_ext = os.path.basename(input_ppt_path).split(".")[0]
    temp_pdf_path = os.path.join(output_image_dir_path, f'{file_name_without_ext}.pdf')
    ppt_to_pdf(input_ppt_path, temp_pdf_path)
    pdf_to_image(temp_pdf_path, output_image_dir_path)
    if os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)

def ppt_to_pdf(ppt_path, pdf_path):
    # 安装 LibreOffice
    # 使用脚本调用Microsoft PowerPoint转换 PPT 为pdf：osascript ppt2pdf.scpt {pptPath} {pdfPath}
    # 获取当前脚本文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 获取当前脚本文件所在的目录
    current_dir = os.path.dirname(current_file_path)
    apple_script_path = os.path.join(current_dir, 'ppt2pdf.scpt')
    result = subprocess.run(['osascript', apple_script_path, ppt_path, pdf_path], 
        check=True)
    if result.returncode != 0:
        return False
    return True


if __name__ == "__main__":
    # 使用示例
    current_dir = os.getcwd()
    test_path = os.path.join(current_dir, "test")
    ppt_path = os.path.join(test_path, "test.pptx")
    temp_dir = os.path.join(current_dir, "temp")
    image_dir_path = os.path.join(temp_dir, "image")
    ppt_to_image(ppt_path, image_dir_path)  # 设置目标 DPI
