import os
import json
import fitz  # PyMuPDF

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from dotenv import load_dotenv

from Rpost import post
from json_html import layout_to_html

load_dotenv()
endpoint = os.getenv("ENDPOINT")
model_id = "prebuilt-layout"
api_version = os.getenv("API_VERSION")
subscription_key = os.getenv("SUBSCRIPTION_KEY")
url_source = "https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf"
pdf_path = "/home/vatsal/Documents/VS Code/Azure/R_Models/10537633.pdf"
output_dir = "/home/vatsal/Documents/VS Code/Azure/R_Models/chunks/1.2"
final_output_json = "/home/vatsal/Documents/VS Code/Azure/R_Models/1.2.json"
fig_path = "/home/vatsal/Documents/VS Code/Azure/R_Models/figures/1.2"

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
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    chunk_path = os.path.join(output_dir, f"chunk_{i//chunk_size + 1}.pdf")
    
    # Extract 2-page chunk
    chunk_doc = fitz.open()
    for j in range(i, min(i + chunk_size, total_pages)):
        chunk_doc.insert_pdf(doc, from_page=j, to_page=j)
    chunk_doc.save(chunk_path)

    # Send to Azure
    output_json_path = os.path.join(output_dir, f"chunk_{i//chunk_size + 1}.json")
    post(endpoint, model_id, subscription_key, chunk_path, output_json_path, fig_path, page_offset)

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
layout_to_html(final_output_json, "1.2.html", figure_image_dir=fig_path)