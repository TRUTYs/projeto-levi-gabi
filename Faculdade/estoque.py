from flask import Blueprint, flash, redirect, render_template, request, url_for
from auth import login_required
from models import Fornecedor
from services import EstoqueService

estoque_bp = Blueprint("estoque", __name__)

def _parse_form():
    nome    = request.form.get("nome","").strip()
    qtd_raw = request.form.get("quantidade","").strip()
    forn_id = request.form.get("fornecedor_id") or None
    if not nome or not qtd_raw:
        flash("Campos obrigatórios não preenchidos.", "erro"); return None
    try:
        quantidade  = int(qtd_raw)
        preco_venda = float(request.form.get("preco_venda") or 0)
        preco_custo = float(request.form.get("preco_custo") or 0)
    except ValueError:
        flash("Valores numéricos inválidos.", "erro"); return None
    if quantidade < 0 or preco_venda < 0 or preco_custo < 0:
        flash("Valores não podem ser negativos.", "erro"); return None
    return {"nome":nome,"categoria":request.form.get("categoria","").strip(),
            "quantidade":quantidade,"preco_venda":preco_venda,"preco_custo":preco_custo,
            "fornecedor_id":int(forn_id) if forn_id else None}

@estoque_bp.route("/estoque")
@login_required
def estoque():
    produtos = EstoqueService.listar_produtos()
    fornecedores = Fornecedor.query.order_by(Fornecedor.nome).all()
    lista = [{"id":p.id,"nome":p.nome,"quantidade":p.quantidade,"preco_venda":p.preco_venda,
              "preco_custo":p.preco_custo,"fornecedor_nome":p.fornecedor.nome if p.fornecedor else "Sem Fornecedor",
              "fornecedor_id":p.fornecedor_id,"categoria":p.categoria,"estoque_minimo":p.estoque_minimo}
             for p in produtos]
    return render_template("estoque.html", produtos=lista, fornecedores=fornecedores)

@estoque_bp.route("/adicionar_produto", methods=["POST"])
@login_required
def adicionar_produto():
    dados = _parse_form()
    if dados is None: return redirect(url_for("estoque.estoque"))
    ex = EstoqueService.produto_por_nome(dados["nome"])
    if ex:
        flash(f'__PRODUTO_EXISTENTE__|{ex.id}|{dados["nome"]}|{dados["quantidade"]}', "confirmacao_produto")
        return redirect(url_for("estoque.estoque"))
    p = EstoqueService.criar_produto(**dados)
    flash(f'Produto "{p.nome}" cadastrado!', "sucesso")
    return redirect(url_for("estoque.estoque"))

@estoque_bp.route("/confirmar_adicionar_produto/<int:produto_id>/<int:quantidade>")
@login_required
def confirmar_adicionar_produto(produto_id, quantidade):
    p = EstoqueService.buscar_produto(produto_id)
    if p:
        EstoqueService.adicionar_quantidade(p, quantidade)
        flash(f'{quantidade} unidade(s) adicionada(s) a "{p.nome}".', "sucesso")
    return redirect(url_for("estoque.estoque"))

@estoque_bp.route("/editar_produto/<int:produto_id>", methods=["POST"])
@login_required
def editar_produto(produto_id):
    p = EstoqueService.buscar_produto(produto_id)
    if not p: flash("Produto não encontrado.", "erro"); return redirect(url_for("estoque.estoque"))
    dados = _parse_form()
    if dados is None: return redirect(url_for("estoque.estoque"))
    EstoqueService.atualizar_produto(p, **dados)
    flash(f'Produto "{dados["nome"]}" atualizado!', "sucesso")
    return redirect(url_for("estoque.estoque"))

@estoque_bp.route("/excluir_produto/<int:produto_id>")
@login_required
def excluir_produto(produto_id):
    p = EstoqueService.buscar_produto(produto_id)
    if p:
        nome = p.nome; EstoqueService.excluir_produto(p)
        flash(f'Produto "{nome}" excluído.', "sucesso")
    return redirect(url_for("estoque.estoque"))

@estoque_bp.route("/vender_produto/<int:produto_id>", methods=["POST"])
@login_required
def vender_produto(produto_id):
    p = EstoqueService.buscar_produto(produto_id)
    if not p: flash("Produto não encontrado.", "erro"); return redirect(url_for("estoque.estoque"))
    try:
        qtd = int(request.form.get("quantidade",0))
        if qtd <= 0: raise ValueError("Quantidade deve ser maior que zero.")
        EstoqueService.registrar_venda(p, qtd)
        flash(f'Venda de {qtd}x "{p.nome}" realizada!', "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    return redirect(url_for("estoque.estoque"))

@estoque_bp.route("/comprar_produto/<int:produto_id>", methods=["POST"])
@login_required
def comprar_produto(produto_id):
    p = EstoqueService.buscar_produto(produto_id)
    if not p: flash("Produto não encontrado.", "erro"); return redirect(url_for("estoque.estoque"))
    try:
        qtd = int(request.form.get("quantidade",0))
        EstoqueService.registrar_compra(p, qtd)
        flash(f'Reposição de {qtd}x "{p.nome}" registrada!', "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    return redirect(url_for("estoque.estoque"))
