from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Sale:
    """Entidade de domínio Venda."""
    id: Optional[int]
    date: date
    product: str
    category: str
    quantity: int
    unit_price: float
    total_value: float
    region: str
    seller: str
    created_at: datetime = None

    def calculate_total(self):
        """Business rule to calculate the total sale value."""
        self.total_value = self.quantity * self.unit_price

    def to_dict(self):
        """Serializa para dicionário."""
        return {
            'id': self.id,
            'data': self.date.isoformat() if self.date else None,
            'produto': self.product,
            'categoria': self.category,
            'quantidade': self.quantity,
            'preco_unitario': self.unit_price,
            'valor_total': self.total_value,
            'regiao': self.region,
            'vendedor': self.seller,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
