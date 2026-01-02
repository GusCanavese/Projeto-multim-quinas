import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox
from consultas.update import Atualiza
from consultas.insert import Insere
from datetime import datetime, date


def _registrar_conta_a_receber(identificador, cliente, valor, vencimento):
    if valor is None or valor == "":
        return
    valor_str = str(valor).replace(",", ".")
    try:
        valor_final = float(valor_str)
    except ValueError:
        valor_final = valor
    descricao = f"lançamento referente ao pedido de número {identificador}, com o cliente {cliente}"
    Insere.registraFaturamentoNoBanco("Não", vencimento, descricao, valor_final, "Pedido", 1)


def confirmarHoje(self, identificador, frame, subtotal, cliente):
    resposta = messagebox.askquestion('Aviso!', 'A o pedido será confirmado com a data de hoje, deseja prosseguir?', icon='question')
    if resposta == 'yes':
        Atualiza.atualizaPedido(identificador)
        data_formatada = date.today().strftime("%Y-%m-%d")
        _registrar_conta_a_receber(identificador, cliente, subtotal, data_formatada)
        frame.destroy()
    else:
        pass
   
#!essa função ta imcompleta
def confirmarAlteracoesNoPedido(self, dataConfirmacao, identificador, frame, subtotal, cliente):
    if dataConfirmacao == '':
        messagebox.showerror('Erro', 'A a data de confirmação deve ser no formato dd/mm/aaaa')
    else:
        try:
            data_formatada = datetime.strptime(dataConfirmacao, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror('Erro', 'A a data de confirmação deve ser no formato dd/mm/aaaa')
            return
        resposta = messagebox.askquestion(
            "Confirmação",
            "Você irá alterar dados no pedido, deseja continuar?",
            icon='question'
        )
        if resposta == "yes":
            frame.destroy()
            Atualiza.atualizaPedido(identificador)
            _registrar_conta_a_receber(identificador, cliente, subtotal, data_formatada)
