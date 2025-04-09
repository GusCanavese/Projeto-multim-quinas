import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from tkcalendar import DateEntry

def verificaSeQuerFiltrarPorPeriodo(self, checkbox, event=None):
    if checkbox:
        print("teste")
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
    else:
        self.labelDataInicio.destroy()
        del self.labelDataInicio
        self.datePickerInicio.destroy()
        del self.datePickerInicio
        self.labelDataFim.destroy()
        del self.labelDataFim
        self.datePickerFim.destroy()
        del self.datePickerFim
        