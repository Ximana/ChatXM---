from app import db
from datetime import datetime

class MensagemGrupo(db.Model):
    __tablename__ = 'MensagensGrupo'
    id_mensagem_grupo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_grupo = db.Column(db.Integer, db.ForeignKey('Grupos.id_grupo'), nullable=False, index=True)
    id_remetente = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False, index=True)
    mensagem = db.Column(db.Text, nullable=False)
    tipo_mensagem = db.Column(db.Enum('texto', 'imagem', 'video', 'arquivo'), nullable=False, default='texto')
    enviado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    lida = db.Column(db.Boolean, default=False)