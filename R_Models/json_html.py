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
        ".block.title { font-size: 16px; font-weight: bold; color: #002855; }",
        ".block.header { font-size: 14px; color: #666; }",
        ".block.heading { font-size: 12px; font-weight: bold; color: #444; }",
        ".block.footnote { font-size: 10px; font-style: italic; color: #777; }",
        ".block.footer { font-size: 10px; text-align: center; color: #999; }",
        "img.figure-img { width: 100%; height: 100%; object-fit: contain; }",
        "</style></head><body>"
    ]

    paras_by_page = defaultdict(list)
    figures_by_page = defaultdict(list)

    for para in paragraphs:
        for region in para.get("boundingRegions", []):
            page = region["pageNumber"]
            paras_by_page[page].append((para, region))

    for fig in figures:
        for region in fig.get("boundingRegions", []):
            page = region["pageNumber"]
            figures_by_page[page].append((fig, region))

    def compute_style(polygon, page_width, page_height):
        xs = polygon[::2]
        ys = polygon[1::2]
        x = min(xs)
        y = min(ys)
        width = max(xs) - x
        height = max(ys) - y
        scale_x = 850 / page_width
        scale_y = 1100 / page_height
        return (
            f"left: {x * scale_x:.2f}px; top: {y * scale_y:.2f}px; "
            f"width: {width * scale_x:.2f}px; height: {height * scale_y:.2f}px;"
        )

    for page in sorted(page_dims):
        html_parts.append(f'<div class="page" id="page-{page}">')

        page_width, page_height = page_dims.get(page, (8.5, 11))

        for para, region in paras_by_page.get(page, []):
            content = para.get("content", "").replace("\n", " ").strip()
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

            html_parts.append(f'<div class="{class_name}" style="{style}">{content}</div>')

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
    json_path = "/home/vatsal/Documents/VS Code/Azure/R_Models/exp2.json"
    output_html = "/home/vatsal/Documents/VS Code/Azure/R_Models/exp2.html"
    figure_image_dir = "/home/vatsal/Documents/VS Code/Azure/R_Models/figures/exp2"

    layout_to_html(json_path, output_html, figure_image_dir)
    print(f"HTML layout saved to: {output_html}")
