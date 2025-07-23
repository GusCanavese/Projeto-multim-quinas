import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.registraUsuarioNoBanco import registraUsuarioNoBanco
from componentes import criaFrame, criaFrameJanela, criarLabelComboBox, criarLabelEntry, criaBotao
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries


def telaCadastroFuncionario(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)

    opcoes = ["Gerente", "Vendedor(a) interno", "Vendedor(a) externo", "Financeiro"]


    self.textoCadastro = ctk.CTkLabel(frame, width=950, height=0, text="Cadastrar funcionário", font=("Century Gothic bold", 30))
    self.textoCadastro.place(relx=0.5, rely=0.03, anchor="center")

    self.nomeFuncionario  = criarLabelEntry(frame, "Nome", 0.15, 0.14, 0.3, None)
    self.senhaFuncionario = criarLabelEntry(frame, "Senha para acesso*", 0.55, 0.14, 0.3, None)
    self.loginFuncionario = criarLabelEntry(frame, "Login para acesso*", 0.15, 0.28, 0.3, None)
    self.cargo = criarLabelComboBox(frame, "Cargo*", 0.55, 0.28, 0.3, opcoes)


    criaBotao(frame, "Voltar", 0.3, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.68, 0.80, 0.20, lambda:registraUsuarioNoBanco(self, frame))
    aplicar_maiusculo_em_todos_entries(self)

