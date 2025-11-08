from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Upload:
    """Domain entity representing a file upload record."""
    id: Optional[int]
    file_name: str
    file_type: str  # csv, json, xlsx
    status: str     # success, error, processing
    record_count: Optional[int] = None
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None

    def mark_as_success(self, record_count: int):
        """Business rule: mark upload as successful."""
        self.status = "success"
        self.record_count = record_count
        self.error_message = None

    def mark_as_error(self, message: str):
        """Business rule: mark upload as failed."""
        self.status = "error"
        self.error_message = message

    def to_dict(self):
        """Serializa para dicionário."""
        return {
            'id': self.id,
            'nome_arquivo': self.file_name,
            'tipo': self.file_type,
            'status': self.status,
            'num_registros': self.record_count,
            'mensagem_erro': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }