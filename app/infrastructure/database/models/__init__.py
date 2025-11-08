"""
Models da aplicação.
"""
from app.infrastructure.database.models.venda import Venda
from app.infrastructure.database.models.custo import Custo
from app.infrastructure.database.models.cotacao import Cotacao
from app.infrastructure.database.models.meta import Meta
from app.infrastructure.database.models.upload import Upload

__all__ = ['Venda', 'Custo', 'Cotacao', 'Meta', 'Upload']

