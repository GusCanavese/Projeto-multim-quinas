import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import filtrarPedidos, verificaSeQuerFiltrarPorPeriodo



def telaRelatorioDeVendas(self):

    self.frameTelaRelatorioDeVendas = ctk.CTkFrame(self, corner_radius=5)
    self.frameTelaRelatorioDeVendas.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    # Frame rolável (conteúdo principal)
    self.frameParaVendasNoRelatorio = ctk.CTkScrollableFrame(self.frameTelaRelatorioDeVendas)
    self.frameParaVendasNoRelatorio.place(relx=0.3, rely=0.01, relwidth=0.68, relheight=0.93)

    # Filtros - lado esquerdo
    self.labelfiltrarPorNumero = ctk.CTkLabel(self.frameTelaRelatorioDeVendas, text="Filtrar pelo Nº", font=("Century Gothic bold", 15))
    self.labelfiltrarPorNumero.place(relx=0.03, rely=0.01, anchor="nw")
    
    self.filtrarPorNumero = ctk.CTkEntry(self.frameTelaRelatorioDeVendas, corner_radius=5, font=("Century Gothic bold", 20))
    self.filtrarPorNumero.place(relx=0.03, rely=0.06, relwidth=0.22, anchor="nw")

    opcoes = ["Nenhum", "Yara", "Camila", "Jenifer", "Bruna", "Ana Flávia", "Maurício"]
    self.labelfiltrarPorVendedor = ctk.CTkLabel(self.frameTelaRelatorioDeVendas, text="Filtrar por vendedor(a)", font=("Century Gothic bold", 15))
    self.labelfiltrarPorVendedor.place(relx=0.03, rely=0.14, anchor="nw")
    self.filtrarPorVendedor = ctk.CTkComboBox(self.frameTelaRelatorioDeVendas, font=("Century Gothic bold", 20), values=opcoes)
    self.filtrarPorVendedor.place(relx=0.03, rely=0.19, relwidth=0.22, anchor="nw")

    self.selecionarPeriodo = ctk.CTkCheckBox(self.frameTelaRelatorioDeVendas, text="Selecionar período")
    self.selecionarPeriodo.place(relx=0.03, rely=0.27, anchor="nw")

    
    self.selecionarPeriodo.bind("<Button-1>", command=lambda event: verificaSeQuerFiltrarPorPeriodo.verificaSeQuerFiltrarPorPeriodo(self, self.selecionarPeriodo.get(), event))
    

    # Botões
    self.botaoFiltrarPedidos = ctk.CTkButton(self.frameTelaRelatorioDeVendas,text="Buscar",command=lambda: filtrarPedidos.filtrarPedidos( self, self.filtrarPorVendedor.get(), self.filtrarPorNumero.get(), self.datePickerInicio.get() if hasattr(self, "datePickerInicio") else None, self.datePickerFim.get() if hasattr(self, "datePickerFim") else None, self.selecionarPeriodo.get()))
    self.botaoFiltrarPedidos.place(relx=0.05, rely=0.55, relwidth=0.15, anchor="nw")

    self.botaoLimpar = ctk.CTkButton(self.frameTelaRelatorioDeVendas, text="Atualizar", command=lambda: filtrarPedidos.filtrarPedidos( self, self.filtrarPorVendedor.get(), self.filtrarPorNumero.get(), self.datePickerInicio.get() if hasattr(self, "datePickerInicio") else None, self.datePickerFim.get() if hasattr(self, "datePickerFim") else None, self.selecionarPeriodo.get()))
    self.botaoLimpar.place(relx=0.05, rely=0.63, relwidth=0.15, anchor="nw")

    self.botaoVoltar = ctk.CTkButton(self.frameTelaRelatorioDeVendas, text="Voltar", command=self.frameTelaRelatorioDeVendas.destroy)
    self.botaoVoltar.place(relx=0.79, rely=0.94, relwidth=0.15, anchor="nw")

    # Cabeçalhos da tabela
    colunas = ["Pedido", "Vendedor", "Data de emissão", "Subtotal", "Confirmação da venda"]
    for i, coluna in enumerate(colunas):
        label = ctk.CTkLabel(self.frameParaVendasNoRelatorio, text=coluna, width=150, fg_color="#2C3E50", anchor="center")
        label.grid(row=0, column=i, padx=2, pady=5)
        label.grid_columnconfigure(0, minsize=20)
