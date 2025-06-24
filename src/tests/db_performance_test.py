import time
from datetime import datetime
from typing import List
import random
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from storage.db import Database, Product
from storage.db.queries import ProductQueries
from storage.db.connection import DatabaseConnection

def generate_test_products(count: int) -> List[Product]:
    """Generate test products"""
    products = []
    stores = ['microcenter', 'bestbuy', 'amazon']
    
    for i in range(count):
        product = Product(
            id=None,
            name=f"Test Product {i}",
            price=random.uniform(100, 1000),
            link=f"https://example.com/product{i}",
            image_url=f"https://example.com/image{i}.jpg",
            store=random.choice(stores),
            price_change_percentage=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        products.append(product)
    return products

class TestProductQueries:
    """Test version of ProductQueries that demonstrates the performance difference"""
    
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def insert_product_separate_connections(self, product: Product) -> int:
        """Insert a single product with its own connection"""
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
            
            # Record price history
            product_id = cursor.lastrowid
            conn.execute("""
                INSERT INTO price_history (product_id, price)
                VALUES (?, ?)
            """, (product_id, product.price))
            
            conn.commit()
            return cursor.lastrowid

    def insert_products_separate_connections(self, products: List[Product]) -> List[int]:
        """Insert products with separate connections for each"""
        product_ids = []
        for product in products:
            product_id = self.insert_product_separate_connections(product)
            product_ids.append(product_id)
        return product_ids

    def insert_products_single_connection(self, products: List[Product]) -> List[int]:
        """Insert products with a single connection"""
        product_ids = []
        with self.connection.get_connection() as conn:
            for product in products:
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
                
                product_id = cursor.lastrowid
                product_ids.append(product_id)
                
                # Record price history
                conn.execute("""
                    INSERT INTO price_history (product_id, price)
                    VALUES (?, ?)
                """, (product_id, product.price))
            
            conn.commit()
        return product_ids

def run_performance_test(product_count: int = 100):
    """Run performance comparison test"""
    print(f"\nRunning performance test with {product_count} products...")
    
    # Initialize database with test path
    db = Database("src/tests/test_performance.db")
    test_queries = TestProductQueries(db.connection)
    
    # Generate test products
    print("\nGenerating test products...")
    products = generate_test_products(product_count)
    
    # Test separate connections
    print("\nTesting with separate connections...")
    start_time = time.time()
    try:
        ids_separate = test_queries.insert_products_separate_connections(products)
        separate_time = time.time() - start_time
        print(f"✓ Separate connections completed in {separate_time:.2f} seconds")
    except Exception as e:
        print(f"✗ Separate connections failed: {e}")
        separate_time = None
    
    # Clear database for next test
    with db.connection.get_connection() as conn:
        conn.execute("DELETE FROM price_history")
        conn.execute("DELETE FROM products")
        conn.commit()
    
    # Test single connection
    print("\nTesting with single connection...")
    start_time = time.time()
    try:
        ids_single = test_queries.insert_products_single_connection(products)
        single_time = time.time() - start_time
        print(f"✓ Single connection completed in {single_time:.2f} seconds")
    except Exception as e:
        print(f"✗ Single connection failed: {e}")
        single_time = None
    
    # Print comparison
    if separate_time and single_time:
        speedup = (separate_time - single_time) / separate_time * 100
        print(f"\nResults:")
        print(f"Separate connections: {separate_time:.2f} seconds")
        print(f"Single connection:    {single_time:.2f} seconds")
        print(f"Performance improvement: {speedup:.1f}%")

if __name__ == "__main__":
    # Test with different numbers of products
    for count in [10, 100, 1000]:
        run_performance_test(count) 