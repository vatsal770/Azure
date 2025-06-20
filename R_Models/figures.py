import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeOutputOption, AnalyzeDocumentRequest, AnalyzeResult

# endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
# key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

endpoint = "https://azuredemo70.cognitiveservices.azure.com"
key = "Cey04m2tukpZkObAKcH3LTMwEUJEuHHZeZnRdAUiW9KmxUvOkfkwJQQJ99BFACGhslBXJ3w3AAALACOGQUJ2"

document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
path_to_sample_documents = "/home/vatsal/Documents/VS Code/Azure/Read_Models/D0879824.pdf"  

with open(path_to_sample_documents, "rb") as f:
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        body = AnalyzeDocumentRequest(bytes_source=f.read()),
        output=[AnalyzeOutputOption.FIGURES],
    )
result: AnalyzeResult = poller.result()
operation_id = poller.details["operation_id"]

if result.figures:
    for figure in result.figures:
        if figure.id:
            response = document_intelligence_client.get_analyze_result_figure(
                model_id=result.model_id, result_id=operation_id, figure_id=figure.id
            )
            parts = figure.id.split('.')
            new_id = f"{int(parts[0]) + 2}.{parts[1]}"
            with open(f"{new_id}.png", "wb") as writer:
                writer.writelines(response)
else:
    print("No figures found.")