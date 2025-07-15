import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox
from consultas.delete import deleta
from consultas.update import Atualiza

   
def confirmarExclusaoNoPedido(self, identificador, desc, frame):

    resposta = messagebox.askquestion(
        "Confirmação",
        "Você está excluindo esse pedido, deseja continuar?",
        icon='question'
    )
    if resposta == "yes":
        deleta.deletarPedidos(identificador)
        frame.destroy()
        if hasattr(self, "dadosTelaVerPedidos"):
            for item in self.dadosTelaVerPedidos:
                item.destroy()
        Atualiza.retornaProdutoParaOEstoque(desc)
        
        