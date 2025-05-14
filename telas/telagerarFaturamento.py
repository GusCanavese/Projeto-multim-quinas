
    # def verificaParcelas(self, valor):
    #     print(valor)
    #     if valor != "a vista":
    #         self.labelQtdParcelas = ctk.CTkLabel(self.frameTelaGerarOrcamento,  text="QTD parcelas", font=("Century Gothic bold", 14))
    #         self.labelQtdParcelas.place(x=250, y=235)
    #         self.QtdParcelas = ctk.CTkEntry(self.frameTelaGerarOrcamento, width=180, corner_radius=5, font=("Arial", 15))
    #         self.QtdParcelas.place(x=250, y=260)

    #     else:
    #         if hasattr(self, "QtdParcelas"):
    #             self.labelQtdParcelas.destroy()
    #             del self.labelQtdParcelas
    #             self.QtdParcelas.destroy()
    #         else:
    #             pass

    # opcoesPagamento = ["a vista", "cartão a prazo", "boleto a prazo"]
    # self.labelformaDePagamento = ctk.CTkLabel(self.frameTelaGerarOrcamento,  text="Forma de pagamento", font=("Century Gothic bold", 14))
    # self.labelformaDePagamento.place(relx=470/largura, y=235)
    # self.formaDePagamento = ctk.CTkComboBox(self.frameTelaGerarOrcamento,values=opcoesPagamento, width=180, corner_radius=5, font=("Arial", 15), command=lambda valor:verificaParcelas(self, valor))
    # self.formaDePagamento.place(relx=470/largura, y=260)


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.consultarUsuarioCadastrado import consultarUsuarioCadastrado


def telaGerarFaturamento(self):
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
