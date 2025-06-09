import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.consultarUsuarioCadastrado import consultarUsuarioCadastrado
from componentes import criaFrame


def telaLogin(self):
    self.title("login")

    # Frame centralizado com place(relx, rely)
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)

    self.texto = ctk.CTkLabel(frame, width=1000, height=100, text="Fazer Login", font=("Century Gothic bold", 35))
    self.texto.place(relx=0.5, rely=0.2857, anchor="center")

    self.login = ctk.CTkEntry(frame, placeholder_text="Login", width=400, corner_radius=5, font=("Century Gothic bold", 25))
    self.login.place(relx=0.5, rely=0.4286, anchor="center")

    self.senha = ctk.CTkEntry(frame, placeholder_text="Senha", width=400, corner_radius=5, font=("Century Gothic bold", 25), show="*")
    self.senha.place(relx=0.5, rely=0.5, anchor="center")

    self.botaoEntrar = ctk.CTkButton(frame, text="Entrar", width=200, corner_radius=5, font=("Arial", 20), command=lambda:consultarUsuarioCadastrado(self))
    self.botaoEntrar.place(relx=0.5, rely=0.6, anchor="center")
