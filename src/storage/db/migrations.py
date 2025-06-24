import sqlite3
from typing import List, Tuple
from pathlib import Path

# NOTE: Update migrations by adding a new migration to the get_migrations function.
# NOTE: The migrations are run in the order of the version number.
# NOTE: The down migration is the reverse of the up migration.

class DatabaseMigration:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self._ensure_migrations_table()

    def _ensure_migrations_table(self) -> None:
        """Create migrations table if it doesn't exist"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version INTEGER NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def get_current_version(self) -> int:
        """Get the current database version"""
        cursor = self.conn.execute("SELECT MAX(version) FROM migrations")
        result = cursor.fetchone()
        return result[0] if result[0] is not None else 0

    def _run_migration(self, version: int, up_sql: str, down_sql: str) -> None:
        """Run a single migration"""
        try:
            self.conn.executescript(up_sql)
            self.conn.execute(
                "INSERT INTO migrations (version) VALUES (?)",
                (version,)
            )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error applying migration {version}: {e}")
            # Try to rollback the migration
            try:
                self.conn.executescript(down_sql)
                self.conn.commit()
            except Exception as rollback_error:
                print(f"Error rolling back migration {version}: {rollback_error}")
            raise

def get_migrations() -> List[Tuple[int, str, str]]:
    """
    Return list of migrations as (version, up_sql, down_sql)
    Add new migrations here
    """
    return [
        (
            1,
            # Up migration
            """
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                link TEXT NOT NULL,
                image_url TEXT,
                store TEXT NOT NULL,
                price_change_percentage REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX idx_store_name ON products(store, name);
            """,
            # Down migration
            """
            DROP INDEX IF EXISTS idx_store_name;
            DROP TABLE IF EXISTS products;
            """
        ),
        (
            2,
            # Up migration
            """
            CREATE TABLE price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                price REAL NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
            );
            
            CREATE INDEX idx_product_price_history 
            ON price_history(product_id, recorded_at);
            """,
            # Down migration
            """
            DROP INDEX IF EXISTS idx_product_price_history;
            DROP TABLE IF EXISTS price_history;
            """
        )
    ]

def migrate_database(conn: sqlite3.Connection, target_version: int = None) -> None:
    """
    Migrate the database to the target version
    If target_version is None, migrate to the latest version
    """
    migration_manager = DatabaseMigration(conn)
    current_version = migration_manager.get_current_version()
    migrations = get_migrations()
    
    if target_version is None:
        target_version = max(version for version, _, _ in migrations)
    
    if current_version == target_version:
        print(f"Database is already at version {target_version}")
        return
    
    if current_version > target_version:
        print(f"Downgrading database from version {current_version} to {target_version}")
        # Sort migrations in reverse order for downgrade
        relevant_migrations = [
            (v, up, down) for v, up, down in sorted(migrations, reverse=True)
            if target_version < v <= current_version
        ]
        for version, _, down_sql in relevant_migrations:
            print(f"Running down migration for version {version}")
            migration_manager._run_migration(version - 1, down_sql, "")
    else:
        print(f"Upgrading database from version {current_version} to {target_version}")
        # Sort migrations in normal order for upgrade
        relevant_migrations = [
            (v, up, down) for v, up, down in sorted(migrations)
            if current_version < v <= target_version
        ]
        for version, up_sql, down_sql in relevant_migrations:
            print(f"Running up migration for version {version}")
            migration_manager._run_migration(version, up_sql, down_sql) 