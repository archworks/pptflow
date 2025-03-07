import os
import pymupdf

def pdf_to_image(pdf_path, output_image_dir_path, image_width=1920, image_height=1080, start_page_num=None, end_page_num=None):
    # open the PDF file
    pdf_document = pymupdf.open(pdf_path)

    # get the file name without extension
    file_name_without_ext = os.path.basename(pdf_path).split(".")[0]

    for page_number in range(len(pdf_document)):
        if start_page_num and page_number + 1 < start_page_num:
            continue
        if end_page_num and page_number + 1 > end_page_num:
            continue
        # get the page
        page = pdf_document[page_number]

        # set the zoom factor
        zoom_x = int(image_width) / page.rect.width
        zoom_y = int(image_height) / page.rect.height

        # create a matrix for the zoom factor
        mat = pymupdf.Matrix(zoom_x, zoom_y)

        # get a PixMap of the page
        pix = page.get_pixmap(matrix=mat)

        # save the PixMap as a PNG image
        output_image_path = os.path.join(
            output_image_dir_path, f"{file_name_without_ext}-P{page_number + 1}.png"
        )
        pix.save(output_image_path)
        print(f"Saved: {output_image_path}")

    # close the PDF file
    pdf_document.close()