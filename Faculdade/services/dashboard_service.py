from collections import defaultdict
from datetime import datetime, timedelta
from sqlalchemy import func
from extensions import db
from models import Movimentacao, Produto

FILTROS_DELTA = {
    "diario":     timedelta(days=1),
    "semanal":    timedelta(weeks=1),
    "mensal":     timedelta(days=30),
    "trimestral": timedelta(days=90),
    "semestral":  timedelta(days=180),
    "anual":      timedelta(days=365),
}


class DashboardService:

    @staticmethod
    def totais_rapidos():
        from models import Fornecedor
        alertas = Produto.query.filter(Produto.quantidade <= Produto.estoque_minimo).count()
        data_30d = datetime.now() - timedelta(days=30)
        movs = Movimentacao.query.filter(
            Movimentacao.tipo == "saida",
            Movimentacao.origem == "venda",
            Movimentacao.data_movimentacao >= data_30d,
        ).all()
        return {
            "total_produtos":     Produto.query.count(),
            "total_fornecedores": Fornecedor.query.count(),
            "alertas_count":      alertas,
            "total_vendas_mes":   sum(float(m.valor_unitario or 0) * m.quantidade for m in movs),
        }

    @staticmethod
    def grafico_seis_meses():
        seis = datetime.now() - timedelta(days=180)
        ent, sai = defaultdict(float), defaultdict(float)
        for m in Movimentacao.query.filter(Movimentacao.data_movimentacao >= seis).all():
            mes = m.data_movimentacao.strftime("%b/%y") if m.data_movimentacao else "?"
            (ent if m.tipo == "entrada" else sai)[mes] += m.quantidade
        meses = sorted(set(ent) | set(sai))
        return {
            "labels":   meses,
            "entradas": [ent.get(m, 0) for m in meses],
            "saidas":   [sai.get(m, 0) for m in meses],
        }

    @staticmethod
    def top_vendidos(limit=5):
        rows = (
            db.session.query(Produto.nome, func.sum(Movimentacao.quantidade).label("total"))
            .join(Movimentacao, Movimentacao.produto_id == Produto.id)
            .filter(Movimentacao.tipo == "saida", Movimentacao.origem == "venda")
            .group_by(Produto.id)
            .order_by(func.sum(Movimentacao.quantidade).desc())
            .limit(limit).all()
        )
        maxv = max((int(t) for _, t in rows), default=1) or 1
        return [{"nome": n, "total": int(t), "pct": round(int(t) / maxv * 100)} for n, t in rows]

    @staticmethod
    def estoque_rapido():
        return [
            {"id": p.id, "nome": p.nome, "categoria": p.categoria or "—",
             "quantidade": p.quantidade, "ok": not p.estoque_baixo}
            for p in Produto.query.order_by(Produto.quantidade.asc()).all()
        ]

    @staticmethod
    def relatorio_movimento(filtro="mensal"):
        # Garante que o delta existe; fallback para mensal
        delta      = FILTROS_DELTA.get(filtro, FILTROS_DELTA["mensal"])
        data_inicio = datetime.now() - delta

        rows = (
            db.session.query(Movimentacao, Produto)
            .join(Produto, Movimentacao.produto_id == Produto.id)
            .filter(Movimentacao.data_movimentacao >= data_inicio)
            .order_by(Movimentacao.data_movimentacao.desc())
            .all()
        )

        total_vendas = total_lucro = total_compras = 0.0
        movs = []

        for mov, prod in rows:
            valor = float(mov.valor_unitario or 0) * mov.quantidade

            if mov.tipo == "saida" and mov.origem == "venda":
                # Venda soma na receita e no lucro
                total_vendas += valor
                total_lucro  += valor

            elif mov.tipo == "entrada" and mov.origem == "compra":
                # Compra soma no total de compras e desconta do lucro
                total_compras += valor
                total_lucro   -= valor

            movs.append({
                "id":            mov.id,
                "produto_nome":  prod.nome,
                "tipo":          mov.tipo,
                "origem":        mov.origem,
                "quantidade":    mov.quantidade,
                "valor_unitario": mov.valor_unitario,
                "data": mov.data_movimentacao.strftime("%d/%m/%Y %H:%M")
                        if mov.data_movimentacao else "—",
            })

        return {
            "movimentacoes": movs,
            "total_vendas":  total_vendas,
            "total_lucro":   total_lucro,
            "total_compras": total_compras,
        }
