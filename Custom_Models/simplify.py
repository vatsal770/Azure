# i have a folder with lots of folders inside one another, i want to extract all .pdf files from all folders and subfolders and save them in a single folder

import os
def extract_pdf_files(source_folder: str, destination_folder: str):
    """
    Extract all .pdf files from the source folder and its subfolders and save them in the destination folder.
    
    :param source_folder: The path to the source folder containing .pdf files.
    :param destination_folder: The path to the destination folder where .pdf files will be saved.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(destination_folder, file)
                print(f"Copying {source_file_path} to {destination_file_path}")
                with open(source_file_path, 'rb') as src_file:
                    with open(destination_file_path, 'wb') as dest_file:
                        dest_file.write(src_file.read())

source_folder = '/home/vatsal/Downloads/patents_1'  # Replace with your source folder path
destination_folder = '/home/vatsal/Downloads/patents_1_pdf'  # Replace with your destination folder path

extract_pdf_files(source_folder, destination_folder)