from typing import List, Optional, Dict
import sqlite3
from datetime import datetime

from .models import Product, PriceHistory

class ProductQueries:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert_product(self, product: Product) -> int:
        """Insert a single product and return its ID"""
        cursor = self.conn.execute("""
            INSERT INTO products (name, price, link, image_url, store, price_change_percentage, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product.name,
            product.price,
            product.link,
            product.image_url,
            product.store,
            product.price_change_percentage,
            product.created_at.isoformat(),
            product.updated_at.isoformat()
        ))
        return cursor.lastrowid

    def insert_products(self, products: List[Product]) -> List[int]:
        """Insert multiple products and return their IDs"""
        product_ids = []
        for product in products:
            product_id = self.insert_product(product)
            product_ids.append(product_id)
            # Record initial price in history
            self.insert_price_history(product_id, product.price)
        return product_ids

    def update_product(self, product: Product) -> None:
        """Update a product's information"""
        if product.id is None:
            raise ValueError("Cannot update product without ID")
        
        self.conn.execute("""
            UPDATE products 
            SET name = ?, price = ?, link = ?, image_url = ?, 
                store = ?, price_change_percentage = ?, updated_at = ?
            WHERE id = ?
        """, (
            product.name,
            product.price,
            product.link,
            product.image_url,
            product.store,
            product.price_change_percentage,
            datetime.now().isoformat(),
            product.id
        ))
        
        # Record new price in history
        self.insert_price_history(product.id, product.price)

    def get_products(self, store: Optional[str] = None, limit: int = 100) -> List[Product]:
        """Retrieve products with optional store filter"""
        query = """
            SELECT id, name, price, link, image_url, store, price_change_percentage, created_at, updated_at
            FROM products
        """
        params = []
        
        if store:
            query += " WHERE store = ?"
            params.append(store)
        
        query += f" LIMIT {limit}"
        
        cursor = self.conn.execute(query, params)
        return [Product.from_row(dict(row)) for row in cursor.fetchall()]

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Retrieve a single product by ID"""
        cursor = self.conn.execute("""
            SELECT id, name, price, link, image_url, store, price_change_percentage, created_at, updated_at
            FROM products
            WHERE id = ?
        """, (product_id,))
        row = cursor.fetchone()
        return Product.from_row(dict(row)) if row else None

    def delete_product(self, product_id: int) -> None:
        """Delete a product and its price history"""
        self.conn.execute("DELETE FROM price_history WHERE product_id = ?", (product_id,))
        self.conn.execute("DELETE FROM products WHERE id = ?", (product_id,))

    def insert_price_history(self, product_id: int, price: float) -> None:
        """Record a price point in the history"""
        self.conn.execute("""
            INSERT INTO price_history (product_id, price)
            VALUES (?, ?)
        """, (product_id, price))

    def get_price_history(self, product_id: int) -> List[PriceHistory]:
        """Get price history for a specific product"""
        cursor = self.conn.execute("""
            SELECT id, product_id, price, recorded_at
            FROM price_history
            WHERE product_id = ?
            ORDER BY recorded_at DESC
        """, (product_id,))
        return [PriceHistory.from_row(dict(row)) for row in cursor.fetchall()]

    def get_latest_prices(self, product_ids: List[int]) -> Dict[int, float]:
        """Get the most recent price for multiple products"""
        placeholders = ','.join('?' * len(product_ids))
        cursor = self.conn.execute(f"""
            SELECT ph1.product_id, ph1.price
            FROM price_history ph1
            INNER JOIN (
                SELECT product_id, MAX(recorded_at) as max_date
                FROM price_history
                WHERE product_id IN ({placeholders})
                GROUP BY product_id
            ) ph2 ON ph1.product_id = ph2.product_id 
            AND ph1.recorded_at = ph2.max_date
        """, product_ids)
        return {row['product_id']: row['price'] for row in cursor} 