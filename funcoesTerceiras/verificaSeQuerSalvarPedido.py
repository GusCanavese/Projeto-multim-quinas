import tkinter as tk
from tkinter import messagebox
from funcoesTerceiras.PassaDadosParaPedido import PassaDadosParaPedido

def salvarPedido(self):
    resposta = messagebox.askquestion(
        "Confirmação",
        "O pedido está sendo salvo no banco de dados, deseja continuar?",
        icon='question'
    )
    
    if resposta == 'yes':
        PassaDadosParaPedido(self)

    else:
        return

