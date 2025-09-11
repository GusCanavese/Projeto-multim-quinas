import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.buscarProdutosFiscal import buscarProdutosFiscal
from componentes import criaFrameJanela, criaFrameJanela, criarLabelEntry, criarLabelComboBox, criaBotao, criaLabel

 
def telaEstoqueFiscal(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    opcoes = ["Todos", "Multimáquinas", "Nutrigel", "Polimáquinas"]


    # Filtros - lado esquerdo
    buscar = criarLabelEntry(frame,"Filtrar", 0.05, 0.04, 0.22, None)
    filtrarPorVendedor = criarLabelComboBox(frame, "Escolher estoque", 0.315, 0.04, 0.22, opcoes)


    buscarProdutosFiscal(self, frame, buscar.get(), filtrarPorVendedor.get(), 1)
    
    criaBotao(frame, "Buscar", 0.84, 0.08, 0.1, lambda:buscarProdutosFiscal(self, frame, buscar.get(), filtrarPorVendedor.get(), 1))
    criaLabel(frame, "Fiscal", 0.60, 0.08, 0.1, "#1F8107")
    buscar.bind("<Return>", lambda event: buscarProdutosFiscal(self, frame, buscar.get(), filtrarPorVendedor.get(), 1))
    criaBotao(frame, "◀️ Voltar", 0.15, 0.94, 0.15, lambda:frame.destroy())


    # Cabeçalhos da tabela
    colunas = [ "Produto", "QTD", "Código", "Preço venda", "Marca"]
    
    x = 0.05
    y = 0.13

    for i, coluna in enumerate(colunas):
        if i == 0:
            label = criaLabel(frame, coluna, x, y, 0.4, self.cor)
            x+=0.403
        elif i == 1:
            label = criaLabel(frame, coluna, x, y, 0.04, self.cor)
            x+=0.043
        elif i ==2:
            label = criaLabel(frame, coluna, x, y, 0.15, self.cor)
            x+=0.153
        elif i ==3:
            label = criaLabel(frame, coluna, x, y, 0.10, self.cor)
            x+=0.103
        else:
            label = criaLabel(frame, coluna, x, y, 0.17, self.cor)
            x+=0.178

