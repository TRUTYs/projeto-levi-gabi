from extensions import db
from models import Produto, Movimentacao

class EstoqueService:
    @staticmethod
    def listar_produtos():
        return Produto.query.order_by(Produto.nome).all()

    @staticmethod
    def buscar_produto(pid):
        return Produto.query.get(pid)

    @staticmethod
    def produto_por_nome(nome):
        return Produto.query.filter_by(nome=nome).first()

    @staticmethod
    def criar_produto(nome, categoria, quantidade, preco_venda, preco_custo, fornecedor_id):
        p = Produto(nome=nome, categoria=categoria, quantidade=quantidade,
                    preco_venda=preco_venda, preco_custo=preco_custo, fornecedor_id=fornecedor_id)
        db.session.add(p)
        db.session.commit()
        return p

    @staticmethod
    def atualizar_produto(p, nome, categoria, quantidade, preco_venda, preco_custo, fornecedor_id):
        p.nome=nome; p.categoria=categoria; p.quantidade=quantidade
        p.preco_venda=preco_venda; p.preco_custo=preco_custo; p.fornecedor_id=fornecedor_id
        db.session.commit()
        return p

    @staticmethod
    def excluir_produto(p):
        db.session.delete(p); db.session.commit()

    @staticmethod
    def adicionar_quantidade(p, qtd):
        p.quantidade += qtd; db.session.commit(); return p

    @staticmethod
    def alertas_estoque():
        return Produto.query.filter(Produto.quantidade <= Produto.estoque_minimo).all()

    @staticmethod
    def registrar_venda(p, qtd):
        if p.quantidade < qtd:
            raise ValueError(f"Estoque insuficiente: disponível {p.quantidade}, solicitado {qtd}.")
        mov = Movimentacao(produto_id=p.id, tipo="saida", quantidade=qtd, origem="venda",
                           valor_unitario=p.preco_venda, custo_unitario=p.preco_custo)
        p.quantidade -= qtd
        db.session.add(mov); db.session.commit(); return mov

    @staticmethod
    def registrar_compra(p, qtd):
        if qtd <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        mov = Movimentacao(produto_id=p.id, tipo="entrada", quantidade=qtd, origem="compra",
                           valor_unitario=p.preco_custo, custo_unitario=p.preco_custo)
        p.quantidade += qtd
        db.session.add(mov); db.session.commit(); return mov
