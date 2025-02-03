import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from src.database.db import conectar_bd
from src.pagamento import confirmar_pagamento
from src.cliente import abrir_tela_cadastro_cliente


dados_pedido_temp = {}  # Variável para armazenar temporariamente os dados do pedido

def enviar_pedido_para_pagamento(entry_cliente, entry_endereco, tamanho_var, combo_sabor, entry_quantidade):
    print("Função enviar_pedido_para_pagamento chamada")  # Verifique se entra aqui
    
    global dados_pedido_temp
    cliente = entry_cliente.get()
    endereco = entry_endereco.get()
    tamanho = tamanho_var.get()
    sabor_nome = combo_sabor.get()
    quantidade = entry_quantidade.get()
    
    if not cliente or not endereco or not sabor_nome or not quantidade:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return
    
    try:
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
    except ValueError as e:
        messagebox.showerror("Erro", f"Erro na quantidade de pizzas: {e}")
        return

    conn, cursor = conectar_bd()

    # Buscar o valor do sabor (para buscar o sabor pelo nome)
    cursor.execute("SELECT id FROM sabores WHERE nome = %s", (sabor_nome,))
    sabor = cursor.fetchone()
    
    if not sabor:
        messagebox.showerror("Erro", "Sabor não encontrado no banco de dados!")
        return
    
    sabor_id = sabor[0]
    
    # Agora, vamos buscar o valor do tamanho selecionado
    cursor.execute("SELECT valor FROM tamanho WHERE nome = %s", (tamanho,))
    tamanho_info = cursor.fetchone()
    
    if not tamanho_info:
        messagebox.showerror("Erro", "Tamanho não encontrado no banco de dados!")
        return
    
    valor_unitario = tamanho_info[0]
    valor_total = valor_unitario * quantidade
    
    cursor.close()
    conn.close()

    # Armazenando os dados temporariamente
    dados_pedido_temp = {
        "cliente": cliente,
        "endereco": endereco,
        "tamanho": tamanho,
        "sabor_id": sabor_id,
        "sabor_nome": sabor_nome,
        "quantidade": quantidade,
        "valor_total": valor_total
    }

    # Debug para garantir que os dados foram preenchidos corretamente
    print("Dados do pedido em dados_pedido_temp:", dados_pedido_temp)

    # Passando os dados do pedido para a função de pagamento
    print("Cliente:", cliente)
    print("Endereço:", endereco)
    print("Tamanho:", tamanho)
    print("Sabor:", sabor_nome)
    print("Quantidade:", quantidade)
    confirmar_pagamento(dados_pedido_temp)

