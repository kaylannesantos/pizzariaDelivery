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
