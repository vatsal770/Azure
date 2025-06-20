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

    html_parts = [
        "<html><head><style>",
        "body { margin: 0; padding: 0; font-family: Arial; }",
        ".page { position: relative; width: 850px; height: 1100px; border: 1px solid #ccc; margin: 20px auto; }",
        ".block, .figure { position: absolute; font-size: 12px; line-height: 1.4; white-space: pre-wrap; }",
        "img.figure-img { width: 100%; height: 100%; object-fit: contain; }",
        "</style></head><body>"
    ]

    current_page = None

    def start_page_if_needed(page):
        nonlocal current_page
        if current_page != page:
            if current_page is not None:
                html_parts.append("</div>")
            html_parts.append(f'<div class="page" id="page-{page}">')
            current_page = page

    # Render paragraphs
    for para in paragraphs:
        content = para.get("content", "").replace("\n", " ").strip()
        if not content:
            continue

        for region in para.get("boundingRegions", []):
            page = region["pageNumber"]
            polygon = region["polygon"]

            xs = polygon[::2]
            ys = polygon[1::2]
            x = min(xs)
            y = min(ys)
            width = max(xs) - x
            height = max(ys) - y

            page_width, page_height = page_dims.get(page, (8.5, 11))
            scale_x = 850 / page_width
            scale_y = 1100 / page_height

            style = (
                f"left: {x * scale_x:.2f}px; top: {y * scale_y:.2f}px; "
                f"width: {width * scale_x:.2f}px; height: {height * scale_y:.2f}px;"
            )

            start_page_if_needed(page)
            html_parts.append(f'<div class="block" style="{style}">{content}</div>')

    # Track figure index per page
    figure_index_counter = defaultdict(int)

    # Render figures
    for figure in figures:
        regions = figure.get("boundingRegions", [])
        for region in regions:
            page = region["pageNumber"]
            figure_index_counter[page] += 1
            figure_index = figure_index_counter[page]
            figure_id = f"{page}.{figure_index}"

            polygon = region["polygon"]
            xs = polygon[::2]
            ys = polygon[1::2]
            x = min(xs)
            y = min(ys)
            width = max(xs) - x
            height = max(ys) - y

            page_width, page_height = page_dims.get(page, (8.5, 11))
            scale_x = 850 / page_width
            scale_y = 1100 / page_height

            style = (
                f"left: {x * scale_x:.2f}px; top: {y * scale_y:.2f}px; "
                f"width: {width * scale_x:.2f}px; height: {height * scale_y:.2f}px;"
            )

            start_page_if_needed(page)

            image_path = os.path.join(figure_image_dir, f"figure_{figure_id}.png")
            rel_path = os.path.relpath(image_path, os.path.dirname(output_html))

            if os.path.exists(image_path):
                html_parts.append(
                    f'<div class="figure" style="{style}">'
                    f'<img class="figure-img" src="{rel_path}" alt="Figure {figure_id}"/></div>'
                )
            else:
                html_parts.append(
                    f'<div class="figure" style="{style}; border: 1px dashed red;">[Missing Figure {figure_id}]</div>'
                )


    if current_page is not None:
        html_parts.append("</div>")

    html_parts.append("</body></html>")

    with open(output_html, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))


