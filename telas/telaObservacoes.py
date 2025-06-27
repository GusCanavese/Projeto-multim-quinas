import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
import json
from consultas.insert import Insere
from funcoesTerceiras import calculaParcelasFaturamento
from componentes import criarLabelEntry, criarLabelComboBox, criarLabelLateralEntry, criarLabelLateralComboBox, criaFrame, criaBotao


def telaObservacoes(self, dadosNota):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    
    def safe_get(dados, path, default=""):
        """Acessa dados aninhados de forma segura"""
        keys = path.split('.')
        current = dados
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current.get("#text", current) if isinstance(current, dict) else current

    # Extrair todos os dados necessários
    dados_insercao = {
        'chave_nfe': safe_get(dadosNota, "NFe.infNFe.Id").replace("NFe", ""),
        'numero_nfe': safe_get(dadosNota, "NFe.infNFe.ide.nNF"),
        'serie_nfe': safe_get(dadosNota, "NFe.infNFe.ide.serie"),
        'data_emissao': safe_get(dadosNota, "NFe.infNFe.ide.dhEmi"),
        'data_saida': safe_get(dadosNota, "NFe.infNFe.ide.dhSaiEnt"),
        'emitente_cnpj': safe_get(dadosNota, "NFe.infNFe.emit.CNPJ"),
        'emitente_nome': safe_get(dadosNota, "NFe.infNFe.emit.xNome"),
        'destinatario_cnpj': safe_get(dadosNota, "NFe.infNFe.dest.CNPJ"),
        'destinatario_nome': safe_get(dadosNota, "NFe.infNFe.dest.xNome"),
        'valor_total': safe_get(dadosNota, "NFe.infNFe.total.ICMSTot.vNF", "0"),
        'valor_produtos': safe_get(dadosNota, "NFe.infNFe.total.ICMSTot.vProd", "0"),
        'valor_bc_icms': safe_get(dadosNota, "NFe.infNFe.total.ICMSTot.vBC", "0"),
        'valor_icms': safe_get(dadosNota, "NFe.infNFe.total.ICMSTot.vICMS", "0"),
        'valor_icms_desonerado': safe_get(dadosNota, "NFe.infNFe.total.ICMSTot.vICMSDeson", "0"),
        'valor_bc_icms_st': safe_get(dadosNota, "NFe.infNFe.total.ICMSTot.vBCST", "0"),
        'valor_icms_st': safe_get(dadosNota, "NFe.infNFe.total.ICMSTot.vST", "0"),
        'valor_ipi': safe_get(dadosNota, "NFe.infNFe.total.ICMSTot.vIPI", "0"),
        'valor_pis': safe_get(dadosNota, "NFe.infNFe.total.ICMSTot.vPIS", "0"),
        'valor_cofins': safe_get(dadosNota, "NFe.infNFe.total.ICMSTot.vCOFINS", "0"),
        'valor_bc_irrf': safe_get(dadosNota, "NFe.infNFe.total.retTrib.vBCIRRF", "0"),
        'transportadora_cnpj': safe_get(dadosNota, "NFe.infNFe.transp.transporta.CNPJ", ""),
        'transportadora_nome': safe_get(dadosNota, "NFe.infNFe.transp.transporta.xNome", ""),
    }

    # Preparar itens da nota
    itens = dadosNota["NFe"]["infNFe"]["det"]
    if not isinstance(itens, list):
        itens = [itens]  # Garante que itens seja sempre uma lista

    itens_json = []
    for item in itens:
        itens_json.append({
            'codigo': safe_get(item, "prod.cProd"),
            'descricao': safe_get(item, "prod.xProd"),
            'quantidade': safe_get(item, "prod.qCom"),
            'unidade': safe_get(item, "prod.uCom"),
            'valor_unitario': safe_get(item, "prod.vUnCom"),
            'valor_total': safe_get(item, "prod.vProd"),
            'cfop': safe_get(item, "prod.CFOP"),
            'ncm': safe_get(item, "prod.NCM"),
            'cest': safe_get(item, "prod.CEST", ""),
            'ean': safe_get(item, "prod.cEAN", "")
        })

    # Adicionar itens ao dicionário de dados
    dados_insercao['itens_json'] = json.dumps(itens_json, ensure_ascii=False)

    # Chamar a função de inserção (que já existe)
    

    criaBotao(frame, "Prntar", 0.25, 0.94, 0.15, lambda: Insere.inserir_nota_fiscal(**dados_insercao)).place(anchor="nw")
    criaBotao(frame, "Voltar", 0.05, 0.94, 0.15, lambda: frame.destroy()).place(anchor="nw")