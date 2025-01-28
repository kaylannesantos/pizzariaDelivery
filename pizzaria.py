import tkinter as tk
from tkinter import ttk, messagebox
import csv
import psycopg2

#conexão com o banco
def conectar_bd():
    return psycopg2.connect(
        dbname="pizzaria",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )

# Função de autenticação (simulação)
def autenticar():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    if usuario == "admin" and senha == "1234":
        tela_login.destroy()
        abrir_tela_pedido()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

# Função para abrir a tela de pedidos
def abrir_tela_pedido():
    tela_pedido = tk.Tk()
    tela_pedido.title("Registro de Pedido - Pizzaria")
    
    # Dados do Cliente
    tk.Label(tela_pedido, text="Nome do Cliente:").grid(row=0, column=0, padx=5, pady=5)
    entry_cliente = tk.Entry(tela_pedido, width=50)
    entry_cliente.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(tela_pedido, text="Endereço:").grid(row=1, column=0, padx=5, pady=5)
    entry_endereco = tk.Entry(tela_pedido, width=50)
    entry_endereco.grid(row=1, column=1, padx=5, pady=5)
    
    # Dados do Pedido
    tk.Label(tela_pedido, text="Tamanho da Pizza:").grid(row=2, column=0, padx=5, pady=5)
    tamanho_var = tk.StringVar(value="Média")
    ttk.Combobox(tela_pedido, textvariable=tamanho_var, 
                 values=["Média", "Grande", "Gigante"], width=28).grid(row=2, column=1, padx=5, pady=5)
    
    tk.Label(tela_pedido, text="Sabor da Pizza:").grid(row=3, column=0, padx=5, pady=5)
    entry_sabor = tk.Entry(tela_pedido, width=30)
    entry_sabor.grid(row=3, column=1, padx=5, pady=5)
    
    # Botão para registrar o pedido
    def registrar_pedido():
        cliente = entry_cliente.get()
        endereco = entry_endereco.get()
        tamanho = tamanho_var.get()
        sabor = entry_sabor.get()
        
        if not cliente or not endereco or not sabor:
            messagebox.showerror("Erro", "Preencha todos os campos!")
        else:
            try:
                # Salvar pedido no banco de dados
                conn = conectar_bd()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO pedidos (cliente, endereco, tamanho, sabor)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (cliente, endereco, tamanho, sabor)
                )
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Sucesso", f"Pedido registrado:\nCliente: {cliente}\nEndereço: {endereco}\n"
                                               f"Tamanho: {tamanho}\nSabor: {sabor}")
                tela_pedido.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar no banco de dados: {e}")
    
    tk.Button(tela_pedido, text="Registrar Pedido", command=registrar_pedido, bg="green", fg="white").grid(
        row=4, column=0, columnspan=2, pady=10
    )
    
    tela_pedido.mainloop()

# Tela de Login
tela_login = tk.Tk()
tela_login.title("Login - Pizzaria")

tk.Label(tela_login, text="Usuário:").grid(row=0, column=0, padx=5, pady=5)
entry_usuario = tk.Entry(tela_login)
entry_usuario.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tela_login, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
entry_senha = tk.Entry(tela_login, show="*")
entry_senha.grid(row=1, column=1, padx=5, pady=5)

tk.Button(tela_login, text="Entrar", command=autenticar, bg="blue", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

tela_login.mainloop()
