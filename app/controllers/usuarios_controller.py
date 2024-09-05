
from flask import Blueprint, request, jsonify, make_response, render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid
import os
from app.models.usuario import Usuario, db
from datetime import datetime

from app.decorador import login_obrigatorio # decorador para secao obrigatoria


usuario_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Registro de novo usuário
@usuario_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':

        usuario = dict(request.form)

        # Verifica se o email ou numero de telefone já existe
        if Usuario.query.filter_by(email=usuario['email']).first() or Usuario.query.filter_by(numero_telefone=usuario['telefone']).first():
            
            flash('Email ou número de telefone já está em uso', 'danger')
            return redirect(url_for('usuarios.registrar'))
            #return "Email ou número de telefone já está em uso"
        
        # Fazer upload da imagem do usuario
        upload_folder = 'app/static/img/usuarios'
        imagem = request.files['imagem']

        if imagem:
            filename = secure_filename(imagem.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            nome_unico_imagem = f"{uuid.uuid4().hex}.{ext}"
            imagem.save(os.path.join(upload_folder, nome_unico_imagem))
        else:
            nome_unico_imagem = 'imagem_usuario_padrao.png'  # Imagem padrão caso nenhuma imagem seja enviada

        # Criar um novo usuário
        hashed_password = generate_password_hash(usuario['senha'])
        novo_usuario = Usuario(
            nome_usuario=usuario['nome'],
            email=usuario['email'],
            numero_telefone=usuario['telefone'],
            senha=hashed_password,
            foto_perfil=nome_unico_imagem,
            status='offline'
        )

        # Guardar na BD
        try:
            db.session.add(novo_usuario)
            db.session.commit()

            flash('Usuário registrado com sucesso!', 'success')
            return redirect(url_for('usuarios.login'))
            #return "Usuário registrado com sucesso!"

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar usuario: {str(e)}', 'danger')

    return render_template('signup.html')
    

# Login de usuário
@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        usuario = dict(request.form)
        usuario_resultado = Usuario.query.filter_by(email=usuario['email']).first() or Usuario.query.filter_by(numero_telefone=usuario['email']).first()

        if not usuario_resultado or not check_password_hash(usuario_resultado.senha, usuario['senha']):
            
            flash('Credenciais inválidas!', 'danger')
            return redirect(url_for('usuarios.login'))

        session['id_usuario'] = usuario_resultado.id_usuario
        session['nome_usuario'] = usuario_resultado.nome_usuario
        session['imagem_usuario'] = usuario_resultado.foto_perfil
        
        usuario_resultado.status = 'online'
        usuario_resultado.ultimo_visto = datetime.utcnow()
        db.session.commit()

        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('chat.home'))
        #return 'Login realizado com sucesso!'

    return render_template('login.html')
    

# Atualização do perfil do usuário
@usuario_bp.route('/update', methods=['POST'])
@login_obrigatorio
def update_usuario():
    usuario_id = session.get('id_usuario')
    usuario = Usuario.query.get(usuario_id)

    data = dict(request.form) #dados do usuario passado

    # Atualiza as informações do usuário
    if 'nome' in data:
        usuario.nome_usuario = data['nome']
    if 'email' in data:
        usuario.email = data['email']
    if 'telefone' in data:
        usuario.numero_telefone = data['telefone']
    if 'senha' in data:
        usuario.senha = generate_password_hash(data['senha'])
    if 'imagem' in data:
        usuario.foto_perfil = data['imagem']

    usuario.atualizado_em = datetime.utcnow()
    db.session.commit()

    flash('Perfil atualizado com sucesso!', 'success')
    return render_template('perfil.html', usuario=usuario)

    

# Visualizar informações do perfil
@usuario_bp.route('/perfil/<int:usuario_id>', methods=['GET'])
@login_obrigatorio
def ver_perfil(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        flash('Usuário não emcontrado!', 'warning')
        return redirect(url_for('chat.home'))

    return render_template('perfil.html', usuario=usuario)

# Excluir conta de usuário
@usuario_bp.route('/remover', methods=['POST'])
@login_obrigatorio
def remover_usuario():

    usuario_id = session.get('id_usuario')
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        flash('Usuário não emcontrado!', 'warning')
        return redirect(url_for('usuarios.ver_perfil'))

    db.session.delete(usuario)
    db.session.commit()

    flash('Conta excluída com sucesso!', 'success')
    return redirect(url_for('chat.index'))
    

# Sair e atualizar status do usuário
@usuario_bp.route('/logout', methods=['POST'])
@login_obrigatorio
def logout():

    usuario_id = session.get('id_usuario')

    if not usuario_id:
        flash('Usuário não está logado!', 'warning')
        return redirect(url_for('usuarios.login'))

    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        flash('Usuário não encontrado!', 'danger')
        return redirect(url_for('usuarios.login'))

    usuario.status = 'offline'
    usuario.ultimo_visto = datetime.utcnow()
    db.session.commit()

    # Limpar a sessão
    session.clear()

    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('usuarios.login'))
    

# Listar todos os usuários
@usuario_bp.route('/usuarios', methods=['GET'])
@login_obrigatorio
def listar_usuarios():
    
    return render_template('index.html')
   