from werkzeug.security import check_password_hash
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from models import Usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if "usuario_id" in session:
        return redirect(url_for("dashboard.index"))
    if request.method == "POST":
        nome  = request.form.get("username","").strip()
        senha = request.form.get("password","").strip()
        if not nome or not senha:
            flash("Preencha todos os campos.", "erro")
            return render_template("login.html")
        usuario = Usuario.query.filter_by(nome=nome).first()
        if usuario and not check_password_hash(usuario.senha, senha):
            usuario = None
        if usuario:
            session["usuario_id"]   = usuario.id
            session["usuario_nome"] = usuario.nome
            session["usuario_tipo"] = usuario.tipo
            return redirect(url_for("dashboard.index"))
        flash("Usuário ou senha inválidos.", "erro")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth_bp.route("/alterar_senha", methods=["POST"])
def alterar_senha():
    from werkzeug.security import generate_password_hash, check_password_hash
    from extensions import db
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    usuario  = Usuario.query.get(session["usuario_id"])
    atual    = request.form.get("senha_atual", "")
    nova     = request.form.get("senha_nova", "")
    confirma = request.form.get("senha_confirma", "")

    if not check_password_hash(usuario.senha, atual):
        flash("Senha atual incorreta.", "erro")
    elif len(nova) < 6:
        flash("A nova senha deve ter pelo menos 6 caracteres.", "erro")
    elif nova != confirma:
        flash("As senhas não coincidem.", "erro")
    else:
        usuario.senha = generate_password_hash(nova)
        db.session.commit()
        flash("Senha alterada com sucesso!", "sucesso")

    return redirect(url_for("dashboard.index"))
