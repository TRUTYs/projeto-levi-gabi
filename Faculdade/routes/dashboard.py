from flask import Blueprint, render_template
from auth import login_required
from services import DashboardService

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    totais  = DashboardService.totais_rapidos()
    grafico = DashboardService.grafico_seis_meses()
    return render_template("index.html", **totais,
        graf_labels=grafico["labels"], graf_entradas=grafico["entradas"],
        graf_saidas=grafico["saidas"], top_vendidos=DashboardService.top_vendidos(),
        estoque_rapido=DashboardService.estoque_rapido())
