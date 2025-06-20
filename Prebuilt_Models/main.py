import json

from extraction import extract_fields_invoice


# Replace with your actual values
endpoint = "https://azuredemo70.cognitiveservices.azure.com"
model_id = "prebuilt-invoice"
api_version = "2024-11-30"
subscription_key = "Cey04m2tukpZkObAKcH3LTMwEUJEuHHZeZnRdAUiW9KmxUvOkfkwJQQJ99BFACGhslBXJ3w3AAALACOGQUJ2"
url_source = "https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf"
pdf_path = "/home/vatsal/Documents/VS Code/Azure/invoice.pdf"
output_file = "/home/vatsal/Documents/VS Code/Azure/invoice.json"


# Load the JSON file
with open("invoice.json", "r") as f:
    data = json.load(f)

fields = data["analyzeResult"]["documents"][0]["fields"]
result = extract_fields(fields)

# #print the extracted key-value pairs
# for key, value in result.items():
#     print(f"{key}: {value}")

# save the result in a text file
with open("invoice.md", "w") as f:
    for key, value in result.items():
        f.write(f"{key}: {value}\n")