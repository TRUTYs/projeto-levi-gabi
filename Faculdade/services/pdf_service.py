"""
Eight Sistemas — PDF Service
Gera o relatório de movimentações em PDF usando ReportLab.
Inclui: cabeçalho, cards de totais, gráfico de barras e tabela completa.
"""

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group
from reportlab.graphics import renderPDF
from reportlab.platypus.flowables import Flowable

# ── Paleta de cores (espelha o CSS do sistema) ───────────────
C_BG        = colors.HexColor("#0B1120")
C_CARD      = colors.HexColor("#1A2235")
C_CARD2     = colors.HexColor("#1F2D42")
C_BORDER    = colors.HexColor("#263348")
C_TEXT      = colors.HexColor("#E8EFF8")
C_MUTED     = colors.HexColor("#7A8FA8")
C_BLUE      = colors.HexColor("#3B82F6")
C_GREEN     = colors.HexColor("#10B981")
C_AMBER     = colors.HexColor("#F59E0B")
C_RED       = colors.HexColor("#EF4444")
C_PURPLE    = colors.HexColor("#8B5CF6")
C_ENTRADA   = colors.HexColor("#1D3461")
C_SAIDA     = colors.HexColor("#2D1B4E")

FILTRO_LABEL = {
    "diario": "Diária", "semanal": "Semanal", "mensal": "Mensal",
    "trimestral": "Trimestral", "semestral": "Semestral", "anual": "Anual",
}

# ── Estilos de parágrafo ─────────────────────────────────────
def _estilos():
    base = getSampleStyleSheet()
    def p(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        "titulo":    p("titulo",    fontSize=20, textColor=C_TEXT,  leading=26, fontName="Helvetica-Bold"),
        "subtitulo": p("subtitulo", fontSize=11, textColor=C_MUTED, leading=16, fontName="Helvetica"),
        "secao":     p("secao",     fontSize=12, textColor=C_TEXT,  leading=18, fontName="Helvetica-Bold"),
        "normal":    p("normal",    fontSize=9,  textColor=C_TEXT,  leading=13, fontName="Helvetica"),
        "muted":     p("muted",     fontSize=8,  textColor=C_MUTED, leading=12, fontName="Helvetica"),
        "mono":      p("mono",      fontSize=8,  textColor=C_MUTED, leading=12, fontName="Courier"),
        "direita":   p("direita",   fontSize=9,  textColor=C_TEXT,  leading=13, fontName="Helvetica",
                       alignment=TA_RIGHT),
        "card_val":  p("card_val",  fontSize=18, textColor=C_TEXT,  leading=22, fontName="Helvetica-Bold",
                       alignment=TA_CENTER),
        "card_lbl":  p("card_lbl",  fontSize=8,  textColor=C_MUTED, leading=11, fontName="Helvetica",
                       alignment=TA_CENTER),
    }


# ── Flowable: gráfico de barras ──────────────────────────────
class GraficoBarras(Flowable):
    """
    Gráfico de barras lado a lado (entradas × saídas) por mês.
    Desenhado vetorialmente com ReportLab Graphics.
    """

    def __init__(self, labels, entradas, saidas, width=160*mm, height=55*mm):
        super().__init__()
        self.labels   = labels
        self.entradas = entradas
        self.saidas   = saidas
        self.width    = width
        self.height   = height

    def wrap(self, *_):
        return self.width, self.height

    def draw(self):
        c      = self.canv
        W, H   = self.width, self.height
        pad_l  = 10*mm
        pad_b  = 8*mm
        pad_t  = 6*mm
        area_w = W - pad_l - 4*mm
        area_h = H - pad_b - pad_t
        n      = len(self.labels)

        if n == 0:
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 9)
            c.drawCentredString(W / 2, H / 2, "Sem dados no período")
            return

        max_v  = max(max(self.entradas, default=0), max(self.saidas, default=0), 1)
        grp_w  = area_w / n
        bar_w  = min(grp_w * 0.28, 8*mm)
        gap    = bar_w * 0.4

        # Eixo Y — linhas de grade
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.3)
        for i in range(5):
            y = pad_b + (area_h * i / 4)
            c.line(pad_l, y, W - 4*mm, y)

        # Barras
        for i, mes in enumerate(self.labels):
            x_base = pad_l + i * grp_w + (grp_w - 2 * bar_w - gap) / 2

            # Entrada
            h_e = (self.entradas[i] / max_v) * area_h
            c.setFillColor(C_BLUE)
            c.rect(x_base, pad_b, bar_w, max(h_e, 1), fill=1, stroke=0)

            # Saída
            h_s = (self.saidas[i] / max_v) * area_h
            c.setFillColor(C_PURPLE)
            c.rect(x_base + bar_w + gap, pad_b, bar_w, max(h_s, 1), fill=1, stroke=0)

            # Label do mês
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 6.5)
            c.drawCentredString(x_base + bar_w + gap / 2, pad_b - 5*mm, mes)

        # Legenda
        leg_x = pad_l
        leg_y = H - 3*mm
        for cor, texto in [(C_BLUE, "Entradas"), (C_PURPLE, "Saídas")]:
            c.setFillColor(cor)
            c.rect(leg_x, leg_y - 2.5*mm, 3*mm, 3*mm, fill=1, stroke=0)
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 7.5)
            c.drawString(leg_x + 4*mm, leg_y - 2*mm, texto)
            leg_x += 22*mm


