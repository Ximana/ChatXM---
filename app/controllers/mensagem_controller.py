from flask import Blueprint, jsonify, request, session
from app.models.conversa import Conversa
from app.models.mensagem import Mensagem
from app.models.usuario import Usuario
from app.models.participante_conversa import ParticipanteConversa
from app.models.grupo import Grupo
from app.models.mensagem_grupo import MensagemGrupo
from app.models.membro_grupo import MembroGrupo
from app import db
import logging

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

@mensagem_bp.route('/carregar_todas_mensagens_grupo/<int:id_grupo>', methods=['GET'])
def carregar_todas_mensagens_grupo(id_grupo):
    id_usuario_logado = session.get('id_usuario')
    
    # Verificar se o usuário logado faz parte do grupo
    membro = MembroGrupo.query.filter_by(id_grupo=id_grupo, id_usuario=id_usuario_logado).first()
    if not membro:
        return jsonify({'erro': 'Usuário não faz parte deste grupo'}), 403
    
    # Carregar todas as mensagens do grupo
    mensagens = MensagemGrupo.query.filter_by(id_grupo=id_grupo).order_by(MensagemGrupo.enviado_em).all()
    
    mensagens_formatadas = [{
        'id_mensagem_grupo': msg.id_mensagem_grupo,
        'id_remetente': msg.id_remetente,
        'mensagem': msg.mensagem,
        'tipo_mensagem': msg.tipo_mensagem,
        'enviado_em': msg.enviado_em.strftime('%Y-%m-%d %H:%M:%S'),
        'lida': msg.lida,
        'foto_perfil': Usuario.query.get(msg.id_remetente).foto_perfil
    } for msg in mensagens]
    
    grupo = Grupo.query.get(id_grupo)
    
    return jsonify({
        'id_grupo': grupo.id_grupo,
        'nome_grupo': grupo.nome_grupo,
        'descricao_grupo': grupo.descricao_grupo,
        'foto_grupo': grupo.foto_grupo,
        'criado_por': grupo.criado_por,
        'criado_em': grupo.criado_em.strftime('%Y-%m-%d %H:%M:%S'),
        'atualizado_em': grupo.atualizado_em.strftime('%Y-%m-%d %H:%M:%S'),
        'mensagens': mensagens_formatadas
    })

@mensagem_bp.route('/atualizar_mensagens_grupo/<int:id_grupo>/<int:ultima_mensagem_id>', methods=['GET'])
def atualizar_mensagens_grupo(id_grupo, ultima_mensagem_id):
    novas_mensagens = MensagemGrupo.query.filter(
        MensagemGrupo.id_grupo == id_grupo,
        MensagemGrupo.id_mensagem_grupo > ultima_mensagem_id
    ).order_by(MensagemGrupo.enviado_em).all()

    mensagens_formatadas = [{
        'id_mensagem_grupo': msg.id_mensagem_grupo,
        'id_remetente': msg.id_remetente,
        'nome_remetente': Usuario.query.get(msg.id_remetente).nome_usuario,
        'mensagem': msg.mensagem,
        'enviado_em': msg.enviado_em.strftime('%Y-%m-%d %H:%M:%S'),
        'foto_perfil': Usuario.query.get(msg.id_remetente).foto_perfil
    } for msg in novas_mensagens]

    return jsonify({'novas_mensagens': mensagens_formatadas})

@mensagem_bp.route('/carregar_mensagens_grupo/<int:id_grupo>', methods=['GET'])
def carregar_mensagens_grupo(id_grupo):
    logging.info(f'Recebida solicitação para carregar mensagens do grupo {id_grupo}')
    id_usuario_logado = session.get('id_usuario')
    
    logging.info(f'Usuário logado: {id_usuario_logado}')
    
    # Verificar se o usuário é membro do grupo
    membro = MembroGrupo.query.filter_by(id_grupo=id_grupo, id_usuario=id_usuario_logado).first()
    if not membro:
        logging.warning(f'Usuário {id_usuario_logado} não é membro do grupo {id_grupo}')
        return jsonify({'erro': 'Usuário não é membro deste grupo'}), 403
    
    grupo = Grupo.query.get(id_grupo)
    mensagens = MensagemGrupo.query.filter_by(id_grupo=id_grupo).order_by(MensagemGrupo.enviado_em).all()
    
    logging.info(f'Encontradas {len(mensagens)} mensagens para o grupo {id_grupo}')
    
    mensagens_formatadas = [{
        'id_mensagem_grupo': msg.id_mensagem_grupo,
        'id_remetente': msg.id_remetente,
        'nome_remetente': Usuario.query.get(msg.id_remetente).nome_usuario,
        'mensagem': msg.mensagem,
        'enviado_em': msg.enviado_em.isoformat(),
        'foto_perfil': Usuario.query.get(msg.id_remetente).foto_perfil
    } for msg in mensagens]
    
    resposta = {
        'id_grupo': grupo.id_grupo,
        'nome_grupo': grupo.nome_grupo,
        'foto_grupo': grupo.foto_grupo,
        'membros_count': MembroGrupo.query.filter_by(id_grupo=id_grupo).count(),
        'mensagens': mensagens_formatadas
    }
    
    logging.info(f'Retornando resposta para o grupo {id_grupo}')
    return jsonify(resposta)