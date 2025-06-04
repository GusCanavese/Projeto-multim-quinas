import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import datetime
from componentes import criarLabelEntry, criarLabelComboBox, criarLabelLateralEntry, criarLabelLateralComboBox


def telaTotais(self, dadosNota):
    frame = self.frameTelaRegistroCredito = ctk.CTkFrame(self)
    frame.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    # variaveis
    variavelOutrasDespesas = ctk.StringVar()
    variavelValorTotalProdutos = ctk.StringVar()
    variavelOutrasDespesas.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vIPI"]["#text"])
    variavelValorTotalProdutos.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vProd"]["#text"])


    criarLabelLateralEntry(frame, "Total frete", 0.1, 0.05, 0.11, None)
    criarLabelLateralEntry(frame, "Total Seguro", 0.1, 0.10, 0.11, None)
    criarLabelLateralEntry(frame, "Total Desconto", 0.1, 0.15, 0.11, None)
    criarLabelLateralEntry(frame, "Outras despesas", 0.1, 0.20, 0.11, variavelOutrasDespesas)

    criarLabelLateralEntry(frame, "Total Produtos",   0.35, 0.05, 0.11, variavelValorTotalProdutos)
    criarLabelLateralEntry(frame, "Valor do serviço", 0.35, 0.10, 0.11, None)
    criarLabelLateralEntry(frame, "Total BC ICMS",    0.35, 0.15, 0.11, None)
    criarLabelLateralEntry(frame, "ICMS",             0.35, 0.05, 0.11, None)
    criarLabelLateralEntry(frame, "Total BC ICMS ST", 0.35, 0.05, 0.11, None)
