import json
import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeOutputOption, AnalyzeResult, AnalyzeDocumentRequest, DocumentAnalysisFeature

from get_barcode import crop_from_pdf

def post(endpoint, model_id, key, pdf_path, output_json_path, fig_path, page_offset):
# def post(endpoint, model_id, key, pdf_path, fig_path):
    
    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    with open(pdf_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
        model_id = model_id,
        body = AnalyzeDocumentRequest(bytes_source=f.read()),
        features=[
            DocumentAnalysisFeature.BARCODES,
        ],
        output=[AnalyzeOutputOption.FIGURES],
    )

    result: AnalyzeResult = poller.result()
    operation_id = poller.details["operation_id"]

    # Save the result to a JSON file
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump({"analyzeResult": result.as_dict()}, f, indent=2)

    print(f"✅ Saved analysis result to: {output_json_path}")

    if result.figures:
        for figure in result.figures:
            if figure.id:
                # print(f"Downloading figure {figure.id}...")
                response = document_intelligence_client.get_analyze_result_figure(
                    model_id=result.model_id, result_id=operation_id, figure_id=figure.id
                )
                parts = figure.id.split('.')
                new_id = f"{int(parts[0]) + page_offset}.{parts[1]}"
                with open(fig_path+f"/{new_id}.png", "wb") as writer:
                    writer.writelines(response)

    # Save barcodes
    for page in result.pages:
        page_num = page.page_number
        if hasattr(page, "barcodes") and page.barcodes:
            for count, barcode in enumerate(page.barcodes):
                if barcode.polygon:
                    image_name = f"{page_num + page_offset}.{count+1}b"
                    crop_from_pdf(
                        pdf_path=pdf_path,
                        page_number=page_num,
                        polygon=barcode.polygon,
                        output_path=fig_path,
                        image_name=image_name,
                        page_width=page.width,
                        page_height=page.height
                    )

if __name__ == "__main__":
    
    load_dotenv()
    endpoint = os.getenv("ENDPOINT")
    model_id = "prebuilt-layout"
    subscription_key = os.getenv("SUBSCRIPTION_KEY")    
    pdf_path = "/home/vatsal/Documents/VS Code/Azure/R_Models/D0879824.pdf"
    output_dir = "/home/vatsal/Documents/VS Code/Azure/R_Models"
    fig_path = "/home/vatsal/Documents/VS Code/Azure/R_Models"

    # Define the output JSON path
    output_json_path = os.path.join(output_dir, "a1.json")

    # Call the post function to analyze the document
    post(endpoint, model_id, subscription_key, pdf_path, output_json_path, fig_path, 0)

