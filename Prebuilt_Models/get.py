import json
import requests
import time

from post import operation_location, subscription_key, output_file

while True:
    result_response = requests.get(operation_location, headers={"Ocp-Apim-Subscription-Key": subscription_key})
    result_json = result_response.json()

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
