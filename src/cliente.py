import tkinter as tk
from tkinter import ttk, messagebox
from src.database.db import conectar_bd

def cadastrar_cliente(entry_cliente, entry_telefone, entry_endereco, entry_bairro, janela):
    nome = entry_cliente.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()
    bairro = entry_bairro.get()

    if not nome or not telefone or not endereco or not bairro:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    conn, cursor = conectar_bd()
    if not conn or not cursor:
        return []
    cursor.execute(
        "INSERT INTO clientes (nome, telefone, endereco, bairro) VALUES (%s, %s, %s, %s)",
        (nome, telefone, endereco, bairro),
    )
    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
    janela.destroy()


def abrir_tela_cadastro_cliente():
    janela = tk.Toplevel()
    janela.title("Cadastro de Cliente")
    janela.geometry("414x800")
    janela.resizable(False, False)
    janela.configure(bg="#E63926") # Fundo vermelho

    # Estilização dos campos
    entry_bg = "#F5E9D2"  # Cor de fundo dos inputs

    tk.Label(janela, text="Nome:", bg="#E63926", fg="white", font=("Arial", 12, "bold")).pack(pady=(120, 5))
    entry_cliente = tk.Entry(janela, width=30, font=("Arial", 12), bg=entry_bg, fg="black", relief="flat")
    # entry_cliente.insert(0, "Kaylanne")  # Placeholder
    entry_cliente.pack(ipady=10, pady=5)

    tk.Label(janela, text="Telefone:", bg="#E63926", fg="white", font=("Arial", 12, "bold")).pack(pady=(5))
    entry_telefone = tk.Entry(janela, width=30, font=("Arial", 12), bg=entry_bg, fg="black", relief="flat")
    # entry_telefone.insert(0, "+55 (DD) 0000-0000")  # Placeholder
    entry_telefone.pack(ipady=10, pady=5)

    tk.Label(janela, text="Endereço:", bg="#E63926", fg="white", font=("Arial", 12, "bold")).pack(pady=(5))
    entry_endereco = tk.Entry(janela, width=30, font=("Arial", 12), bg=entry_bg, fg="black", relief="flat")
    # entry_endereco.insert(0, "Rua dois, N-1234...")  # Placeholder
    entry_endereco.pack(ipady=10, pady=5)

    tk.Label(janela, text="Bairro:", bg="#E63926", fg="white", font=("Arial", 12, "bold")).pack(pady=(5))
    entry_bairro = tk.Entry(janela, width=30, font=("Arial", 12), bg=entry_bg, fg="black", relief="flat")
    # entry_bairro.insert(0, "Santo Amaro")  # Placeholder
    entry_bairro.pack(ipady=10, pady=5)

    tk.Button(janela, text="Salvar Cliente", command=lambda: cadastrar_cliente(entry_cliente, entry_telefone, entry_endereco, entry_bairro, janela), bg="green", fg="white").pack(pady=10)

    janela.mainloop()