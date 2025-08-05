import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.escolherNotaFiscal import escolherNotaFiscal
from funcoesTerceiras import filtrar, verificaSeQuerFiltrarPorPeriodo
from componentes import criaFrameJanela, criaFrameJanela, criaLabel, criaBotao, criaComboBox, criarLabelEntry

def telaNotaFiscalSaida(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    frameContas = criaFrameJanela(frame, 0.5, 0.50, 0.95, 0.7, self.corFundo)
    