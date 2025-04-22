import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.consultarUsuarioCadastrado import consultarUsuarioCadastrado


def telaLogin(self):
    self.title("login")

    # Frame centralizado com place(relx, rely)
    self.frameTelaLogin = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
    self.frameTelaLogin.place(relx=0.5, rely=0.5, anchor="center")  # Centraliza o frame
    self.frameTelaLogin.grid_propagate(False)

    # Título
    self.texto = ctk.CTkLabel(self.frameTelaLogin, width=1000, height=100, text="Fazer Login", font=("Century Gothic bold", 35))
    self.texto.place(relx=0.5, rely=0.2857, anchor="center")

    # Input de login
    self.login = ctk.CTkEntry(self.frameTelaLogin, placeholder_text="Login", width=400, corner_radius=5, font=("Century Gothic bold", 25))
    self.login.place(relx=0.5, rely=0.4286, anchor="center")

    # Input de senha
    self.senha = ctk.CTkEntry(self.frameTelaLogin, placeholder_text="Senha", width=400, corner_radius=5, font=("Century Gothic bold", 25), show="*")
    self.senha.place(relx=0.5, rely=0.5, anchor="center")

    # Botão para entrar
    self.botaoEntrar = ctk.CTkButton(self.frameTelaLogin, text="Entrar", width=200, corner_radius=5, font=("Arial", 20), command=lambda:consultarUsuarioCadastrado(self))
    self.botaoEntrar.place(relx=0.5, rely=0.6, anchor="center")
