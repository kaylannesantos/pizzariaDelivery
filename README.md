# **Pizzaria Delivery - Projeto Final (Disc.: Análise e Projeto de Sistemas)**

## 👥 Equipe
- **Kaylanne Mendes dos Santos**
- **Lays Emanuelly dos Santos Lima**

## 📌 Sobre o Projeto
O **Pizzaria Delivery**🍕 é um sistema desenvolvido para automatizar o processo de pedidos de pizza, facilitando o registro de clientes e pedidos, garantindo persistência dos dados e permitindo consulta e edição de pedidos.

## 🚀 Tecnologias Utilizadas
- **Backend:** Python
- **Frontend:** Tkinter
- **Banco de Dados:** PostgreSQL
- **Protótipo:** Figma

## 🛠️ Funcionalidades
- Cadastrar Cliente
- Registrar Pedido
- Pagar Pedido
- Histórico de Pedidos
- Tela de Login
- Persistência de dados no banco de dados.

## 📂 Estrutura do Repositório
```
pizzariaDelivery/
│── docs/                      # Documentação do sistema
│   ├── casos_de_uso/          # Diagramas e descrições de casos de uso
│   ├── diagramas/             # Diagramas UML (sequência, classes, etc.)
│   ├── figma/                 # Protótipo do Figma
│   ├── mapeamento_classes/    # Modelagem das classes do sistema
│   ├── especificacoes.pdf     # Documento com especificações
│── src/                       # Código-fonte da aplicação
│   ├── images/                # imagens usadas na aplicação
│   ├── backend/               # Código do backend
│   ├── frontend/              # Código do frontend (Tkinter)
│   │── database/              # Arquivos relacionados ao banco de dados
│   │   ├── scripts/           # Scripts de criação e manipulação
│   │   ├── backups/           # Backups do banco de dados
│── .gitignore   
│── README.md                  # Guia do projeto
│── requirements.txt           # Dependências                  
```

### 🔧 Pré-requisitos para Rodar o Projeto
- Python instalado
- PostgreSQL configurado

## **Configuração do Banco de Dados**
### Criar Banco de Dados e Tabela:

### 🏃 Passos para rodar a aplicação
1. Clone este repositório:
   ```sh
   git clone https://github.com/kaylannesantos/pizzariaDelivery.git
   ```
2. Acesse a pasta do projeto:
   ```sh
   cd pizzariaDelivery
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
4. Abra o arquivo Python em `src/database` e configure os dados da conexão com o banco de dados na função `conectar_bd`:
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
5. Execute o arquivo Python no terminal:
   ```bash
   python src/pizzaria.py
   --ou
   python -m src.pizzaria
   ```
6. Faça login com as credenciais padrão:
   - **Usuário**: `admin`
   - **Senha**: `1234`

## 📖 Documentação
A documentação completa do projeto está disponível na pasta `docs/` e inclui:
- Diagramas de Casos de Uso
- Descrição dos Casos de Uso
- Diagramas de Sequência
- Diagrama de Classes
- Protótipo no Figma
- Mapeamento de Classes
- Documento com Especificações

## 🗄️ Banco de Dados
Os arquivos relacionados ao banco de dados estão na pasta `src/database` e incluem:
- **db.py**: SQL para criação e manipulação do banco
- **backups.sql**: Arquivos de backup para recuperação
---