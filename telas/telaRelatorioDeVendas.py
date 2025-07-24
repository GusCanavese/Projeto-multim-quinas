
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import filtrar, verificaSeQuerFiltrarPorPeriodo
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criarLabelEntry, criarLabelComboBox, criaBotao, criaLabel



def telaRelatorioDeVendas(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    frameVendas = criaFrameJanela(frame, 0.5, 0.5, 0.95, 0.7, self.corFundo)
    opcoes = ["Todos", "1", "Yara", "Camila", "Jenifer", "Bruna", "Ana Flávia", "Maurício"]


    self.filtrarPorNumero = criarLabelEntry(frame,"Filtrar", 0.055, 0.04, 0.22, None)
    self.filtrarPorVendedor = criarLabelComboBox(frame, "Filtrar por vendedor(a)", 0.315, 0.04, 0.22, opcoes)
    
    self.selecionarPeriodo = ctk.CTkCheckBox(frame, text="Selecionar período")
    self.selecionarPeriodo.place(relx=0.54, rely=0.065, anchor="nw")
    self.selecionarPeriodo.bind("<Button-1>", command=lambda event: verificaSeQuerFiltrarPorPeriodo.verificaSeQuerFiltrarPorPeriodo(self,frame, self.selecionarPeriodo.get(), event))
    

    # Botões
    
    
    criaBotao(frame, "Buscar", 0.90, 0.08, 0.1, lambda:filtrar.filtrarPedidos( self, frameVendas, self.filtrarPorVendedor.get(), self.filtrarPorNumero.get(), self.datePickerInicio.get() if hasattr(self, "datePickerInicio") else None, self.datePickerFim.get() if hasattr(self, "datePickerFim") else None, self.selecionarPeriodo.get()))
    criaBotao(frame, "Voltar", 0.32, 0.94, 0.15, lambda:frame.destroy())

    # Cabeçalhos da tabela
    colunas = ["Pedido", "Cliente", "Vendedor", "Data de emissão", "Subtotal", "Confirmação"]
    x = 0.03
    y = 0.05

    for i, coluna in enumerate(colunas):
        if i == 0:
            criaLabel(frameVendas, coluna, x, y, 0.05, self.cor)  # Pedido
            x += 0.055
        elif i == 1:
            criaLabel(frameVendas, coluna, x, y, 0.15, self.cor)  # Cliente
            x += 0.155
        elif i == 2:
            criaLabel(frameVendas, coluna, x, y, 0.15, self.cor)  # Vendedor
            x += 0.155
        else:
            criaLabel(frameVendas, coluna, x, y, 0.17, self.cor)  # Data de emissão
            x += 0.175


