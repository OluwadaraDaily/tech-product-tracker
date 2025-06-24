from .db import Database, Product, PriceHistory
from typing import List, Dict

def store_products(products: List[Dict], store: str) -> List[int]:
    """
    Store products in the database, updating existing ones and tracking price changes
    Args:
        products: List of product dictionaries
        store: Store name (e.g., 'microcenter')
    Returns:
        List of inserted/updated product IDs
    """
    # Convert raw products to Product objects with store info
    product_objects = [
        Product.from_dict({**product, 'store': store, 'price_change_percentage': 0})
        for product in products
    ]
    
    # Store in database (will handle updates and price tracking)
    with Database() as db:
        return db.products.insert_products(product_objects)

def get_products(store: str = None) -> List[Product]:
    """Get all products for a store with their current price changes"""
    with Database() as db:
        return db.products.get_products(store)

def get_price_history(product_id: int) -> List[PriceHistory]:
    """Get complete price history for a product"""
    with Database() as db:
        return db.products.get_price_history(product_id)

def get_latest_prices(product_ids: List[int]) -> Dict[int, float]:
    """Get the most recent prices for multiple products"""
    with Database() as db:
        return db.products.get_latest_prices(product_ids)