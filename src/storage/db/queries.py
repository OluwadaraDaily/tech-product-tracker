from typing import List, Optional, Dict
import sqlite3
from datetime import datetime

from .models import Product, PriceHistory
from .connection import DatabaseConnection

class ProductQueries:
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def insert_product(self, product: Product, conn=None) -> int:
        """
        Insert a single product and return its ID
        Args:
            product: Product to insert
            conn: Optional connection to use (for batch operations)
        """
        if conn is None:
            with self.connection.get_connection() as conn:
                cursor = conn.execute("""
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
                conn.commit()
                return cursor.lastrowid
        else:
            cursor = conn.execute("""
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
        """Insert or update multiple products and return their IDs"""
        product_ids = []
        with self.connection.get_connection() as conn:
            for product in products:
                # Use upsert instead of insert
                product_id = self.upsert_product(product, conn)
                product_ids.append(product_id)
            return product_ids

    def update_product(self, product: Product) -> None:
        """Update a product's information"""
        if product.id is None:
            raise ValueError("Cannot update product without ID")
        
        with self.connection.get_connection() as conn:
            conn.execute("""
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
            conn.execute("""
                INSERT INTO price_history (product_id, price)
                VALUES (?, ?)
            """, (product.id, product.price))
            
            conn.commit()

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
        
        with self.connection.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [Product.from_row(dict(row)) for row in cursor.fetchall()]

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Retrieve a single product by ID"""
        with self.connection.get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, name, price, link, image_url, store, price_change_percentage, created_at, updated_at
                FROM products
                WHERE id = ?
            """, (product_id,))
            row = cursor.fetchone()
            return Product.from_row(dict(row)) if row else None

    def delete_product(self, product_id: int) -> None:
        """Delete a product and its price history"""
        with self.connection.get_connection() as conn:
            conn.execute("DELETE FROM price_history WHERE product_id = ?", (product_id,))
            conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()

    def get_price_history(self, product_id: int) -> List[PriceHistory]:
        """Get price history for a specific product"""
        with self.connection.get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, product_id, price, recorded_at
                FROM price_history
                WHERE product_id = ?
                ORDER BY recorded_at DESC
            """, (product_id,))
            return [PriceHistory.from_row(dict(row)) for row in cursor.fetchall()]

    def get_latest_prices(self, product_ids: List[int]) -> Dict[int, float]:
        """Get the most recent price for multiple products"""
        placeholders = ','.join('?' * len(product_ids))
        with self.connection.get_connection() as conn:
            cursor = conn.execute(f"""
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

    def get_product_by_name_and_store(self, name: str, store: str) -> Optional[Product]:
        """Find a product by name and store"""
        with self.connection.get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, name, price, link, image_url, store, price_change_percentage, created_at, updated_at
                FROM products
                WHERE name = ? AND store = ?
            """, (name, store))
            row = cursor.fetchone()
            return Product.from_row(dict(row)) if row else None

    def calculate_price_change(self, product_id: int, new_price: float) -> float:
        """Calculate price change percentage from the last known price"""
        with self.connection.get_connection() as conn:
            cursor = conn.execute("""
                SELECT price
                FROM price_history
                WHERE product_id = ?
                ORDER BY recorded_at DESC
                LIMIT 1
            """, (product_id,))
            row = cursor.fetchone()
            
            if row:
                last_price = row['price']
                if last_price > 0:  # Avoid division by zero
                    return ((new_price - last_price) / last_price) * 100
            return 0.0

    def upsert_product(self, product: Product, conn=None) -> int:
        """Insert or update a product based on name and store"""
        existing_product = self.get_product_by_name_and_store(product.name, product.store)
        
        if existing_product:
            # Calculate price change
            price_change = self.calculate_price_change(existing_product.id, product.price)
            
            # Update existing product
            if conn is None:
                with self.connection.get_connection() as conn:
                    conn = conn
            else:
                conn = conn
            
                conn.execute("""
                    UPDATE products 
                    SET price = ?, link = ?, image_url = ?, 
                        price_change_percentage = ?, updated_at = ?
                    WHERE id = ?
                """, (
                    product.price,
                    product.link,
                    product.image_url,
                    price_change,
                    datetime.now().isoformat(),
                    existing_product.id
                ))
                
                # Record new price in history
                conn.execute("""
                    INSERT INTO price_history (product_id, price)
                    VALUES (?, ?)
                """, (existing_product.id, product.price))
                
                conn.commit()
                return existing_product.id
        else:
            # Insert new product
            return self.insert_product(product)

    def get_price_statistics(self, product_id: int) -> Dict[str, float]:
        """Get price statistics for a product (lowest, highest, average price)"""
        with self.connection.get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                    MIN(price) as lowest_price,
                    MAX(price) as highest_price,
                    AVG(price) as avg_price
                FROM price_history
                WHERE product_id = ?
            """, (product_id,))
            row = cursor.fetchone()
            return {
                'lowest_price': row['lowest_price'] if row['lowest_price'] is not None else 0.0,
                'highest_price': row['highest_price'] if row['highest_price'] is not None else 0.0,
                'avg_price': round(row['avg_price'], 2) if row['avg_price'] is not None else 0.0
            }

    def get_products_with_stats(self, store: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Get products with their price statistics"""
        products = self.get_products(store, limit)
        result = []
        
        for product in products:
            stats = self.get_price_statistics(product.id)
            product_dict = {
                'product': product,
                'stats': stats
            }
            result.append(product_dict)
        
        return result 