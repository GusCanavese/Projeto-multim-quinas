import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from tkinter import messagebox

def telaCalculaVendas(self):
    self.frameTelaCalculaVendas = ctk.CTkFrame(self, corner_radius=5)
    self.frameTelaCalculaVendas.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    # ================ widgets da tela de calculo de vendas =====================#

