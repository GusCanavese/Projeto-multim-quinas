import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from tkcalendar import DateEntry

def verificaSeQuerFiltrarPorPeriodo(self, frame, checkbox, event=None):
    # relx=0.50, rely=0.065
    if checkbox:
        # Data Inicial
        self.labelDataInicio = ctk.CTkLabel(frame, text="Data Inicial:")
        self.labelDataInicio.place(relx=0.65, rely=0.02, anchor="nw")
        self.datePickerInicio = DateEntry(frame, width=12, date_pattern="dd/MM/yyyy")
        self.datePickerInicio.place(relx=0.65, rely=0.069, anchor="nw")

        # Data Final
        self.labelDataFim = ctk.CTkLabel(frame, text="Data Final:")
        self.labelDataFim.place(relx=0.76, rely=0.02, anchor="nw")
        self.datePickerFim = DateEntry(frame, width=12, date_pattern="dd/MM/yyyy")
        self.datePickerFim.place(relx=0.76, rely=0.069, anchor="nw")
    else:
        self.labelDataInicio.destroy()
        del self.labelDataInicio
        self.datePickerInicio.destroy()
        del self.datePickerInicio
        self.labelDataFim.destroy()
        del self.labelDataFim
        self.datePickerFim.destroy()
        del self.datePickerFim



def verificaSeQuerFiltrarPorPeriodoContas(self, frame, checkbox, event=None):
    if checkbox:
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
        self.labelDataInicio.destroy()
        del self.labelDataInicio
        self.datePickerInicio.destroy()
        del self.datePickerInicio
        self.labelDataFim.destroy()
        del self.labelDataFim
        self.datePickerFim.destroy()
        del self.datePickerFim
        