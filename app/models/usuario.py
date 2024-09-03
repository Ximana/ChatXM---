from app import db
from datetime import datetime

class Usuario(db.Model):
	__tablename__ = 'Usuarios'
	id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nome_usuario = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False, index=True)
	numero_telefone = db.Column(db.String(30), unique=True)
	senha = db.Column(db.String(255), nullable=False)
	foto_perfil = db.Column(db.String(255), default='imagem_usuario_padrao.png')
	status = db.Column(db.Enum('online', 'offline'), default='offline')
	ultimo_visto = db.Column(db.TIMESTAMP)
	criado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
	atualizado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)