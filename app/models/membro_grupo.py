from app import db
from datetime import datetime

class MembroGrupo(db.Model):
    __tablename__ = 'MembrosGrupo'
    id_membro_grupo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_grupo = db.Column(db.Integer, db.ForeignKey('Grupos.id_grupo'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    adicionado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    e_admin = db.Column(db.Boolean, default=False)
    papel = db.Column(db.Enum('admin', 'membro', 'moderador'), default='membro')
    db.UniqueConstraint('id_grupo', 'id_usuario')