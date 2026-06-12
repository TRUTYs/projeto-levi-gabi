"""
Rota da Curva ABC.
"""
from flask import Blueprint, render_template, request
from auth import login_required
from services.curva_abc_service import CurvaABCService

curva_abc_bp = Blueprint("curva_abc", __name__)

@curva_abc_bp.route("/curva-abc")
@login_required
def curva_abc():
    filtro    = request.args.get("filtro", "trimestral")
    resultado = CurvaABCService.calcular(filtro)
    return render_template("curva_abc.html", **resultado)
