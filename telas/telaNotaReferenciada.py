import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from telas.telaProdutoNotaSaida import telaProdutosNotaSaida
from componentes import criaFrameJanela, criaBotao
import customtkinter as ctk



def telaNotaReferenciada(self, emt, cfop, repeticao):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    label = ctk.CTkLabel(frame, text="Tela em desenvolvimento", font=("Arial", 20))
    label.place(relx=0.5, rely=0.5, anchor="center")

    criaBotao(frame, "◀️ Voltar", 0.33, 0.80, 0.18, lambda: frame.destroy())

    print(repeticao)
    criaBotao(self.frameTelaNotaSaida, "Próximo - Tela de Produtos", 0.25, 0.94, 0.15, lambda: telaProdutosNotaSaida(self, emt, cfop)).place(anchor="nw")