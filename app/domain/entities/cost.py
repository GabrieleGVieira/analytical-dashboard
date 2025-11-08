from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Cost:
    """Domain entity representing the cost of a product."""
    id: Optional[int]
    product: str
    category: str
    unit_cost: float
    updated_at: date
    created_at: Optional[datetime] = None

    def update_cost(self, new_cost: float):
        """
        Business rule: update the cost of a product and record the update date.
        """
        self.unit_cost = new_cost
        self.updated_at = date.today()

    def to_dict(self):
        """Serializa para dicionário."""
        return {
            'id': self.id,
            'produto': self.product,
            'categoria': self.category,
            'custo_unitario': self.unit_cost,
            'data_atualizacao': self.updated_at.isoformat() if self.updated_at else None
        }
