import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
from funcoesTerceiras import calculaParcelasFaturamento
from componentes import criaFrameJanela, criarLabelEntry, criarLabelComboBox, criarLabelLateralEntry, criaBotao
from telas.telaObservacoes import telaObservacoes
from telas.telaTotaisNota import telaTotaisNotaSaida


def acessar(dados, *caminho, default=""):
    for chave in caminho:
        if isinstance(dados, dict) and chave in dados:
            dados = dados[chave]
        else:
            return default
    if isinstance(dados, dict) and "#text" in dados:
        return dados["#text"]
    return dados if isinstance(dados, str) else default


def telaTransporteNotaSaida(self):
    self.frametelaTransporte = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    # opções
    opcoesSerie = ["", "B", "C", "U"]
    opcoesModelo = ["", "57", "07", "08", "09", "10", "11"]
    opcoesTributacao = ["", "00", "10", "20", "30", "40", "41", "50", "51", "60", "70", "90"]

    # variáveis
    variavelModalidade = ctk.StringVar()
    variavelTransportador = ctk.StringVar()
    variavelCNPJTransportador = ctk.StringVar()
    variavelModelo = ctk.StringVar()
    variavelTributacao = ctk.StringVar()

    criarLabelEntry(self.frametelaTransporte, "Modalidade do frete", 0.05, 0.1, 0.25, variavelModalidade)
    criarLabelEntry(self.frametelaTransporte, "Transportador", 0.35, 0.1, 0.3, variavelTransportador)
    criarLabelEntry(self.frametelaTransporte, "CPF/CNPJ", 0.7, 0.1, 0.1, variavelCNPJTransportador)

    criarLabelEntry(self.frametelaTransporte, "Número", 0.05, 0.2, 0.05, ctk.StringVar())
    criarLabelComboBox(self.frametelaTransporte, "Série", 0.12, 0.2, 0.05, opcoesSerie)
    criarLabelEntry(self.frametelaTransporte, "SubSérie", 0.19, 0.2, 0.05, ctk.StringVar())
    modelo = criarLabelComboBox(self.frametelaTransporte, "Modelo", 0.26, 0.2, 0.05, opcoesModelo)
    modelo.set(variavelModelo.get())
    tribut = criarLabelComboBox(self.frametelaTransporte, "Tributação", 0.33, 0.2, 0.05, opcoesTributacao)
    tribut.set(variavelTributacao.get())
    criarLabelEntry(self.frametelaTransporte, "Chave CT-e ", 0.40, 0.2, 0.15, ctk.StringVar())
    criarLabelEntry(self.frametelaTransporte, "Data Emissão", 0.57, 0.2, 0.10, ctk.StringVar())
    criarLabelEntry(self.frametelaTransporte, "Data Prestação", 0.69, 0.2, 0.10, ctk.StringVar())
    criarLabelEntry(self.frametelaTransporte, "Desconto", 0.81, 0.2, 0.05, ctk.StringVar())
    criarLabelEntry(self.frametelaTransporte, "Total da Nota ", 0.88, 0.2, 0.05, ctk.StringVar())

    criarLabelLateralEntry(self.frametelaTransporte, "CFOP", 0.10, 0.4, 0.08, ctk.StringVar())
    criarLabelLateralEntry(self.frametelaTransporte, "BC Retenção ICMS", 0.40, 0.4, 0.15, ctk.StringVar())
    criarLabelLateralEntry(self.frametelaTransporte, "Valor ICMS Retido", 0.70, 0.4, 0.15, ctk.StringVar())
    criarLabelLateralEntry(self.frametelaTransporte, "Valor do Serviço", 0.10, 0.5, 0.15, ctk.StringVar())
    criarLabelLateralEntry(self.frametelaTransporte, "Aliquota Ret. ICMS", 0.40, 0.5, 0.15, ctk.StringVar())
    criarLabelLateralEntry(self.frametelaTransporte, "Município Gerador", 0.70, 0.5, 0.15, ctk.StringVar())


    criaBotao(self.frametelaTransporte, "Próximo - Tela Totais", 0.25, 0.94, 0.15, lambda: telaTotaisNotaSaida(self)).place(anchor="nw")
    criaBotao(self.frametelaTransporte, "Voltar", 0.05, 0.94, 0.15, lambda: self.frametelaTransporte.destroy()).place(anchor="nw")