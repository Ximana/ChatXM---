from app import db
from datetime import datetime

class Notificacao(db.Model):
    __tablename__ = 'Notificacoes'
    id_notificacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False, index=True)
    id_mensagem = db.Column(db.Integer, db.ForeignKey('Mensagens.id_mensagem', ondelete='SET NULL'))
    id_grupo = db.Column(db.Integer, db.ForeignKey('Grupos.id_grupo', ondelete='SET NULL'))
    tipo_notificacao = db.Column(db.Enum('mensagem', 'convite_grupo', 'atualizacao_grupo', 'mencao_grupo'), nullable=False)
    conteudo_notificacao = db.Column(db.Text)
    lida = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
