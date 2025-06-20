import html2text

# Read the HTML content
with open("exp2_1.html", "r", encoding="utf-8") as html_file:
    html_content = html_file.read()

# Convert HTML to Markdown
markdown = html2text.html2text(html_content)

# Write to a Markdown file
with open("exp2_1.md", "w", encoding="utf-8") as md_file:
    md_file.write(markdown)

print("✅ Markdown file created: exp2_1.md")