import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from dateutil.relativedelta import relativedelta
from datetime import datetime


def SalvaAlteracoesFaturamento(self, valor, qtdParcelas, datas):
    self.data=datas[4]

    for widget in self.frameTelaGerarFaturamento.winfo_children():
        try:
            widget.configure(state="normal")
        except:
            print("alguns ignorados")
        self.valorDoPedidoVariavel.set(valor)
        self.variavelQuantidade.set(qtdParcelas)
    self.frame.destroy()

def calcularParcelasTotais(self, quantidade, valor):
    valor = float(valor)
    quantidade = int(quantidade)
    valordividido = valor/quantidade
    dataHoje = self.dataHojeFormatada

    if hasattr(self, "listaEntryModal"):
        for widget in self.listaEntryModal:
            widget.destroy()
        self.listaEntryModal.clear()
    else:
        self.listaEntryModal = []

    posicaoY = 0.312

    for i in range(quantidade): 
        posicaoY += 0.039
        posicaoX = 0.2

        for j, row in enumerate(self.opcoesLabelModal):
            variavelEntryModal = ctk.StringVar()

            if j != 0:
                entryModal = ctk.CTkEntry(self.frame, width=120, corner_radius=0, textvariable=variavelEntryModal)
                entryModal.place(relx=posicaoX -0.04, rely=posicaoY)
                self.listaEntryModal.append(entryModal)
                posicaoX += 0.15

            if j == 0:
                entryModal = ctk.CTkLabel(self.frame, width=60, corner_radius=0, fg_color="#4d4246", text=i+1)
                entryModal.place(relx=posicaoX +0.028, rely=posicaoY)
                self.listaEntryModal.append(entryModal)
                posicaoX += 0.15

            if j == 2:
                variavelEntryModal.set(f"{valordividido:.2f}")

            if j == 3:  
                dataOriginal = datetime.strptime(dataHoje, "%d/%m/%Y")
                
                dataComMaisUmMes = dataOriginal + relativedelta(months=1)
                dataHoje = dataComMaisUmMes.strftime("%d/%m/%Y")
                variavelEntryModal.set(dataHoje)

                    



