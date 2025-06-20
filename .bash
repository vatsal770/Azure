curl -v -i -X POST "https://azuredemo70.cognitiveservices.azure.com/documentintelligence/documentModels/prebuilt-idDocument:analyze?api-version=2024-11-30" \
  -H "Content-Type: application/pdf" \
  -H "Ocp-Apim-Subscription-Key: Cey04m2tukpZkObAKcH3LTMwEUJEuHHZeZnRdAUiW9KmxUvOkfkwJQQJ99BFACGhslBXJ3w3AAALACOGQUJ2" \
  --data-binary "@/home/vatsal/Documents/VS Code/Azure/2025-06-17 14-32-32.pdf"


curl -v -X GET "https://azuredemo70.cognitiveservices.azure.com/documentintelligence/documentModels/prebuilt-idDocument/analyzeResults/{01229574-1dd5-40c9-aa34-baf6a854b599}?api-version=2024-11-30"\
   -H "Ocp-Apim-Subscription-Key: Cey04m2tukpZkObAKcH3LTMwEUJEuHHZeZnRdAUiW9KmxUvOkfkwJQQJ99BFACGhslBXJ3w3AAALACOGQUJ2" | jq . > output.json





curl -v -i -X POST "https://azuredemo70.cognitiveservices.azure.com/documentintelligence/documentModels/prebuilt-invoice:analyze?api-version=2024-11-30" \
  -H "Content-Type: application/pdf" \
  -H "Ocp-Apim-Subscription-Key: Cey04m2tukpZkObAKcH3LTMwEUJEuHHZeZnRdAUiW9KmxUvOkfkwJQQJ99BFACGhslBXJ3w3AAALACOGQUJ2" \
  --data-binary "@/home/vatsal/Documents/VS Code/Azure/invoice.pdf"

curl -v -X GET "https://azuredemo70.cognitiveservices.azure.com/documentintelligence/documentModels/prebuilt-invoice/analyzeResults/{58c67968-7fae-432e-9e38-093183d16ac8}?api-version=2024-11-30"\
   -H "Ocp-Apim-Subscription-Key: Cey04m2tukpZkObAKcH3LTMwEUJEuHHZeZnRdAUiW9KmxUvOkfkwJQQJ99BFACGhslBXJ3w3AAALACOGQUJ2" | jq . > invoice.json
   