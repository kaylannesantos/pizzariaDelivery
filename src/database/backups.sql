CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    endereco TEXT NOT NULL,
    bairro VARCHAR(50) NOT NULL
);

CREATE TABLE sabores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

INSERT INTO sabores (nome) VALUES
('Mussarela'),
('Calabresa'),
('Frango com Catupiry'),
('Portuguesa'),
('Quatro Queijos'),
('Napolitana'),
('Pepperoni'),
('Veggie'),
('Margherita'),
('Barbecue Chicken');

CREATE TABLE tamanho (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL,
    tamanho_cm INT NOT NULL,
    valor REAL NOT NULL
);

INSERT INTO tamanho (nome, quantidade, tamanho_cm, valor) VALUES
('Pequeno', 4, 25, 15.00),
('Médio', 6, 30, 30.00),
('Grande', 8, 40, 45.00),
('GG', 12, 50, 55.00);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    id_sabor INT NOT NULL REFERENCES sabores(id),
    id_tamanho INT NOT NULL REFERENCES tamanho(id),
	quantidade INT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	valor_total REAL NOT NULL
);

CREATE TABLE itens_pedido (
    id SERIAL PRIMARY KEY,
	id_pedido INT NOT NULL REFERENCES pedidos(id),
	id_sabor INT NOT NULL REFERENCES sabores(id),
	id_tamanho INT NOT NULL REFERENCES tamanho(id),
	quantidade_item INT NOT NULL,
	valor_total_item REAL NULL
);
