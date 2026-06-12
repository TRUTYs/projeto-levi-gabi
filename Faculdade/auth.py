"""
Helpers de autenticação reutilizáveis.
"""

from functools import wraps
from flask import redirect, session, url_for, abort


def login_required(f):
    """Redireciona para /login se não houver sessão ativa."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Retorna 403 se o usuário não for admin."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        if session.get("usuario_tipo") != "admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated
