import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import datetime
from telas.telaFaturamentoEntradaNota import telaGerarFaturamentoEntradaNota
from componentes import criarLabelEntry, criarLabelComboBox, criarLabelLateralEntry, criarLabelLateralComboBox


def telaTotais(self, dadosNota):
    frame = self.frameTelaRegistroCredito = ctk.CTkFrame(self)
    frame.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    # variaveis
    none = ctk.StringVar()
    none.set(0)
    variavelOutrasDespesas = ctk.StringVar()
    variavelValorTotalProdutos = ctk.StringVar()
    variavelTotalBCIMS = ctk.StringVar()
    variavelIMCS = ctk.StringVar()
    variavelBcImcsST = ctk.StringVar()
    variavelTotalPis = ctk.StringVar()
    variavelTotalIPI = ctk.StringVar()
    variavelICMSCompleto = ctk.StringVar()
    variavelTotalICMSST = ctk.StringVar()
    variavelTotalCOFINS = ctk.StringVar()
    variavelValorLiquido = ctk.StringVar()
    variavelBCdoIRRF = ctk.StringVar()
    variavelBCdoIRRF.set(dadosNota["NFe"]["infNFe"]["total"]["retTrib"]["vBCIRRF"]["#text"])
    variavelValorLiquido.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vNF"]["#text"])
    variavelTotalCOFINS.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vCOFINS"]["#text"])
    variavelTotalICMSST.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vST"]["#text"])
    variavelICMSCompleto.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vICMSDeson"]["#text"])
    variavelTotalIPI.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vIPI"]["#text"])
    variavelTotalPis.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vPIS"]["#text"])
    variavelBcImcsST.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vBCST"]["#text"])
    variavelIMCS.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vICMSDeson"]["#text"] )
    variavelTotalBCIMS.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vBC"]["#text"])
    variavelOutrasDespesas.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vIPI"]["#text"])
    variavelValorTotalProdutos.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vProd"]["#text"])


    criarLabelLateralEntry(frame, "Total frete",     0.1, 0.05, 0.11, none)
    criarLabelLateralEntry(frame, "Total Seguro",    0.1, 0.10, 0.11, none)
    criarLabelLateralEntry(frame, "Total Desconto",  0.1, 0.15, 0.11, none)
    criarLabelLateralEntry(frame, "Outras despesas", 0.1, 0.20, 0.11, variavelOutrasDespesas)

    criarLabelLateralEntry(frame, "Total Produtos",   0.35, 0.05, 0.11, variavelValorTotalProdutos)
    criarLabelLateralEntry(frame, "Valor do serviço", 0.35, 0.10, 0.11, none)
    criarLabelLateralEntry(frame, "Total BC ICMS",    0.35, 0.15, 0.11, variavelTotalBCIMS)
    criarLabelLateralEntry(frame, "ICMS",             0.35, 0.20, 0.11, variavelIMCS)
    criarLabelLateralEntry(frame, "Total BC ICMS ST", 0.35, 0.25, 0.11, variavelBcImcsST)
    
    criarLabelLateralEntry(frame, "Total ICMS ST", 0.6, 0.05, 0.11, variavelTotalICMSST)
    criarLabelLateralEntry(frame, "Total 2",       0.6, 0.10, 0.11, none)
    criarLabelLateralEntry(frame, "Total IPI",     0.6, 0.15, 0.11, variavelTotalIPI)
    criarLabelLateralEntry(frame, "Total PIS",     0.6, 0.20, 0.11, variavelTotalPis)
    criarLabelLateralEntry(frame, "Comple. ICMS",  0.6, 0.25, 0.11, variavelICMSCompleto)

    criarLabelLateralEntry(frame, "Total COFINS ST",  0.85, 0.05, 0.11, none)
    criarLabelLateralEntry(frame, "Total PIS ST",     0.85, 0.10, 0.11, none)
    criarLabelLateralEntry(frame, "Total COFINS",     0.85, 0.15, 0.11, variavelTotalCOFINS)
    criarLabelLateralEntry(frame, "Valor líquido",    0.85, 0.20, 0.11, variavelValorLiquido)


    destinatario = ctk.CTkLabel(frame, text="Valores retidos-------------------------------")
    destinatario.place(relx=0.02, rely=0.45)



    criarLabelLateralEntry(frame, "Valor PIS retido",       0.1, 0.50, 0.11, none)
    criarLabelLateralEntry(frame, "Valor do COFINS Retido", 0.1, 0.55, 0.11, none)
    criarLabelLateralEntry(frame, "Valores Retido CSLL",    0.1, 0.60, 0.11, none)
    criarLabelLateralEntry(frame, "BC do IRRF",             0.1, 0.65, 0.11, variavelBCdoIRRF)
    
    criarLabelLateralEntry(frame, "Valor Retido IRRF",        0.35, 0.50, 0.11, none)
    criarLabelLateralEntry(frame, "BC da Previdência Social", 0.35, 0.55, 0.11, none)
    criarLabelLateralEntry(frame, "VR Previdência Social",    0.35, 0.60, 0.11, none)

    
    proximo = ctk.CTkButton(frame, text="Próximo - Tela de faturamento", command=lambda:telaGerarFaturamentoEntradaNota(self, dadosNota))
    proximo.place(relx=0.25, rely=0.94, relwidth=0.15, anchor="nw")

    botaoVoltar = ctk.CTkButton(frame, text="Voltar", command=frame.destroy)
    botaoVoltar.place(relx=0.05, rely=0.94, relwidth=0.15, anchor="nw")