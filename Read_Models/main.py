import os
import json
import fitz  # PyMuPDF

from Rpost import post
from Rget import get
from to_html import layout_to_html
from figure_get import download_all_figures_from_json

endpoint = "https://azuredemo70.cognitiveservices.azure.com"
model_id = "prebuilt-layout"
api_version = "2024-11-30"
subscription_key = "Cey04m2tukpZkObAKcH3LTMwEUJEuHHZeZnRdAUiW9KmxUvOkfkwJQQJ99BFACGhslBXJ3w3AAALACOGQUJ2"
url_source = "https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf"
pdf_path = "/home/vatsal/Documents/VS Code/Azure/Read_Models/D0879824.pdf"
output_dir = "/home/vatsal/Documents/VS Code/Azure/chunks"
final_output_json = "/home/vatsal/Documents/VS Code/Azure/Read_Models/exp3.json"
image_dir = "/home/vatsal/Documents/VS Code/Azure/Read_Models/figures/exp3"

# split the pdf into chunks of 2 pages each, and pass them
chunk_size = 2

doc = fitz.open(pdf_path)
total_pages = len(doc)

# Final merged result
merged_result = {
    "pages": [],
    "tables": [],
    "paragraphs": [],
    "sections": [],
    "figures": []
}

# Running counters
para_offset = 0
table_offset = 0
figure_offset = 0
page_offset = 0  # new counter

for i in range(0, total_pages, chunk_size):
    chunk_path = os.path.join(output_dir, f"chunk_{i//chunk_size + 1}.pdf")
    
    # Extract 2-page chunk
    chunk_doc = fitz.open()
    for j in range(i, min(i + chunk_size, total_pages)):
        chunk_doc.insert_pdf(doc, from_page=j, to_page=j)
    chunk_doc.save(chunk_path)

    # Send to Azure
    operation_location = post(endpoint, model_id, api_version, subscription_key, chunk_path)

    # from operation_location, extract the result_id
    # Split into parts after last '/'
    after_last_slash = operation_location.rsplit('/', 1)[-1]
    # Then take the part before last '?'
    long_result_id = after_last_slash.rsplit('?', 1)[0]

    print(long_result_id)

    output_json_path = os.path.join(output_dir, f"chunk_{i//chunk_size + 1}.json")
    get(operation_location, subscription_key, output_json_path)

    with open(output_json_path, "r", encoding="utf-8") as f:
        chunk_data = json.load(f)
    
    result = chunk_data["analyzeResult"]

    # Merge pages
    pages = result.get("pages", [])
    for page in pages:
        page["pageNumber"] += page_offset
    merged_result["pages"].extend(pages)

    # Merge and shift paragraph references
    paragraphs = result.get("paragraphs", [])
    for idx, p in enumerate(paragraphs):
        # Adjust internal paragraph ID
        p["id"] = f"{para_offset + idx}"
        for region in p.get("boundingRegions", []):
            region["pageNumber"] += page_offset
    merged_result["paragraphs"].extend(paragraphs)

    # Merge and shift tables
    tables = result.get("tables", [])
    for idx, t in enumerate(tables):
        t["id"] = f"{table_offset + idx}"
        for region in t.get("boundingRegions", []):
            region["pageNumber"] += page_offset
    merged_result["tables"].extend(tables)

    # Merge and shift figures
    figures = result.get("figures", [])
    for idx, fig in enumerate(figures):
        fig["id"] = f"{figure_offset + idx}"
        for el in fig.get("elements", []):
            el_idx = int(el.split("/")[-1]) + para_offset
            fig["elements"] = [f"/paragraphs/{el_idx}"]
        for region in fig.get("boundingRegions", []):
            region["pageNumber"] += page_offset
    merged_result["figures"].extend(figures)

    # Merge and shift sections
    sections = result.get("sections", [])
    for sec in sections:
        # Update paragraph/table/figure references
        updated_elements = []
        for el in sec.get("elements", []):
            type_, idx = el.strip("/").split("/")
            idx = int(idx)
            if type_ == "paragraphs":
                updated_elements.append(f"/paragraphs/{idx + para_offset}")
            elif type_ == "tables":
                updated_elements.append(f"/tables/{idx + table_offset}")
            elif type_ == "figures":
                updated_elements.append(f"/figures/{idx + figure_offset}")
        sec["elements"] = updated_elements
        for region in sec.get("boundingRegions", []):
            region["pageNumber"] += page_offset
    merged_result["sections"].extend(sections)

    # Save the changes made in the individual chunk JSON
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump({"analyzeResult": result}, f, indent=2)

    # extract the cropped images for all detected figures
    download_all_figures_from_json(output_json_path, endpoint, model_id, long_result_id, subscription_key)

    # Update counters
    para_offset += len(paragraphs)
    table_offset += len(tables)
    figure_offset += len(figures)
    page_offset += len(pages)

# Final merged file
final_json = {
    "analyzeResult": merged_result
}
with open(final_output_json, "w", encoding="utf-8") as f:
    json.dump(final_json, f, indent=2)

print("✅ Merged JSON created at:", final_output_json)


# extract the data from the JSON file
layout_to_html(final_output_json, "exp3.html", figure_image_dir=image_dir)


# # Load the JSON file
# with open("invoice.json", "r") as f:
#     data = json.load(f)

# fields = data["analyzeResult"]["documents"][0]["fields"]
# result = extract_fields(fields)

# # #print the extracted key-value pairs
# # for key, value in result.items():
# #     print(f"{key}: {value}")

# # save the result in a text file
# with open("invoice.md", "w") as f:
#     for key, value in result.items():
#         f.write(f"{key}: {value}\n")