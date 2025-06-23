# Imple

import csv
import os

FOLDER_PATH = "src/data/"

def write_to_csv(data: list, filename: str) -> None:
    # Create the folder if it doesn't exist
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    file_path = os.path.join(FOLDER_PATH, filename)

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Price", "Link", "Image"])
        for item in data:
            writer.writerow([item["name"], item["price"], item["link"], item["image"]])