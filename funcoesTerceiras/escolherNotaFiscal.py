import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.lerNotaFiscal import lerNotaFiscal
from tkinter import filedialog
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela


def escolherNotaFiscal(self):
    self.variavel = ctk.StringVar()
    self.frameEscolherNotaFiscal = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    self.variavel.set("Nenhum arquivo selecionado")

    self.label = ctk.CTkLabel(self.frameEscolherNotaFiscal, text="Escolher ficheiro", font=("Century Gothic bold", 15))
    self.label.place(relx=0.5, rely=0.4, anchor="center")

    botaoEscolherFicheiro = ctk.CTkButton(self.frameEscolherNotaFiscal, width=40, command=lambda:lerNotaFiscal(self, self.frameEscolherNotaFiscal))
    botaoEscolherFicheiro.place(relx=0.4, rely=0.5, anchor="center")

    labelCaminhoDaNota = ctk.CTkLabel(self.frameEscolherNotaFiscal, textvariable=self.variavel, font=("Century Gothic bold", 12))
    labelCaminhoDaNota.place(relx=0.55, rely=0.5, anchor="center")

    cadastrarNF = ctk.CTkButton(self.frameEscolherNotaFiscal, text="Buscar NF", command=self.frameEscolherNotaFiscal.destroy)
    cadastrarNF.place(relx=0.05, rely=0.94, relwidth=0.15, anchor="nw")

    botaoVoltar = ctk.CTkButton(self.frameEscolherNotaFiscal, text="◀️ Voltar", command=self.frameEscolherNotaFiscal.destroy)
    botaoVoltar.place(relx=0.05, rely=0.94, relwidth=0.15, anchor="nw")


