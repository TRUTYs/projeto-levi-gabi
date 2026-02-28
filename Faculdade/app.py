from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
import os
from flask import request, redirect, url_for

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
    __tablename__ = 'fornecedores' # Nome exato da tabela no MySQL
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))


class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    quantidade = db.Column(db.Integer, default=0)
    preco_venda = db.Column(db.Numeric(10, 2))
    # Esta linha liga o produto ao fornecedor
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))

#   ------------
#   ROTAS
#   ------------

@app.route('/')
def index():
    # Isso vai abrir o teu index.html (os 3 botões coloridos)
    return render_template('index.html')

@app.route('/estoque')
def estoque():
    # Busca todos os produtos
    produtos_db = Produto.query.all()

    lista_para_exibir = []

    for p in produtos_db:
        # Busca o fornecedor pelo ID que está no produto
        forn = Fornecedor.query.get(p.fornecedor_id)

        lista_para_exibir.append({
            "id": p.id,
            "nome": p.nome,
            "quantidade": p.quantidade,
            "preco_venda": p.preco_venda, # Nome exato para o HTML
            "fornecedor_nome": forn.nome if forn else "Sem Fornecedor", # Busca o nome real
            "categoria": p.categoria
        })

    return render_template('estoque.html', produtos=lista_para_exibir)
#   -----------
#   FORNECEDORES
#   -----------
@app.route('/fornecedores')
def fornecedores():
    todos_fornecedores = Fornecedor.query.all()
    return render_template('fornecedores.html', fornecedores=todos_fornecedores)

@app.route('/cadastrar_fornecedor', methods=['POST'])
def cadastrar_fornecedor():
    nome = request.form.get('nome_fornecedor')
    if nome:
        novo_forn = Fornecedor(nome=nome)
        db.session.add(novo_forn)
        db.session.commit()
    return redirect(url_for('fornecedores'))

#   ADICIONAR PRODUTOS AO ESTOQUE
@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto():
    # Pega os dados que o seu formulário HTML enviou
    nome = request.form.get('nome')
    categoria = request.form.get('categoria')
    quantidade = request.form.get('quantidade')
    preco = request.form.get('preco')

    try:
        # Cria o novo produto para o MySQL
        novo_produto = Produto(
            nome=nome,
            categoria=categoria,
            quantidade=int(quantidade),
            preco_venda=float(preco)
        )

        db.session.add(novo_produto)
        db.session.commit()

        print(f"✅ Produto {nome} salvo com sucesso!")

        return redirect(url_for('estoque'))

    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        return f"Erro ao salvar no banco: {e}", 500
    

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
    
