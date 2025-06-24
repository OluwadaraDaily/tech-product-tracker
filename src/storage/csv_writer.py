# Imple

import csv
import os
from typing import List
from .db import Product

FOLDER_PATH = "src/data/"

def write_to_csv(products: List[Product], filename: str) -> None:
    """
    Write products to CSV file, including price change information
    Args:
        products: List of Product objects from database
        filename: Name of the CSV file
    """
    # Create the folder if it doesn't exist
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    file_path = os.path.join(FOLDER_PATH, filename)

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Price", "Price Change %", "Link", "Image", "Store"])
        for product in products:
            writer.writerow([
                product.name,
                f"${product.price:.2f}",
                f"{product.price_change_percentage:+.1f}%" if product.price_change_percentage else "0.0%",
                product.link,
                product.image_url,
                product.store
            ])