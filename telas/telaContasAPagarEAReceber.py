import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.lerNotaFiscal import lerNotaFiscal

def telaContasAPagarEAReceber(self):
    self.frameTelaContasAPagarEAReceber = ctk.CTkFrame(self)
    self.frameTelaContasAPagarEAReceber.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    botaoNovo = ctk.CTkButton(self.frameTelaContasAPagarEAReceber, text="Novo", command=lambda:lerNotaFiscal(self))
    botaoNovo.place(relx=0.1, rely=0.1)
