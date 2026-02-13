import customtkinter as ctk
import gc


def criarLabelEntry(frame, texto, relx, rely, width, variavel):

    
    if texto in ("Desconto total(%)", "Desconto total($)", "Acréscimo total", 
                    "Valor frete", "TOTAL:", "Produto:", "Código:", "NCM:", 
                    "CSET:", "QTD:", "Beneficio Fisc:", "CST A", "CSOSN", 
                    "Alíq. Cálc. Créd. (%)", "Vr. Cred. ICMS", "Alíq. IOF (%)", 
                    "Alíq. II (%)", "BC II ", "Vr. IOF", "Vr. II", "Vr. Desp. Aduaneiras", "Alíq. PIS (%)", "BC PIS", "Vr. PIS",
                    "Vr. COFINS ST", "BC COFINS ST", "Alíq. COFINS ST (%)","Vr. COFINS", "BC COFINS", "Alíq. COFINS (%)", "Vr. PIS ST",
                    "BC PIS ST","Alíq. PIS ST (%)", 
                ):
        y=0.01
        
        dif = 0.055
        fonte = ("TkDefaultFont", 11)

    elif texto in ("Descrição", "Parcelas", "Total", "Forma", "Vencimento"):
        dif = 0.13
        fonte = ("TkDefaultFont", 15)
        y=0
    else:
        dif = 0.055
        fonte = ("TkDefaultFont", 15)
        y=0

    label = ctk.CTkLabel(frame, text=texto, width=50, font=fonte)
    label.place(relx=relx, rely=rely+y, anchor="w")

    if texto == "CPF" or texto == "CNPJ" or texto == "CPF/CNPJ *" or texto == "CPF *" or texto == "CNPJ *":
        max_length = 14
        numeric_only = True
    elif texto == "CEP" or texto == "CEP *":
        max_length = 8
        numeric_only = True
    elif texto == "Quantidade" or texto == "Quantidade *":
        max_length = 4
        numeric_only = True
    elif texto == "Valor de custo" or texto == "Valor de venda" or texto == "Quantidade":
        max_length = 30
        numeric_only = True
    elif texto == "Nome do produto":
        max_length = 40
        numeric_only = False
    else:
        max_length = 100
        numeric_only = False

    def _validate_input(valor_pos_edicao):
        if valor_pos_edicao == "":
            return True
        
        if len(valor_pos_edicao) > max_length:
            return False
            
        if numeric_only:
            if not valor_pos_edicao.isdigit():
                return False
        
        return True

    validation_command = frame.register(_validate_input)

    entry = ctk.CTkEntry(frame, textvariable=variavel, corner_radius=0, validate="key", validatecommand=(validation_command, '%P'))
    entry.place(relx=relx, rely=rely + dif, relwidth=width, anchor="w")

    return entry

def criarLabelComboBox(frame, texto, relx, rely, width, lista):
    if texto in ("CST A", "CSOSN", "CST B", "CST",):
        fonte = ("TkDefaultFont", 11)
        y=0.01
    elif texto in ("Filtrar por vendedor(a)"):
        fonte = ("TkDefaultFont", 15)
        y = -0.04
    else:
        fonte = ("TkDefaultFont", 15)
        y=0
    label = ctk.CTkLabel(frame, text=texto, width=50, font=fonte)
    label.place(relx=relx, rely=rely+y, anchor="w")
    entry = ctk.CTkComboBox(frame, values=lista, corner_radius=0)
    entry.bind("<Key>", lambda e: "break")
    entry.place(relx=relx, rely=rely + 0.04, relwidth=width, anchor="w")
    return entry


def checkbox(frame, texto, relx, rely, variavel, comando):
    checkbox = ctk.CTkCheckBox(master = frame, text=texto, variable=variavel, onvalue="on", offvalue="off", command=lambda:comando)
    checkbox.place(relx=relx, rely=rely)

def criaComboBox(frame, relx, rely, width, lista, comando):
    entry = ctk.CTkComboBox(frame, values=lista, corner_radius=0, command=comando)
    entry.bind("<Key>", lambda e: "break")
    entry.place(relx=relx, rely=rely, relwidth=width, anchor="center")
    return entry

