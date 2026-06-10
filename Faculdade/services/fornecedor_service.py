from extensions import db
from models import Fornecedor, Produto

class FornecedorService:
    @staticmethod
    def listar():
        return Fornecedor.query.order_by(Fornecedor.nome).all()

    @staticmethod
    def buscar(fid):
        return Fornecedor.query.get(fid)

    @staticmethod
    def criar(nome, contato, email, cnpj, localizacao):
        f = Fornecedor(nome=nome, contato=contato or None, email=email or None,
                       cnpj=cnpj or None, localizacao=localizacao or None)
        db.session.add(f); db.session.commit(); return f

    @staticmethod
    def atualizar(f, nome, contato, email, cnpj, localizacao):
        f.nome=nome; f.contato=contato or None; f.email=email or None
        f.cnpj=cnpj or None; f.localizacao=localizacao or None
        db.session.commit(); return f

    @staticmethod
    def excluir(f):
        Produto.query.filter_by(fornecedor_id=f.id).update({"fornecedor_id": None})
        db.session.delete(f); db.session.commit()
