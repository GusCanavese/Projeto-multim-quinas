import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk

def telaRegistroCredito(self, dadosNota):
    self.frameTelaRegistroCredito = ctk.CTkFrame(self)
    self.frameTelaRegistroCredito.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    botaoVoltar = ctk.CTkButton(self.frameTelaRegistroCredito, text="Voltar", command=self.frameTelaCredito.destroy)
    botaoVoltar.place(relx=0.05, rely=0.94, relwidth=0.15, anchor="nw")

    print(dadosNota['ide']["nNF"])