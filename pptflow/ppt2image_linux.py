import os
import subprocess
from .pdf2image import pdf_to_image

def ppt_to_image(input_ppt_path, output_image_dir_path,
    start_page_num=None, end_page_num=None):
    # Create a dir to save the slides as images
    if not os.path.exists(output_image_dir_path):
        os.makedirs(output_image_dir_path)
    pass


# 参考https://jdhao.github.io/2020/03/30/pptx_to_image/
def ppt_to_pdf(ppt_path, pdf_path):
    # 安装 LibreOffice
    # 使用命令行转换 PPT 为pdf：soffice --headless --invisible --convert-to pdf --outdir {output_image_dir_path} {input_ppt_path}
    soffice_command = '/usr/bin/soffice'
    result = subprocess.run([soffice_command, '--headless','--invisible',"--convert-to", "pdf", '--outdir', f'{output_image_dir_path}'], 
        check=True)
    pass

if __name__ == "__main__":
    # 使用示例
    current_dir = os.getcwd()
    test_path = os.path.join(current_dir, "test")
    pdf_path = os.path.join(test_path, "test.pdf")
    temp_dir = os.path.join(current_dir, "temp")
    image_dir_path = os.path.join(temp_dir, "image")
    pdf_to_images(pdf_path, image_dir_path, target_dpi=300)  # 设置目标 DPI
