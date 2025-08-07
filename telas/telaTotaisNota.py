import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import datetime
from telas.telaFaturamentoEntradaNota import telaGerarFaturamentoEntradaNota
from componentes import criaFrameJanela, criarLabelLateralEntry, criaBotao


def telaTotaisNotaSaida(self):
    self.frameTelaTotais = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    # variaveis
    none = ctk.StringVar()
    none.set(0.00)

    variavelValorTotalProdutos = ctk.StringVar()
    variavelTotalBCIMS = ctk.StringVar()
    variavelICMS = ctk.StringVar()
    variavelBcImcsST = ctk.StringVar()
    variavelTotalPis = ctk.StringVar()
    variavelICMSCompleto = ctk.StringVar()
    variavelTotalICMSST = ctk.StringVar()
    variavelTotalCOFINS = ctk.StringVar()
    variavelValorLiquido = ctk.StringVar()
    variavelBCdoIRRF = ctk.StringVar()
    variavelIPI = ctk.StringVar()
    variavelTotalOutrasDespesas = ctk.StringVar()
    variavelICMS = ctk.StringVar()
    # variavelIPI.set(IPI)
    

    criarLabelLateralEntry(self.frameTelaTotais, "Total frete",     0.12, 0.05, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total Seguro",    0.12, 0.10, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total Desconto",  0.12, 0.15, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Outras despesas", 0.12, 0.20, 0.11, none)

    criarLabelLateralEntry(self.frameTelaTotais, "Total Produtos",   0.35, 0.05, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Valor do serviço", 0.35, 0.10, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total BC ICMS",    0.35, 0.15, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "ICMS",             0.35, 0.20, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total BC ICMS ST", 0.35, 0.25, 0.11, none)
    
    criarLabelLateralEntry(self.frameTelaTotais, "Total ICMS ST", 0.6, 0.05, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total 2",       0.6, 0.10, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total IPI",     0.6, 0.15, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total PIS",     0.6, 0.20, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Comple. ICMS",  0.6, 0.25, 0.11, none)

    criarLabelLateralEntry(self.frameTelaTotais, "Total COFINS ST",  0.85, 0.05, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total PIS ST",     0.85, 0.10, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total COFINS",     0.85, 0.15, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Valor líquido",    0.85, 0.20, 0.11, none)


    destinatario = ctk.CTkLabel(self.frameTelaTotais, text="Valores retidos-----------------------------------------------------------------------------")
    destinatario.place(relx=0.02, rely=0.45)



    criarLabelLateralEntry(self.frameTelaTotais, "Valor PIS retido",       0.22, 0.50, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Valor do COFINS Retido", 0.22, 0.55, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Valores Retido CSLL",    0.22, 0.60, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "BC do IRRF",             0.22, 0.65, 0.11, none)
    
    criarLabelLateralEntry(self.frameTelaTotais, "Valor Retido IRRF",        0.48, 0.50, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "BC da Previdência Social", 0.48, 0.55, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "VR Previdência Social",    0.48, 0.60, 0.11, none)

    criaBotao(self.frameTelaTotais, "Próximo - Tela de faturamento", 0.25, 0.94, 0.15, lambda: telaGerarFaturamentoEntradaNota(self)).place(anchor="nw")
    criaBotao(self.frameTelaTotais, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaTotais.destroy()).place(anchor="nw")

