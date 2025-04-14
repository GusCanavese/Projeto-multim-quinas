import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox
from consultas.update import Atualiza


def confirmarAlteracoesNoPedido(self, dataConfirmacao, identificador):
    if dataConfirmacao=='':
        messagebox.showerror('a',"A data de confirmação deve ser preenchida no modelo dd/mm/aa")
    else:
        resposta = messagebox.askquestion(
            "Confirmação",
            "Você irá alteral dados no pedido, deseja continuar?",
            icon='question'
        )
        if resposta == "yes":
            Atualiza.atualizaPedido(identificador)
            