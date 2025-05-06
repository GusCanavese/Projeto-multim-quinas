from tkinter import messagebox
from funcoesTerceiras.PassaDadosParaPedido import PassaDadosParaPedido
from funcoesTerceiras.passaDadosParaOrcamento import PassaDadosParaOrcamento

def salvarPedido(self):
    resposta = messagebox.askquestion(
        "Confirmação",
        "O pedido está sendo salvo no banco de dados, deseja continuar?",
        icon='question'
    )
    
    if resposta == 'no':
        return
        

    else:
        PassaDadosParaPedido(self)

def salvarOrcamento(self):
    resposta = messagebox.askquestion(
        "Confirmação",
        "Esse orçamento está sendo salvo no banco de dados, deseja continuar?",
        icon='question'
    )
    
    if resposta == 'no':
        return
        

    else:
        PassaDadosParaOrcamento(self)



