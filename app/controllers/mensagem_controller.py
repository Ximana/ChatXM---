from flask import Blueprint, jsonify, request, session
from app.models.conversa import Conversa
from app.models.mensagem import Mensagem
from app.models.usuario import Usuario
from app.models.participante_conversa import ParticipanteConversa
from app import db

mensagem_bp = Blueprint('mensagem', __name__)

@mensagem_bp.route('/carregar_conversa/<int:id_usuario>', methods=['GET'])
def carregar_conversa(id_usuario):
    id_usuario_logado = session.get('id_usuario')

    # Buscar dados do usuário da conversa
    usuario_conversa = Usuario.query.get(id_usuario)
    
    # Verificar se já existe uma conversa entre os usuários
    conversa = db.session.query(Conversa).join(ParticipanteConversa).filter(
        ParticipanteConversa.id_usuario.in_([id_usuario_logado, id_usuario])
    ).group_by(Conversa.id_conversa).having(db.func.count(ParticipanteConversa.id_usuario) == 2).first()

    if not conversa:
        # Se não existir, criar uma nova conversa
        conversa = Conversa()
        db.session.add(conversa)
        db.session.flush()  # Para obter o id_conversa

        # Adicionar os participantes
        participante1 = ParticipanteConversa(id_conversa=conversa.id_conversa, id_usuario=id_usuario_logado)
        participante2 = ParticipanteConversa(id_conversa=conversa.id_conversa, id_usuario=id_usuario)
        db.session.add_all([participante1, participante2])
        db.session.commit()

    # Carregar as mensagens da conversa
    mensagens = Mensagem.query.filter_by(id_conversa=conversa.id_conversa).order_by(Mensagem.enviado_em).all()

    mensagens_formatadas = [{
        'id_remetente': msg.id_remetente,
        'mensagem': msg.mensagem,
        'enviado_em': msg.enviado_em.strftime('%Y-%m-%d %H:%M:%S'),
        'foto_perfil': Usuario.query.get(msg.id_remetente).foto_perfil  # Adicionando a foto de perfil
    } for msg in mensagens]

    return jsonify({
        'id_conversa': conversa.id_conversa,
        'mensagens': mensagens_formatadas,
        'usuario_conversa': {
            'nome': usuario_conversa.nome_usuario,
            'status': usuario_conversa.status,
            'foto_perfil': usuario_conversa.foto_perfil,
            'id_usuario': usuario_conversa.id_usuario
        }
    })

@mensagem_bp.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    dados = request.json
    id_conversa = dados.get('id_conversa')
    mensagem_texto = dados.get('mensagem')
    id_remetente = session.get('id_usuario')

    nova_mensagem = Mensagem(
        id_conversa=id_conversa,
        id_remetente=id_remetente,
        mensagem=mensagem_texto
    )
    db.session.add(nova_mensagem)
    db.session.commit()

    usuario = Usuario.query.get(id_remetente)

    return jsonify({
        'status': 'success',
        'mensagem': {
            'id_remetente': nova_mensagem.id_remetente,
            'mensagem': nova_mensagem.mensagem,
            'enviado_em': nova_mensagem.enviado_em.strftime('%Y-%m-%d %H:%M:%S'),
            'foto_perfil': usuario.foto_perfil
        }
    })


@mensagem_bp.route('/carregar_novas_mensagens/<int:id_conversa>/<int:ultima_mensagem_id>', methods=['GET'])
def carregar_novas_mensagens(id_conversa, ultima_mensagem_id):
    novas_mensagens = Mensagem.query.filter(
        Mensagem.id_conversa == id_conversa,
        Mensagem.id_mensagem > ultima_mensagem_id
    ).order_by(Mensagem.enviado_em).all()

    mensagens_formatadas = [{
        'id_mensagem': msg.id_mensagem,
        'id_remetente': msg.id_remetente,
        'mensagem': msg.mensagem,
        'enviado_em': msg.enviado_em.strftime('%Y-%m-%d %H:%M:%S'),
        'foto_perfil': Usuario.query.get(msg.id_remetente).foto_perfil
    } for msg in novas_mensagens]

    return jsonify({
        'mensagens': mensagens_formatadas
    })
