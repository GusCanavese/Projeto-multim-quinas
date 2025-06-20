import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox
from consultas.update import Atualiza
from consultas.insert import Insere

def confirmarSalvamentoDoFaturamento(self, quantidade, valor, formaPag, data, pedido, cliente):
    confirmado = "Não"
    resposta = messagebox.askquestion('Aviso!', 'O faturamento será salvo referente ao pedido tal.', icon='question')
    if resposta == 'yes':
        qtdParcelas = quantidade[0].get()
        valorTotal = valor[0].get()
        formaPagamento = formaPag[0].get()
        dataFaturamento = data.get()
        descricao = f"lançamento referente ao pedido de número {pedido}, com o cliente {cliente}"

        Insere.registraFaturamentoNoBanco(confirmado, dataFaturamento, descricao, valorTotal, formaPagamento, qtdParcelas)
    else:
        pass