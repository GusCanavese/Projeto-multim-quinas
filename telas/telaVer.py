import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import confirmarExclusaoDoProduto, confirmarAlteracoesNoProduto
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criaLabelDescritivo, criaBotao, criarLabelEntry;

def telaVer(self, p):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)


    for row, i in enumerate(p):
        x = 0.1
        y = 0.07
        criaLabelDescritivo(frame, i, x, 0.07, 0.35, self.cor, None)
        x +=0.35
        if row >=5:
            y += 0.07

