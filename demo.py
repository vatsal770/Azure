curl -v -i -X POST "{https://azuredemo70.cognitiveservices.azure.com}/documentintelligence/documentModels/{prebuilt-idDocument}:analyze?api-version=2024-11-30" -H "Content-Type: application/json" -H "Ocp-Apim-Subscription-Key: {Cey04m2tukpZkObAKcH3LTMwEUJEuHHZeZnRdAUiW9KmxUvOkfkwJQQJ99BFACGhslBXJ3w3AAALACOGQUJ2}" --data-ascii "{'urlSource': '{https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/identity_documents.png}'}"



--data-binary "/home/vatsal/Documents/VS Code/Azure/2025-06-17 14-32-32.pdf"
--data-ascii "{'urlSource': '{https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/identity_documents.png}'}"

curl -v -i -X POST "https://azuredemo70.cognitiveservices.azure.com/documentintelligence/documentModels/prebuilt-idDocument:analyze?api-version=2024-11-30" \
  -H "Content-Type: application/pdf" \
  -H "Ocp-Apim-Subscription-Key: Cey04m2tukpZkObAKcH3LTMwEUJEuHHZeZnRdAUiW9KmxUvOkfkwJQQJ99BFACGhslBXJ3w3AAALACOGQUJ2" \
  --data-ascii "https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf"

https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf

https://azuredemo70.cognitiveservices.azure.com/documentintelligence/documentModels/prebuilt-idDocument/analyzeResults/01229574-1dd5-40c9-aa34-baf6a854b599?api-version=2024-11-30
https://azuredemo70.cognitiveservices.azure.com/documentintelligence/documentModels/prebuilt-invoice/analyzeResults/58c67968-7fae-432e-9e38-093183d16ac8?api-version=2024-11-30

curl -v -X GET "https://azuredemo70.cognitiveservices.azure.com/documentintelligence/documentModels/prebuilt-idDocument/analyzeResults/{01229574-1dd5-40c9-aa34-baf6a854b599}?api-version=2024-11-30"   -H "Ocp-Apim-Subscription-Key: Cey04m2tukpZkObAKcH3LTMwEUJEuHHZeZnRdAUiW9KmxUvOkfkwJQQJ99BFACGhslBXJ3w3AAALACOGQUJ2" | jq . > output.json