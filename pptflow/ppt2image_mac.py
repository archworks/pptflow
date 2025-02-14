import os
import subprocess
from .ppt2image import PptToImage
from .pdf2image import pdf_to_image
from .config.setting import Setting
class PptToImageMac(PptToImage):
    def convert(self, input_ppt_path: str, setting: Setting, progress_tracker=None):
        # Create a dir to save the slides as images
        if not os.path.exists(setting.image_dir_path):
            os.makedirs(setting.image_dir_path)
        file_name_without_ext = os.path.basename(input_ppt_path).split(".")[0]
        temp_pdf_path = os.path.join(setting.image_dir_path, f'{file_name_without_ext}.pdf')
        self._ppt_to_pdf(input_ppt_path, temp_pdf_path)
        pdf_to_image(temp_pdf_path, setting.image_dir_path, setting.video_width, setting.video_height, \
                    setting.start_page_num, setting.end_page_num)

        # remove the temporary pdf file
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

    # using AppleScript to call Microsoft PowerPoint to convert PPT to pdf
    def _ppt_to_pdf(self, ppt_path, pdf_path):
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
