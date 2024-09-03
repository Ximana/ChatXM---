from app import db
from datetime import datetime

class Mensagem(db.Model):
    __tablename__ = 'Mensagens'
    id_mensagem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_conversa = db.Column(db.Integer, db.ForeignKey('Conversas.id_conversa'), nullable=False, index=True)
    id_remetente = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False, index=True)
    id_destinatario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    tipo_mensagem = db.Column(db.Enum('texto', 'imagem', 'video', 'arquivo'), nullable=False, default='texto')
    enviado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    lida = db.Column(db.Boolean, default=False)