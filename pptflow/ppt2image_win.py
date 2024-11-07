import win32com.client
import os
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


# 依赖安装：Microsoft PowerPoint
# How to export pptx to image (png, jpeg) in Python? https://stackoverflow.com/questions/61815883/how-to-export-pptx-to-image-png-jpeg-in-python

def ppt_to_image(input_ppt_path, output_image_dir_path, setting):
    try:
        # Create a PowerPoint application object
        Application = win32com.client.Dispatch("PowerPoint.Application")

        # Open the presentation without making it visible
        Presentation = Application.Presentations.Open(input_ppt_path, ReadOnly=True, WithWindow=False)
        file_name_without_ext = os.path.basename(input_ppt_path).split(".")[0]

        # Create a dir to save the slides as images
        if not os.path.exists(output_image_dir_path):
            os.makedirs(output_image_dir_path)

        # Export each slide as an image
        for idx, slide in enumerate(Presentation.Slides):
            # Checks whether the current slide falls within the specified start and end page ranges
            if setting.start_page_num and idx + 1 < setting.start_page_num:
                continue
            if setting.end_page_num and idx + 1 > setting.end_page_num:
                continue
            # Create a save path for the image file
            image_file_path = os.path.join(
                output_image_dir_path, f"{file_name_without_ext}-P{idx + 1}.png"
            )
            # Export the slide as an image
            slide.Export(image_file_path, "PNG", 1280, 720)

        # Close the presentation
        Presentation.Close()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Quit the PowerPoint application
        Application.Quit()
