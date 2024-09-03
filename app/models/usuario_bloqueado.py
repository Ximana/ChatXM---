from app import db
from datetime import datetime

class UsuarioBloqueado(db.Model):
    __tablename__ = 'UsuariosBloqueados'
    id_usuario_bloqueado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_bloqueador = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    id_bloqueado = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    bloqueado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    db.UniqueConstraint('id_bloqueador', 'id_bloqueado')
