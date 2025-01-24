import os
import subprocess
from .pdf2image import pdf_to_image

def ppt_to_image(input_ppt_path, setting, progress_tracker=None):
    file_name_without_ext = os.path.basename(input_ppt_path).split(".")[0]
    temp_pdf_path = os.path.join(setting.image_dir_path, f'{file_name_without_ext}.pdf')
    ppt_to_pdf(input_ppt_path, setting.image_dir_path)
    pdf_to_image(temp_pdf_path, setting.image_dir_path, setting.video_width, setting.video_height)

    # remove the temporary pdf file
    if os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)

# convert ppt to pdf using LibreOffice 
def ppt_to_pdf(ppt_path, pdf_dir):
    # convert ppt to pdf with LibreOffice command：soffice --headless --invisible --convert-to pdf --outdir {output_image_dir_path} {input_ppt_path}
    soffice_command = '/usr/bin/soffice'
    result = subprocess.run([soffice_command, '--headless','--invisible',"--convert-to", "pdf", '--outdir', f'{pdf_dir}', f'{ppt_path}'], 
        check=True)
    if result.returncode != 0:
        raise SystemError(f"Failed to convert ppt to pdf: {ppt_path}, returncode: {result.returncode}")
    return True
