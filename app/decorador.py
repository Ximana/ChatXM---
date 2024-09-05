from functools import wraps
from flask import session, redirect, url_for, flash

def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_usuario' not in session:
            flash('Faça login para acessar o ChatXm.', 'warning')
            return redirect(url_for('usuarios.login'))
        return f(*args, **kwargs)
    return decorated_function
