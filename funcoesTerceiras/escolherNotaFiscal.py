import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.lerNotaFiscal import lerNotaFiscal
from tkinter import filedialog


def escolherNotaFiscal(self):
    self.frameTelaCredito = ctk.CTkFrame(self)
    self.frameTelaCredito.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    self.framePequeno = ctk.CTkFrame(self.frameTelaCredito)
    self.framePequeno.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5, anchor="center")
    self.variavel = ctk.StringVar()
    self.variavel.set("Nenhum ficheiro selecionado")

    self.label = ctk.CTkLabel(self.framePequeno, text="Escolher ficheiro", font=("Century Gothic bold", 15))
    self.label.place(relx=0.5, rely=0.4, anchor="center")

    botaoEscolherFicheiro = ctk.CTkButton(self.framePequeno, width=40, command=lambda:lerNotaFiscal(self))
    botaoEscolherFicheiro.place(relx=0.35, rely=0.5, anchor="center")

    labelCaminhoDaNota = ctk.CTkLabel(self.framePequeno, textvariable=self.variavel, font=("Century Gothic bold", 12))
    labelCaminhoDaNota.place(relx=0.55, rely=0.5, anchor="center")

    cadastrarNF = ctk.CTkButton(self.frameTelaCredito, text="Buscar NF", command=self.frameTelaCredito.destroy)
    cadastrarNF.place(relx=0.05, rely=0.94, relwidth=0.15, anchor="nw")

    botaoVoltar = ctk.CTkButton(self.frameTelaCredito, text="Voltar", command=self.frameTelaCredito.destroy)
    botaoVoltar.place(relx=0.05, rely=0.94, relwidth=0.15, anchor="nw")


