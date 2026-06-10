import pytz
from datetime import datetime
from extensions import db

def _agora_sp():
    tz = pytz.timezone("America/Sao_Paulo")
    return datetime.now(pytz.utc).astimezone(tz).replace(tzinfo=None)

class Movimentacao(db.Model):
    __tablename__ = "movimentacoes_estoque"
    id                = db.Column(db.Integer, primary_key=True)
    produto_id        = db.Column(db.Integer, db.ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)
    tipo              = db.Column(db.Enum("entrada","saida"), nullable=False)
    quantidade        = db.Column(db.Integer, nullable=False)
    origem            = db.Column(db.Enum("compra","venda","ajuste"), nullable=False)
    valor_unitario    = db.Column(db.Numeric(10,2))
    custo_unitario    = db.Column(db.Numeric(10,2))
    data_movimentacao = db.Column(db.DateTime, default=_agora_sp, nullable=False)
