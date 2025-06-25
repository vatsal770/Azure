import fitz # or import pymupdf

# Open a PDF document
doc = fitz.open("/home/vatsal/Documents/VS Code/Azure/R_Models/GAN (1).pdf")

# Iterate through pages and extract text
for page in doc:
    text = page.get_text()
    # save the text into a text file as a whole
    with open("/home/vatsal/Documents/VS Code/Azure/R_Models/D1002554.txt", "a", encoding="utf-8") as f:
        f.write(text)

# Close the document
doc.close()