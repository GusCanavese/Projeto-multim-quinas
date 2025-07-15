import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
import gc
from telas.telaAcoes import telaAcoes


def consultarUsuarioCadastrado(self):
    login = self.login.get()
    senha = self.senha.get()
    usuarioLogando = Buscas.consultaUsuario(login, senha)

    if not usuarioLogando:
        self.frameUsuarioNaoCadastrado = ctk.CTkFrame(self, height=100, width=300, corner_radius=5, border_width=2, border_color="red",fg_color="transparent")
        self.frameUsuarioNaoCadastrado.place(relx=0.5, y=600, anchor="center")
        self.usuarioNaoCadastrado = ctk.CTkLabel(self.frameUsuarioNaoCadastrado,  text="Esse usuário não foi encontrado.", font=("Arial", 18))
        self.usuarioNaoCadastrado.place(x=20, y=35)
        self.after(3000, self.frameUsuarioNaoCadastrado.destroy)
        gc.collect

    else:
        telaAcoes(self)
        
