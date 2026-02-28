CREATE DATABASE IF NOT EXISTS projeto;
USE projeto;

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50),
    email VARCHAR(50) UNIQUE,
    senha VARCHAR(100) NOT NULL,
    tipo ENUM('admin', 'vendedor')
);

CREATE TABLE fornecedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50),
    contato VARCHAR(50) NOT NULL,
    telefone VARCHAR(20)
);

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50),
    categoria VARCHAR(50),
    quantidade INT DEFAULT 0,
    estoque_minimo INT DEFAULT 5, -- Para os alertas!
    preco_custo DECIMAL(10,2),    -- Necessário para calcular o LUCRO no Dashboard
    preco_venda DECIMAL(10,2),    -- O teu "Valor Unitário"
    fornecedor_id INT,
    descricao TEXT,
    FOREIGN KEY(fornecedor_id) REFERENCES fornecedores(id)
);

CREATE TABLE movimentacoes_estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT,
    tipo ENUM('entrada', 'saida'),
    quantidade INT,
    origem ENUM('compra', 'venda', 'ajuste'),
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);

CREATE TABLE alertas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT,
    mensagem VARCHAR(255),
    data_alerta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolvido BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(produto_id) REFERENCES produtos(id)
);
