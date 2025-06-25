import json
import os
from collections import defaultdict

def layout_to_html(json_path, output_html, figure_image_dir=None):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    paragraphs = data.get("analyzeResult", {}).get("paragraphs", [])
    pages = data.get("analyzeResult", {}).get("pages", [])
    figures = data.get("analyzeResult", {}).get("figures", [])
    page_dims = {p["pageNumber"]: (p["width"], p["height"]) for p in pages}
    page_angles = {p["pageNumber"]: p.get("angle", 0) for p in pages}


    html_parts = [
        "<html><head><style>",
        "body { margin: 0; padding: 0; font-family: 'Times New Roman', Times, serif; }",
        ".page { position: relative; width: 850px; height: 1100px; border: 1px solid #ccc; margin: 20px auto; }",
        ".block, .figure { position: absolute; font-size: 12px; line-height: 1.0; white-space: pre-wrap; }",
        ".block.title { font-size: 16px; font-weight: bold; color: #002855; }",
        ".block.header { font-size: 14px; color: #666; }",
        ".block.heading { font-size: 12px; font-weight: bold; color: #444; }",
        ".block.footnote { font-size: 10px; font-style: italic; color: #777; }",
        ".block.footer { font-size: 10px; text-align: center; color: #999; }",
        "img.figure-img { width: 100%; height: 100%; object-fit: contain; }",
        ".barcode { position: absolute;background: white;padding: 2px;overflow: hidden; }",
        ".barcode-img { width: 100%;height: 100%;object-fit: contain;display: block; }",
        ".barcode-text { font-size: 10px; text-align: center; font-weight: bold; margin-top: 2px; color: #222; word-break: break-all; }",
        ".formula-text { font-family: 'Courier New', Courier, monospace;font-size: 12px;color: #111;white-space: pre;font-style: italic;background-color: #f8f8f8; }"
        "</style></head><body>"
    ]


    paras_by_page = defaultdict(list)
    figures_by_page = defaultdict(list)
    barcodes_by_page = defaultdict(list)
    lines_by_page = defaultdict(list)

    for para in paragraphs:
        for region in para.get("boundingRegions", []):
            page = region["pageNumber"]
            paras_by_page[page].append((para, region))

    for fig in figures:
        for region in fig.get("boundingRegions", []):
            page = region["pageNumber"]
            figures_by_page[page].append((fig, region))

    for page in data.get("analyzeResult", {}).get("pages", []):
        page_number = page["pageNumber"]
        for barcode in page.get("barcodes", []):
            barcodes_by_page[page_number].append(barcode)
        for line in page.get("lines", []):
            lines_by_page[page_number].append(line)




    def compute_style(polygon, page_width, page_height, x_offset=0, y_offset=0):
        xs = polygon[::2]
        ys = polygon[1::2]
        x = min(xs) + x_offset
        y = min(ys) + y_offset
        width = max(xs) - x + x_offset
        height = max(ys) - y + y_offset
        scale_x = 850 / page_width
        scale_y = 1100 / page_height
        return (
            f"position:absolute; left: {x * scale_x:.2f}px; top: {y * scale_y:.2f}px; "
            f"position:absolute; width: {width * scale_x:.2f}px; height: {height * scale_y:.2f}px;"
        )

    replacements = {
    "\n": " ",
    ":selected:": "",
    ":unselected:": "",
    ":checked:": "",
    ":unchecked:": "",
    ":figure:": "",
    ":barcode:": "",
    ":formula:": "",
    }

    for page in sorted(page_dims):

        angle = page_angles.get(page, 0)

        # Apply rotation if angle is ±90
        rotation_style = ""
        if angle >= 85:
            rotation_style = "transform: rotate(90deg); transform-origin: top left;"
        elif angle <= -85:
            rotation_style = "transform: rotate(-90deg); transform-origin: top left;"

        html_parts.append(f'<div class="page" id="page-{page}">')

        page_width, page_height = page_dims.get(page, (8.5, 11))


        # Barcodes
        for idx, barcode in enumerate(barcodes_by_page.get(page, [])):
            polygon = barcode.get("polygon", [])
            if not polygon:
                continue

            style = compute_style(polygon, page_width, page_height)
            barcode_id = f"{page}.{idx+1}b"
            barcode_value = barcode.get("value", "").strip()
            # add barcode value to replacements using add function
            replacements[f"{barcode_value}"] = ""   
            image_path = os.path.join(figure_image_dir, f"{barcode_id}.png")
            rel_path = os.path.relpath(image_path, os.path.dirname(output_html))

            if os.path.exists(image_path):
                html_parts.append(
                    f'<div class="barcode" style="{style}">'
                    f'<img class="barcode-img" src="{rel_path}" alt="Barcode {barcode_id}"/></div>'
                )
            # Position for text below the image (shift Y position)
                text_offset_y = 0.35  # shift down by 0.3 units in page coordinate system
                text_offset_x = 0.2  # Adjust this value as needed for spacing
                text_style = compute_style(
                    [polygon[0] + text_offset_x, polygon[1] + text_offset_y,  # top-left
                    polygon[2] + text_offset_x, polygon[3] + text_offset_y,  # top-right
                    polygon[4] + text_offset_x, polygon[5] + text_offset_y,  # bottom-right
                    polygon[6] + text_offset_x, polygon[7] + text_offset_y],  # bottom-left
                    page_width, page_height
                )

                html_parts.append(
                    f'<div class="barcode-text" style="{text_style}">{barcode_value}</div>'
                )
            else:
                html_parts.append(
                    f'<div class="barcode" style="{style}; border: 1px dashed red;">[Missing Barcode {barcode_id}]</div>'
                )



        # Paragraphs
        for para, region in paras_by_page.get(page, []):
            content = para.get("content", "").strip()
            # startswith :barcode: then ignore that paragraph
            if content.startswith(":barcode:"):
                continue
            for old, new in replacements.items():
                content = content.replace(old, new)
            if not content:
                continue

            style = compute_style(region["polygon"], page_width, page_height)


            role = para.get("role", "").lower()
            class_name = "block"
            if role == "title":
                class_name += " title"
            elif role == "pageheader":
                class_name += " header"
            elif role == "sectionheading":
                class_name += " heading"
            elif role == "footnote":
                class_name += " footnote"
            elif role == "pagefooter":
                class_name += " footer"

            # html_parts.append(f'<div class="{class_name}" style="{style} {rotation_style}">{content}</div>')
            html_parts.append(f'<div class="{class_name}" style="{style}">{content}</div>')


        # for line in lines_by_page.get(page, []):
        #     content = line.get("content", "").strip()
        #     for old, new in replacements.items():
        #         content = content.replace(old, new)
        #     if not content:
        #         continue
        #     style = compute_style(line["polygon"], page_width, page_height)
        #     html_parts.append(f'<div class="block" style="{style}">{content}</div>')

        # Figures
        for idx, (fig, region) in enumerate(figures_by_page.get(page, []), start=1):
            style = compute_style(region["polygon"], page_width, page_height)
            figure_id = f"{page}.{idx}"
            image_path = os.path.join(figure_image_dir, f"{figure_id}.png")
            rel_path = os.path.relpath(image_path, os.path.dirname(output_html))

            if os.path.exists(image_path):
                html_parts.append(
                    f'<div class="figure" style="{style}">' +
                    f'<img class="figure-img" src="{rel_path}" alt="Figure {figure_id}"/></div>'
                )
            else:
                html_parts.append(
                    f'<div class="figure" style="{style}; border: 1px dashed red;">[Missing Figure {figure_id}]</div>'
                )


        html_parts.append("</div>")  # close .page

    with open(output_html, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

if __name__ == "__main__":
    json_path = "/home/vatsal/Documents/VS Code/Azure/R_Models/exp4.json"
    output_html = "/home/vatsal/Documents/VS Code/Azure/R_Models/exp4.html"
    figure_image_dir = "/home/vatsal/Documents/VS Code/Azure/R_Models/figures/exp4"

    layout_to_html(json_path, output_html, figure_image_dir)
    print(f"HTML layout saved to: {output_html}")
