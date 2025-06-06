import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
from funcoesTerceiras import calculaParcelasFaturamento
from componentes import criarLabelEntry, criarLabelComboBox, criarLabelLateralEntry, criarLabelLateralComboBox
from telas.telaObservacoes import telaObservacoes


def telaTransporte(self, dadosNota):
    frame = self.frametelaTransporte = ctk.CTkFrame(self)
    frame.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    # opções
    opcoesSerie = ["", "B", "C", "U"]
    opcoesModelo = ["","57", "07", "08", "09", "10", "11"]
    opcoesTributacao = ["","00", "10", "20", "30", "40", "41","50", "51", "60", "70", "90"]
    
    # variaveis 
    none = ctk.StringVar()
    none.set("")
    variavelModalidade = ctk.StringVar()
    variavelTransportador = ctk.StringVar()
    variavelCNPJTransportador = ctk.StringVar()
    variavelModalidade.set(self.modalidadeDoFrete.get())
    variavelTransportador.set(dadosNota["NFe"]["infNFe"]["transp"]["transporta"]["xNome"]["#text"])
    variavelCNPJTransportador.set(dadosNota["NFe"]["infNFe"]["transp"]["transporta"]["CNPJ"]["#text"])

    criarLabelEntry(frame, "Modalidade do frete", 0.05, 0.1, 0.25, variavelModalidade)
    criarLabelEntry(frame, "Transportador", 0.35, 0.1, 0.3, variavelTransportador)
    criarLabelEntry(frame, "CPF/CNPJ", 0.7, 0.1, 0.1, variavelCNPJTransportador)


    criarLabelEntry(frame, "Número",         0.05, 0.2, 0.05, none)
    criarLabelComboBox(frame, "Série",       0.12, 0.2, 0.05, opcoesSerie)
    criarLabelEntry(frame, "SubSérie",       0.19, 0.2, 0.05, none)
    criarLabelComboBox(frame, "Modelo",      0.26, 0.2, 0.05, opcoesModelo)
    criarLabelComboBox(frame, "Tributação",  0.33, 0.2, 0.05, opcoesTributacao)
    criarLabelEntry(frame, "Chave CT-e ",    0.40, 0.2, 0.15, none)
    criarLabelEntry(frame, "Data Emissão",   0.57, 0.2, 0.10, none)
    criarLabelEntry(frame, "Data Prestação", 0.69, 0.2, 0.10, none)
    criarLabelEntry(frame, "Desconto",       0.81, 0.2, 0.05, none)
    criarLabelEntry(frame, "Total da Nota ", 0.88, 0.2, 0.05, none)

    criarLabelLateralEntry(frame, "CFOP",                0.10, 0.4, 0.08, None)
    criarLabelLateralEntry(frame, "BC Retenção ICMS",    0.40, 0.4, 0.15, None)
    criarLabelLateralEntry(frame, "Valor ICMS Retido",   0.70, 0.4, 0.15, None)
    criarLabelLateralEntry(frame, "Valor do Serviço",    0.10, 0.5, 0.15, None)
    criarLabelLateralEntry(frame, "Aliquota Ret. ICMS",  0.40, 0.5, 0.15, None)
    criarLabelLateralEntry(frame, "Município Gerador",   0.70, 0.5, 0.15, None)

    


    proximo = ctk.CTkButton(frame, text="Próximo - Observações", command=lambda:telaObservacoes(self, dadosNota))
    proximo.place(relx=0.25, rely=0.94, relwidth=0.15, anchor="nw")

    botaoVoltar = ctk.CTkButton(frame, text="Voltar", command=frame.destroy)
    botaoVoltar.place(relx=0.05, rely=0.94, relwidth=0.15, anchor="nw")
 

 
 


 


 

 

