import json

def layout_to_html(json_path, output_html):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    paragraphs = data.get("analyzeResult", {}).get("paragraphs", [])
    pages = data.get("analyzeResult", {}).get("pages", [])
    page_dims = {p["pageNumber"]: (p["width"], p["height"]) for p in pages}

    html_parts = [
        "<html><head><style>",
        "body { margin: 0; padding: 0; font-family: Arial; }",
        ".page { position: relative; width: 850px; height: 1100px; border: 1px solid #ccc; margin: 20px auto; }",
        ".block { position: absolute; font-size: 12px; line-height: 1.4; width: auto; white-space: pre-wrap; }",
        "</style></head><body>"
    ]

    current_page = None
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

            if current_page != page:
                if current_page is not None:
                    html_parts.append("</div>")
                html_parts.append(f'<div class="page" id="page-{page}">')
                current_page = page

            html_parts.append(f'<div class="block" style="{style}">{content}</div>')

    if current_page is not None:
        html_parts.append("</div>")

    html_parts.append("</body></html>")

    with open(output_html, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))




