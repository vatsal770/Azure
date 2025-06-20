import json
import requests
import base64


def post(endpoint, model_id, api_version, subscription_key, pdf_path):
    """
    Post a PDF file to the Document Intelligence API for analysis.
    """
    # API URL with key-value extraction feature
    url = f"{endpoint}/documentintelligence/documentModels/{model_id}:analyze?api-version={api_version}&features=keyValuePairs,formulas,barcodes&output=figures"  # ,queryFields&queryFields=TERMS for additional query fields
    # {endpoint}/documentintelligence/documentModels/{modelId}:analyze?api-version={apiVersion}&features=keyValuePairs,formulas,barcodes&output=figures

    # Headers
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key
    }

    with open(pdf_path, "rb") as file:
        base64_encoded = base64.b64encode(file.read()).decode("utf-8")
    
    body = {"base64Source": base64_encoded}

    response = requests.post(url, headers=headers, data=json.dumps(body))

    if response.status_code != 202:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        exit()

    operation_location = response.headers.get("Operation-Location")
    print("📨 Uploaded. Waiting for analysis...")
    
    return operation_location



