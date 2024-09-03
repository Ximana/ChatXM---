from app import db
from datetime import datetime

class ConfiguracaoUsuario(db.Model):
    __tablename__ = 'ConfiguracoesUsuario'
    id_configuracao_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), primary_key=True)
    tema = db.Column(db.Enum('claro', 'escuro'), default='claro')
    notificacoes_ativas = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    atualizado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
