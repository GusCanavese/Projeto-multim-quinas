import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from tkcalendar import DateEntry
from funcoesTerceiras import filtrarPedidos

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

    self.labelfiltrarPorPeriodo = ctk.CTkLabel(self.frameTelaRelatorioDeVendas, text="Filtrar por perído", font=("Century Gothic bold", 15))
    self.labelfiltrarPorPeriodo.place(relx=0.03, rely=0.27, anchor="nw")

    # Data Inicial
    self.labelDataInicio = ctk.CTkLabel(self.frameTelaRelatorioDeVendas, text="Data Inicial:")
    self.labelDataInicio.place(relx=0.03, rely=0.31, anchor="nw")

    self.datePickerInicio = DateEntry(self.frameTelaRelatorioDeVendas, width=12, date_pattern="dd/MM/yyyy")
    self.datePickerInicio.place(relx=0.03, rely=0.35, anchor="nw")

    # Data Final
    self.labelDataFim = ctk.CTkLabel(self.frameTelaRelatorioDeVendas, text="Data Final:")
    self.labelDataFim.place(relx=0.14, rely=0.31, anchor="nw")

    self.datePickerFim = DateEntry(self.frameTelaRelatorioDeVendas, width=12, date_pattern="dd/MM/yyyy")
    self.datePickerFim.place(relx=0.14, rely=0.35, anchor="nw")

    self.todoOPeriodo = ctk.CTkCheckBox(self.frameTelaRelatorioDeVendas, text="todo o período")
    self.todoOPeriodo.place(relx=0.07, rely=0.39, anchor="nw")

    # Botões
    self.botaoFiltrarPedidos = ctk.CTkButton(
        self.frameTelaRelatorioDeVendas,
        text="Buscar",
        command=lambda: filtrarPedidos.filtrarPedidos(
            self,
            self.filtrarPorVendedor.get(),
            self.filtrarPorNumero.get(),
            self.datePickerInicio.get(),
            self.datePickerFim.get(),
            self.todoOPeriodo.get()
        )
    )
    self.botaoFiltrarPedidos.place(relx=0.05, rely=0.55, relwidth=0.15, anchor="nw")

    self.botaoLimpar = ctk.CTkButton(self.frameTelaRelatorioDeVendas, text="Limpar", command=lambda: print("Limpar"))
    self.botaoLimpar.place(relx=0.05, rely=0.63, relwidth=0.15, anchor="nw")

    self.botaoVoltar = ctk.CTkButton(self.frameTelaRelatorioDeVendas, text="Voltar", command=self.frameTelaRelatorioDeVendas.destroy)
    self.botaoVoltar.place(relx=0.79, rely=0.94, relwidth=0.15, anchor="nw")

    # Cabeçalhos da tabela
    colunas = ["Pedido", "Vendedor", "Data de emissão", "Subtotal"]
    for i, coluna in enumerate(colunas):
        label = ctk.CTkLabel(self.frameParaVendasNoRelatorio, text=coluna, width=150, fg_color="green", anchor="center")
        label.grid(row=0, column=i, padx=2, pady=5)
