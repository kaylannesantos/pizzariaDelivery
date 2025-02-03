import tkinter as tk
from PIL import Image, ImageTk
from src.cliente import abrir_tela_cadastro_cliente
from src.registrar import abrir_tela_pedido
from src.historico import RegistroPedido

def home(voltar_para_login):  # Passando a função de voltar para login como parâmetro
    # Criando a janela principal
    root = tk.Tk()
    root.title("Pizza para Você")
    root.geometry("414x800")
    root.configure(bg="#F8F1E4")

    # Criando um frame para conter o Canvas e a Scrollbar
    container = tk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True)

    # Criando um Canvas para rolagem
    canvas = tk.Canvas(container, bg="#F8F1E4", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    frame_principal = tk.Frame(canvas, bg="#F8F1E4")

    # Criando a janela dentro do Canvas
    canvas_frame = canvas.create_window((0, 0), window=frame_principal, anchor="nw", width=414)

    # Configuração da barra de rolagem
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_frame_configure(event):
        """Atualiza a região de rolagem do canvas"""
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_principal.bind("<Configure>", on_frame_configure)

    # Vincular evento de rolagem do mouse
    def on_mouse_wheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Posicionamento do Canvas e Scrollbar
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Criando um frame para o topo
    top_frame = tk.Frame(frame_principal, bg="#E63926", height=50)
    top_frame.pack(fill=tk.X, pady=2)

    # Criando um frame para as imagens
    img_frame = tk.Frame(frame_principal, bg="#F8F1E4")
    img_frame.pack(pady=2)

    # Carregar imagem do chef
    img = Image.open("src/images/chef.png")  
    img = img.resize((300, 300))
    chef_img = ImageTk.PhotoImage(img)

    chef_label = tk.Label(img_frame, image=chef_img, bg="#F8F1E4")
    chef_label.image = chef_img  
    chef_label.pack(pady=2)

    # Carregar imagem da pizza
    img = Image.open("src/images/home_pizza.png")  
    img = img.resize((300, 300))
    home_pizza_img = ImageTk.PhotoImage(img)

    pizza_label = tk.Label(img_frame, image=home_pizza_img, bg="#F8F1E4")
    pizza_label.image = home_pizza_img  
    pizza_label.pack(pady=2)

    # Funções para fechar a janela antes de abrir a nova tela
    def abrir_pedidos():
        root.destroy()
        abrir_tela_pedido()

    def abrir_cadastro():
        root.destroy()
        abrir_tela_cadastro_cliente()

    def abrir_historico():
        root.destroy()
        RegistroPedido()

    def sair_da_aplicacao():
        root.destroy()  # Fecha a janela home
        voltar_para_login()  # Chama a função que volta para a tela de login

    # Botões com espaçamentos menores
    btn_style = {"font": ("Arial", 12, "bold"), "width": 25, "height": 2, "bd": 0}

    btn_pedidos = tk.Button(frame_principal, text="Registre seus pedidos", bg="#E6C07B", command=abrir_pedidos, **btn_style)
    btn_pedidos.pack(pady=2)

    btn_clientes = tk.Button(frame_principal, text="Cadastre seus clientes", bg="#E6A23C", command=abrir_cadastro, **btn_style)
    btn_clientes.pack(pady=2)

    btn_historico = tk.Button(frame_principal, text="Histórico dos Pedidos", bg="#E6A23C", command=abrir_historico, **btn_style)
    btn_historico.pack(pady=2)

    # Botão de Sair (voltar para o login)
    btn_sair = tk.Button(frame_principal, text="Sair", bg="#E63926", command=sair_da_aplicacao, **btn_style)
    btn_sair.pack(pady=2)

    root.mainloop()