# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_manage_models.py

DESCRIPTION:
    This sample demonstrates how to manage the models on your account. To learn
    how to build a model, look at sample_build_model.py.

USAGE:
    python sample_manage_models.py

    Set the environment variables with your own values before running the sample:
    1) DOCUMENTINTELLIGENCE_ENDPOINT - the endpoint to your Document Intelligence resource.
    2) DOCUMENTINTELLIGENCE_API_KEY - your Document Intelligence API key.
    3) DOCUMENTINTELLIGENCE_STORAGE_CONTAINER_SAS_URL - The shared access signature (SAS) Url of your Azure Blob Storage container
"""

import os


from azure.ai.documentintelligence import DocumentIntelligenceAdministrationClient
from azure.ai.documentintelligence.models import (
    DocumentBuildMode,
    BuildDocumentModelRequest,
    AzureBlobContentSource,
    DocumentModelDetails,
)
from azure.core.credentials import AzureKeyCredential

import os


def sample_build_model_with_prefix():
    endpoint = os.environ["ENDPOINT"]
    key = os.environ["SUBSCRIPTION_KEY"]
    container_sas_url = os.environ["STORAGE_CONTAINER_SAS_URL"]  # URL up to the container
    blob_prefix = "trainingDocs/"  # Optional folder prefix inside the container

    client = DocumentIntelligenceAdministrationClient(endpoint, AzureKeyCredential(key))

    model_id = "myCustomModel"  # Use your own model ID

    # 👇 AzureBlobContentSource now includes prefix
    azure_blob_source = AzureBlobContentSource(
        container_url=container_sas_url,
        prefix=blob_prefix
    )

    # 👇 Full build request with tags
    build_request = BuildDocumentModelRequest(
        model_id=model_id,
        build_mode=DocumentBuildMode.TEMPLATE,
        azure_blob_source=azure_blob_source,
        description="Custom model description",
        tags={"createdBy": "myUserId"}
    )

    print("Starting model build...")
    poller = client.begin_build_document_model(build_request)
    model: DocumentModelDetails = poller.result()

    print(f"\n✅ Model successfully built!")
    print(f"Model ID: {model.model_id}")
    print(f"Description: {model.description}")
    print(f"Created on: {model.created_date_time}")
    print(f"Expires on: {model.expiration_date_time}")
    if model.doc_types:
        print("Document Types:")
        for name, doc_type in model.doc_types.items():
            print(f" - {name} (build mode: {doc_type.build_mode})")


if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    from azure.core.exceptions import HttpResponseError

    load_dotenv(find_dotenv())
    try:
        sample_build_model_with_prefix()
    except HttpResponseError as e:
        print("❌ HTTP error occurred:", e)
        raise
