from src.home import home
from src.login import criar_tela_login, autenticar
from src.cliente import abrir_tela_cadastro_cliente
from src.registrar import abrir_tela_pedido
from src.historico import RegistroPedido

def main():
    # Função de callback para verificar o login
    def verificar_login():
        if autenticar():
            home(voltar_para_login)  # Passando a função para voltar para login quando sair da home

    # Função para voltar para a tela de login
    def voltar_para_login():
        criar_tela_login(verificar_login)  # Chama a tela de login novamente

    # Inicia a tela de login
    criar_tela_login(verificar_login)  # Passa a função que valida o login

if __name__ == "__main__":
    main()