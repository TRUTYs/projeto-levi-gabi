from extensions import db
class Produto(db.Model):
    __tablename__ = "produtos"
    id             = db.Column(db.Integer, primary_key=True)
    nome           = db.Column(db.String(100), nullable=False)
    categoria      = db.Column(db.String(50))
    quantidade     = db.Column(db.Integer, default=0, nullable=False)
    estoque_minimo = db.Column(db.Integer, default=5, nullable=False)
    preco_custo    = db.Column(db.Numeric(10,2))
    preco_venda    = db.Column(db.Numeric(10,2))
    descricao      = db.Column(db.Text)
    fornecedor_id  = db.Column(db.Integer, db.ForeignKey("fornecedores.id"))
    movimentacoes  = db.relationship("Movimentacao", backref="produto", lazy=True, cascade="all, delete-orphan")

    @property
    def estoque_baixo(self):
        return self.quantidade <= self.estoque_minimo
