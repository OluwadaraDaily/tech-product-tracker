from .connection import DatabaseConnection
from .models import Product, PriceHistory
from .queries import ProductQueries
from .migrations import migrate_database, get_migrations

class Database:
    def __init__(self, db_path: str = "src/data/products.db"):
        self.connection = DatabaseConnection(db_path)
        self._initialize_database()

    def _initialize_database(self) -> None:
        """Initialize the database with latest migrations"""
        with self.connection.get_connection() as conn:
            migrate_database(conn)

    @property
    def products(self) -> ProductQueries:
        """Get the product queries interface"""
        return ProductQueries(self.connection)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # The connection will be closed by the context manager
        pass

__all__ = ['Database', 'Product', 'PriceHistory'] 