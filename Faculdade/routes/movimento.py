"""
Rotas de Movimento — relatório e exportação PDF.
"""
from flask import Blueprint, render_template, request, send_file, Response
from auth import login_required
from services import DashboardService, EstoqueService

movimento_bp = Blueprint("movimento", __name__)


@movimento_bp.route("/movimento")
@login_required
def movimento():
    filtro    = request.args.get("filtro", "mensal")
    relatorio = DashboardService.relatorio_movimento(filtro)
    grafico   = DashboardService.grafico_seis_meses()
    return render_template(
        "movimento.html",
        filtro_ativo=filtro,
        **relatorio,
        alertas=EstoqueService.alertas_estoque(),
        graf_labels=grafico["labels"],
        graf_entradas=grafico["entradas"],
        graf_saidas=grafico["saidas"],
    )


@movimento_bp.route("/movimento/exportar-pdf")
@login_required
def exportar_pdf():
    from services.pdf_service import gerar_pdf_movimento

    filtro    = request.args.get("filtro", "mensal")
    relatorio = DashboardService.relatorio_movimento(filtro)
    grafico   = DashboardService.grafico_seis_meses()

    pdf_bytes = gerar_pdf_movimento(
        filtro=filtro,
        total_vendas=relatorio["total_vendas"],
        total_lucro=relatorio["total_lucro"],
        total_compras=relatorio["total_compras"],
        movimentacoes=relatorio["movimentacoes"],
        graf_labels=grafico["labels"],
        graf_entradas=grafico["entradas"],
        graf_saidas=grafico["saidas"],
    )

    from io import BytesIO
    from datetime import datetime
    nome_arquivo = f"relatorio_movimento_{filtro}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=nome_arquivo,
    )
