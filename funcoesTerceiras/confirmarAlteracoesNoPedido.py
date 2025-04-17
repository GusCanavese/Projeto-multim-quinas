import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox
from consultas.update import Atualiza


def confirmarHoje(self, identificador):
    resposta = messagebox.askquestion('Aviso!', 'A o pedido será confirmado com a data de hoje, deseja prosseguir?', icon='question')
    if resposta == 'yes':
        Atualiza.atualizaPedido(identificador)
        self.frameTelaVerPedidos.destroy()
    else:
        pass
   
#!essa função ta imcompleta
def confirmarAlteracoesNoPedido(self, dataConfirmacao, identificador):
    if dataConfirmacao == '':
        messagebox.showerror('Erro', 'A a data de confirmação deve ser no formato dd/mm/aaaa')
    else:
        resposta = messagebox.askquestion(
            "Confirmação",
            "Você irá alterar dados no pedido, deseja continuar?",
            icon='question'
        )
        if resposta == "yes":
            Atualiza.atualizaPedido(identificador)