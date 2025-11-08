"""
Model de Venda.
"""
from datetime import datetime
from app import db


class Venda(db.Model):
    """Representa uma venda."""
    
    __tablename__ = 'vendas'
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, index=True)
    produto = db.Column(db.String(100), nullable=False, index=True)
    categoria = db.Column(db.String(50), nullable=False, index=True)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    regiao = db.Column(db.String(50), nullable=False, index=True)
    vendedor = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Venda {self.id}: {self.produto} - R$ {self.valor_total}>'
