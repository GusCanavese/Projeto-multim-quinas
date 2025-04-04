import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from tkcalendar import DateEntry
from funcoesTerceiras import filtrarPedidos

def telaRelatorioDeVendas(self):
    self.frameTelaRelatorioDeVendas = ctk.CTkFrame(self, height=800, width=1200, corner_radius=5)
    self.frameTelaRelatorioDeVendas.place(x=40, y=50)
    
    # Frame rolável
    self.frameParaVendasNoRelatorio = ctk.CTkScrollableFrame(self.frameTelaRelatorioDeVendas, width=800, height=730 )
    self.frameParaVendasNoRelatorio.place(x=360, y=10)

    self.labelfiltrarPorNumero = ctk.CTkLabel(self.frameTelaRelatorioDeVendas, text="Filtrar pelo Nº", font=("Century Gothic bold", 15))
    self.labelfiltrarPorNumero.place(x=50, y=10)
    self.filtrarPorNumero = ctk.CTkEntry(self.frameTelaRelatorioDeVendas, width=250, corner_radius=5, font=("Century Gothic bold", 20))
    self.filtrarPorNumero.place(x=50, y=50)
    
    opcoes = ["Nenhum", "Yara", "Camila", "Jenifer", "Bruna", "Ana Flávia", "Maurício"]
    self.labelfiltrarPorVendedor = ctk.CTkLabel(self.frameTelaRelatorioDeVendas, text="Filtrar por vendedor(a)", font=("Century Gothic bold", 15))
    self.labelfiltrarPorVendedor.place(x=50, y=130)
    self.filtrarPorVendedor = ctk.CTkComboBox(self.frameTelaRelatorioDeVendas, width=250, corner_radius=5, font=("Century Gothic bold", 20), values=opcoes)
    self.filtrarPorVendedor.place(x=50, y=160)

    self.labelfiltrarPorPeriodo = ctk.CTkLabel(self.frameTelaRelatorioDeVendas, text="Filtrar por perído", font=("Century Gothic bold", 15))
    self.labelfiltrarPorPeriodo.place(x=50, y=240)
    
    # Label e DatePicker para a Data Inicial
    self.labelDataInicio = ctk.CTkLabel(self.frameTelaRelatorioDeVendas, text="Data Inicial:").place(x=50, y=270)
    self.datePickerInicio = DateEntry(self.frameTelaRelatorioDeVendas, width=12, date_pattern="dd/MM/yyyy")
    self.datePickerInicio.place(x=50, y=300)

    # Label e DatePicker para a Data Final
    self.labelDataFim = ctk.CTkLabel(self.frameTelaRelatorioDeVendas, text="Data Final:").place(x=150, y=270)
    self.datePickerFim = DateEntry(self.frameTelaRelatorioDeVendas, width=12, date_pattern="dd/MM/yyyy")
    self.datePickerFim.place(x=150, y=300)



    self.botaoFiltrarPedidos = ctk.CTkButton(self.frameTelaRelatorioDeVendas, text="Buscar", width=150, command=lambda:filtrarPedidos.filtrarPedidos(self, self.filtrarPorVendedor.get(), self.filtrarPorNumero.get()))
    self.botaoFiltrarPedidos.place(x=100, y=500)

    self.botaoVoltar = ctk.CTkButton(self.frameTelaRelatorioDeVendas, text="Voltar", width=150, command=self.frameTelaRelatorioDeVendas.destroy)
    self.botaoVoltar.place(x=950, y=760)



    # tela rolavel
    colunas = ["Pedido", "Vendedor", "Data de emissão", "Subtotal"]
    for i, coluna in enumerate(colunas):
        label = ctk.CTkLabel(self.frameParaVendasNoRelatorio, text=coluna, width=150, fg_color="green", anchor="center")
        label.grid(row=0, column=i, padx=2, pady=5)  