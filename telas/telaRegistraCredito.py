import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk

def telaRegistroCredito(self, dadosNota):
    self.frameTelaRegistroCredito = ctk.CTkFrame(self)
    self.frameTelaRegistroCredito.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    print(dadosNota['ide']["nNF"])