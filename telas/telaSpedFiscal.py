import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criaBotao

def telaGerenciar(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    label = ctk.CTkLabel(frame, text="Tela em desenvolvimento", font=("Arial", 20))
    label.place(relx=0.5, rely=0.5, anchor="center")

    criaBotao(frame, "◀️ Voltar", 0.33, 0.80, 0.18, lambda: frame.destroy())
