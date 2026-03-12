import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from tkcalendar import DateEntry


def _destruir_filtro_periodo(self):
    for atributo in ("labelDataInicio", "datePickerInicio", "labelDataFim", "datePickerFim"):
        widget = getattr(self, atributo, None)
        if widget is not None:
            widget.destroy()
            delattr(self, atributo)

def verificaSeQuerFiltrarPorPeriodo(self, frame, checkbox, event=None):
    if checkbox:
        _destruir_filtro_periodo(self)
        # Data Inicial
        self.labelDataInicio = ctk.CTkLabel(frame, text="Data Inicial:")
        self.labelDataInicio.place(relx=0.68, rely=0.02, anchor="nw")
        self.datePickerInicio = DateEntry(frame, width=12, date_pattern="dd/MM/yyyy")
        self.datePickerInicio.place(relx=0.68, rely=0.079, anchor="nw")

        # Data Final
        self.labelDataFim = ctk.CTkLabel(frame, text="Data Final:")
        self.labelDataFim.place(relx=0.76, rely=0.02, anchor="nw")
        self.datePickerFim = DateEntry(frame, width=12, date_pattern="dd/MM/yyyy")
        self.datePickerFim.place(relx=0.76, rely=0.079, anchor="nw")
    else:
        _destruir_filtro_periodo(self)



def verificaSeQuerFiltrarPorPeriodoContas(self, frame, checkbox, event=None):
    if checkbox:
        _destruir_filtro_periodo(self)
        # Data Inicial
        self.labelDataInicio = ctk.CTkLabel(frame, text="Data Inicial:")
        self.labelDataInicio.place(relx=0.7, rely=0.02, anchor="nw")
        self.datePickerInicio = DateEntry(frame, width=12, date_pattern="dd/MM/yyyy")
        self.datePickerInicio.place(relx=0.7, rely=0.06, anchor="nw")

        # Data Final
        self.labelDataFim = ctk.CTkLabel(frame, text="Data Final:")
        self.labelDataFim.place(relx=0.8, rely=0.02, anchor="nw")
        self.datePickerFim = DateEntry(frame, width=12, date_pattern="dd/MM/yyyy")
        self.datePickerFim.place(relx=0.8, rely=0.06, anchor="nw")
    else:
        _destruir_filtro_periodo(self)
        
