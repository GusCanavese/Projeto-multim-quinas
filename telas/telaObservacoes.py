import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
import json
from consultas.insert import Insere
from componentes import criaFrameJanela, criaBotao, criaTextArea


def acessar(dados, *caminho, default=""):
    for chave in caminho:
        if isinstance(dados, dict) and chave in dados:
            dados = dados[chave]
        else:
            return default
    if isinstance(dados, dict) and "#text" in dados:
        return dados["#text"]
    return dados if isinstance(dados, str) else default


def montar_parametros_nota_saida(dadosNota):
    def pegar_valor(dados, *caminhos, default=""):
        for caminho in caminhos:
            atual = dados
            for chave in caminho:
                if isinstance(atual, dict) and chave in atual:
                    atual = atual[chave]
                else:
                    atual = None
                    break
            if atual not in (None, ""):
                if isinstance(atual, dict) and "#text" in atual:
                    return atual["#text"]
                return atual
        return default

    def obter_estrutura(dados, *caminho):
        atual = dados
        for chave in caminho:
            if isinstance(atual, dict) and chave in atual:
                atual = atual[chave]
            else:
                return {}
        return atual

    dados_base = (dadosNota or {}).get("nfeProc", dadosNota or {})
    nfe = obter_estrutura(dados_base, "NFe")
    inf_nfe = obter_estrutura(nfe, "infNFe")
    prot_nfe = obter_estrutura(dados_base, "protNFe", "infProt")

    modelo = acessar(inf_nfe, "ide", "mod")
    tipo = {"55": "NF-e", "65": "NFC-e"}.get(modelo, "")
    serie = acessar(inf_nfe, "ide", "serie")
    numero = acessar(inf_nfe, "ide", "nNF")
    chave = acessar(prot_nfe, "chNFe") or (
        acessar(inf_nfe, "Id").replace("NFe", "") if acessar(inf_nfe, "Id") else ""
    )
    cUF = acessar(inf_nfe, "ide", "cUF")
    uf_emit = acessar(inf_nfe, "emit", "enderEmit", "UF")
    uf_dest = acessar(inf_nfe, "dest", "enderDest", "UF")
    tpAmb = acessar(inf_nfe, "ide", "tpAmb")
    tpNF = acessar(inf_nfe, "ide", "tpNF")
    idDest = acessar(inf_nfe, "ide", "idDest")
    natOp = acessar(inf_nfe, "ide", "natOp")
    dhEmi = acessar(inf_nfe, "ide", "dhEmi")
    dhSaiEnt = acessar(inf_nfe, "ide", "dhSaiEnt")

    emitente_cnpjcpf = pegar_valor(inf_nfe, ("emit", "CNPJ"), ("emit", "CPF"))
    emitente_nome = acessar(inf_nfe, "emit", "xNome")
    emitente_ie = acessar(inf_nfe, "emit", "IE")

    destinatario_cnpjcpf = pegar_valor(inf_nfe, ("dest", "CNPJ"), ("dest", "CPF"))
    destinatario_nome = acessar(inf_nfe, "dest", "xNome")
    destinatario_ie = acessar(inf_nfe, "dest", "IE")

    icms_tot = obter_estrutura(inf_nfe, "total", "ICMSTot")
    valor_total = acessar(icms_tot, "vNF")
    valor_produtos = acessar(icms_tot, "vProd")
    valor_desconto = acessar(icms_tot, "vDesc")
    valor_frete = acessar(icms_tot, "vFrete")
    valor_seguro = acessar(icms_tot, "vSeg")
    valor_outras_despesas = acessar(icms_tot, "vOutro")
    valor_bc_icms = acessar(icms_tot, "vBC")
    valor_icms = acessar(icms_tot, "vICMS")
    valor_icms_desonerado = acessar(icms_tot, "vICMSDeson")
    valor_fcp = acessar(icms_tot, "vFCP")
    valor_bc_icms_st = acessar(icms_tot, "vBCST")
    valor_icms_st = acessar(icms_tot, "vST")
    valor_ipi = acessar(icms_tot, "vIPI")
    valor_pis = acessar(icms_tot, "vPIS")
    valor_cofins = acessar(icms_tot, "vCOFINS")
    valor_bc_irrf = acessar(inf_nfe, "retTrib", "vIRRF")

    transp = obter_estrutura(inf_nfe, "transp")
    transportadora_cnpjcpf = pegar_valor(transp, ("transporta", "CNPJ"), ("transporta", "CPF"))
    transportadora_nome = acessar(transp, "transporta", "xNome")
    mod_frete = acessar(transp, "modFrete")
    placa_veiculo = acessar(transp, "veicTransp", "placa")
    uf_veiculo = acessar(transp, "veicTransp", "UF")
    rntc = acessar(transp, "veicTransp", "RNTC")

    vol = transp.get("vol", {}) if isinstance(transp, dict) else {}
    if isinstance(vol, list):
        vol = vol[0] if vol else {}
    volum_qVol = acessar(vol, "qVol")
    volum_esp = acessar(vol, "esp")
    volum_marca = acessar(vol, "marca")
    volum_nVol = acessar(vol, "nVol")
    peso_liquido = acessar(vol, "pesoL")
    peso_bruto = acessar(vol, "pesoB")

    cStat = acessar(prot_nfe, "cStat")
    xMotivo = acessar(prot_nfe, "xMotivo")
    protocolo = acessar(prot_nfe, "nProt")
    nRec = acessar(prot_nfe, "nRec")
    dhRecbto = acessar(prot_nfe, "dhRecbto")
    status = cStat
    qrcode_url = acessar(nfe, "infNFeSupl", "qrCode")

    cobr = obter_estrutura(inf_nfe, "cobr")
    duplicatas = cobr.get("dup", {}) if isinstance(cobr, dict) else {}
    if isinstance(duplicatas, list):
        data_vencimento = next((acessar(dup, "dVenc") for dup in duplicatas if acessar(dup, "dVenc")), "")
    else:
        data_vencimento = acessar(duplicatas, "dVenc")

    itens = inf_nfe.get("det", [])
    if isinstance(itens, dict):
        itens = [itens]
    itens_json = json.dumps(itens, ensure_ascii=False)
    cfop = acessar(itens[0], "prod", "CFOP") if itens else ""
    operacao = natOp

    def vazio_para_none(valor):
        return None if valor in ("", None) else valor

    dhSaiEnt = vazio_para_none(dhSaiEnt)
    valor_bc_irrf = vazio_para_none(valor_bc_irrf)
    volum_qVol = vazio_para_none(volum_qVol)
    volum_esp = vazio_para_none(volum_esp)
    volum_marca = vazio_para_none(volum_marca)
    volum_nVol = vazio_para_none(volum_nVol)
    peso_liquido = vazio_para_none(peso_liquido)
    peso_bruto = vazio_para_none(peso_bruto)
    cStat = vazio_para_none(cStat)
    xMotivo = vazio_para_none(xMotivo)
    protocolo = vazio_para_none(protocolo)
    nRec = vazio_para_none(nRec)
    dhRecbto = vazio_para_none(dhRecbto)
    data_vencimento = vazio_para_none(data_vencimento)
    cfop = vazio_para_none(cfop)
    operacao = vazio_para_none(operacao)

    return (
        tipo,
        modelo,
        serie,
        numero,
        chave,
        cUF,
        uf_emit,
        uf_dest,
        tpAmb,
        tpNF,
        idDest,
        natOp,
        dhEmi,
        dhSaiEnt,
        emitente_cnpjcpf,
        emitente_nome,
        emitente_ie,
        destinatario_cnpjcpf,
        destinatario_nome,
        destinatario_ie,
        valor_total,
        valor_produtos,
        valor_desconto,
        valor_frete,
        valor_seguro,
        valor_outras_despesas,
        valor_bc_icms,
        valor_icms,
        valor_icms_desonerado,
        valor_fcp,
        valor_bc_icms_st,
        valor_icms_st,
        valor_ipi,
        valor_pis,
        valor_cofins,
        valor_bc_irrf,
        transportadora_cnpjcpf,
        transportadora_nome,
        mod_frete,
        placa_veiculo,
        uf_veiculo,
        rntc,
        volum_qVol,
        volum_esp,
        volum_marca,
        volum_nVol,
        peso_liquido,
        peso_bruto,
        cStat,
        xMotivo,
        protocolo,
        nRec,
        dhRecbto,
        status,
        qrcode_url,
        data_vencimento,
        itens_json,
        cfop,
        operacao,
    )


