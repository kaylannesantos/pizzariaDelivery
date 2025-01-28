# Pizzaria - Sistema de Controle de Pedidos

## **Pré-requisitos**

1. **Biblioteca psycopg2**: Para conectar ao PostgreSQL. Instale com:
   ```bash
   pip install psycopg2
   ```
2. **PostgreSQL**: Instale e configure o PostgreSQL no seu computador.

---

## **Configuração do Banco de Dados**

### Criar Banco de Dados e Tabela:
1. Crie o banco de dados "pizzaria":
   ```sql
   CREATE DATABASE pizzaria;
   ```

2. Acesse o banco de dados criado:
   ```sql
   \c pizzaria
   ```

3. Crie a tabela `pedidos`:
   ```sql
   CREATE TABLE pedidos (
       id SERIAL PRIMARY KEY,
       cliente VARCHAR(100) NOT NULL,
       endereco VARCHAR(255) NOT NULL,
       tamanho VARCHAR(50) NOT NULL,
       sabor VARCHAR(100) NOT NULL,
       data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```
---

## **Configuração do Código**

1. Clone este repositório ou copie o arquivo do código para o seu ambiente.

2. Abra o arquivo Python e configure os dados da conexão com o banco de dados na função `conectar_bd`:
   ```python
   def conectar_bd():
       return psycopg2.connect(
           dbname="pizzaria",
           user="seu_usuario",  # Substitua pelo seu usuário do PostgreSQL
           password="sua_senha",  # Substitua pela sua senha do PostgreSQL
           host="localhost",
           port="5432"
       )
   ```
---

## **Como Executar**

1. Execute o arquivo Python no terminal:
   ```bash
   python pizzaria.py
   ```

2. Faça login com as credenciais padrão:
   - **Usuário**: `admin`
   - **Senha**: `1234`

3. Preencha os dados do cliente e do pedido na interface gráfica.

4. Clique em **"Registrar Pedido"** para salvar o pedido no banco de dados PostgreSQL.

---

## **Funcionalidades exigidas no trabalho**
- Tela de Login.
- Registro de clientes e pedidos com interface gráfica.
- Persistência de dados no banco de dados.

---

## **Falta**
- Implementar funcionalidades adicionais, como consulta e edição de pedidos.
- Melhorar a interface gráfica.
- Adicionar suporte a múltiplos sabores por pizza.

---

