from flask import Flask, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config


#importar outros arquivos
from app.decorador import login_obrigatorio

db = SQLAlchemy()
migrate = Migrate()

# Importar os modelos
from app.models import usuario, mensagem, conversa, configuracao_usuario, grupo, membro_grupo, mensagem_grupo, notificacao, participante_conversa, usuario_bloqueado

# Importar os controladores
from .controllers.chat_controller import chat_bp
from .controllers.usuarios_controller import usuario_bp
from .controllers.mensagem_controller import mensagem_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)

    #Registrar os blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(mensagem_bp)

    return app