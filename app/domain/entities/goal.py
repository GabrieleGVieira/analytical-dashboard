from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Goal:
    """Domain entity representing a sales goal."""
    id: Optional[int]
    year: int
    month: int
    category: str
    region: str
    target_value: float
    target_quantity: int
    created_at: Optional[datetime] = None

    def is_reached(self, total_value: float, total_quantity: int) -> bool:
        """
        Business rule: checks if the goal has been reached.
        """
        return total_value >= self.target_value and total_quantity >= self.target_quantity

    def to_dict(self):
        """Serializa para dicionário."""
        return {
            'id': self.id,
            'ano': self.year,
            'mes': self.month,
            'categoria': self.category,
            'regiao': self.region,
            'meta_valor': self.target_value,
            'meta_quantidade': self.target_quantity
        }