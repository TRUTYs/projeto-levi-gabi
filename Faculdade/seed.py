"""
Eight Sistemas — Seed de dados iniciais.

Executado automaticamente pelo app.py ao iniciar.
É idempotente: verifica existência antes de inserir,
portanto pode ser chamado quantas vezes quiser sem duplicar dados.
"""

from extensions import db


# ── Dados ────────────────────────────────────────────────────────

FORNECEDORES = [
    {
        "nome":        "TechSupply Ltda.",
        "contato":     "(11) 98765-4321",
        "email":       "contato@techsupply.com.br",
        "cnpj":        "12.345.678/0001-90",
        "localizacao": "São Paulo, SP",
    },
    {
        "nome":        "Distribuidora Norte Sul",
        "contato":     "(41) 93322-1100",
        "email":       "vendas@nortesul.com.br",
        "cnpj":        "98.765.432/0001-11",
        "localizacao": "Curitiba, PR",
    },
    {
        "nome":        "GlobalParts Comércio",
        "contato":     "(21) 97788-5500",
        "email":       "pedidos@globalparts.com.br",
        "cnpj":        "55.444.333/0001-22",
        "localizacao": "Rio de Janeiro, RJ",
    },
]

# Chave "fornecedor" referencia o campo "nome" acima
PRODUTOS = [
    {"nome": "Notebook Dell Inspiron 15",    "categoria": "Informática",   "quantidade": 8,  "preco_custo": 2800.00, "preco_venda": 3999.90, "fornecedor": "TechSupply Ltda."},
    {"nome": "Mouse Logitech MX Master 3",   "categoria": "Periféricos",   "quantidade": 35, "preco_custo":  180.00, "preco_venda":  299.90, "fornecedor": "TechSupply Ltda."},
    {"nome": "Teclado Mecânico Redragon",    "categoria": "Periféricos",   "quantidade": 22, "preco_custo":  190.00, "preco_venda":  320.00, "fornecedor": "TechSupply Ltda."},
    {"nome": "Monitor LG 24\" Full HD",      "categoria": "Informática",   "quantidade": 10, "preco_custo":  680.00, "preco_venda":  999.00, "fornecedor": "TechSupply Ltda."},
    {"nome": "Headset HyperX Cloud II",      "categoria": "Áudio",         "quantidade": 18, "preco_custo":  220.00, "preco_venda":  389.90, "fornecedor": "GlobalParts Comércio"},
    {"nome": "Cabo HDMI 2.0 2m",             "categoria": "Cabos",         "quantidade": 60, "preco_custo":   15.00, "preco_venda":   39.90, "fornecedor": "GlobalParts Comércio"},
    {"nome": "HD Externo Seagate 1TB",       "categoria": "Armazenamento", "quantidade": 14, "preco_custo":  240.00, "preco_venda":  379.90, "fornecedor": "Distribuidora Norte Sul"},
    {"nome": "Pen Drive Kingston 64GB",      "categoria": "Armazenamento", "quantidade": 80, "preco_custo":   22.00, "preco_venda":   49.90, "fornecedor": "Distribuidora Norte Sul"},
    {"nome": "Webcam Full HD Logitech C920", "categoria": "Periféricos",   "quantidade": 12, "preco_custo":  360.00, "preco_venda":  549.90, "fornecedor": "TechSupply Ltda."},
    {"nome": "Roteador TP-Link AX1500",      "categoria": "Redes",         "quantidade": 9,  "preco_custo":  280.00, "preco_venda":  429.00, "fornecedor": "Distribuidora Norte Sul"},
    {"nome": "SSD Kingston 480GB",           "categoria": "Armazenamento", "quantidade": 25, "preco_custo":  180.00, "preco_venda":  299.90, "fornecedor": "Distribuidora Norte Sul"},
    {"nome": "Fonte ATX 650W Corsair",       "categoria": "Hardware",      "quantidade": 7,  "preco_custo":  340.00, "preco_venda":  520.00, "fornecedor": "GlobalParts Comércio"},
    {"nome": "Memória RAM DDR4 16GB",        "categoria": "Hardware",      "quantidade": 16, "preco_custo":  280.00, "preco_venda":  430.00, "fornecedor": "GlobalParts Comércio"},
    {"nome": "Placa de Vídeo GTX 1660",      "categoria": "Hardware",      "quantidade": 4,  "preco_custo": 1400.00, "preco_venda": 1999.90, "fornecedor": "TechSupply Ltda."},
    {"nome": "Mousepad Gamer XL",            "categoria": "Periféricos",   "quantidade": 40, "preco_custo":   35.00, "preco_venda":   79.90, "fornecedor": "GlobalParts Comércio"},
    {"nome": "Hub USB-C 7 em 1",             "categoria": "Cabos",         "quantidade": 28, "preco_custo":   90.00, "preco_venda":  169.90, "fornecedor": "Distribuidora Norte Sul"},
    {"nome": "Suporte Monitor Articulado",   "categoria": "Acessórios",    "quantidade": 11, "preco_custo":  120.00, "preco_venda":  199.90, "fornecedor": "GlobalParts Comércio"},
    {"nome": "Nobreak APC 700VA",            "categoria": "Energia",       "quantidade": 6,  "preco_custo":  380.00, "preco_venda":  589.00, "fornecedor": "Distribuidora Norte Sul"},
    {"nome": "Leitor de Cartão SD USB",      "categoria": "Periféricos",   "quantidade": 55, "preco_custo":   18.00, "preco_venda":   44.90, "fornecedor": "GlobalParts Comércio"},
    {"nome": "Caixa de Som Bluetooth JBL Go3","categoria": "Áudio",        "quantidade": 20, "preco_custo":  130.00, "preco_venda":  219.90, "fornecedor": "TechSupply Ltda."},
]


