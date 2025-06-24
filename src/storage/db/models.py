from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Product:
    id: Optional[int]
    name: str
    price: float
    link: str
    image_url: str
    store: str
    price_change_percentage: float
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: dict) -> 'Product':
        """Create a Product instance from a database row"""
        return cls(
            id=row['id'],
            name=row['name'],
            price=row['price'],
            link=row['link'],
            image_url=row['image_url'],
            store=row['store'],
            price_change_percentage=row['price_change_percentage'],
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Create a Product instance from a dictionary"""
        return cls(
            id=None,
            name=data['name'],
            price=float(str(data['price']).replace('$', '').replace(',', '')),
            link=data['link'],
            image_url=data['image'],
            store=data.get('store', 'unknown'),
            price_change_percentage=data.get('price_change_percentage', 0),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

@dataclass
class PriceHistory:
    id: Optional[int]
    product_id: int
    price: float
    recorded_at: datetime

    @classmethod
    def from_row(cls, row: dict) -> 'PriceHistory':
        """Create a PriceHistory instance from a database row"""
        return cls(
            id=row['id'],
            product_id=row['product_id'],
            price=row['price'],
            recorded_at=datetime.fromisoformat(row['recorded_at'])
        ) 