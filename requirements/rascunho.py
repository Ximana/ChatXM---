from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import Usuario, db
from datetime import datetime

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

# Registro de novo usuário
@usuario_bp.route('/register', methods=['POST'])
def register_usuario():
    data = request.get_json()

    # Verifica se o email ou nome de usuário já existe
    if Usuario.query.filter_by(email=data['email']).first() or Usuario.query.filter_by(nome_usuario=data['nome_usuario']).first():
        return make_response(jsonify({'message': 'Email ou nome de usuário já está em uso.'}), 409)

    # Cria um novo usuário
    hashed_password = generate_password_hash(data['senha'], method='sha256')
    novo_usuario = Usuario(
        nome_usuario=data['nome_usuario'],
        email=data['email'],
        senha=hashed_password,
        status='offline'
    )
    db.session.add(novo_usuario)
    db.session.commit()

    return make_response(jsonify({'message': 'Usuário registrado com sucesso!'}), 201)

# Login de usuário
@usuario_bp.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()

    usuario = Usuario.query.filter_by(email=data['email']).first()

    if not usuario or not check_password_hash(usuario.senha, data['senha']):
        return make_response(jsonify({'message': 'Credenciais inválidas!'}), 401)

    access_token = create_access_token(identity=usuario.id_usuario)
    usuario.status = 'online'
    usuario.ultimo_visto = datetime.utcnow()
    db.session.commit()

    return make_response(jsonify({'access_token': access_token, 'message': 'Login realizado com sucesso!'}), 200)

# Atualização do perfil do usuário
@usuario_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_usuario():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    data = request.get_json()

    # Atualiza as informações do usuário
    if 'nome_usuario' in data:
        usuario.nome_usuario = data['nome_usuario']
    if 'email' in data:
        usuario.email = data['email']
    if 'senha' in data:
        usuario.senha = generate_password_hash(data['senha'], method='sha256')
    if 'foto_perfil' in data:
        usuario.foto_perfil = data['foto_perfil']

    usuario.atualizado_em = datetime.utcnow()
    db.session.commit()

    return make_response(jsonify({'message': 'Perfil atualizado com sucesso!'}), 200)

# Visualizar informações do perfil
@usuario_bp.route('/profile', methods=['GET'])
@jwt_required()
def view_profile():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return make_response(jsonify({'message': 'Usuário não encontrado!'}), 404)

    user_data = {
        'nome_usuario': usuario.nome_usuario,
        'email': usuario.email,
        'foto_perfil': usuario.foto_perfil,
        'status': usuario.status,
        'ultimo_visto': usuario.ultimo_visto,
        'criado_em': usuario.criado_em,
        'atualizado_em': usuario.atualizado_em
    }

    return make_response(jsonify(user_data), 200)

# Listar todos os usuários
@usuario_bp.route('/users', methods=['GET'])
@jwt_required()
def list_usuarios():
    usuarios = Usuario.query.all()
    output = []

    for usuario in usuarios:
        usuario_data = {
            'id_usuario': usuario.id_usuario,
            'nome_usuario': usuario.nome_usuario,
            'email': usuario.email,
            'status': usuario.status,
            'ultimo_visto': usuario.ultimo_visto
        }
        output.append(usuario_data)

    return make_response(jsonify(output), 200)

# Excluir conta de usuário
@usuario_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_usuario():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return make_response(jsonify({'message': 'Usuário não encontrado!'}), 404)

    db.session.delete(usuario)
    db.session.commit()

    return make_response(jsonify({'message': 'Conta excluída com sucesso!'}), 200)

# Sair e atualizar status do usuário
@usuario_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout_usuario():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return make_response(jsonify({'message': 'Usuário não encontrado!'}), 404)

    usuario.status = 'offline'
    usuario.ultimo_visto = datetime.utcnow()
    db.session.commit()

    return make_response(jsonify({'message': 'Logout realizado com sucesso!'}), 200)








# Adicione esta linha se não estiver presente
sqlalchemy.url = mysql+pymysql://ximana:ximana@localhost/chatxm