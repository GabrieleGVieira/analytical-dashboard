"""
Model de Upload.
"""
from datetime import datetime
from app import db


class Upload(db.Model):
    """Registra uploads de arquivos realizados."""
    
    __tablename__ = 'uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_arquivo = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # csv, json, xlsx
    status = db.Column(db.String(20), nullable=False)  # success, error, processing
    num_registros = db.Column(db.Integer)
    mensagem_erro = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Upload {self.nome_arquivo} - {self.status}>'
    
    def to_dict(self):
        """Serializa para dicionário."""
        return {
            'id': self.id,
            'nome_arquivo': self.nome_arquivo,
            'tipo': self.tipo,
            'status': self.status,
            'num_registros': self.num_registros,
            'mensagem_erro': self.mensagem_erro,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

