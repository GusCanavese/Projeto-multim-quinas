import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
import json
from consultas.insert import Insere
from funcoesTerceiras import calculaParcelasFaturamento
from componentes import criaFrameJanela, criaBotao, criaLabel, criaTextArea
from tkinter import messagebox


def acessar(dados, *caminho, default=""):
    for chave in caminho:
        if isinstance(dados, dict) and chave in dados:
            dados = dados[chave]
        else:
            return default
    if isinstance(dados, dict) and "#text" in dados:
        return dados["#text"]
    return dados if isinstance(dados, str) else default



def telaObservacoesNotaSaida(self):

    self.frameTelaObservacoes = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    


    variavelObsFisco = ctk.StringVar()
    # variavelObsFisco.set(acessar(dadosNota, "NFe", "infNFe", "infAdic", "infAdFisco"))

    variavelObsContribuinte = ctk.StringVar()
    # variavelObsContribuinte.set(acessar(dadosNota, "NFe", "infNFe", "infAdic", "infCpl"))

    area1 = criaTextArea(self.frameTelaObservacoes, 0.5, 0.15, 0.4, "INFORMAÇÕES DO INTERESSE DO CONTRIBUINTE", variavelObsContribuinte.get())
    area1.place(relheight=0.3)
    area2 = criaTextArea(self.frameTelaObservacoes, 0.05, 0.15, 0.4, "INFORMAÇÕES DO INTERESSE DO FISCO", variavelObsFisco.get())
    area2.place(relheight=0.3)
                    

    print(variavelObsContribuinte.get())
    print(variavelObsFisco.get())

    # Extrair todos os dados necessários
    # dados_insercao = {
    #     'chave_nfe': acessar(dadosNota, "NFe", "infNFe", "Id").replace("NFe", ""),
    #     'numero_nfe': acessar(dadosNota, "NFe", "infNFe", "ide", "nNF"),
    #     'serie_nfe': acessar(dadosNota, "NFe", "infNFe", "ide", "serie"),
    #     'data_emissao': acessar(dadosNota, "NFe", "infNFe", "ide", "dhEmi"),
    #     'data_saida': acessar(dadosNota, "NFe", "infNFe", "ide", "dhSaiEnt"),
    #     'emitente_cnpj': acessar(dadosNota, "NFe", "infNFe", "emit", "CNPJ"),
    #     'emitente_nome': acessar(dadosNota, "NFe", "infNFe", "emit", "xNome"),
    #     'destinatario_cnpj': acessar(dadosNota, "NFe", "infNFe", "dest", "CNPJ"),
    #     'destinatario_nome': acessar(dadosNota, "NFe", "infNFe", "dest", "xNome"),
    #     'valor_total': acessar(dadosNota, "NFe", "infNFe", "total", "ICMSTot", "vNF", default="0"),
    #     'valor_produtos': acessar(dadosNota, "NFe", "infNFe", "total", "ICMSTot", "vProd", default="0"),
    #     'valor_bc_icms': acessar(dadosNota, "NFe", "infNFe", "total", "ICMSTot", "vBC", default="0"),
    #     'valor_icms': acessar(dadosNota, "NFe", "infNFe", "total", "ICMSTot", "vICMS", default="0"),
    #     'valor_icms_desonerado': acessar(dadosNota, "NFe", "infNFe", "total", "ICMSTot", "vICMSDeson", default="0"),
    #     'valor_bc_icms_st': acessar(dadosNota, "NFe", "infNFe", "total", "ICMSTot", "vBCST", default="0"),
    #     'valor_icms_st': acessar(dadosNota, "NFe", "infNFe", "total", "ICMSTot", "vST", default="0"),
    #     'valor_ipi': acessar(dadosNota, "NFe", "infNFe", "total", "ICMSTot", "vIPI", default="0"),
    #     'valor_pis': acessar(dadosNota, "NFe", "infNFe", "total", "ICMSTot", "vPIS", default="0"),
    #     'valor_cofins': acessar(dadosNota, "NFe", "infNFe", "total", "ICMSTot", "vCOFINS", default="0"),
    #     'valor_bc_irrf': acessar(dadosNota, "NFe", "infNFe", "total", "retTrib", "vBCIRRF", default="0"),
    #     'transportadora_cnpj': acessar(dadosNota, "NFe", "infNFe", "transp", "transporta", "CNPJ", default=""),
    #     'transportadora_nome': acessar(dadosNota, "NFe", "infNFe", "transp", "transporta", "xNome", default=""),
    #     'data_vencimento': acessar(dadosNota, "NFe", "infNFe", "cobr", "dup", "dVenc", default="")
    # }

    # Preparar itens da nota
    # itens = dadosNota["NFe"]["infNFe"]["det"]
    # if not isinstance(itens, list):
    #     itens = [itens]  # Garante que itens seja sempre uma lista

    itens_json = []
    # for item in itens:
    #     itens_json.append({
    #         'codigo': acessar(item, "prod", "cProd"),
    #         'descricao': acessar(item, "prod", "xProd"),
    #         'quantidade': acessar(item, "prod", "qCom"),
    #         'unidade': acessar(item, "prod", "uCom"),
    #         'valor_unitario': acessar(item, "prod", "vUnCom"),
    #         'valor_total': acessar(item, "prod", "vProd"),
    #         'cfop': acessar(item, "prod", "CFOP"),
    #         'ncm': acessar(item, "prod", "NCM"),
    #         'cest': acessar(item, "prod", "CEST", default=""),
    #         'ean': acessar(item, "prod", "cEAN", default="")
    #     })

    # dados_insercao['itens_json'] = json.dumps(itens_json, ensure_ascii=False)

    def insereRetorna():
        # Insere.inserir_nota_fiscal(**dados_insercao)
        try:
            self.frameTelaRegistraCredito.destroy()
            self.frameTelaProdutos.destroy()
            self.frameTelaTotais.destroy()
            self.frameTelaGerarFaturamento.destroy()
            self.frametelaTransporte.destroy()
            self.frameTelaObservacoes.destroy()
            self.frameEscolherNotaFiscal.destroy()
        except Exception as e:
            print(f"Erro ao inserir nota fiscal: {e}")
            messagebox.showinfo(title="Acessar Info", message="Fluxo finalizado")
            self.frameTelaRegistraCredito.destroy()
            self.frameTelaProdutos.destroy()
            self.frameTelaTotais.destroy()
            self.frameTelaGerarFaturamento.destroy()
            self.frametelaTransporte.destroy()
            self.frameTelaObservacoes.destroy()
            self.frameEscolherNotaFiscal.destroy()
            
    criaBotao(self.frameTelaObservacoes, "salvar", 0.25, 0.94, 0.15, lambda: insereRetorna()).place(anchor="nw")
    criaBotao(self.frameTelaObservacoes, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaObservacoes.destroy()).place(anchor="nw")
