"""
Rotas de Configurações:
  - /configuracoes          → listagem de usuários (admin only)
  - /configuracoes/criar    → cadastrar novo usuário (admin only)
  - /configuracoes/editar   → editar nome/email/tipo (admin only)
  - /configuracoes/excluir  → excluir usuário (admin only)
  - /configuracoes/senha    → qualquer usuário altera a própria senha
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from auth import admin_required, login_required
from extensions import db
from models.usuario import Usuario
from services.usuario_service import UsuarioService

configuracoes_bp = Blueprint("configuracoes", __name__)


# ── Página principal (admin) ─────────────────────────────────

@configuracoes_bp.route("/configuracoes")
@admin_required
def configuracoes():
    return render_template("configuracoes.html", usuarios=UsuarioService.listar())


# ── Cadastrar usuário (admin) ────────────────────────────────

@configuracoes_bp.route("/configuracoes/criar", methods=["POST"])
@admin_required
def criar_usuario():
    nome    = request.form.get("nome", "").strip()
    email   = request.form.get("email", "").strip()
    senha   = request.form.get("senha", "").strip()
    confirma = request.form.get("confirma", "").strip()
    tipo    = request.form.get("tipo", "vendedor")

    if not nome or not senha:
        flash("Nome e senha são obrigatórios.", "erro")
        return redirect(url_for("configuracoes.configuracoes"))

    if not UsuarioService.nome_disponivel(nome):
        flash(f'O nome de usuário "{nome}" já está em uso.', "erro")
        return redirect(url_for("configuracoes.configuracoes"))

    if len(senha) < 6:
        flash("A senha deve ter pelo menos 6 caracteres.", "erro")
        return redirect(url_for("configuracoes.configuracoes"))

    if senha != confirma:
        flash("As senhas não coincidem.", "erro")
        return redirect(url_for("configuracoes.configuracoes"))

    if tipo not in ("admin", "vendedor"):
        tipo = "vendedor"

    u = UsuarioService.criar(nome, email, senha, tipo)
    flash(f'Usuário "{u.nome}" criado com sucesso!', "sucesso")
    return redirect(url_for("configuracoes.configuracoes"))


# ── Editar usuário (admin) ───────────────────────────────────

@configuracoes_bp.route("/configuracoes/editar/<int:uid>", methods=["POST"])
@admin_required
def editar_usuario(uid):
    u = UsuarioService.buscar(uid)
    if not u:
        flash("Usuário não encontrado.", "erro")
        return redirect(url_for("configuracoes.configuracoes"))

    nome  = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    tipo  = request.form.get("tipo", "vendedor")

    if not nome:
        flash("Nome é obrigatório.", "erro")
        return redirect(url_for("configuracoes.configuracoes"))

    if not UsuarioService.nome_disponivel(nome, excluir_id=uid):
        flash(f'O nome de usuário "{nome}" já está em uso.', "erro")
        return redirect(url_for("configuracoes.configuracoes"))

    # Admin não pode rebaixar a si mesmo
    if uid == session["usuario_id"] and tipo != "admin":
        flash("Você não pode alterar o seu próprio tipo de acesso.", "erro")
        return redirect(url_for("configuracoes.configuracoes"))

    UsuarioService.atualizar(u, nome, email, tipo)
    flash(f'Usuário "{u.nome}" atualizado!', "sucesso")
    return redirect(url_for("configuracoes.configuracoes"))


# ── Excluir usuário (admin) ──────────────────────────────────

@configuracoes_bp.route("/configuracoes/excluir/<int:uid>")
@admin_required
def excluir_usuario(uid):
    if uid == session["usuario_id"]:
        flash("Você não pode excluir a sua própria conta.", "erro")
        return redirect(url_for("configuracoes.configuracoes"))

    u = UsuarioService.buscar(uid)
    if u:
        nome = u.nome
        UsuarioService.excluir(u)
        flash(f'Usuário "{nome}" excluído.', "sucesso")

    return redirect(url_for("configuracoes.configuracoes"))


# ── Alterar senha (qualquer usuário logado) ──────────────────

@configuracoes_bp.route("/configuracoes/senha", methods=["POST"])
@login_required
def alterar_senha():
    u        = UsuarioService.buscar(session["usuario_id"])
    atual    = request.form.get("senha_atual", "")
    nova     = request.form.get("senha_nova", "")
    confirma = request.form.get("senha_confirma", "")

    if not check_password_hash(u.senha, atual):
        flash("Senha atual incorreta.", "erro")
    elif len(nova) < 6:
        flash("A nova senha deve ter pelo menos 6 caracteres.", "erro")
    elif nova != confirma:
        flash("As senhas não coincidem.", "erro")
    else:
        UsuarioService.alterar_senha(u, nova)
        flash("Senha alterada com sucesso!", "sucesso")

    # Admin volta para configurações, vendedor volta para o dashboard
    if session.get("usuario_tipo") == "admin":
        return redirect(url_for("configuracoes.configuracoes"))
    return redirect(url_for("dashboard.index"))


# ── Página de senha para vendedores ─────────────────────────

@configuracoes_bp.route("/minha-senha")
@login_required
def minha_senha():
    return render_template("minha_senha.html")
