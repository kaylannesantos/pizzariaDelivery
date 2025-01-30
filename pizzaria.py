import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# Função para conectar ao banco de dados PostgreSQL
def conectar_bd():
    try:
        return psycopg2.connect(
            dbname="pizzaria",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função de autenticação (simulação)
def autenticar():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    if usuario == "admin" and senha == "123":
        tela_login.destroy()
        abrir_tela_pedido()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

# Função para listar pedidos
def listar_pedidos(tree):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT cliente, endereco, tamanho, sabor FROM pedidos")
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()

    tree.delete(*tree.get_children())  # Limpa a tabela antes de preencher novamente

    for pedido in pedidos:
        tree.insert("", "end", values=pedido)

# Função para excluir pedido
def excluir_pedido(tree):
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione um pedido para excluir!")
        return

    item = tree.item(selecionado)["values"]
    pedido_id = item[0]

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id = %s", (pedido_id,))
    conn.commit()
    cursor.close()
    conn.close()

    listar_pedidos(tree)  # Atualiza a lista
    messagebox.showinfo("Sucesso", "Pedido excluído com sucesso!")

# Função para atualizar um pedido
def atualizar_pedido(tree, entry_cliente, entry_endereco, tamanho_var, entry_sabor):
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione um pedido para atualizar!")
        return

    item = tree.item(selecionado)["values"]
    pedido_id = item[0]

    novo_cliente = entry_cliente.get()
    novo_endereco = entry_endereco.get()
    novo_tamanho = tamanho_var.get()
    novo_sabor = entry_sabor.get()

    if not novo_cliente or not novo_endereco or not novo_sabor:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pedidos SET cliente=%s, endereco=%s, tamanho=%s, sabor=%s WHERE id=%s",
        (novo_cliente, novo_endereco, novo_tamanho, novo_sabor, pedido_id),
    )
    conn.commit()
    cursor.close()
    conn.close()

    listar_pedidos(tree)  # Atualiza a lista
    messagebox.showinfo("Sucesso", "Pedido atualizado com sucesso!")

# Função para verificar se o cliente já está cadastrado e preencher o campo de endereço
def verificar_cliente(entry_endereco):
    nome_cliente = entry_cliente.get()
    if not nome_cliente:
        messagebox.showerror("Erro", "Digite o nome do cliente!")
        return
    
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE nome = %s", (nome_cliente,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()

    if cliente:
        messagebox.showinfo("Cliente encontrado", "O cliente já está cadastrado!")
        # Preenche o campo de endereço com o endereço do cliente encontrado
        entry_endereco.delete(0, tk.END)  # Limpa o campo de endereço
        entry_endereco.insert(0, cliente[3])  # Assume que o endereço está no índice 3

    else:
        messagebox.showinfo("Cliente não encontrado", "Cliente não está cadastrado. Você pode cadastrá-lo.")
        # Aqui você pode chamar a função para cadastrar o cliente, caso necessário
        abrir_tela_cadastro_cliente(nome_cliente)

# Função para cadastrar um novo cliente
def cadastrar_cliente(entry_nome, entry_telefone, entry_endereco, entry_bairro, janela):
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()
    bairro = entry_bairro.get()

    if not nome or not telefone or not endereco or not bairro:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clientes (nome, telefone, endereco, bairro) VALUES (%s, %s, %s, %s)",
        (nome, telefone, endereco, bairro),
    )
    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
    janela.destroy()

# Tela de Cadastro de Cliente
def abrir_tela_cadastro_cliente(nome_cliente):
    janela = tk.Toplevel()
    janela.title("Cadastro de Cliente")
    janela.geometry("400x300")

    tk.Label(janela, text="Nome:").pack(pady=5)
    entry_nome = tk.Entry(janela, width=40)
    entry_nome.insert(0, nome_cliente)
    entry_nome.pack(pady=5)

    tk.Label(janela, text="Telefone:").pack(pady=5)
    entry_telefone = tk.Entry(janela, width=40)
    entry_telefone.pack(pady=5)

    tk.Label(janela, text="Endereço:").pack(pady=5)
    entry_endereco = tk.Entry(janela, width=40)
    entry_endereco.pack(pady=5)

    tk.Label(janela, text="Bairro:").pack(pady=5)
    entry_bairro = tk.Entry(janela, width=40)
    entry_bairro.pack(pady=5)

    tk.Button(janela, text="Salvar Cliente", command=lambda: cadastrar_cliente(entry_nome, entry_telefone, entry_endereco, entry_bairro, janela), bg="green", fg="white").pack(pady=10)

