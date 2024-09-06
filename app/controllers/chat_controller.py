
from flask import render_template, Blueprint, jsonify, session

from app.models.usuario import Usuario, db
from app.models.participante_conversa import ParticipanteConversa, db
from app.models.conversa import Conversa, db
from app.models.mensagem import Mensagem, db
from app.models.usuario_bloqueado import UsuarioBloqueado, db
from app.models.grupo import Grupo, db
from app.models.membro_grupo import MembroGrupo, db

from sqlalchemy.orm import joinedload


from app.decorador import login_obrigatorio # decorador para secao obrigatoria


chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/')
def index():
    return render_template('index.html')

@chat_bp.route('/home')
def home():
    return render_template('home.html')
   
    
@chat_bp.route('/chat')
@login_obrigatorio
def chat():

    return render_template('chat.html')



@chat_bp.route('/conversas', methods=['GET'])
def listar_conversas():
    id_usuario_logado = session.get('id_usuario')
    
    conversas = db.session.query(ParticipanteConversa).filter(
        ParticipanteConversa.id_usuario == id_usuario_logado
    ).options(joinedload(ParticipanteConversa.conversa)).all()

    resultado = []
    for participante in conversas:
        ultima_mensagem = db.session.query(Mensagem).filter(
            Mensagem.id_conversa == participante.conversa.id_conversa
        ).order_by(Mensagem.enviado_em.desc()).first()

        if ultima_mensagem:
            usuario_remetente = Usuario.query.get(ultima_mensagem.id_remetente)
            resultado.append({
                'nome_usuario': usuario_remetente.nome_usuario,
                'mensagem': ultima_mensagem.mensagem,
                'enviado_em': ultima_mensagem.enviado_em
            })

    return jsonify(resultado)


@chat_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuario_logado_id = session.get('id_usuario')  # Pegando o ID do usuário logado
    
    # Subconsulta para pegar os IDs dos usuários bloqueados pelo usuário logado
    subquery_bloqueados = db.session.query(UsuarioBloqueado.id_bloqueado).filter_by(id_bloqueador=usuario_logado_id)
    
    
    # Consulta para pegar todos os usuários, exceto os que estão na subquery de bloqueados
    usuarios = Usuario.query.filter(Usuario.id_usuario.notin_(subquery_bloqueados)).all()
    
    # Retornando apenas os nomes dos usuários
    resultado = [{'nome_usuario': usuario.nome_usuario} for usuario in usuarios]
    return jsonify(resultado)


@chat_bp.route('/bloqueados', methods=['GET'])
def listar_bloqueados():
    id_usuario_logado = session.get('id_usuario')
    
    bloqueados = UsuarioBloqueado.query.filter_by(id_bloqueador=id_usuario_logado).all()
    resultado = [{'nome_usuario': Usuario.query.get(bloqueado.id_bloqueado).nome_usuario} for bloqueado in bloqueados]
    
    return jsonify(resultado)


@chat_bp.route('/grupos', methods=['GET'])
def listar_grupos():
    id_usuario_logado = session.get('id_usuario')
    
    grupos = MembroGrupo.query.filter_by(id_usuario=id_usuario_logado).all()
    resultado = [{'nome_grupo': Grupo.query.get(grupo.id_grupo).nome_grupo} for grupo in grupos]
    
    return jsonify(resultado)