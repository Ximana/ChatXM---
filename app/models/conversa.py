from app import db
from datetime import datetime

class Conversa(db.Model):
    __tablename__ = 'Conversas'
    id_conversa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    criado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    atualizado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    esta_ativa = db.Column(db.Boolean, default=True)