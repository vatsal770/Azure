import requests
import time
import json

def fget(endpoint, model_id, long_result_id, page_number, figure_index, subscription_key):
    figure_id = f"{page_number}.{figure_index}"
    figure_url = f"{endpoint}/documentintelligence/documentModels/{model_id}/analyzeResults/{long_result_id}/figures/{figure_id}"
    # figure_url = f"{long_result_id}/figures/{figure_id}"
    
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key
    }

    while True:
        response = requests.get(figure_url, headers=headers)

        if response.status_code == 200:
            print(f"✅ Figure {figure_id} is ready.")
            break
        elif response.status_code == 202:
            print(f"⏳ Figure {figure_id} is still being processed...")
            time.sleep(2)
        else:
            print(f"❌ Error {response.status_code} for Figure {figure_id}")
            print(response.text)
            return

    with open(f"figures/exp3/figure_{figure_id}.png", "wb") as f:
        f.write(response.content)


def download_all_figures_from_json(json_path, endpoint, model_id, long_result_id, subscription_key):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    figures = data.get("analyzeResult", {}).get("figures", [])
    page_figure_counts = {}

    for fig in figures:
        page = fig["boundingRegions"][0]["pageNumber"]
        page_figure_counts.setdefault(page, 0)
        page_figure_counts[page] += 1
        figure_index = page_figure_counts[page]

        fget(endpoint, model_id, long_result_id, page, figure_index, subscription_key)
