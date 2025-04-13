import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox


def confirmarAlteracoesNoPedido(self, dataConfirmacao):
    if dataConfirmacao=='':
        messagebox.ERROR("A data de confirmação deve ser preenchida no modelo dd/mm/aa")
    else:
        resposta = messagebox.askquestion(
            "Confirmação",
            "Você irá alteral dados no pedido, deseja continuar?",
            icon='question'
        )
        if resposta == "yes":
            pass
            