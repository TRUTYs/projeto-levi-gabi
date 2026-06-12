from flask import Blueprint, flash, redirect, render_template, request, url_for
from auth import login_required
from services import FornecedorService

fornecedores_bp = Blueprint("fornecedores", __name__)

def _campos():
    return {k: request.form.get(v,"").strip() for k,v in [
        ("nome","nome_fornecedor"),("contato","contato_fornecedor"),
        ("email","email_fornecedor"),("cnpj","cnpj_fornecedor"),("localizacao","localizacao_fornecedor")]}

@fornecedores_bp.route("/fornecedores")
@login_required
def fornecedores():
    return render_template("fornecedores.html", fornecedores=FornecedorService.listar())

@fornecedores_bp.route("/cadastrar_fornecedor", methods=["POST"])
@login_required
def cadastrar_fornecedor():
    d = _campos()
    if not d["nome"]:
        flash("Nome obrigatório.", "erro")
        return redirect(url_for("fornecedores.fornecedores"))
    FornecedorService.criar(**d)
    flash(f'Fornecedor "{d["nome"]}" cadastrado!', "sucesso")
    return redirect(url_for("fornecedores.fornecedores"))

@fornecedores_bp.route("/editar_fornecedor/<int:fid>", methods=["POST"])
@login_required
def editar_fornecedor(fid):
    f = FornecedorService.buscar(fid)
    if not f:
        flash("Fornecedor não encontrado.", "erro")
        return redirect(url_for("fornecedores.fornecedores"))
    FornecedorService.atualizar(f, **_campos())
    flash(f'Fornecedor "{f.nome}" atualizado!', "sucesso")
    return redirect(url_for("fornecedores.fornecedores"))

@fornecedores_bp.route("/excluir_fornecedor/<int:fid>")
@login_required
def excluir_fornecedor(fid):
    f = FornecedorService.buscar(fid)
    if f:
        nome = f.nome; FornecedorService.excluir(f)
        flash(f'Fornecedor "{nome}" excluído.', "sucesso")
    return redirect(url_for("fornecedores.fornecedores"))
