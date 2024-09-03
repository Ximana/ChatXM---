from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    senha = db.Column(db.String(255), nullable=False)
    foto_perfil = db.Column(db.String(255), default='url_padrao.jpg')
    status = db.Column(db.Enum('online', 'offline', 'ocupado', 'ausente'), default='offline')
    ultimo_visto = db.Column(db.TIMESTAMP)
    criado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    atualizado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class Conversa(db.Model):
    __tablename__ = 'Conversas'
    id_conversa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    criado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    atualizado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    esta_ativa = db.Column(db.Boolean, default=True)

class ParticipanteConversa(db.Model):
    __tablename__ = 'ParticipantesConversa'
    id_participante = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_conversa = db.Column(db.Integer, db.ForeignKey('Conversas.id_conversa'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    adicionado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    db.UniqueConstraint('id_conversa', 'id_usuario')

class Mensagem(db.Model):
    __tablename__ = 'Mensagens'
    id_mensagem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_conversa = db.Column(db.Integer, db.ForeignKey('Conversas.id_conversa'), nullable=False, index=True)
    id_remetente = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False, index=True)
    id_destinatario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    tipo_mensagem = db.Column(db.Enum('texto', 'imagem', 'video', 'arquivo'), nullable=False)
    enviado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    lida = db.Column(db.Boolean, default=False)

class Grupo(db.Model):
    __tablename__ = 'Grupos'
    id_grupo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_grupo = db.Column(db.String(100), unique=True, nullable=False)
    descricao_grupo = db.Column(db.Text)
    foto_grupo = db.Column(db.String(255), default='url_padrao.jpg')
    criado_por = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    criado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    atualizado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class MembroGrupo(db.Model):
    __tablename__ = 'MembrosGrupo'
    id_membro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_grupo = db.Column(db.Integer, db.ForeignKey('Grupos.id_grupo'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    adicionado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    e_admin = db.Column(db.Boolean, default=False)
    papel = db.Column(db.Enum('admin', 'membro', 'moderador'), default='membro')
    db.UniqueConstraint('id_grupo', 'id_usuario')

class MensagemGrupo(db.Model):
    __tablename__ = 'MensagensGrupo'
    id_mensagem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_grupo = db.Column(db.Integer, db.ForeignKey('Grupos.id_grupo'), nullable=False, index=True)
    id_remetente = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False, index=True)
    mensagem = db.Column(db.Text, nullable=False)
    tipo_mensagem = db.Column(db.Enum('texto', 'imagem', 'video', 'arquivo'), nullable=False)
    enviado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    lida = db.Column(db.Boolean, default=False)

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

class ConfiguracaoUsuario(db.Model):
    __tablename__ = 'ConfiguracoesUsuario'
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), primary_key=True)
    tema = db.Column(db.Enum('claro', 'escuro'), default='claro')
    notificacoes_ativas = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    atualizado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class UsuarioBloqueado(db.Model):
    __tablename__ = 'UsuariosBloqueados'
    id_bloqueio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_bloqueador = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    id_bloqueado = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    bloqueado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    db.UniqueConstraint('id_bloqueador', 'id_bloqueado')
