from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
import os
from flask import request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

usuario = 'root'
senha = 'fucapfaculdade.2026'
host = 'localhost'
banco = 'projeto'
senha_segura = urllib.parse.quote_plus(senha)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{usuario}:{senha_segura}@{host}/{banco}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#   ----------
#   CLASSES
#   ----------

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    contato = db.Column(db.String(50))


class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    quantidade = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=5)
    preco_custo = db.Column(db.Float) # Adicionei aqui para você ter o custo fixo
    preco_venda = db.Column(db.Float)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))


class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes_estoque'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False)

    tipo = db.Column(db.Enum('entrada', 'saida'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    origem = db.Column(db.Enum('compra', 'venda', 'ajuste'), nullable=False)


    valor_unitario = db.Column(db.Float) 
    custo_unitario = db.Column(db.Float) 
    data_movimentacao = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Esse é o jeito certo de fazer o link:
    produto = db.relationship('Produto', backref=db.backref('historico', lazy=True))


#   ------------
#   ROTAS
#   ------------

@app.route('/')
def index():
    # Isso vai abrir o teu index.html (os 3 botões coloridos)
    return render_template('index.html')

@app.route('/estoque')
def estoque():
    # Buscamos as duas listas: produtos e fornecedores
    produtos_db = Produto.query.all()
    fornecedores_db = Fornecedor.query.all()

    lista_para_exibir = []
    for p in produtos_db:
        # Busca o nome do fornecedor associado ao produto
        forn = Fornecedor.query.get(p.fornecedor_id)
        lista_para_exibir.append({
            "id": p.id,
            "nome": p.nome,
            "quantidade": p.quantidade,
            "preco_venda": p.preco_venda,
            "fornecedor_nome": forn.nome if forn else "Sem Fornecedor",
            "categoria": p.categoria
        })

    return render_template('estoque.html', produtos=lista_para_exibir, fornecedores=fornecedores_db)
#   -----------
#   FORNECEDORES
#   -----------
@app.route('/fornecedores')
def fornecedores(): # <--- É ESTE NOME AQUI QUE O FLASK PRECISA!
    lista = Fornecedor.query.all()
    return render_template('fornecedores.html', fornecedores=lista)

@app.route('/cadastrar_fornecedor', methods=['POST'])
def cadastrar_fornecedor():
    nome_forn = request.form.get('nome_fornecedor')
    contato_forn = request.form.get('contato_fornecedor') # Novo campo

    if nome_forn:
        # Agora enviamos os dois campos para o banco
        novo_forn = Fornecedor(nome=nome_forn, contato=contato_forn)
        db.session.add(novo_forn)
        db.session.commit()
    return redirect(url_for('fornecedores'))


@app.route('/editar_fornecedor/<int:id>', methods=['POST'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get(id)
    if fornecedor:
        fornecedor.nome = request.form.get('nome_fornecedor')
        fornecedor.contato = request.form.get('contato_fornecedor')
        db.session.commit()
    # TROQUE 'listar_fornecedores' pelo nome da função acima (ex: 'fornecedores')
    return redirect(url_for('fornecedores')) 

@app.route('/excluir_fornecedor/<int:id>')
def excluir_fornecedor(id):
    # 1. Tenta achar o fornecedor no banco
    fornecedor = Fornecedor.query.get(id)

    if fornecedor:
        # AQUI ESTÁ O PULO DO GATO:
        # 2. Busca todos os produtos que pertencem a esse fornecedor
        produtos_vinculados = Produto.query.filter_by(fornecedor_id=id).all()

        for p in produtos_vinculados:
            p.fornecedor_id = None 

        db.session.commit()

        db.session.delete(fornecedor)
        db.session.commit()

    return redirect(url_for('fornecedores'))


#   ADICIONAR PRODUTOS AO ESTOQUE
@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto():
    nome = request.form.get('nome')
    categoria = request.form.get('categoria')
    quantidade = int(request.form.get('quantidade'))
    preco = float(request.form.get('preco'))
    forn_id = request.form.get('fornecedor_id')

    # 1. Tenta encontrar um produto que já tenha esse nome exato
    produto_existente = Produto.query.filter_by(nome=nome).first()

    if produto_existente:
        # 2. Se existir, apenas SOMAMOS a nova quantidade à que já tem lá
        produto_existente.quantidade += quantidade
        # Opcional: Atualizar o preço se ele mudou
        produto_existente.preco_venda = preco
        db.session.commit()
        print(f"Estoque atualizado: {nome} agora tem {produto_existente.quantidade}")
    else:
        # 3. Se não existir, aí sim criamos um NOVO
        novo_produto = Produto(
            nome=nome,
            categoria=categoria,
            quantidade=quantidade,
            preco_venda=preco,
            fornecedor_id=int(forn_id)
        )
        db.session.add(novo_produto)
        db.session.commit()
        print(f"Novo produto cadastrado: {nome}")

    return redirect(url_for('estoque'))


@app.route('/editar_produto/<int:id>', methods=['POST'])
def editar_produto(id):
    produto = Produto.query.get(id)
    if produto:
        # Pega o valor do formulário
        forn_id = request.form.get('fornecedor_id')

        produto.nome = request.form.get('nome')
        produto.categoria = request.form.get('categoria') 
        produto.quantidade = int(request.form.get('quantidade'))
        produto.preco_venda = float(request.form.get('preco'))

        # SE O VALOR FOR VAZIO, SALVA COMO NULO (NONE)
        if forn_id == "" or forn_id == "None":
            produto.fornecedor_id = None
        else:
            produto.fornecedor_id = forn_id

        db.session.commit()
        print(f"Produto {id} atualizado com sucesso!")

    return redirect(url_for('estoque'))
#   --------    
#   EXCLUIR PRODUTO
#   --------

@app.route('/excluir_produto/<int:id>')
def excluir_produto(id):
    produto = Produto.query.get(id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
        print(f"Produto {id} removido com sucesso!")

    return redirect(url_for('estoque'))

#   ------------
#   CADASTRAR VENDA
#   ------------
  
@app.route('/vender_produto/<int:id>', methods=['POST'])
def vender_produto(id):  # <-- O nome aqui TEM QUE SER vender_produto
    p = Produto.query.get(id)
    qtd_venda = int(request.form.get('quantidade'))

    if p and p.quantidade >= qtd_venda:
        # Registra a movimentação salvando o PREÇO e o CUSTO daquele momento
        nova_venda = Movimentacao(
            produto_id=p.id,
            tipo='saida',
            quantidade=qtd_venda,
            origem='venda',
            valor_unitario=p.preco_venda, # Preço que o cliente pagou
            custo_unitario=p.preco_custo, # Quanto você pagou (para calcular o lucro)
        )

        p.quantidade -= qtd_venda # Baixa no estoque
        db.session.add(nova_venda)
        db.session.commit()

    return redirect(url_for('estoque'))


if __name__ == '__main__':
    print("Sistema da Faculdade Iniciado!")
    app.run(debug=True)

@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto():
    if request.method == 'POST':
        # Pega os dados vindos do formulário HTML
        novo_nome = request.form['nome']
        nova_categoria = request.form['categoria']
        nova_qtd = request.form['quantidade']
        novo_preco = request.form['preco']

        # Cria o objeto Produto conforme o seu banco
        novo_item = Produto(
            nome=novo_nome, 
            categoria=nova_categoria, 
            quantidade=nova_qtd, 
            preco_venda=novo_preco
        )

        db.session.add(novo_item)
        db.session.commit() # Salva no MySQL!

        return redirect(url_for('estoque'))


#   ---------------
#   MOVIMENTAÇÃO E DASHBOARD
#   ---------------

def registrar_movimentacao(produto_id, tipo, quantidade, origem):
    p = Produto.query.get(produto_id)
    if p:
        # 1. Atualiza a quantidade física no estoque
        if tipo == 'saida':
            p.quantidade -= quantidade
        else:
            p.quantidade += quantidade

        # 2. "Fotografa" os preços atuais para o histórico
        nova_mov = Movimentacao(
            produto_id=p.id,
            tipo=tipo,
            quantidade=quantidade,
            origem=origem,
            valor_unitario=p.preco_venda, # Preço da venda no momento
            custo_unitario=p.preco_custo, # Custo do produto no momento
            data_movimentacao=datetime.now()
        )

        db.session.add(nova_mov)
        db.session.commit()
