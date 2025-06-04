import customtkinter as ctk

def criarLabelEntry(frame, texto, relx, rely, width, variavel):
    label = ctk.CTkLabel(frame, text=texto, width=50)
    label.place(relx=relx, rely=rely, anchor="w")
    entry = ctk.CTkEntry(frame, textvariable=variavel, corner_radius=0)
    entry.place(relx=relx, rely=rely + 0.04, relwidth=width, anchor="w")
    return entry

def criarLabelComboBox(frame, texto, relx, rely, width, lista):
    label = ctk.CTkLabel(frame, text=texto, width=50)
    label.place(relx=relx, rely=rely, anchor="w")
    entry = ctk.CTkComboBox(frame, values=lista, corner_radius=0)
    entry.place(relx=relx, rely=rely + 0.04, relwidth=width, anchor="w")
    return entry

def criarLabelLateralEntry(frame, texto, relx, rely, width, variavel):
    label = ctk.CTkLabel(frame, text=texto, anchor="e", width=100)
    label.place(relx=relx, rely=rely, anchor="e")
    entry = ctk.CTkEntry(frame, textvariable=variavel, corner_radius=0)
    entry.place(relx=relx + 0.01, rely=rely, relwidth=width, anchor="w")
    return entry

def criarLabelLateralComboBox(frame, texto, relx, rely, width, opcoes):
    label = ctk.CTkLabel(frame, text=texto, anchor="e", width=100)
    label.place(relx=relx, rely=rely, anchor="e")
    entry = ctk.CTkComboBox(frame, corner_radius=0, values=opcoes)
    entry.place(relx=relx + 0.01, rely=rely, relwidth=width, anchor="w")
    return entry

