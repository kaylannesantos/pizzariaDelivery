import tkinter as tk
from tkinter import messagebox
from src.database.db import conectar_bd

class RegistroPedido(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Registro de Pedido")
        self.geometry("414x800")
        self.configure(bg="#F4F2DE")

        # Conectar ao banco de dados
        self.conn, self.cursor = conectar_bd()  # Usando a função conectar_bd() para obter a conexão e o cursor
        if self.conn is None:
            print("Falha ao conectar ao banco de dados.")
            return  # Se não conseguir conectar, não continua a execução do código

        # Criando o frame principal e o canvas para rolagem
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg="#F4F2DE", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

        frame_principal = tk.Frame(canvas, bg="#F4F2DE")

        # Criando a janela dentro do Canvas
        canvas.create_window((0, 0), window=frame_principal, anchor="nw", width=414)

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
        
        # Barra superior (simulando a "status bar")
        top_bar = tk.Frame(frame_principal, bg="#E6361D", height=56)
        top_bar.pack(fill="x", pady=10)

        # Posicionamento do Canvas e Scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Título
        title_label = tk.Label(frame_principal, text="Registro de Pedido", font=("Montserrat", 25, 'bold'), fg="black", bg="#F4F2DE")
        title_label.pack(pady=20, anchor="w", padx=15)

        # Carregar pedidos do banco de dados
        self.carregar_pedidos(frame_principal)

    def carregar_pedidos(self, frame_principal):
        # Buscar todos os pedidos no banco de dados
        query = """
        SELECT p.id, c.nome, s.nome AS sabor, t.nome AS tamanho, p.data_hora, p.valor_total
        FROM pedidos p
        JOIN clientes c ON c.nome = p.cliente
        JOIN sabores s ON s.id = p.id_sabor
        JOIN tamanho t ON t.id = p.id_tamanho
        ORDER BY p.data_hora DESC;
        """
        self.cursor.execute(query)
        pedidos = self.cursor.fetchall()

        # Criar um Frame para cada pedido
        for pedido in pedidos:
            pedido_id, cliente_nome, sabor, tamanho, data_hora, valor_total = pedido

            # Frame para cada pedido
            pedido_frame = tk.Frame(frame_principal, bg="white", bd=0, relief="solid", padx=16, pady=16)
            pedido_frame.pack(fill="x", pady=5, padx=10)

            # Informações do pedido
            pedido_info = tk.Label(pedido_frame, text=f"Cliente: {cliente_nome} - {pedido_id}\nPizza: {sabor} - {tamanho}",
                                   font=("Lusitana", 13, 'bold'), fg="#2B3241", anchor="w")
            pedido_info.pack(fill="x")

            # Valor do pedido
            valor_label = tk.Label(pedido_frame, text=f"R${valor_total:.2f}", font=("Inter", 14, 'bold'), fg="#2B3241")
            valor_label.place(relx=1.0, x=-12, y=8, anchor="ne")

            # Data e Hora do pedido
            data_label = tk.Label(pedido_frame, text=f"Data: {data_hora.strftime('%d/%m/%Y  %H:%M')}", font=("Inter", 9), fg="#798397", anchor="w")
            data_label.pack(fill="x", pady=4)

    def ver_pedido(self, pedido):
        """Abrir uma nova janela para exibir detalhes do pedido"""
        pedido_id, cliente_nome, sabor, tamanho, data_hora, valor_total = pedido

        # Criar uma nova janela para exibir os detalhes do pedido
        detalhes_janela = tk.Toplevel(self)
        detalhes_janela.title(f"Detalhes do Pedido {pedido_id}")
        detalhes_janela.geometry("414x800")
        detalhes_janela.configure(bg="#F4F2DE")

        # Adicionar informações do pedido na nova janela
        title_label = tk.Label(detalhes_janela, text="Detalhes do Pedido", font=("Montserrat", 20, 'bold'), fg="black", bg="#F4F2DE")
        title_label.pack(pady=20)

        cliente_label = tk.Label(detalhes_janela, text=f"Cliente: {cliente_nome}", font=("Lusitana", 14), fg="#2B3241", anchor="w", bg="#F4F2DE")
        cliente_label.pack(fill="x", pady=5)

        sabor_label = tk.Label(detalhes_janela, text=f"Sabor: {sabor}", font=("Lusitana", 14), fg="#2B3241", anchor="w", bg="#F4F2DE")
        sabor_label.pack(fill="x", pady=5)

        tamanho_label = tk.Label(detalhes_janela, text=f"Tamanho: {tamanho}", font=("Lusitana", 14), fg="#2B3241", anchor="w", bg="#F4F2DE")
        tamanho_label.pack(fill="x", pady=5)

        valor_label = tk.Label(detalhes_janela, text=f"Valor Total: R${valor_total:.2f}", font=("Lusitana", 14), fg="#2B3241", anchor="w", bg="#F4F2DE")
        valor_label.pack(fill="x", pady=5)

        data_label = tk.Label(detalhes_janela, text=f"Data/Hora: {data_hora.strftime('%d/%m/%Y %H:%M')}", font=("Lusitana", 12), fg="#798397", anchor="w", bg="#F4F2DE")
        data_label.pack(fill="x", pady=5)

        # Botão para fechar a janela
        close_btn = tk.Button(detalhes_janela, text="Fechar", bg="#E31837", fg="white", font=("Raleway", 12, 'bold'),
                              relief="solid", borderwidth=2, padx=16, pady=8, command=detalhes_janela.destroy)
        close_btn.pack(pady=20)

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    app = RegistroPedido()
    app.mainloop()