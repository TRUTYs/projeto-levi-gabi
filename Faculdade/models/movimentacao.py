from datetime import datetime
from extensions import db


class Movimentacao(db.Model):
    __tablename__ = "movimentacoes_estoque"
    id                = db.Column(db.Integer, primary_key=True)
    produto_id        = db.Column(db.Integer, db.ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)
    tipo              = db.Column(db.Enum("entrada", "saida"), nullable=False)
    quantidade        = db.Column(db.Integer, nullable=False)
    origem            = db.Column(db.Enum("compra", "venda", "ajuste"), nullable=False)
    valor_unitario    = db.Column(db.Numeric(10, 2))
    custo_unitario    = db.Column(db.Numeric(10, 2))
    # Usa datetime.now() sem fuso — consistente com os filtros do dashboard
    data_movimentacao = db.Column(db.DateTime, default=datetime.now, nullable=False)
