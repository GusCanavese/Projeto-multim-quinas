import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox
from consultas.update import Atualiza

   
def confirmarAlteracoesNoProduto(self, frame, id, quantidade, preco, custo):
    print(id)
    if quantidade == '' or preco == '':
        messagebox.showerror('Erro', 'todos os campos devem estar preenchidos')
    else:
        resposta = messagebox.askquestion(
            "Confirmação",
            "Você irá alterar dados no produto, deseja continuar?",
            icon='question'
        )
        if resposta == "yes":
            Atualiza.atualizaProduto(quantidade, preco, custo, id)
            messagebox.showinfo('Sucesso', 'O produto foi atualizado com sucesso')
            frame.destroy()
