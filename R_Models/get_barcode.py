from PIL import Image
import fitz  # PyMuPDF

def crop_from_pdf(pdf_path, page_number, polygon, output_path, image_name, page_width, page_height):
    """
    Crop and save a region using normalized polygon and original page size.
    """

    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]  # convert to 0-based indexing

    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Use same logic as compute_style but scaled to actual image size
    xs = polygon[::2]
    ys = polygon[1::2]
    x = min(xs)
    y = min(ys)
    width = max(xs) - x
    height = max(ys) - y

    # Calculate scale between page logical units and rendered image
    scale_x = pix.width / page_width
    scale_y = pix.height / page_height

    # Convert to pixel values
    left = int(x * scale_x)
    top = int(y * scale_y)
    right = int((x + width) * scale_x)
    bottom = int((y + height) * scale_y)

    # Sanity check: crop within bounds
    left = max(0, left)
    top = max(0, top)
    right = min(pix.width, right)
    bottom = min(pix.height, bottom)

    cropped = img.crop((left, top, right, bottom))
    cropped.save(f"{output_path}/{image_name}.png")
    print(f"✅ Cropped saved: {output_path}/{image_name}.png")


if __name__ == "__main__":

    pdf_path = "/home/vatsal/Documents/VS Code/Azure/R_Models/D0879824.pdf"  # Replace with your PDF path
    page_number = 1  # Example page number
    polygon = [4.1172,
              0.2159,
              7.3324,
              0.2159,
              7.3324,
              0.5315,
              4.1172,
              0.5315]  # Example polygon coordinates
    output_path = "/home/vatsal/Documents/VS Code/Azure/R_Models"  # Replace with your output path
    image_name = "example_barcode"

    crop_from_pdf(pdf_path, page_number, polygon, output_path, image_name, 8.5, 11)
