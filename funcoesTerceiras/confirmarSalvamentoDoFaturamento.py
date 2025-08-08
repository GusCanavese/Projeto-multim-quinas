import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox
from datetime import datetime
from dateutil.relativedelta import relativedelta
from consultas.update import Atualiza
from consultas.insert import Insere

def confirmarSalvamentoDoFaturamento(self, quantidade, valor, formaPag, data, pedido, cliente, repeticao):
    print(repeticao)

    confirmado = "Não"
    resposta = messagebox.askquestion('Aviso!', 'O faturamento será salvo referente ao pedido tal.', icon='question')
    if resposta == 'yes':
        qtdParcelas = quantidade[0].get()
        valorTotal = valor[0].get()
        formaPagamento = formaPag[0].get()
        dataFaturamento = data.get()
        descricao = f"lançamento referente ao pedido de número {pedido}, com o cliente {cliente}"

        dataBase = datetime.strptime(dataFaturamento, "%d/%m/%Y")
        
        valorParcela = round(float(valorTotal) / int(qtdParcelas), 2)
        for i in range(int(qtdParcelas)):
            if repeticao == "Mensal":
                dataParcela = dataBase + relativedelta(months=i)
            elif repeticao == "Bimestral":
                dataParcela = dataBase + relativedelta(months=2 * i)
            elif repeticao == "Semestral":
                dataParcela = dataBase + relativedelta(months=6 * i)
            elif repeticao == "Anual":
                dataParcela = dataBase + relativedelta(years=i)

            dataFormatada = dataParcela.strftime("%Y-%m-%d")
 
            Insere.registraFaturamentoNoBanco(confirmado, dataFormatada, descricao, valorParcela, formaPagamento, 1)
        messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")

    else:            

        pass








def confirmarSalvamentoDoFaturamentoNota(self, quantidade, valor, formaPag, data, repeticao):
    print("aoooopa")

    confirmado = "Não"
    resposta = messagebox.askquestion('Aviso!', 'O faturamento será salvo referente ao pedido tal.', icon='question')
    if resposta == 'yes':
        qtdParcelas = quantidade[0].get()
        valorTotal = valor[0].get()
        formaPagamento = formaPag[0].get()
        dataFaturamento = data.get()

        dataBase = datetime.strptime(dataFaturamento, "%d/%m/%Y")
        
        valorParcela = round(float(valorTotal) / int(qtdParcelas), 2)
        for i in range(int(qtdParcelas)):
            if repeticao == "Mensal":
                dataParcela = dataBase + relativedelta(months=i)
            elif repeticao == "Bimestral":
                dataParcela = dataBase + relativedelta(months=2 * i)
            elif repeticao == "Semestral":
                dataParcela = dataBase + relativedelta(months=6 * i)
            elif repeticao == "Anual":
                dataParcela = dataBase + relativedelta(years=i)

            dataFormatada = dataParcela.strftime("%Y-%m-%d")
 
            # Insere.registraFaturamentoNoBanco(confirmado, dataFormatada, valorParcela, formaPagamento, 1)
            self.faturamento = ({
                "confirmado": confirmado,
                "dataFormatada": dataFormatada,
                "valorParcela": valorParcela,
                "formaPagamento": formaPagamento,
            })

        messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")

    else:            

        pass