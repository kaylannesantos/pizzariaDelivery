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
INSERT INTO sabores (nome, valor) VALUES
('Mussarela', 29.90),
('Calabresa', 32.90),
('Frango com Catupiry', 34.90),
('Portuguesa', 35.90),
('Quatro Queijos', 36.90),
('Napolitana', 33.90),
('Pepperoni', 38.90),
('Veggie', 31.90),
('Margherita', 33.90),
('Barbecue Chicken', 37.90);


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