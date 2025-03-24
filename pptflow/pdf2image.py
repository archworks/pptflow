import os
import pymupdf
from pptflow.config.setting import Setting
from pptflow.utils.mylogger import get_logger
logger = get_logger(__name__)


def pdf_to_image(pdf_path, setting):
    # open the PDF file
    pdf_document = pymupdf.open(pdf_path)

    # get the file name without extension
    file_name_without_ext = os.path.basename(pdf_path).split(".")[0]

    for page_number in range(len(pdf_document)):
        if setting.start_page_num and page_number + 1 < setting.start_page_num:
            continue
        if setting.end_page_num and page_number + 1 > setting.end_page_num:
            continue
        # get the page
        page = pdf_document[page_number]

        # set the zoom factor
        zoom_x = int(setting.video_width) / page.rect.width
        zoom_y = int(setting.video_height) / page.rect.height

        # create a matrix for the zoom factor
        mat = pymupdf.Matrix(zoom_x, zoom_y)

        # get a PixMap of the page
        pix = page.get_pixmap(matrix=mat)

        # save the PixMap as a PNG image
        output_image_path = os.path.join(
            setting.image_dir_path, f"{file_name_without_ext}-P{page_number + 1}.png"
        )
        pix.save(output_image_path)
        logger.info(f"Saved: {output_image_path}")

    # close the PDF file
    pdf_document.close()


if __name__ == '__main__':
    setting = Setting()
    pdf_to_image(
        pdf_path="D:/workspace/ppt/黑灰白色极简风年度汇报述职通用ppt演示文稿.pdf",
        setting=setting
    )
