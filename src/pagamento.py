import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from src.database.db import conectar_bd

def confirmar_pagamento(dados_pedido):
    if not dados_pedido:
        messagebox.showerror("Erro", "Nenhum pedido encontrado!")
        return
    
    # Debug para verificar os dados recebidos
    print("Dados do pedido no pagamento:", dados_pedido)
    
    cliente = dados_pedido['cliente']
    endereco = dados_pedido['endereco']
    sabor = dados_pedido['sabor_nome']
    tamanho = dados_pedido['tamanho']
    valor_tamanho = dados_pedido['valor_total'] / dados_pedido['quantidade']
    quantidade = dados_pedido['quantidade']
    
    def atualizar_total():
        nova_quantidade = int(quantidade_var.get())
        total = valor_tamanho * nova_quantidade
        total_label.config(text=f"R$ {total:.2f}")
    
    def aumentar_quantidade():
        quantidade_var.set(quantidade_var.get() + 1)
        atualizar_total()
    
    def diminuir_quantidade():
        if quantidade_var.get() > 1:
            quantidade_var.set(quantidade_var.get() - 1)
            atualizar_total()
    
    def voltar():
        janela_pagamento.destroy()
    
    def pagar():
        conn, cursor = conectar_bd()
        
        if not conn or not cursor:
            return []

        total_pedido = valor_tamanho * quantidade_var.get()
        cursor.execute("INSERT INTO pedidos (cliente, endereco, id_sabor, id_tamanho, quantidade, valor_total) VALUES (%s, %s, (SELECT id FROM sabores WHERE nome=%s), (SELECT id FROM tamanho WHERE nome=%s), %s, %s)",
                       (cliente, endereco, sabor, tamanho, quantidade_var.get(), total_pedido))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Pagamento realizado com sucesso!")
        janela_pagamento.destroy()
    
    janela_pagamento = tk.Toplevel()
    janela_pagamento.title("Total do Pedido")
    janela_pagamento.geometry("414x800")
    janela_pagamento.configure(bg="#F8F1E4")
    
    header = tk.Frame(janela_pagamento, bg="#E63926", height=60)
    header.pack(fill=tk.X)
    
    btn_voltar = tk.Button(header, text="←", command=voltar, font=("Arial", 14), bg="#E63926", fg="white", border=0)
    btn_voltar.place(x=10, y=15)
    
    tk.Label(janela_pagamento, text="Total do Pedido", font=("Arial", 16, "bold"), bg="#F8F1E4").pack(pady=10)
    
    frame_pedido = tk.Frame(janela_pagamento, bg="white", relief=tk.RIDGE, borderwidth=2)
    frame_pedido.pack(pady=10, padx=10, fill=tk.X)
    
    try:
        img_pizza = Image.open("src/images/pizza_pag.png")
        img_pizza = img_pizza.resize((100, 100))
        pizza_img = ImageTk.PhotoImage(img_pizza)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar imagem: {e}")
        return
    
    lbl_img = tk.Label(frame_pedido, image=pizza_img, bg="white")
    lbl_img.image = pizza_img
    lbl_img.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
    
    tk.Label(frame_pedido, text="Pizza", font=("Arial", 20, "bold"), fg="red", bg="white").grid(row=0, column=1, sticky="w")
    tk.Label(frame_pedido, text=f"Sabor: {sabor}", font=("Arial", 12), bg="white").grid(row=1, column=1, sticky="w")
    tk.Label(frame_pedido, text=f"Tamanho: {tamanho}", font=("Arial", 12), bg="white").grid(row=2, column=1, sticky="w")
    
    quantidade_var = tk.IntVar(value=quantidade)
    frame_qtd = tk.Frame(frame_pedido, bg="white")
    frame_qtd.grid(row=1, column=2, padx=10)
    
    btn_menos = tk.Button(frame_qtd, text="-", command=diminuir_quantidade, bg="red", fg="white", width=2)
    btn_menos.pack(side=tk.LEFT)
    tk.Label(frame_qtd, textvariable=quantidade_var, width=3, font=("Arial", 12), bg="white").pack(side=tk.LEFT)
    btn_mais = tk.Button(frame_qtd, text="+", command=aumentar_quantidade, bg="red", fg="white", width=2)
    btn_mais.pack(side=tk.LEFT)
    
    frame_total = tk.Frame(janela_pagamento, bg="white", relief=tk.RIDGE, borderwidth=2)
    frame_total.pack(pady=10, padx=10, fill=tk.X)
    
    tk.Label(frame_total, text="Informações", font=("Arial", 12, "bold"), bg="white").pack()
    tk.Label(frame_total, text=f"Pizza {sabor} - R$ {valor_tamanho:.2f}", bg="white").pack()
    
    tk.Label(frame_total, text="Total", font=("Arial", 12, "bold"), fg="red", bg="white").pack()
    total_label = tk.Label(frame_total, text=f"R$ {valor_tamanho * quantidade:.2f}", font=("Arial", 12, "bold"), bg="white")
    total_label.pack()
    
    frame_botoes = tk.Frame(janela_pagamento, bg="#F8F1E4")
    frame_botoes.pack(pady=20)
    
    btn_cancelar = tk.Button(frame_botoes, text="Cancelar", fg="white", bg="red", font=("Arial", 12, "bold"), width=10, command=voltar)
    btn_cancelar.pack(side=tk.LEFT, padx=10)
    
    btn_pagar = tk.Button(frame_botoes, text="Pagar", fg="white", bg="green", font=("Arial", 12, "bold"), width=10, command=pagar)
    btn_pagar.pack(side=tk.RIGHT, padx=10)
    
    janela_pagamento.mainloop()