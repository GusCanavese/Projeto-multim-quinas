import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox
from consultas.delete import deleta

   
def confirmarExclusaoDoProduto(self, frame, descricao,):
    print(descricao)

    resposta = messagebox.askquestion(
        "Confirmação",
        "Você está excluindo esse produto, deseja continuar?",
        icon='question'
    )
    if resposta == "yes":
        deleta.deletarProduto(descricao)
        frame.destroy()
        messagebox.showinfo('Sucesso', "Você excluiu esse produto")
        
        