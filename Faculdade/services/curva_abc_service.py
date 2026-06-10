"""
Serviço de Curva ABC.

Classificação baseada em receita acumulada de vendas:
  Classe A — primeiros 80 % da receita total  (poucos produtos, alto impacto)
  Classe B — 80 % a 95 %                      (importância intermediária)
  Classe C — 95 % a 100 %                     (muitos produtos, baixo impacto)

O período de análise é configurável via filtro (mesmo padrão do módulo Movimento).
"""

from datetime import datetime, timedelta
from sqlalchemy import func
from extensions import db
from models import Movimentacao, Produto

FILTROS_DELTA = {
    "mensal":     timedelta(days=30),
    "trimestral": timedelta(days=90),
    "semestral":  timedelta(days=180),
    "anual":      timedelta(days=365),
}

LIMITES = {"A": 0.80, "B": 0.95, "C": 1.00}


class CurvaABCService:

    @staticmethod
    def calcular(filtro: str = "trimestral") -> dict:
        delta       = FILTROS_DELTA.get(filtro, FILTROS_DELTA["trimestral"])
        data_inicio = datetime.now() - delta

        # Receita por produto no período
        rows = (
            db.session.query(
                Produto.id,
                Produto.nome,
                Produto.categoria,
                func.sum(Movimentacao.quantidade).label("qtd_vendida"),
                func.sum(Movimentacao.quantidade * Movimentacao.valor_unitario).label("receita"),
            )
            .join(Movimentacao, Movimentacao.produto_id == Produto.id)
            .filter(
                Movimentacao.tipo == "saida",
                Movimentacao.origem == "venda",
                Movimentacao.data_movimentacao >= data_inicio,
            )
            .group_by(Produto.id)
            .order_by(func.sum(Movimentacao.quantidade * Movimentacao.valor_unitario).desc())
            .all()
        )

        if not rows:
            return {
                "itens": [], "filtro": filtro,
                "totais": {"A": 0, "B": 0, "C": 0},
                "receita_total": 0,
            }

        receita_total = float(sum(r.receita or 0 for r in rows)) or 1.0
        acumulado = 0.0
        itens = []

        for rank, r in enumerate(rows, start=1):
            receita_item = float(r.receita or 0)
            acumulado   += receita_item
            pct_item     = receita_item / receita_total * 100
            pct_acum     = acumulado / receita_total * 100

            if pct_acum <= LIMITES["A"] * 100:
                classe = "A"
            elif pct_acum <= LIMITES["B"] * 100:
                classe = "B"
            else:
                classe = "C"

            itens.append({
                "rank":        rank,
                "id":          r.id,
                "nome":        r.nome,
                "categoria":   r.categoria or "—",
                "qtd_vendida": int(r.qtd_vendida or 0),
                "receita":     receita_item,
                "pct_item":    round(pct_item, 2),
                "pct_acum":    round(pct_acum, 2),
                "classe":      classe,
            })

        totais = {
            "A": sum(1 for i in itens if i["classe"] == "A"),
            "B": sum(1 for i in itens if i["classe"] == "B"),
            "C": sum(1 for i in itens if i["classe"] == "C"),
        }

        return {
            "itens":         itens,
            "filtro":        filtro,
            "totais":        totais,
            "receita_total": receita_total,
        }
