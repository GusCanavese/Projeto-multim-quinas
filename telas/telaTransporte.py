import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
from funcoesTerceiras import calculaParcelasFaturamento
from componentes import criarLabelEntry, criarLabelComboBox, criarLabelLateralEntry, criarLabelLateralComboBox


def telaTransporte(self, dadosNota):
    frame = self.frametelaTransporte = ctk.CTkFrame(self)
    frame.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)
    
    # variaveis 
    variavelModalidade = ctk.StringVar()
    variavelTransportador = ctk.StringVar()
    variavelCPFCNPJ = ctk.StringVar()
    variavelCNPJTransportador = ctk.StringVar()
    variavelModalidade.set(self.modalidadeDoFrete.get())
    variavelTransportador.set(dadosNota["NFe"]["infNFe"]["transp"]["transporta"]["xNome"]["#text"])
    variavelCNPJTransportador.set(dadosNota["NFe"]["infNFe"]["transp"]["transporta"]["CNPJ"]["#text"])

    criarLabelEntry(frame, "Modalidade do frete", 0.05, 0.1, 0.25, variavelModalidade)
    criarLabelEntry(frame, "Transportador", 0.35, 0.1, 0.3, variavelTransportador)
    criarLabelEntry(frame, "CPF/CNPJ", 0.7, 0.1, 0.1, variavelCNPJTransportador)
    