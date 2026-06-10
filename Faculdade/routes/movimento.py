from flask import Blueprint, render_template, request
from auth import login_required
from services import DashboardService, EstoqueService

movimento_bp = Blueprint("movimento", __name__)

@movimento_bp.route("/movimento")
@login_required
def movimento():
    filtro    = request.args.get("filtro","mensal")
    relatorio = DashboardService.relatorio_movimento(filtro)
    grafico   = DashboardService.grafico_seis_meses()
    return render_template("movimento.html", filtro_ativo=filtro, **relatorio,
        alertas=EstoqueService.alertas_estoque(),
        graf_labels=grafico["labels"], graf_entradas=grafico["entradas"],
        graf_saidas=grafico["saidas"], top_vendidos=DashboardService.top_vendidos(),
        estoque_rapido=DashboardService.estoque_rapido(),
        total_produtos=Produto_count())

def Produto_count():
    from models import Produto
    return Produto.query.count()