def criarLabelLateralEntry(frame, texto, relx, rely, width, variavel):
    if texto in (
        "Mod. BC ICMS",
        "BC ICMS",
        "Red. BC ICMS (%)",
        "Aliq. ICMS (%)",
        "Vr. ICMS",
        "Mod. BC ICMS ST",
        "MVA ICMS ST (%)",
        "BC ICMS ST",
        "Red. BC ICMS ST (%)",
        "Aliq. ICMS ST (%)",
        "Vr. ICMS ST",
        "Vr. BC ICMS ST Ret.",
        "Vr. ICMS ST Ret.",
        "Mod. BC ICMS",
        "Mod. BC ICMS ST",
        "Vr. ICMS Subst.",
        "Alíq. ICMS ST c/ FCP",
        "BC ICMS ST Dest.",
        "Vr. ICMS ST Dest.",
        "BC FCP",
        "Alíq. FCP (%)",
        "Vr. FCP",
        "Aliq. FCP Dif.(%)",
        "BC FCP ST",
        "Alíq. FCP ST (%)",
        "Vr. FCP ST",
        "Vr. FCP Dif.",
        "BC FCP ST Ret.",
        "Alíq. FCP ST Ret.(%)",
        "Vr. FCP ST Ret.",
        "Vr. FCP Efetivo"
        "Valor BC ICMS"
    ):
        fonte = ("TkDefaultFont", 11)
    else:
        fonte = ("TkDefaultFont", 15)

    label = ctk.CTkLabel(frame, text=texto, width=100, font=fonte)
    label.place(relx=relx, rely=rely, anchor="e")

    if texto == "CPF" or texto == "CNPJ" or texto == "CPF/CNPJ *":
        max_length = 14
        numeric_only = True
    elif texto == "CEP" or texto == "CEP *":
        max_length = 8
        numeric_only = True
    elif texto == "Valor de custo" or texto == "Valor de venda":
        max_length = 30
        numeric_only = True
    else:
        max_length = 100
        numeric_only = False

    def _validate_input(valor_pos_edicao):
        if valor_pos_edicao == "":
            return True
        
        if len(valor_pos_edicao) > max_length:
            return False
            
        if numeric_only:
            if not valor_pos_edicao.isdigit():
                return False
        
        return True
    


    validation_command = frame.register(_validate_input)


    entry = ctk.CTkEntry(frame, textvariable=variavel, corner_radius=0, validate="key", validatecommand=(validation_command, '%P'))
    entry.place(relx=relx + 0.01, rely=rely, relwidth=width, anchor="w")
    return entry

def criarLabelLateralComboBox(frame, texto, relx, rely, width, opcoes):
    if texto in ("Mod. BC ICMS", "Mod. BC ICMS ST"):
        fonte = ("TkDefaultFont", 11)
    else:
        fonte = ("TkDefaultFont", 15)
    label = ctk.CTkLabel(frame, text=texto, anchor="e", width=100, font=fonte)
    label.place(relx=relx, rely=rely, anchor="e")
    entry = ctk.CTkComboBox(frame, corner_radius=0, values=opcoes)
    entry.bind("<Key>", lambda e: "break")
    entry.place(relx=relx + 0.01, rely=rely, relwidth=width, anchor="w")
    return entry

def criaFrameJanela(self, relx, rely, width, height, cor):
    frame = ctk.CTkFrame(self, fg_color=cor)
    frame.place(relx=relx, rely=rely, relwidth=width, relheight=height, anchor="center")
    return frame

def criaFrame(self, relx, rely, width, height):
    frame = ctk.CTkFrame(self)
    frame.place(relx=relx, rely=rely, relwidth=width, relheight=height, anchor="center")
    return frame

def criaBotao(frame, texto, relx, rely, width, comando):
    modo_atual = ctk.get_appearance_mode().lower()
    if modo_atual == "dark":
        text = "white"
    else:
        text = "white"
    fonte=("TkDefaultFont", 16)
    botao = ctk.CTkButton(frame, text=texto, corner_radius=5, font=fonte, command=lambda:comando(), text_color=text)
    botao.place(relx=relx, rely=rely, relwidth=width,  anchor="center")
    return botao

