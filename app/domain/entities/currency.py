from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Currency:
    """Domain entity representing an exchange rate."""
    id: Optional[int]
    currency: str
    value: float
    timestamp: datetime
    created_at: datetime

    def is_recent(self, max_age_minutes: int = 60) -> bool:
        """
        Business rule: determines if the exchange rate is still recent.
        """
        if not self.timestamp:
            return False
        delta = datetime.utcnow() - self.timestamp
        return delta.total_seconds() <= max_age_minutes * 60

    def to_dict(self):
        """Serializa para dicionário."""
        return {
            'id': self.id,
            'moeda': self.currency,
            'valor': self.value,
            'data_hora': self.timestamp.isoformat() if self.timestamp else None
        }
