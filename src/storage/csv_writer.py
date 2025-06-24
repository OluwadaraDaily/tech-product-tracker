# Imple

import csv
import os
from typing import List, Dict
from .db import Product

FOLDER_PATH = "src/data/"

def write_to_csv(products_with_stats: List[Dict], filename: str) -> None:
    """
    Write products to CSV file, including price statistics
    Args:
        products_with_stats: List of dictionaries containing products and their price statistics
        filename: Name of the CSV file
    """
    # Create the folder if it doesn't exist
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    file_path = os.path.join(FOLDER_PATH, filename)

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Name",
            "Current Price",
            "Price Change %",
            "Lowest Price",
            "Highest Price",
            "Average Price",
            "Link",
            "Image",
            "Store"
        ])
        
        for product_data in products_with_stats:
            product = product_data['product']
            stats = product_data['stats']
            
            writer.writerow([
                product.name,
                f"${product.price:.2f}",
                f"{product.price_change_percentage:+.1f}%" if product.price_change_percentage else "0.0%",
                f"${stats['lowest_price']:.2f}",
                f"${stats['highest_price']:.2f}",
                f"${stats['avg_price']:.2f}",
                product.link,
                product.image_url,
                product.store
            ])