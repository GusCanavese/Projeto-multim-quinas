import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
from funcoesTerceiras import calculaParcelasFaturamento
from componentes import criaFrameJanela, criarLabelEntry, criarLabelComboBox, criarLabelLateralEntry, criaBotao
from telas.telaObservacoes import telaObservacoes


def acessar(dados, *caminho, default=""):
    for chave in caminho:
        if isinstance(dados, dict) and chave in dados:
            dados = dados[chave]
        else:
            return default
    if isinstance(dados, dict) and "#text" in dados:
        return dados["#text"]
    return dados if isinstance(dados, str) else default


def telaTransporte(self, dadosNota):
    self.frametelaTransporte = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    # opções
    opcoesSerie = ["", "B", "C", "U"]
    opcoesModelo = ["", "57", "07", "08", "09", "10", "11"]
    opcoesTributacao = ["", "00", "10", "20", "30", "40", "41", "50", "51", "60", "70", "90"]

    # variáveis
    variavelModalidade = ctk.StringVar(value=self.modalidadeDoFrete.get())
    variavelTransportador = ctk.StringVar(value=acessar(dadosNota, "NFe", "infNFe", "transp", "transporta", "xNome"))
    variavelCNPJTransportador = ctk.StringVar(value=acessar(dadosNota, "NFe", "infNFe", "transp", "transporta", "CNPJ"))
    variavelModelo = ctk.StringVar(value=acessar(dadosNota, "NFe", "infNFe", "ide", "mod"))
    variavelTributacao = ctk.StringVar(value=acessar(dadosNota, "NFe", "infNFe", "transp", "ICMS", "tomaICMS") or acessar(dadosNota, "NFe", "infNFe", "transp", "ICMS", "vServ") or "00")
    self.variavelCFOPTransporte = ctk.StringVar(value=acessar(dadosNota, "NFe", "infNFe", "transp", "retTransp", "CFOP") or acessar(dadosNota, "NFe", "infNFe", "det", "prod", "CFOP"))
    self.variavelBCRetencaoICMS = ctk.StringVar(value=acessar(dadosNota, "NFe", "infNFe", "transp", "retTransp", "vBCRet"))
    self.variavelValorICMSRetido = ctk.StringVar(value=acessar(dadosNota, "NFe", "infNFe", "transp", "retTransp", "vICMSRet"))
    self.variavelValorServicoTransp = ctk.StringVar(value=acessar(dadosNota, "NFe", "infNFe", "transp", "retTransp", "vServ"))
    self.variavelAliquotaRetICMS = ctk.StringVar(value=acessar(dadosNota, "NFe", "infNFe", "transp", "retTransp", "pICMSRet"))
    self.variavelMunicipioGerador = ctk.StringVar(value=acessar(dadosNota, "NFe", "infNFe", "transp", "retTransp", "cMunFG"))

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
    criarLabelEntry(self.frametelaTransporte, "Total da Nota ", 0.88, 0.2, 0.05, ctk.StringVar(value=acessar(dadosNota, "NFe", "infNFe", "total", "ICMSTot", "vNF")))

    # Bloco de tributação organizado em colunas para evitar sobreposição
    frame_tributacao = ctk.CTkFrame(self.frametelaTransporte, fg_color="transparent")
    frame_tributacao.place(relx=0.08, rely=0.52, relwidth=0.88, relheight=0.2)

    colunas = [0.9, 0.41, 0.73]
    largura_coluna = 0.9

    criarLabelLateralEntry(frame_tributacao, "CFOP", colunas[0], 0.20, largura_coluna, self.variavelCFOPTransporte)
    criarLabelLateralEntry(frame_tributacao, "BC Retenção ICMS", colunas[1], 0.20, largura_coluna, self.variavelBCRetencaoICMS)
    criarLabelLateralEntry(frame_tributacao, "Valor ICMS Retido", colunas[2], 0.20, largura_coluna, self.variavelValorICMSRetido)

    criarLabelLateralEntry(frame_tributacao, "Valor do Serviço", colunas[0], 0.68, largura_coluna, self.variavelValorServicoTransp)
    criarLabelLateralEntry(frame_tributacao, "Aliquota Ret. ICMS", colunas[1], 0.68, largura_coluna, self.variavelAliquotaRetICMS)
    criarLabelLateralEntry(frame_tributacao, "Município Gerador", colunas[2], 0.68, largura_coluna, self.variavelMunicipioGerador)


    criaBotao(self.frametelaTransporte, "Próximo - Observações", 0.25, 0.94, 0.15, lambda: telaObservacoes(self, dadosNota)).place(anchor="nw")
    criaBotao(self.frametelaTransporte, "Voltar", 0.05, 0.94, 0.15, lambda: self.frametelaTransporte.destroy()).place(anchor="nw")