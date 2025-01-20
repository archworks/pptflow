import os
import fitz

def pdf_to_image(pdf_path, output_image_dir_path, image_width=1920, image_height=1080):
    # open the PDF file
    pdf_document = fitz.open(pdf_path)

    # get the file name without extension
    file_name_without_ext = os.path.basename(pdf_path).split(".")[0]

    for page_number in range(len(pdf_document)):
        # get the page
        page = pdf_document[page_number]

        # set the zoom factor
        zoom_x = image_width / page.rect.width
        zoom_y = image_height / page.rect.height

        # create a matrix for the zoom factor
        mat = fitz.Matrix(zoom_x, zoom_y)

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