def criaBotaoPequeno(frame, texto, relx, rely, width, comando):
    modo_atual = ctk.get_appearance_mode().lower()
    if modo_atual == "dark":
        text = "white"
    else:
        text = "white"
    fonte=("TkDefaultFont", 11)
    botao = ctk.CTkButton(frame, text=texto, corner_radius=5, font=fonte, command=lambda:comando(), text_color=text)
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


def criaSimouNaoLateral(frame, texto, textobt1, textobt2, relx, rely, comando):
    variavel = ctk.StringVar(value="")
    label = ctk.CTkLabel(frame, text=texto, font=("Arial", 14))
    label.place(relx=relx, rely=rely)
    botao1 = ctk.CTkRadioButton(frame,text=textobt1,variable=variavel,value=textobt1,command=lambda: comando(variavel.get()))
    botao1.place(relx=relx, rely=rely + 0.05)
    botao2 = ctk.CTkRadioButton(frame,text=textobt2,variable=variavel, value=textobt2,command=lambda: comando(variavel.get()))
    botao2.place(relx=relx, rely=rely + 0.10) 
    return botao1, botao2, label, variavel


def criaLabel(frame, texto, relx, rely, width, cor):
    label = ctk.CTkLabel(frame, text=texto, fg_color=cor, wraplength=450, text_color="white")
    label.place(relx=relx, rely=rely, relwidth=width, anchor="w")
    return label

def criaEntry(frame, relx, rely, width, variavel):

    max_length = 100
    numeric_only = False

    def _validate_input(valor_pos_edicao):
        if valor_pos_edicao == "":
            return True
        
        if len(valor_pos_edicao) > max_length:
            return False
            
        if numeric_only:
            if not valor_pos_edicao.isdigit():
                return False
        
        return True

    validation_command = frame.register(_validate_input)

    entry = ctk.CTkEntry(frame, textvariable=variavel, corner_radius=0, validate="key", validatecommand=(validation_command, '%P'))
    entry.place(relx=relx, rely=rely, relwidth=width, anchor="w")
    return entry

def criaTextArea(frame, relx, rely, width, titulo, texto):
    label = ctk.CTkLabel(frame, text=titulo, height=30, font=("Century Gothic", 15))
    label.place(relx=relx, rely=rely)
    areaTexto = ctk.CTkTextbox(frame, height=150, corner_radius=0, wrap="word")
    areaTexto.insert("0.0", texto)
    areaTexto.place(relx=relx, rely=rely+0.05, relwidth=width)
    return areaTexto

def criaTextAreaModal(frame, relx, rely, width, titulo, texto):
    label = ctk.CTkLabel(frame, text=titulo, height=10, font=("TkDefaultFont", 11))
    label.place(relx=relx, rely=rely)
    areaTexto = ctk.CTkTextbox(frame, height=80, corner_radius=0, wrap="word")
    areaTexto.insert("0.0", texto)
    areaTexto.place(relx=relx, rely=rely+0.03, relwidth=width)
    return areaTexto

def criaLabelDescritivo(frame, texto, relx, rely, width, cor, variavel):
    labelTitulo = ctk.CTkLabel(frame, text=texto)
    labelTitulo.place(relx=relx, rely=rely, relwidth=width, anchor="w")
    label = ctk.CTkLabel(frame, fg_color=cor, textvariable=variavel, text_color="white")
    label.place(relx=relx, rely=rely+0.05, relwidth=width, anchor="w")
    return label








# casos específicos
def criaFrameScrolavel(self, relx, rely, width, height):
    frame = ctk.CTkFrame(self)
    frame.place(relx=relx, rely=rely, relwidth=width, relheight=height, anchor="center")
    return frame

def criarLabelEntryEmail(frame, texto, relx, rely, width, variavel):
    label = ctk.CTkLabel(frame, text=texto, width=50, font=("Arial", 15))
    label.place(relx=relx, rely=rely, anchor="w")
    entry = ctk.CTkEntry(frame, textvariable=variavel, corner_radius=0)
    entry.place(relx=relx, rely=rely + 0.04, relwidth=width, anchor="w")
    return entry, label