def destruir_quadros_fluxo_entrada(self):
    quadros = [
        "frameTelaNotaFiscalEntrada",
        "frameTelaProdutos",
        "frameTelaTotais",
        "frameTelaGerarFaturamento",
        "frametelaTransporte",
        "frameTelaObservacoes",
        "frameEscolherNotaFiscal",
    ]
    for nome in quadros:
        frame = getattr(self, nome, None)
        if frame is not None:
            try:
                frame.destroy()
            except Exception:
                pass


def telaObservacoes(self, dadosNota):

    self.frameTelaObservacoes = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    variavelObsFisco = ctk.StringVar()
    variavelObsFisco.set(acessar(dadosNota, "NFe", "infNFe", "infAdic", "infAdFisco"))

    variavelObsContribuinte = ctk.StringVar()
    variavelObsContribuinte.set(acessar(dadosNota, "NFe", "infNFe", "infAdic", "infCpl"))

    area1 = criaTextArea(
        self.frameTelaObservacoes,
        0.5,
        0.15,
        0.4,
        "INFORMAÇÕES DO INTERESSE DO CONTRIBUINTE",
        variavelObsContribuinte.get(),
    )
    area1.place(relheight=0.3)
    area2 = criaTextArea(
        self.frameTelaObservacoes,
        0.05,
        0.15,
        0.4,
        "INFORMAÇÕES DO INTERESSE DO FISCO",
        variavelObsFisco.get(),
    )
    area2.place(relheight=0.3)

    parametros = montar_parametros_nota_saida(dadosNota)

    def insereRetorna():
        Insere.inserir_nota_fiscal_saida(*parametros, "Saída")
        destruir_quadros_fluxo_entrada(self)

    criaBotao(self.frameTelaObservacoes, "Salvar nota", 0.25, 0.94, 0.15, lambda: insereRetorna()).place(anchor="nw")
    criaBotao(self.frameTelaObservacoes, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaObservacoes.destroy()).place(anchor="nw")
