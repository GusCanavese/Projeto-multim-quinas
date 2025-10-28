
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import filtrar, verificaSeQuerFiltrarPorPeriodo
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criarLabelEntry, criarLabelComboBox, criaBotao, criaLabel



def telaRelatorioDeNotasFiscais(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    frameVendas = criaFrameJanela(frame, 0.5, 0.5, 0.95, 0.7, self.corFundo)
    opcoes = ["Todos", "1", "Yara", "Camila", "Jenifer", "Bruna", "Ana Flávia", "Maurício"]


    filtroNota = criarLabelEntry(frame,"Filtrar", 0.055, 0.04, 0.22, None)
    
    
    criaBotao(frame, "Buscar", 0.84, 0.08, 0.1, lambda:filtrar.filtrarNotasFiscais(self, frameVendas, filtroNota.get()))
    criaBotao(frame, "◀️ Voltar", 0.15, 0.94, 0.15, lambda:frame.destroy())


    # Cabeçalhos da tabela
    colunas = ["Status", "Tipo", "Op", "Destinatário", "Série", "Valor total", "cfop", "Data de emissão", "Numero"]
    x = 0.03
    y = 0.05

    for i, coluna in enumerate(colunas):
        if i == 0:
            criaLabel(frameVendas, coluna, x, y, 0.07, self.cor)
            x += 0.075
        elif i == 1 or i == 2 or i == 4:
            criaLabel(frameVendas, coluna, x, y, 0.05, self.cor) 
            x += 0.055
        elif i == 3:
            criaLabel(frameVendas, coluna, x, y, 0.2, self.cor)
            x += 0.205
        else:
            criaLabel(frameVendas, coluna, x, y, 0.10, self.cor)
            x += 0.105


