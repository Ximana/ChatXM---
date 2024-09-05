
from flask import render_template, Blueprint

from app.decorador import login_obrigatorio # decorador para secao obrigatoria


chat_bp = Blueprint('chat', __name__, url_prefix='/')

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

'''
@chat_bp.route('/sobre')
def sobre():
    return render_template('sobre.html')


@chat_bp.route('/ajuda')
def ajuda():
    return render_template('ajuda.html')

'''