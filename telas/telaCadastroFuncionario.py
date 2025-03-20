import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.registraUsuarioNoBanco import registraUsuarioNoBanco


def telaCadastroFuncionario(self):
    self.frameTelaCadastroFuncionario = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
    self.frameTelaCadastroFuncionario.place(x=140, y=100)     
    self.frameTelaCadastroFuncionario.grid_propagate(False)


    # ================ widgets da tela cadastro =====================#
    # titulo
    self.textoCadastro = ctk.CTkLabel(self.frameTelaCadastroFuncionario, width=950, height=0, text="Cadastrar funcionário", font=("Century Gothic bold", 30))
    self.textoCadastro.grid(row=0, column=0, padx=10, pady=20)

    # nome
    self.labelNomeFuncionario = ctk.CTkLabel(self.frameTelaCadastroFuncionario, text="Nome", font=("Century Gothic bold", 15))
    self.labelNomeFuncionario.place(x=100, y=100)
    self.nomeFuncionario = ctk.CTkEntry(self.frameTelaCadastroFuncionario, placeholder_text="nomeFuncionario", width=350, corner_radius=5, font=("Century Gothic bold", 20))
    self.nomeFuncionario.place(x=100, y=130)

    # login
    self.labelLogin = ctk.CTkLabel(self.frameTelaCadastroFuncionario, text="Login para acesso*", font=("Century Gothic bold", 15))   
    self.labelLogin.place(x=100, y=200)
    self.loginFuncionario = ctk.CTkEntry(self.frameTelaCadastroFuncionario, placeholder_text="Login", width=350, corner_radius=5, font=("Century Gothic bold", 20))
    self.loginFuncionario.place(x=100, y=230)

    # senha
    self.labelSenha = ctk.CTkLabel(self.frameTelaCadastroFuncionario, text="Senha para acesso*", font=("Century Gothic bold", 15))
    self.labelSenha.place(x=550, y=200)
    self.senhaFuncionario = ctk.CTkEntry(self.frameTelaCadastroFuncionario, placeholder_text="Senha", width=350, corner_radius=5, font=("Century Gothic bold", 20))
    self.senhaFuncionario.place(x=550, y=230)

    # cargo
    self.labelCargo = ctk.CTkLabel(self.frameTelaCadastroFuncionario, text="Cargo", font=("Century Gothic bold", 15))   
    self.labelCargo.place(x=550, y=100)
    opcoes = ["Gerente", "Vendedor(a) interno", "Vendedor(a) externo", "Financeiro"]
    self.cargo = ctk.CTkComboBox(self.frameTelaCadastroFuncionario, width=350, corner_radius=5, font=("Century Gothic bold", 20), values=opcoes)
    self.cargo.place(x=550, y=130)

    # ============== Botões =============== #
    # voltar
    self.botaoVoltar = ctk.CTkButton(self.frameTelaCadastroFuncionario, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaCadastroFuncionario.destroy)
    self.botaoVoltar.place(x=200, y=600)
    
    # registra no bd
    self.botaoCadastrarUsuario = ctk.CTkButton(self.frameTelaCadastroFuncionario, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=lambda:registraUsuarioNoBanco(self))
    self.botaoCadastrarUsuario.place(x=600, y=600)
