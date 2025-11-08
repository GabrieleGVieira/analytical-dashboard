"""
Model de Meta.
"""
from datetime import datetime
from app import db


class Meta(db.Model):
    """Representa uma meta de vendas."""
    
    __tablename__ = 'metas'
    
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer, nullable=False, index=True)
    mes = db.Column(db.Integer, nullable=False, index=True)
    categoria = db.Column(db.String(50), nullable=False, index=True)
    regiao = db.Column(db.String(50), nullable=False, index=True)
    meta_valor = db.Column(db.Float, nullable=False)
    meta_quantidade = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('ano', 'mes', 'categoria', 'regiao', name='uq_meta'),
    )
    
    def __repr__(self):
        return f'<Meta {self.ano}/{self.mes} - {self.categoria}/{self.regiao}>'
    
    def to_dict(self):
        """Serializa para dicionário."""
        return {
            'id': self.id,
            'ano': self.ano,
            'mes': self.mes,
            'categoria': self.categoria,
            'regiao': self.regiao,
            'meta_valor': self.meta_valor,
            'meta_quantidade': self.meta_quantidade
        }

