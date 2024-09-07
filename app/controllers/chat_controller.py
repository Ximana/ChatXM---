
from flask import render_template, Blueprint, jsonify, session
from datetime import datetime, timedelta
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
@login_obrigatorio
def home():
    return render_template('home.html')
   
    
@chat_bp.route('/chat')
@login_obrigatorio
def chat():

    return render_template('chat.html')



@chat_bp.route('/conversas', methods=['GET'])
def listar_conversas():
    id_usuario_logado = session.get('id_usuario')
    
    # Filtra as conversas em que o usuário logado está envolvido
    conversas = db.session.query(ParticipanteConversa).filter(
        ParticipanteConversa.id_usuario == id_usuario_logado
    ).options(joinedload(ParticipanteConversa.conversa)).all()

    resultado = []
    
    for participante in conversas:
        # Buscar a última mensagem da conversa
        ultima_mensagem = db.session.query(Mensagem).filter(
            Mensagem.id_conversa == participante.conversa.id_conversa
        ).order_by(Mensagem.enviado_em.desc()).first()

        if ultima_mensagem:
            # Acessar o outro participante da conversa (excluindo o usuário logado)
            outro_participante = db.session.query(Usuario).join(ParticipanteConversa).filter(
                ParticipanteConversa.id_conversa == participante.conversa.id_conversa,
                ParticipanteConversa.id_usuario != id_usuario_logado
            ).first()

            if outro_participante:
                # Verificar se o outro participante está online
                tempo_agora = datetime.utcnow()
                usuario_online = False
                if outro_participante.ultimo_visto:
                    if tempo_agora - outro_participante.ultimo_visto >= timedelta(minutes=1):
                        usuario_online = True

                # Fatiar a mensagem para mostrar apenas os primeiros 10 caracteres
                mensagem_resumida = ultima_mensagem.mensagem[:10] + '...' if len(ultima_mensagem.mensagem) > 10 else ultima_mensagem.mensagem

                # Adicionar os dados da conversa à lista de resultados
                resultado.append({
                    'nome_usuario': outro_participante.nome_usuario,
                    'id_usuario': outro_participante.id_usuario,
                    'mensagem': mensagem_resumida,
                    'status': 'online' if usuario_online else 'offline',
                    'foto_perfil': outro_participante.foto_perfil,  # Supondo que você tenha um campo foto_perfil no modelo Usuario
                    'enviado_em': ultima_mensagem.enviado_em
                })

    return jsonify(resultado)


@chat_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuario_logado_id = session.get('id_usuario')  # Pegando o ID do usuário logado
    
    # Subconsulta para pegar os IDs dos usuários bloqueados pelo usuário logado
    subquery_bloqueados = db.session.query(UsuarioBloqueado.id_bloqueado).filter_by(id_bloqueador=usuario_logado_id)
    
    # Consulta para pegar todos os usuários, exceto os bloqueados e o usuário logado
    usuarios = Usuario.query.filter(
        Usuario.id_usuario.notin_(subquery_bloqueados),
        Usuario.id_usuario != usuario_logado_id
    ).all()
    
    # Construindo a lista de resultados
    resultado = []
    for usuario in usuarios:
        # Verifica se o usuário está online
        status = 'online' if usuario.status == 'online' else 'offline'
        
        # Adicionando os detalhes de cada usuário à lista de resultados
        resultado.append({
            'nome_usuario': usuario.nome_usuario,
            'id_usuario': usuario.id_usuario,
            'foto_perfil': usuario.foto_perfil,  # Supondo que a coluna foto_perfil exista
            'status': status
        })
    
    return jsonify(resultado)


@chat_bp.route('/bloqueados', methods=['GET'])
def listar_bloqueados():
    id_usuario_logado = session.get('id_usuario')
    
    bloqueados = UsuarioBloqueado.query.filter_by(id_bloqueador=id_usuario_logado).all()
    resultado = [{
        'nome_usuario': Usuario.query.get(bloqueado.id_bloqueado).nome_usuario,
        'id_usuario': Usuario.query.get(bloqueado.id_bloqueado).id_usuario,
        'foto_perfil': Usuario.query.get(bloqueado.id_bloqueado).foto_perfil
        } for bloqueado in bloqueados]
    
    return jsonify(resultado)


@chat_bp.route('/grupos', methods=['GET'])
def listar_grupos():
    id_usuario_logado = session.get('id_usuario')
    
    grupos = MembroGrupo.query.filter_by(id_usuario=id_usuario_logado).all()
    resultado = [{
        'nome_grupo': Grupo.query.get(grupo.id_grupo).nome_grupo,
        'id_grupo': Grupo.query.get(grupo.id_grupo).id_grupo,
        'foto_grupo': Grupo.query.get(grupo.id_grupo).foto_grupo
        } for grupo in grupos]
    
    return jsonify(resultado)