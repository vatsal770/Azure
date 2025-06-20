import json

def is_overlapping(region1, region2):
    """
    Check if two polygon regions overlap.
    Each region is a list of points in the format [[x1, y1], [x2, y2], ...].
    """
    def is_point_in_polygon(point, polygon):
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    # Check if any point of region1 is in region2 or vice versa
    for point in region1:
        if is_point_in_polygon(point, region2):
            return True
    for point in region2:
        if is_point_in_polygon(point, region1):
            return True
    return False


def layout_to_markdown_filtered(data):
    """
    Converts a layout model JSON to Markdown, skipping any paragraphs that overlap with figures.
    """
    analyze_result = data.get("analyzeResult", {})
    paragraphs = analyze_result.get("paragraphs", [])
    figures = analyze_result.get("figures", [])

    # Extract all figure bounding polygons
    figure_regions = [
        figure.get("boundingRegions", [{}])[0].get("polygon", [])
        for figure in figures
    ]

    if not paragraphs:
        return "# ⚠️ No paragraphs found in the layout analysis."

    # Sort paragraphs by text offset to preserve reading order
    paragraphs_sorted = sorted(paragraphs, key=lambda p: p["spans"][0]["offset"])
    md_lines = ["# 📄 Document Content\n"]

    for para in paragraphs_sorted:
        content = para.get("content", "").replace("\n", " ").strip()
        role = para.get("role", "").lower()
        para_regions = para.get("boundingRegions", [])

        # Skip if overlapping with any figure
        if any(
            is_overlapping(para_region["polygon"], figure_region)
            for para_region in para_regions
            for figure_region in figure_regions
        ):
            continue

        # Format based on role
        if role in ("title", "heading", "sectionheading"):
            md_lines.append(f"\n## {content}\n")
        elif role == "pagefooter":
            md_lines.append(f"\n---\n*{content}*\n---\n")
        else:
            md_lines.append(f"{content}\n")

    return "\n".join(md_lines)




# Load the layout JSON file
with open("GAN.json", "r", encoding="utf-8") as f:
    layout_data = json.load(f)

# Convert to markdown string
markdown_output = layout_to_markdown_filtered(layout_data)

# Save to a markdown file
with open("GAN.md", "w", encoding="utf-8") as f:
    f.write(markdown_output)

print("✅ Markdown file created: layout_output.md")