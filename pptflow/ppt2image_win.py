import win32com.client
import os

# 依赖安装：Microsoft PowerPoint


def ppt_to_image(input_ppt_path, output_image_dir_path, 
    start_page_num=None, end_page_num=None):
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
            if start_page_num and idx + 1 < start_page_num:
                continue
            if end_page_num and idx + 1 > end_page_num:
                continue
            image_file_path = os.path.join(
                output_image_dir_path, f"{file_name_without_ext}-P{idx + 1}.png"
            )
            slide.Export(image_file_path, "PNG", 1280, 720)

        # Close the presentation
        Presentation.Close()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Quit the PowerPoint application
        Application.Quit()
