from app import db
from datetime import datetime

class Grupo(db.Model):
    __tablename__ = 'Grupos'
    id_grupo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_grupo = db.Column(db.String(100), unique=False, nullable=False)
    descricao_grupo = db.Column(db.Text)
    foto_grupo = db.Column(db.String(255), default='imagem_grupo_padrao.png')
    criado_por = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    criado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    atualizado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
