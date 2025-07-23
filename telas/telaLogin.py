import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.consultarUsuarioCadastrado import consultarUsuarioCadastrado
from componentes import criaFrame, criaFrameJanela


def telaLogin(self):
    self.title("GestUp")
    self.switch_var = ctk.BooleanVar()

        # Define modo inicial com base no sistema
    # Inicializa modo como system, mas define cor padrão temporária
    ctk.set_appearance_mode("system")
    self.corFundo = "#d0d0d0"  # cor intermediária neutra
    self.switch_var = ctk.BooleanVar(value=False)

    # Frame inicial
    self.frame_login = criaFrameJanela(self, 0.5, 0.5, 0.94, 0.9, self.corFundo)

    # Depois de um pequeno tempo, define a cor correta baseada no modo real
    def aplicar_cor_do_sistema():
        modo_atual = ctk.get_appearance_mode()
        if modo_atual == "Dark":
            self.configure(fg_color="#242424")
            self.corFundo = "#2b2b2b"
            self.cor = "#5a3e3e"
            self.corNegado = "#922B21"
            self.corAfirma = "#196F3D"

            self.switch_var.set(True)
            
        else:
            self.configure(fg_color="#eaeaea")
            self.corFundo = "#eaeaea"
            self.cor = "#3b8ed0"
            self.corNegado = "#DB2E2E"
            self.corAfirma = "#14B457"

            self.switch_var.set(False)
        self.frame_login.configure(fg_color=self.corFundo)

    self.after(100, aplicar_cor_do_sistema)


    # Cria o frame com a cor inicial
    self.frame_login = criaFrameJanela(self, 0.5, 0.5, 0.94, 0.9, self.corFundo)

    # Widgets da tela de login
    self.texto = ctk.CTkLabel(self.frame_login, width=1000, height=100, text="Fazer Login", font=("Century Gothic bold", 35))
    self.texto.place(relx=0.5, rely=0.2857, anchor="center")

    self.login = ctk.CTkEntry(self.frame_login, placeholder_text="Login", width=400, corner_radius=5, font=("Century Gothic bold", 25))
    self.login.place(relx=0.5, rely=0.4286, anchor="center")

    self.senha = ctk.CTkEntry(self.frame_login, placeholder_text="Senha", width=400, corner_radius=5, font=("Century Gothic bold", 25), show="*")
    self.senha.place(relx=0.5, rely=0.5, anchor="center")

    self.botaoEntrar = ctk.CTkButton(self.frame_login, text="Entrar", width=200, corner_radius=5, font=("Arial", 20), command=lambda: consultarUsuarioCadastrado(self))
    self.botaoEntrar.place(relx=0.5, rely=0.6, anchor="center")

    # Switch de tema claro/escuro

    def mudar_estado():
        if self.switch_var.get():
            ctk.set_appearance_mode("dark")
            self.configure(fg_color="#242424")
            self.corFundo = "#2b2b2b"
            self.cor = "#5a3e3e"
            self.corNegado = "#922B21"
            self.corAfirma = "#196F3D"
            
        else:
            ctk.set_appearance_mode("light")
            self.configure(fg_color="#DFDFDF")
            self.corFundo = "#C6C6C6"
            self.cor = "#3b8ed0"
            self.corNegado = "#DB2E2E"
            self.corAfirma = "#358356"

        # Atualiza cor do frame manualmente
        self.frame_login.configure(fg_color=self.corFundo)

    switch = ctk.CTkSwitch(self.frame_login, text="Tema claro/escuro", variable=self.switch_var, command=mudar_estado)
    switch.place(relx=0.44, rely=0.7)

    # Atalhos de teclado para login
    self.login.bind("<Return>", lambda event: consultarUsuarioCadastrado(self))
    self.senha.bind("<Return>", lambda event: consultarUsuarioCadastrado(self))
