from azure.storage.blob import BlobServiceClient
import os

def upload_first_n_files(account_name, account_key, container_name, local_folder, prefix="", limit=10):
    blob_service_client = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=account_key
    )
    container_client = blob_service_client.get_container_client(container_name)

    if not container_client.exists():
        container_client.create_container()

    uploaded_count = 0

    for root, _, files in os.walk(local_folder):
        for filename in sorted(files):  # sorted to make order predictable
            if uploaded_count >= limit:
                print(f"✅ Uploaded {uploaded_count} files. Done.")
                return

            if filename.lower().endswith(('.pdf', '.jpg', '.png', '.tif', '.tiff')):
                file_path = os.path.join(root, filename)
                blob_name = os.path.join(prefix, filename).replace("\\", "/")

                with open(file_path, "rb") as data:
                    container_client.upload_blob(
                        name=blob_name,
                        data=data,
                        overwrite=True
                    )
                uploaded_count += 1
                print(f"[{uploaded_count}] Uploaded: {blob_name}")

    if uploaded_count == 0:
        print("⚠️ No eligible files found.")
    else:
        print(f"✅ Uploaded {uploaded_count} files.")



if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    account_name = os.getenv("STORAGE_ACCOUNT_NAME")
    account_key = os.getenv("STORAGE_ACCOUNT_KEY")
    container_name = "$logs"
    local_folder = "/home/vatsal/Downloads/patents_1_pdf"  # Replace with your local folder path
    prefix = "$logs"  # Optional prefix for the blobs

    upload_first_n_files(account_name, account_key, container_name, local_folder, prefix, limit=10)
