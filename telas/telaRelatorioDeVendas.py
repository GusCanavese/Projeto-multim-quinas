
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import filtrarPedidos, verificaSeQuerFiltrarPorPeriodo
from componentes import criaFrame, criarLabelEntry, criarLabelComboBox, criaBotao, criaLabel



def telaRelatorioDeVendas(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    frameVendas = criaFrame(frame, 0.65, 0.5, 0.68, 0.93)
    opcoes = ["Nenhum", "Yara", "Camila", "Jenifer", "Bruna", "Ana Flávia", "Maurício"]


    self.filtrarPorNumero = criarLabelEntry(frame,"Filtrar pelo Nº", 0.03, 0.05, 0.22, None)
    self.filtrarPorVendedor = criarLabelComboBox(frame, "Filtrar por vendedor(a)", 0.03, 0.14, 0.22, opcoes)
    
    self.selecionarPeriodo = ctk.CTkCheckBox(frame, text="Selecionar período")
    self.selecionarPeriodo.place(relx=0.03, rely=0.27, anchor="nw")
    self.selecionarPeriodo.bind("<Button-1>", command=lambda event: verificaSeQuerFiltrarPorPeriodo.verificaSeQuerFiltrarPorPeriodo(self, self.selecionarPeriodo.get(), event))
    

    # Botões
    
    
    criaBotao(frame, "Buscar", 0.15, 0.55, 0.15, lambda:filtrarPedidos.filtrarPedidos( self, frameVendas, self.filtrarPorVendedor.get(), self.filtrarPorNumero.get(), self.datePickerInicio.get() if hasattr(self, "datePickerInicio") else None, self.datePickerFim.get() if hasattr(self, "datePickerFim") else None, self.selecionarPeriodo.get()))
    criaBotao(frame, "Atualizar", 0.15, 0.63, 0.15, lambda:filtrarPedidos.filtrarPedidos( self, frameVendas, self.filtrarPorVendedor.get(), self.filtrarPorNumero.get(), self.datePickerInicio.get() if hasattr(self, "datePickerInicio") else None, self.datePickerFim.get() if hasattr(self, "datePickerFim") else None, self.selecionarPeriodo.get()))
    criaBotao(frame, "Voltar", 0.15, 0.94, 0.15, lambda:frame.destroy())

    # Cabeçalhos da tabela
    colunas = ["Pedido", "Vendedor", "Data de emissão", "Subtotal", "Confirmação da venda"]
    x = 0.03
    y = 0.05

    for i, coluna in enumerate(colunas):
        criaLabel(frameVendas, coluna, x, y, 0.17, "#2C3E50")
        x+=0.175

