from extensions import db
class Fornecedor(db.Model):
    __tablename__ = "fornecedores"
    id          = db.Column(db.Integer, primary_key=True)
    nome        = db.Column(db.String(100), nullable=False)
    contato     = db.Column(db.String(50))
    email       = db.Column(db.String(100))
    cnpj        = db.Column(db.String(18))
    localizacao = db.Column(db.String(200))
    produtos = db.relationship("Produto", backref="fornecedor", lazy=True)
