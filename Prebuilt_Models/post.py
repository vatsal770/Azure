import json
import requests
import base64

# Replace with your actual values
endpoint = "https://azuredemo70.cognitiveservices.azure.com"
model_id = "prebuilt-invoice"
api_version = "2024-11-30"
subscription_key = "Cey04m2tukpZkObAKcH3LTMwEUJEuHHZeZnRdAUiW9KmxUvOkfkwJQQJ99BFACGhslBXJ3w3AAALACOGQUJ2"
url_source = "https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf"
pdf_path = "/home/vatsal/Documents/VS Code/Azure/invoice.pdf"
output_file = "/home/vatsal/Documents/VS Code/Azure/invoice_3.json"

# API URL
# API URL with key-value extraction feature
url = f"{endpoint}/documentintelligence/documentModels/{model_id}:analyze?api-version={api_version}"

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


