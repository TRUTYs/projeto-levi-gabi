CREATE DATABASE projeto;
USE projeto;

CREATE TABLE usuario (
 id INT PRIMARY KEY,
 nome VARCHAR(50),
 email VARCHAR(50) UNIQUE,
 senha VARCHAR(100) NOT NULL,
 tipo ENUM('admin', 'vendedor')
);

CREATE TABLE fornecedores (
 id INT PRIMARY KEY,
 nome VARCHAR(50),
 contato VARCHAR(50) NOT NULL,
 telefone VARCHAR(20)
);

CREATE TABLE produtos (
 id INT PRIMARY KEY,
 nome VARCHAR(50),
 categoria VARCHAR(50),
 preco DECIMAL(10,2)
);

CREATE TABLE compras (
 id INT PRIMARY KEY,
 fornecedor_id INT,
 data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 valor_total DECIMAL(10,2),
 FOREIGN KEY(fornecedor_id) REFERENCES fornecedores(id) ON DELETE CASCADE
);

CREATE TABLE itens_compra (
 id INT PRIMARY KEY,
 compra_id INT,
 produto_id INT,
 quantidade INT,
 preco_unitario DECIMAL(10,2),
 FOREIGN KEY(compra_id) REFERENCES compras(id) ON DELETE CASCADE,
 FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE CASCADE
 );
 
CREATE TABLE vendas (
 id INT PRIMARY KEY,
 usuario_id INT,
 data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 valor_total DECIMAL(10,2),
 FOREIGN KEY(usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
 );
 
CREATE TABLE itens_venda (
 id INT PRIMARY KEY,
 venda_id INT,
 produto_id INT,
 quantidade INT,
 preco_unitario DECIMAL(10,2),
 FOREIGN KEY(venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
 FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);
 
CREATE TABLE movimentacoes_estoque (
 id INT PRIMARY KEY,
 produto_id INT,
 tipo ENUM('entrada', 'saida'),
 quantidade INT,
 data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 origem ENUM('compra', 'venda', 'ajuste'),
 referencia_compra_id INT,
 referencia_venda_id INT,
 FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
 FOREIGN KEY(referencia_compra_id) REFERENCES compras(id) ON DELETE CASCADE,
 FOREIGN KEY(referencia_venda_id) REFERENCES vendas(id) ON DELETE CASCADE
 );
 
CREATE TABLE alertas (
 id INT PRIMARY KEY,
 produto_id INT,
 mensagem VARCHAR(255),
 tipo ENUM('estoque_baixo', 'vencimento', 'outro'),
 data_alerta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 resolvido BOOLEAN DEFAULT FALSE
);