import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk

def SalvaAlteracoesFaturamento(self, valor, qtdParcelas):
    print(valor)
    print(qtdParcelas)

    for widget in self.frameTelaGerarFaturamento.winfo_children():
        try:
            widget.configure(state="normal")
        except:
            print("alguns ignorados")
        self.valorDoPedidoVariavel.set(valor)
        self.variavelQuantidade.set(qtdParcelas)
    self.frame.destroy()

def calcularParcelasTotais(self, quantidade, valor):
    valor = int(valor)
    quantidade = int(quantidade)
    valordividido = valor/quantidade
    if hasattr(self, "listaEntryModal"):
        for widget in self.listaEntryModal:
            widget.destroy()
        self.listaEntryModal.clear()
    else:
        self.listaEntryModal = []

    posicaoY = 0.312

    for i in range(int(quantidade)): 
        posicaoY += 0.039
        posicaoX = 0.3

        for i in self.opcoesLabelModal:
            variavelEntryModal = ctk.StringVar()
            variavelEntryModal.set(valordividido)

            entryModal = ctk.CTkEntry(self.frame, width=120, corner_radius=0, textvariable=variavelEntryModal)
            entryModal.place(relx=posicaoX, rely=posicaoY)

            self.listaEntryModal.append(entryModal)
            print(self.listaEntryModal[0].get())
            
            posicaoX += 0.15

    self.listaEntryModal


