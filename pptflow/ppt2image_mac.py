import os
import subprocess
from .pdf2image import pdf_to_image

def ppt_to_image(input_ppt_path, setting, progress_tracker=None):
    file_name_without_ext = os.path.basename(input_ppt_path).split(".")[0]
    temp_pdf_path = os.path.join(setting.image_dir_path, f'{file_name_without_ext}.pdf')
    ppt_to_pdf(input_ppt_path, temp_pdf_path)
    pdf_to_image(temp_pdf_path, setting.image_dir_path, setting.video_width, setting.video_height)

    # remove the temporary pdf file
    if os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)

# using AppleScript to call Microsoft PowerPoint to convert PPT to pdf
def ppt_to_pdf(ppt_path, pdf_path):
    # get current file path
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    # get the path of the AppleScript
    apple_script_path = os.path.join(current_dir, 'ppt2pdf.scpt')
    # run the AppleScript to convert PPT to PDF: osascript ppt2pdf.scpt {pptPath} {pdfPath}
    result = subprocess.run(['osascript', apple_script_path, ppt_path, pdf_path], 
        check=True)
    if result.returncode != 0:
        return False
    return True
