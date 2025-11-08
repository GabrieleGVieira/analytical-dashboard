"""
Model de Cotação.
"""
from datetime import datetime
from app import db


class Cotacao(db.Model):
    """Representa uma cotação de moeda."""
    
    __tablename__ = 'cotacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    moeda = db.Column(db.String(10), nullable=False, index=True)
    valor = db.Column(db.Float, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Cotacao {self.moeda}: R$ {self.valor}>'
