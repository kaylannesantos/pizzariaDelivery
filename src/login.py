import tkinter as tk
from tkinter import messagebox

# Função de autenticação (simulação)
def autenticar():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    if usuario == "admin" and senha == "123":
        tela_login.destroy()  # Fecha a janela de login
        return True
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")
        return False

# Criando a janela de login
def criar_tela_login(callback):
    global tela_login, entry_usuario, entry_senha

    tela_login = tk.Tk()
    tela_login.title("Login - Pizzaria")
    tela_login.geometry("414x800")
    tela_login.resizable(False, False)
    tela_login.configure(bg="#E63926")  # Fundo vermelho

    # Estilização dos campos
    entry_bg = "#F5E9D2"  # Cor de fundo dos inputs
    entry_fg = "#A89F91"  # Cor do placeholder
    btn_bg = "#FFFFFF"  # Cor do botão
    btn_fg = "#E63926"  # Cor do texto do botão

    # Campo Usuário
    tk.Label(tela_login, text="Usuário", bg="#E63926", fg="white", font=("Arial", 12, "bold")).pack(pady=(120, 5))
    entry_usuario = tk.Entry(tela_login, width=30, font=("Arial", 12), bg=entry_bg, fg="black", relief="flat")
    entry_usuario.pack(ipady=10, pady=5)

    # Campo Senha
    tk.Label(tela_login, text="Senha", bg="#E63926", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
    entry_senha = tk.Entry(tela_login, width=30, font=("Arial", 12), bg=entry_bg, fg="black", relief="flat", show="*")
    entry_senha.pack(ipady=10, pady=5)

    # Botão de Login
    btn_login = tk.Button(tela_login, text="LOGIN", command=lambda: callback(), font=("Arial", 12, "bold"), bg=btn_bg, fg=btn_fg, relief="flat")
    btn_login.pack(pady=20, ipadx=50, ipady=10)

    tela_login.mainloop()