from tkinter import messagebox
import psycopg2

def conectar_bd():
    try:
        conn = psycopg2.connect(
            dbname="pizzaria",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        return conn, cursor
    
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None, None