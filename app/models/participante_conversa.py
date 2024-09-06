from app import db
from datetime import datetime

class ParticipanteConversa(db.Model):
    __tablename__ = 'ParticipantesConversa'
    id_participante_conversa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_conversa = db.Column(db.Integer, db.ForeignKey('Conversas.id_conversa'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    adicionado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    db.UniqueConstraint('id_conversa', 'id_usuario')

# Adicionando o relacionamento com a tabela Conversa
    conversa = db.relationship('Conversa', backref='participantes')
    
    db.UniqueConstraint('id_conversa', 'id_usuario')