--OBS: essa versão não está compatível com o código da aplicação

CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    endereco TEXT NOT NULL,
    bairro VARCHAR(50) NOT NULL
);

CREATE TABLE sabores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor REAL NOT NULL
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    tamanho VARCHAR(50) NOT NULL,
    id_sabor INT NOT NULL REFERENCES sabores(id),
	quantidade INT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	valor_total REAL NOT NULL
); --drop table pedidos



CREATE TABLE itens_pedido (
    id SERIAL PRIMARY KEY,
	id_pedido INT NOT NULL REFERENCES pedidos(id),
	id_sabor INT NOT NULL REFERENCES sabores(id),
	quantidade_item INT NOT NULL,
	valor_total_item REAL NULL
);