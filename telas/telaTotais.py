import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from telas.telaFaturamentoEntradaNota import telaGerarFaturamentoEntradaNota
from componentes import criaFrameJanela, criarLabelLateralEntry, criaBotao


def telaTotais(self, dadosNota, IPI):
    self.frameTelaTotais = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    # variaveis
    none = ctk.StringVar()
    none.set(0.00)
    variavelOutrasDespesas = ctk.StringVar()
    variavelValorTotalProdutos = ctk.StringVar()
    variavelTotalBCIMS = ctk.StringVar()
    variavelICMS = ctk.StringVar()
    variavelBcImcsST = ctk.StringVar()
    variavelTotalPis = ctk.StringVar()
    variavelTotalIPI = ctk.StringVar()
    variavelICMSCompleto = ctk.StringVar()
    variavelTotalICMSST = ctk.StringVar()
    variavelTotalCOFINS = ctk.StringVar()
    variavelValorLiquido = ctk.StringVar()
    variavelBCdoIRRF = ctk.StringVar()
    variavelIPI = ctk.StringVar()
    variavelTotalOutrasDespesas = ctk.StringVar()
    variavelICMS = ctk.StringVar()

    variavelIPI.set(IPI)
    
    def get_nfe_value(data, path, default="0.00"):
        """Acessa valores aninhados no dict da NFe com fallback seguro"""
        keys = path.split('/')
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current.get("#text", current) if isinstance(current, dict) else current

    # Acessando os dados de forma segura:
    variavelBCdoIRRF.set(get_nfe_value(dadosNota, "NFe/infNFe/total/retTrib/vBCIRRF"))
    variavelValorLiquido.set(get_nfe_value(dadosNota, "NFe/infNFe/total/ICMSTot/vNF"))
    variavelTotalCOFINS.set(get_nfe_value(dadosNota, "NFe/infNFe/total/ICMSTot/vCOFINS"))
    variavelTotalICMSST.set(get_nfe_value(dadosNota, "NFe/infNFe/total/ICMSTot/vST"))
    variavelICMSCompleto.set(get_nfe_value(dadosNota, "NFe/infNFe/total/ICMSTot/vICMSDeson"))
    variavelTotalIPI.set(get_nfe_value(dadosNota, "NFe/infNFe/total/ICMSTot/vIPI"))
    variavelTotalPis.set(get_nfe_value(dadosNota, "NFe/infNFe/total/ICMSTot/vPIS"))
    variavelBcImcsST.set(get_nfe_value(dadosNota, "NFe/infNFe/total/ICMSTot/vBCST"))
    variavelTotalBCIMS.set(get_nfe_value(dadosNota, "NFe/infNFe/total/ICMSTot/vBC"))
    variavelOutrasDespesas.set(get_nfe_value(dadosNota, "NFe/infNFe/total/ICMSTot/vOutro"))
    variavelValorTotalProdutos.set(get_nfe_value(dadosNota, "NFe/infNFe/total/ICMSTot/vProd"))
    variavelICMS.set(get_nfe_value(dadosNota, "NFe/infNFe/total/ICMSTot/vICMS"))

    variavelTotalOutrasDespesas.set(float(variavelOutrasDespesas.get())+float(variavelIPI.get()))


    criarLabelLateralEntry(self.frameTelaTotais, "Total frete",     0.12, 0.05, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total Seguro",    0.12, 0.10, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total Desconto",  0.12, 0.15, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Outras despesas", 0.12, 0.20, 0.11, variavelTotalOutrasDespesas)

    criarLabelLateralEntry(self.frameTelaTotais, "Total Produtos",   0.35, 0.05, 0.11, variavelValorTotalProdutos)
    criarLabelLateralEntry(self.frameTelaTotais, "Valor do serviço", 0.35, 0.10, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total BC ICMS",    0.35, 0.15, 0.11, variavelTotalBCIMS)
    criarLabelLateralEntry(self.frameTelaTotais, "ICMS",             0.35, 0.20, 0.11, variavelICMS)
    criarLabelLateralEntry(self.frameTelaTotais, "Total BC ICMS ST", 0.35, 0.25, 0.11, variavelBcImcsST)
    
    criarLabelLateralEntry(self.frameTelaTotais, "Total ICMS ST", 0.6, 0.05, 0.11, variavelTotalICMSST)
    criarLabelLateralEntry(self.frameTelaTotais, "Total 2",       0.6, 0.10, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total IPI",     0.6, 0.15, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total PIS",     0.6, 0.20, 0.11, variavelTotalPis)
    criarLabelLateralEntry(self.frameTelaTotais, "Comple. ICMS",  0.6, 0.25, 0.11, variavelICMSCompleto)

    criarLabelLateralEntry(self.frameTelaTotais, "Total COFINS ST",  0.85, 0.05, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total PIS ST",     0.85, 0.10, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Total COFINS",     0.85, 0.15, 0.11, variavelTotalCOFINS)
    criarLabelLateralEntry(self.frameTelaTotais, "Valor líquido",    0.85, 0.20, 0.11, variavelValorLiquido)


    destinatario = ctk.CTkLabel(self.frameTelaTotais, text="Valores retidos-----------------------------------------------------------------------------")
    destinatario.place(relx=0.02, rely=0.45)



    criarLabelLateralEntry(self.frameTelaTotais, "Valor PIS retido",       0.22, 0.50, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Valor do COFINS Retido", 0.22, 0.55, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "Valores Retido CSLL",    0.22, 0.60, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "BC do IRRF",             0.22, 0.65, 0.11, variavelBCdoIRRF)
    
    criarLabelLateralEntry(self.frameTelaTotais, "Valor Retido IRRF",        0.48, 0.50, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "BC da Previdência Social", 0.48, 0.55, 0.11, none)
    criarLabelLateralEntry(self.frameTelaTotais, "VR Previdência Social",    0.48, 0.60, 0.11, none)

    criaBotao(self.frameTelaTotais, "Próximo - Tela de faturamento", 0.25, 0.94, 0.15, lambda: telaGerarFaturamentoEntradaNota(self, dadosNota, variavelValorLiquido)).place(anchor="nw")
    criaBotao(self.frameTelaTotais, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaTotais.destroy()).place(anchor="nw")

