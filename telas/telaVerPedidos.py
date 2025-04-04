import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk

def telaVerPedidos(self):
    self.frameTelaVerPedidos = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
    self.frameTelaVerPedidos.place(x=140, y=100)     
    self.frameTelaVerPedidos.grid_propagate(False)

    self.botaoVotlar = ctk.CTkButton(self.frameTelaVerPedidos, text="Gerar pedido", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaVerPedidos.destroy)
    self.botaoVotlar.place(x=500, y=500)
    
    