def abrir_tela_pedido():
    global entry_cliente
    # Criando a janela principal
    pedido_tela = tk.Toplevel()
    pedido_tela.title("Fazer Pedido")
    pedido_tela.geometry("414x800")
    pedido_tela.configure(bg="#F8F1E4")

    # Criar um canvas e um frame de rolagem
    canvas = tk.Canvas(pedido_tela, bg="#F8F1E4")
    scrollbar = ttk.Scrollbar(pedido_tela, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#F8F1E4")

    scroll_frame.bind(
        "<Configure>", 
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")  # Ajusta a área rolável
        )
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Frame superior (faixa laranja)
    top_frame = tk.Frame(scroll_frame, bg="#E63926", height=50)
    top_frame.pack(fill=tk.X)

    # Carregar imagem do logo "Online Pizza"
    img_logo = Image.open("src/images/on_pizza.png")  # Caminho correto da imagem
    img_logo = img_logo.resize((400, 128))
    logo_img = ImageTk.PhotoImage(img_logo)

    logo_label = tk.Label(scroll_frame, image=logo_img, bg="#F8F1E4")
    logo_label.pack(pady=10)

    # Título "Escolha sua pizza"
    titulo_label = tk.Label(scroll_frame, text="Escolha sua pizza", font=("Arial", 16, "bold"), bg="#F8F1E4", fg="black")
    titulo_label.pack(pady=5)

    # Carregar imagem da pizza
    img_pizza = Image.open("src/images/pizza.jpg")  # Caminho correto da imagem
    img_pizza = img_pizza.resize((350, 200))
    pizza_img = ImageTk.PhotoImage(img_pizza)

    pizza_label = tk.Label(scroll_frame, image=pizza_img, bg="#F8F1E4")
    pizza_label.pack(pady=10)

    # Manter referências das imagens
    scroll_frame.logo_img = logo_img
    scroll_frame.pizza_img = pizza_img

    # 🔸 Frame para o formulário (Nome e Endereço)
    frame_form = tk.Frame(scroll_frame, bg="#F8F1E4")
    frame_form.pack(pady=10)

    # 🔸 Nome Cliente
    label_cliente = tk.Label(frame_form, text="Nome do Cliente:", font=("Arial", 12, "bold"))
    label_cliente.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # 🔸 Campo Nome Cliente
    entry_cliente = tk.Entry(frame_form, width=30, font=("Arial", 12))
    entry_cliente.grid(row=1, column=0, padx=5, pady=5)

    # 🔸 Botão para verificar cliente
    btn_verificar = tk.Button(frame_form, text="Verificar Cliente", command=lambda: verificar_cliente(entry_endereco),
                            bg="orange", fg="black", font=("Arial", 10, "bold"), padx=5, pady=2)
    btn_verificar.grid(row=1, column=1, padx=5, pady=5)

    # 🔹 Endereço
    label_endereco = tk.Label(frame_form, text="Endereço", font=("Arial", 12, "bold"), bg="#F8F1E4")
    label_endereco.grid(row=2, column=0, sticky="w", padx=5, pady=5)

    # 🔹 Campo Endereço
    entry_endereco = tk.Entry(frame_form, width=40, font=("Arial", 12))
    entry_endereco.grid(row=3, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5)
    
    # 🔹 Seleção de Sabores (Usando Combobox)
    label_sabor = tk.Label(frame_form, text="Selecione o sabor", font=("Arial", 12, "bold"), bg="#F8F1E4")
    label_sabor.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

    combo_sabor = ttk.Combobox(frame_form, width=40, font=("Arial", 12))
    combo_sabor.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Carregar sabores do banco de dados
    sabores = carregar_sabores()
    combo_sabor['values'] = sabores
    combo_sabor.set(sabores[0])  # Define o valor padrão, por exemplo, o primeiro sabor

    # 🔹 Seleção de Tamanho (Usando Combobox)
    label_tamanho = tk.Label(frame_form, text="Selecione o tamanho", font=("Arial", 12, "bold"), bg="#F8F1E4")
    label_tamanho.grid(row=6, column=0, columnspan=2, pady=10)

    tamanho_var = tk.StringVar(value="Média")
    tamanhos = carregar_tamanhos()

    # Formatar os tamanhos para incluir as informações adicionais (fatias, cm, valor)
    tamanhos_formatados = [nome for nome, in tamanhos] 

    tamanho_combo = ttk.Combobox(frame_form, textvariable=tamanho_var, values=tamanhos_formatados, width=40, font=("Arial", 12))
    tamanho_combo.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    # 🔸 Campo Quantidade
    label_quantidade = tk.Label(frame_form, text="Quantidade", font=("Arial", 12, "bold"), bg="#F8F1E4")
    label_quantidade.grid(row=8, column=0, padx=5, pady=5, sticky="w")

    entry_quantidade = tk.Entry(frame_form, width=40, font=("Arial", 12))
    entry_quantidade.grid(row=9, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5)

    # Botão para confirmar e avançar
    btn_confirmar = tk.Button(frame_form, text="Confirmar Pagamento", command=lambda: enviar_pedido_para_pagamento(entry_cliente, entry_endereco, tamanho_var, combo_sabor, entry_quantidade),
                              bg="green", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)

    btn_confirmar.grid(row=12, column=0, columnspan=2, pady=10)

    pedido_tela.mainloop()

def carregar_sabores():
    conn, cursor = conectar_bd()  # Correção aqui
    if not conn or not cursor:
        return []
    cursor.execute("SELECT nome FROM sabores")  # Pegando nomes dos sabores
    sabores = cursor.fetchall()
    conn.close()
    return [sabor[0] for sabor in sabores]

def carregar_tamanhos():
    conn, cursor = conectar_bd()
    if not conn or not cursor:
        return []
    cursor.execute("SELECT nome FROM tamanho")  # Pegando apenas o nome dos tamanhos
    tamanhos = cursor.fetchall()
    conn.close()
    return tamanhos

def verificar_cliente(entry_endereco):
    nome_cliente = entry_cliente.get()
    if not nome_cliente:
        messagebox.showerror("Erro", "Digite o nome do cliente!")
        return
    
    conn, cursor = conectar_bd()
    if not conn or not cursor:
        return []
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
        abrir_tela_cadastro_cliente()