# ── Funções de seed ──────────────────────────────────────────────

def seed_fornecedores() -> dict[str, int]:
    """
    Insere fornecedores que ainda não existem.
    Retorna mapa nome → id para uso no seed de produtos.
    """
    from models.fornecedor import Fornecedor

    mapa: dict[str, int] = {}
    novos = 0

    for dados in FORNECEDORES:
        existente = Fornecedor.query.filter_by(nome=dados["nome"]).first()
        if existente:
            mapa[existente.nome] = existente.id
            continue

        f = Fornecedor(
            nome=dados["nome"],
            contato=dados["contato"],
            email=dados["email"],
            cnpj=dados["cnpj"],
            localizacao=dados["localizacao"],
        )
        db.session.add(f)
        db.session.flush()   # garante f.id antes do commit
        mapa[f.nome] = f.id
        novos += 1

    db.session.commit()
    if novos:
        print(f"[seed] {novos} fornecedor(es) inserido(s).")
    return mapa


def seed_produtos(mapa_fornecedores: dict[str, int]) -> None:
    """
    Insere produtos que ainda não existem.
    Usa o mapa de fornecedores para resolver o foreign key.
    """
    from models.produto import Produto

    novos = 0

    for dados in PRODUTOS:
        if Produto.query.filter_by(nome=dados["nome"]).first():
            continue

        p = Produto(
            nome=dados["nome"],
            categoria=dados["categoria"],
            quantidade=dados["quantidade"],
            preco_custo=dados["preco_custo"],
            preco_venda=dados["preco_venda"],
            fornecedor_id=mapa_fornecedores.get(dados["fornecedor"]),
        )
        db.session.add(p)
        novos += 1

    db.session.commit()
    if novos:
        print(f"[seed] {novos} produto(s) inserido(s).")


def run_seed() -> None:
    """Ponto de entrada chamado pelo app.py."""
    mapa = seed_fornecedores()
    seed_produtos(mapa)
