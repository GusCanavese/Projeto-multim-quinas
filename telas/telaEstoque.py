import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.buscarProdutos import buscarProdutos
from componentes import criaFrame, criarLabelEntry, criarLabelComboBox, criaBotao, criaLabel


def telaEstoque(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    frameProdutos = criaFrame(frame, 0.65, 0.5, 0.68, 0.93)
    opcoes = ["Multimáquinas", "Nutrigel", "Polimáquinas", "Usados"]


    # Filtros - lado esquerdo
    self.buscarPorCodigo = criarLabelEntry(frame,"Buscar pelo código", 0.03, 0.05, 0.22, None)
    self.buscarPorNome = criarLabelEntry(frame,"Buscar pelo Nome", 0.03, 0.17, 0.22, None)
    self.filtrarPorVendedor = criarLabelComboBox(frame,"Filtrar por vendedor(a)", 0.03, 0.29, 0.22, opcoes)

    
    criaBotao(frame, "Buscar", 0.15, 0.55, 0.15, lambda:buscarProdutos(self, frameProdutos,self.buscarPorNome.get(), self.buscarPorCodigo.get(), 1))
    criaBotao(frame, "Voltar", 0.15, 0.94, 0.15, lambda:frame.destroy())


    # Cabeçalhos da tabela

    colunas = ["QTD", "Produto", "Código", "Preço venda", "CNPJ"]
    
    x = 0.03
    y = 0.05

    for i, coluna in enumerate(colunas):
        if i == 0:
            label = criaLabel(frameProdutos, coluna, x, y, 0.04, "#2C3E50")
            x+=0.043
        elif i ==1:
            label = criaLabel(frameProdutos, coluna, x, y, 0.4, "#2C3E50")
            x+=0.403
        elif i ==2:
            label = criaLabel(frameProdutos, coluna, x, y, 0.15, "#2C3E50")
            x+=0.153
        elif i ==3:
            label = criaLabel(frameProdutos, coluna, x, y, 0.10, "#2C3E50")
            x+=0.103
        else:
            label = criaLabel(frameProdutos, coluna, x, y, 0.17, "#2C3E50")
            x+=0.178