# ── Função principal ─────────────────────────────────────────
def gerar_pdf_movimento(
    filtro: str,
    total_vendas: float,
    total_lucro: float,
    total_compras: float,
    movimentacoes: list,
    graf_labels: list,
    graf_entradas: list,
    graf_saidas: list,
) -> bytes:
    """
    Gera o relatório em PDF e retorna os bytes prontos para download.
    """
    buf    = io.BytesIO()
    doc    = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm,  bottomMargin=15*mm,
    )
    W      = A4[0] - 30*mm   # largura útil
    S      = _estilos()
    story  = []
    agora  = datetime.now().strftime("%d/%m/%Y %H:%M")
    filtro_nome = FILTRO_LABEL.get(filtro, filtro.capitalize())

    # ── Cabeçalho ────────────────────────────────────────────
    story.append(Paragraph("Eight Sistemas", S["titulo"]))
    story.append(Paragraph(f"Relatório de Movimentações — {filtro_nome}", S["subtitulo"]))
    story.append(Paragraph(f"Gerado em {agora}", S["muted"]))
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 5*mm))

    # ── Cards de totais ──────────────────────────────────────
    story.append(Paragraph("Resumo do Período", S["secao"]))
    story.append(Spacer(1, 3*mm))

    def card_data(label, valor, cor):
        return [
            [Paragraph(label, S["card_lbl"])],
            [Paragraph(f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
                       ParagraphStyle("cv", fontSize=15, textColor=cor,
                                      fontName="Helvetica-Bold", alignment=TA_CENTER))],
        ]

    card_w    = W / 3 - 3*mm
    card_style = TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), C_CARD),
        ("BOX",         (0, 0), (-1, -1), 0.5, C_BORDER),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING",  (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0,0), (-1, -1), 8),
        ("ALIGN",       (0, 0), (-1, -1), "CENTER"),
    ])

    cards_row = Table(
        [[
            Table(card_data("TOTAL EM VENDAS",  total_vendas,  C_GREEN), colWidths=[card_w], style=card_style),
            Table(card_data("LUCRO ESTIMADO",    total_lucro,   C_AMBER), colWidths=[card_w], style=card_style),
            Table(card_data("TOTAL EM COMPRAS",  total_compras, C_BLUE),  colWidths=[card_w], style=card_style),
        ]],
        colWidths=[card_w + 1*mm] * 3,
        hAlign="LEFT",
    )
    cards_row.setStyle(TableStyle([
        ("LEFTPADDING",  (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
    ]))
    story.append(cards_row)
    story.append(Spacer(1, 6*mm))

    # ── Gráfico ──────────────────────────────────────────────
    if graf_labels:
        story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER))
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph("Entradas vs Saídas — últimos 6 meses", S["secao"]))
        story.append(Spacer(1, 3*mm))
        story.append(GraficoBarras(graf_labels, graf_entradas, graf_saidas, width=W, height=58*mm))
        story.append(Spacer(1, 6*mm))

    # ── Tabela de movimentações ──────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        f"Movimentações — {filtro_nome} &nbsp;&nbsp;"
        f"<font color='#7A8FA8' size='9'>({len(movimentacoes)} registro(s))</font>",
        S["secao"]
    ))
    story.append(Spacer(1, 3*mm))

    if movimentacoes:
        col_w = [12*mm, 50*mm, 20*mm, 20*mm, 14*mm, 24*mm, 30*mm]
        header = ["#", "Produto", "Tipo", "Origem", "Qtd.", "Valor Unit.", "Data"]

        rows = [header]
        for m in movimentacoes:
            val = f"R$ {float(m['valor_unitario']):,.2f}".replace(",","X").replace(".",",").replace("X",".") \
                  if m["valor_unitario"] else "—"
            rows.append([
                str(m["id"]),
                m["produto_nome"],
                m["tipo"].upper(),
                m["origem"].upper(),
                str(m["quantidade"]),
                val,
                m["data"],
            ])

        tbl = Table(rows, colWidths=col_w, repeatRows=1)
        tbl.setStyle(TableStyle([
            # Cabeçalho
            ("BACKGROUND",   (0, 0), (-1, 0),  C_CARD2),
            ("TEXTCOLOR",    (0, 0), (-1, 0),  C_MUTED),
            ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, 0),  7.5),
            ("TOPPADDING",   (0, 0), (-1, 0),  5),
            ("BOTTOMPADDING",(0, 0), (-1, 0),  5),
            # Corpo
            ("BACKGROUND",   (0, 1), (-1, -1), C_CARD),
            ("TEXTCOLOR",    (0, 1), (-1, -1), C_TEXT),
            ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE",     (0, 1), (-1, -1), 8),
            ("TOPPADDING",   (0, 1), (-1, -1), 4),
            ("BOTTOMPADDING",(0, 1), (-1, -1), 4),
            # Linhas alternadas
            *[("BACKGROUND", (0, i), (-1, i), colors.HexColor("#151F30"))
              for i in range(2, len(rows), 2)],
            # Grid
            ("LINEBELOW",    (0, 0), (-1, -1), 0.3, C_BORDER),
            ("ALIGN",        (0, 0), (0, -1),  "CENTER"),
            ("ALIGN",        (4, 0), (5, -1),  "RIGHT"),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(tbl)
    else:
        story.append(Paragraph("Nenhuma movimentação no período selecionado.", S["muted"]))

    # ── Rodapé via callback de página ────────────────────────
    def rodape(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(C_MUTED)
        canvas.setFont("Helvetica", 7)
        canvas.drawString(15*mm, 8*mm, "Eight Sistemas — Relatório gerado automaticamente")
        canvas.drawRightString(A4[0] - 15*mm, 8*mm, f"Pág. {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=rodape, onLaterPages=rodape)
    return buf.getvalue()
