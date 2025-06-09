import customtkinter as ctk
import gc

def criarLabelEntry(frame, texto, relx, rely, width, variavel):
    label = ctk.CTkLabel(frame, text=texto, width=50, font=("Arial", 15))
    label.place(relx=relx, rely=rely, anchor="w")
    entry = ctk.CTkEntry(frame, textvariable=variavel, corner_radius=0)
    entry.place(relx=relx, rely=rely + 0.04, relwidth=width, anchor="w")
    return entry

def criarLabelComboBox(frame, texto, relx, rely, width, lista):
    label = ctk.CTkLabel(frame, text=texto, width=50, font=("Arial", 15))
    label.place(relx=relx, rely=rely, anchor="w")
    entry = ctk.CTkComboBox(frame, values=lista, corner_radius=0)
    entry.place(relx=relx, rely=rely + 0.04, relwidth=width, anchor="w")
    return entry

def criarLabelLateralEntry(frame, texto, relx, rely, width, variavel):
    label = ctk.CTkLabel(frame, text=texto, anchor="e", width=100, font=("Arial", 15))
    label.place(relx=relx, rely=rely, anchor="e")
    entry = ctk.CTkEntry(frame, textvariable=variavel, corner_radius=0)
    entry.place(relx=relx + 0.01, rely=rely, relwidth=width, anchor="w")
    return entry

def criarLabelLateralComboBox(frame, texto, relx, rely, width, opcoes):
    label = ctk.CTkLabel(frame, text=texto, anchor="e", width=100, font=("Arial", 15))
    label.place(relx=relx, rely=rely, anchor="e")
    entry = ctk.CTkComboBox(frame, corner_radius=0, values=opcoes)
    entry.place(relx=relx + 0.01, rely=rely, relwidth=width, anchor="w")
    return entry

def criaFrame(self, relx, rely, width, height):
    frame = ctk.CTkFrame(self)
    frame.place(relx=relx, rely=rely, relwidth=width, relheight=height, anchor="center")
    return frame

def criaFrameScroll(self, parent):
    frame = ctk.CTkScrollableFrame(parent)
    frame.pack(fill="both", expand=True)
    return frame

def criaBotao(frame, texto, relx, rely, width, comando):
    botao = ctk.CTkButton(frame, text=texto, corner_radius=5,  command=lambda:comando())
    botao.place(relx=relx, rely=rely, relwidth=width,  anchor="center")
    return botao

def criaAviso(self, frame, height, width, texto, relx, rely):
    frameAviso = ctk.CTkFrame(frame, height=height, width=width, corner_radius=5, border_width=2, border_color="red",fg_color="transparent")
    frameAviso.place(relx=relx, rely=rely, anchor="center")
    labelAviso = ctk.CTkLabel(frameAviso,  text=texto, font=("Arial", 18))
    labelAviso.place(relx=0.5, y=30, anchor="center")
    self.after(3000, frameAviso.destroy)
    gc.collect
    return frame

def criaSimouNao(frame, texto, textobt1, textobt2, relx, rely, comando):
    variavel = ctk.StringVar(value="")
    label = ctk.CTkLabel(frame, text=texto, font=("Arial", 14))
    label.place(relx=relx, rely=rely)
    botao1 = ctk.CTkRadioButton(frame, text=textobt1, variable=variavel, value=textobt1,command=lambda: comando(variavel.get()))
    botao1.place(relx=relx - 0.01, rely=rely + 0.05)
    botao2 = ctk.CTkRadioButton(frame, text=textobt2, variable=variavel, value=textobt2,command=lambda: comando(variavel.get()))
    botao2.place(relx=relx + 0.05, rely=rely + 0.05)
    return botao1, botao2, label, variavel










# casos específicos

def criarLabelEntryEmail(frame, texto, relx, rely, width, variavel):
    label = ctk.CTkLabel(frame, text=texto, width=50, font=("Arial", 15))
    label.place(relx=relx, rely=rely, anchor="w")
    entry = ctk.CTkEntry(frame, textvariable=variavel, corner_radius=0)
    entry.place(relx=relx, rely=rely + 0.04, relwidth=width, anchor="w")
    return entry, label