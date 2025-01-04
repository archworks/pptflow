import win32com.client
import os
from pptflow.utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


# 依赖安装：Microsoft PowerPoint
# How to export pptx to image (png, jpeg) in Python? https://stackoverflow.com/questions/61815883/how-to-export-pptx-to-image-png-jpeg-in-python

def ppt_to_image(input_ppt_path, setting, progress_tracker=None):
    Application = None
    try:
        # Create a PowerPoint application object
        Application = win32com.client.Dispatch("PowerPoint.Application")

        # Open the presentation without making it visible
        Presentation = Application.Presentations.Open(input_ppt_path, ReadOnly=True, WithWindow=False)
        file_name_without_ext = os.path.basename(input_ppt_path).split(".")[0]

        # Create a dir to save the slides as images
        if not os.path.exists(setting.image_dir_path):
            os.makedirs(setting.image_dir_path)

        total_slides = len(Presentation.Slides)
        # Export each slide as an image
        for idx, slide in enumerate(Presentation.Slides):
            # Checks whether the current slide falls within the specified start and end page ranges
            if setting.start_page_num and idx + 1 < setting.start_page_num:
                continue
            if setting.end_page_num and idx + 1 > setting.end_page_num:
                continue
            # Create a save path for the image file
            image_file_path = os.path.join(
                setting.image_dir_path, f"{file_name_without_ext}-P{idx + 1}.png"
            )
            # Export the slide as an image
            slide.Export(image_file_path, "PNG", 1280, 720)

            # Update progress
            if progress_tracker:
                progress = (idx + 1) / total_slides
                progress_tracker.update_step(progress)

        # Close the presentation
        Presentation.Close()
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        logger.error("Please run the program in non-admin mode or check COM registration.")
    finally:
        # Quit the PowerPoint application
        if Application:
            Application.Quit()
