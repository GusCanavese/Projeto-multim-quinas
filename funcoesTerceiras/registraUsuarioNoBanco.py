import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere


    # é chamado quando é cadastrado um novo usuário
def registraUsuarioNoBanco(self):
    nome = self.nomeFuncionario.get()
    cargo = self.cargo.get()
    login = self.loginFuncionario.get()
    senha = self.senhaFuncionario.get()

    if not nome or not login or not senha : 
        messagebox.showinfo(title="Registro falhou", message="Campos obrigatórios não podem estar em branco")
    else:
        # cata da classe insere, a query que ta sendo feitra la
        Insere.insereUsuarioNoBanco(nome, cargo, login, senha)
        self.frameTelaCadastroFuncionario.destroy()
    