# Função para registrar um novo pedido no banco de dados
def registrar_pedido(tree, entry_cliente, entry_endereco, tamanho_var, entry_sabor, entry_quantidade):
    cliente = entry_cliente.get()
    endereco = entry_endereco.get()
    tamanho = tamanho_var.get()
    sabor = entry_sabor.get()
    quantidade = entry_quantidade.get()

    # Validação dos campos
    if not cliente or not endereco or not sabor or not quantidade:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    try:
        quantidade = int(quantidade)  # Verifica se a quantidade é um número inteiro
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
    except ValueError as e:
        messagebox.showerror("Erro", f"Erro na quantidade de pizzas: {e}")
        return

    conn = conectar_bd()
    cursor = conn.cursor()
    
    try:
        for _ in range(quantidade):
            cursor.execute(
                "INSERT INTO pedidos (cliente, endereco, tamanho, sabor) VALUES (%s, %s, %s, %s)",
                (cliente, endereco, tamanho, sabor),
            )
        conn.commit()
        messagebox.showinfo("Sucesso", f"{quantidade} Pedido(s) registrado(s) com sucesso!")
        
        listar_pedidos(tree)  # Atualiza a tabela de pedidos
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao registrar pedido: {e}")
    finally:
        cursor.close()
        conn.close()

# Função para abrir a tela de pedidos
def abrir_tela_pedido():
    global entry_cliente  # Permite acesso na função de verificação de cliente
    tela_pedido = tk.Tk()
    tela_pedido.title("Gerenciamento de Pedidos - Pizzaria")
    tela_pedido.geometry("700x500")

    frame_form = tk.Frame(tela_pedido)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nome do Cliente:").grid(row=0, column=0, padx=5, pady=5)
    entry_cliente = tk.Entry(frame_form, width=30)
    entry_cliente.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(frame_form, text="Verificar Cliente", 
          command=lambda: verificar_cliente(entry_endereco), 
          bg="orange", fg="black").grid(row=0, column=2, padx=5)

    tk.Label(frame_form, text="Endereço:").grid(row=1, column=0, padx=5, pady=5)
    entry_endereco = tk.Entry(frame_form, width=30)
    entry_endereco.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Tamanho da Pizza:").grid(row=2, column=0, padx=5, pady=5)
    tamanho_var = tk.StringVar(value="Média")
    ttk.Combobox(frame_form, textvariable=tamanho_var, values=["Média", "Grande", "Gigante"], width=28).grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Sabor da Pizza:").grid(row=3, column=0, padx=5, pady=5)
    entry_sabor = tk.Entry(frame_form, width=30)
    entry_sabor.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Quantidade de Pizzas:").grid(row=4, column=0, padx=5, pady=5)
    entry_quantidade = tk.Entry(frame_form, width=30)
    entry_quantidade.grid(row=4, column=1, padx=5, pady=5)

    # Frame da tabela
    frame_tabela = tk.Frame(tela_pedido)
    frame_tabela.pack(pady=10)

    tree = ttk.Treeview(frame_tabela, columns=("Cliente", "Endereço", "Tamanho", "Sabor"), show="headings")
    #tree.heading("ID", text="ID")
    tree.heading("Cliente", text="Cliente")
    tree.heading("Endereço", text="Endereço")
    tree.heading("Tamanho", text="Tamanho")
    tree.heading("Sabor", text="Sabor")
    tree.pack()

    listar_pedidos(tree)

    # Botões de Ação
    frame_botoes = tk.Frame(tela_pedido)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Excluir Pedido", command=lambda: excluir_pedido(tree), bg="red", fg="white").pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Atualizar Pedido", command=lambda: atualizar_pedido(tree, entry_cliente, entry_endereco, tamanho_var, entry_sabor), bg="blue", fg="white").pack(side="left", padx=5)

    tk.Button(frame_form, text="Registrar Pedido", 
          command=lambda: registrar_pedido(tree, entry_cliente, entry_endereco, tamanho_var, entry_sabor, entry_quantidade),
          bg="green", fg="white").grid(row=5, column=0, columnspan=2, pady=10)

    tela_pedido.mainloop()

# Tela de Login
tela_login = tk.Tk()
tela_login.title("Login - Pizzaria")
tela_login.geometry("300x150") #aumenta a tela de login

tk.Label(tela_login, text="Usuário:").grid(row=0, column=0, padx=5, pady=5)
entry_usuario = tk.Entry(tela_login, width=30)
entry_usuario.grid(row=0, column=1, padx=10, pady=10)

tk.Label(tela_login, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
entry_senha = tk.Entry(tela_login, show="*", width=30)
entry_senha.grid(row=1, column=1, padx=10, pady=10)

tk.Button(tela_login, text="Entrar", command=autenticar, bg="blue", fg="white",width=20).grid(row=2, column=0, columnspan=2, pady=10)

tela_login.mainloop()
