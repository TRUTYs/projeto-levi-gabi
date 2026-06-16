"""
Serviço de Usuários — cadastro, edição e exclusão.
Apenas admins podem gerenciar usuários.
"""

from werkzeug.security import generate_password_hash
from extensions import db
from models.usuario import Usuario


class UsuarioService:

    @staticmethod
    def listar() -> list[Usuario]:
        return Usuario.query.order_by(Usuario.id).all()

    @staticmethod
    def buscar(uid: int) -> Usuario | None:
        return Usuario.query.get(uid)

    @staticmethod
    def nome_disponivel(nome: str, excluir_id: int | None = None) -> bool:
        q = Usuario.query.filter_by(nome=nome)
        if excluir_id:
            q = q.filter(Usuario.id != excluir_id)
        return q.first() is None

    @staticmethod
    def criar(nome: str, email: str, senha: str, tipo: str) -> Usuario:
        u = Usuario(
            nome=nome,
            email=email or None,
            senha=generate_password_hash(senha),
            tipo=tipo,
        )
        db.session.add(u)
        db.session.commit()
        return u

    @staticmethod
    def atualizar(u: Usuario, nome: str, email: str, tipo: str) -> Usuario:
        u.nome  = nome
        u.email = email or None
        u.tipo  = tipo
        db.session.commit()
        return u

    @staticmethod
    def alterar_senha(u: Usuario, nova_senha: str) -> None:
        u.senha = generate_password_hash(nova_senha)
        db.session.commit()

    @staticmethod
    def excluir(u: Usuario) -> None:
        db.session.delete(u)
        db.session.commit()
