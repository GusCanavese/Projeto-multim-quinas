import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.buscarProdutos import buscarProdutos
from funcoesTerceiras import filtrar
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criarLabelEntry, criarLabelComboBox, criaBotao, criaLabel


def telaGerenciarFuncionarios(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    frameProdutos = criaFrame(frame, 0.65, 0.5, 0.68, 0.93)

    # Filtros - lado esquerdo
    self.buscar = criarLabelEntry(frame,"Filtrar", 0.03, 0.05, 0.22, None)
    
    criaBotao(frame, "Buscar", 0.15, 0.05, 0.15, lambda:filtrar.filtrarFuncionarios(self, frameProdutos, self.buscar.get()))
    criaBotao(frame, "◀️ Voltar", 0.15, 0.94, 0.15, lambda:frame.destroy())

    # Cabeçalhos da tabela

    colunas = ["Nome", "Cargo"]
    
    x = 0.03
    y = 0.05

    for i, coluna in enumerate(colunas):
        label = criaLabel(frameProdutos, coluna, x, y, 0.17, self.cor)
        x+=0.175

