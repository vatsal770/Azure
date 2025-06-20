import json
import requests
import time

def get(operation_location, subscription_key, output_file):
    while True:
        """
        Get the analysis result from the Document Intelligence API.
        """
        headers = {
            "Ocp-Apim-Subscription-Key": subscription_key
        }

        response = requests.get(operation_location, headers=headers)
        result_json = response.json()

        status = result_json.get("status")
        if status == "succeeded":
            print("✅ Analysis completed.")
            break
        elif status == "failed":
            print("❌ Analysis failed.")
            # print(json.dumps(result_json, indent=2))
            exit()
        else:
            print("⏳ Still processing...")
            time.sleep(2)
    
    # ✅ Save full JSON for reference
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result_json, f, indent=2)

    print("📄 Full response saved to result.json")

    
    
# while True:
#     result_response = requests.get(operation_location, headers={"Ocp-Apim-Subscription-Key": subscription_key})
#     result_json = result_response.json()

#     status = result_json.get("status")
#     if status == "succeeded":
#         print("✅ Analysis completed.")
#         break
#     elif status == "failed":
#         print("❌ Analysis failed.")
#         # print(json.dumps(result_json, indent=2))
#         exit()
#     else:
#         print("⏳ Still processing...")
#         time.sleep(2)

# # ✅ Save full JSON for reference
# with open(output_file, "w", encoding="utf-8") as f:
#     json.dump(result_json, f, indent=2)

# # # ✅ Extract and save markdown output if available
# # markdown_text = result_json.get("analyzeResult", {}).get("content", "")
# # if markdown_text:
# #     with open("exp1.md", "w", encoding="utf-8") as f:
# #         f.write(markdown_text)
# #     print("📝 Markdown content saved to result.md")

# print("📄 Full response saved to result.json")
