import os
import json
import fitz  # PyMuPDF

pdf_path = "/home/vatsal/Documents/VS Code/Azure/Read_Models/D0879824.pdf"
output_dir = "/home/vatsal/Documents/VS Code/Azure/R_models/chunks/exp3"

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)  # <-- Fixes the error

# split the pdf into chunks of 2 pages each, and pass them
chunk_size = 2

doc = fitz.open(pdf_path)
total_pages = len(doc)

for i in range(0, total_pages, chunk_size):
    chunk_path = os.path.join(output_dir, f"chunk_{i//chunk_size + 1}.pdf")
    
    # Extract 2-page chunk
    chunk_doc = fitz.open()
    for j in range(i, min(i + chunk_size, total_pages)):
        chunk_doc.insert_pdf(doc, from_page=j, to_page=j)
    chunk_doc.save(chunk_path)