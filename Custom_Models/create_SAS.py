import os
import datetime
from dotenv import load_dotenv

from azure.storage.blob import generate_account_sas, AccountSasPermissions, ResourceTypes


def create_account_sas(account_name: str, account_key: str):
    # Create an account SAS that's valid for one day
    start_time = datetime.datetime.now(datetime.timezone.utc)
    expiry_time = start_time + datetime.timedelta(days=1)

    # Define the SAS token permissions
    sas_permissions=AccountSasPermissions(read=True,
        write=True,
        delete=True,
        list=True,
        add=True,
        create=True,
        update=True,
        process=True
)

    # Define the SAS token resource types
    # For this example, we grant access to service-level APIs
    sas_resource_types=ResourceTypes(service=True)

    sas_token = generate_account_sas(
        account_name=account_name,
        account_key=account_key,
        resource_types=sas_resource_types,
        permission=sas_permissions,
        expiry=expiry_time,
        start=start_time
    )

    return sas_token

load_dotenv()
account_name = os.getenv("STORAGE_ACCOUNT_NAME")
key = os.getenv("SUBSCRIPTION_KEY")
sas_token = create_account_sas(account_name, key)
sas_url = f"https://{account_name}.blob.core.windows.net/?{sas_token}"
print(f"SAS URL: {sas_url}")