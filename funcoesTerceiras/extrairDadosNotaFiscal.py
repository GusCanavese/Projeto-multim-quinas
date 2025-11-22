import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consultas.insert import Insere
import xmltodict
from datetime import date


def acessar(dados, *caminho, default=""):
    for chave in caminho:
        if isinstance(dados, dict) and chave in dados:
            dados = dados[chave]
        else:
            return default
    if isinstance(dados, dict) and "#text" in dados:
        return dados["#text"]
    return dados if isinstance(dados, str) else default



def extrairDadosDaNota(self, xmlCaminho, tipo, status):
    xmlCaminho = (xmlCaminho or "").strip()
    if not xmlCaminho:
        raise FileNotFoundError(
            "O caminho do XML não foi retornado pelo ACBr Monitor. "
            "Verifique se o monitor está configurado para gravar os logs/arquivos na mesma pasta do executável."
        )

    if not os.path.isabs(xmlCaminho):
        xmlCaminho = os.path.abspath(xmlCaminho)

    if not os.path.exists(xmlCaminho):
        raise FileNotFoundError(f"XML da nota não encontrado: {xmlCaminho}")

    with open(xmlCaminho, "r", encoding="utf-8", errors="ignore") as f:
            xml_conteudo = f.read()
    dados = xmltodict.parse(xml_conteudo, force_list=("det", "dup"), dict_constructor=dict)
    print(dados)

    nfe = dados["nfeProc"]["NFe"]["infNFe"]

    id_nfe = acessar(dados, "nfeProc", "NFe", "infNFe", "@Id")
    modelo = acessar(dados, "nfeProc", "NFe", "infNFe", "ide", "mod")
    tipo = {"55": "NF-e", "65": "NFC-e"}.get(modelo, "")

    serie = acessar(dados, "nfeProc", "NFe", "infNFe", "ide", "serie")
    numero = acessar(dados, "nfeProc", "NFe", "infNFe", "ide", "nNF")
    chave = acessar(dados, "nfeProc", "protNFe", "infProt", "chNFe")

    cUF = acessar(dados, "nfeProc", "NFe", "infNFe", "ide", "cUF")
    uf_emit = acessar(dados, "nfeProc", "NFe", "infNFe", "emit", "enderEmit", "UF")
    uf_dest = acessar(dados, "nfeProc", "NFe", "infNFe", "dest", "enderDest", "UF")
    tpAmb = acessar(dados, "nfeProc", "NFe", "infNFe", "ide", "tpAmb")
    tpNF = acessar(dados, "nfeProc", "NFe", "infNFe", "ide", "tpNF")
    idDest = acessar(dados, "nfeProc", "NFe", "infNFe", "ide", "idDest")
    natOp = acessar(dados, "nfeProc", "NFe", "infNFe", "ide", "natOp")
    dhEmi = acessar(dados, "nfeProc", "NFe", "infNFe", "ide", "dhEmi")
    dhSaiEnt = acessar(dados, "nfeProc", "NFe", "infNFe", "ide", "dhSaiEnt")

    emit_cnpj = acessar(dados, "nfeProc", "NFe", "infNFe", "emit", "CNPJ")
    emit_cpf = acessar(dados, "nfeProc", "NFe", "infNFe", "emit", "CPF")
    emitente_cnpjcpf = emit_cnpj or emit_cpf
    emitente_nome = acessar(dados, "nfeProc", "NFe", "infNFe", "emit", "xNome")
    emitente_ie = acessar(dados, "nfeProc", "NFe", "infNFe", "emit", "IE")

    dest_cnpj = acessar(dados, "nfeProc", "NFe", "infNFe", "dest", "CNPJ")
    dest_cpf = acessar(dados, "nfeProc", "NFe", "infNFe", "dest", "CPF")
    destinatario_cnpjcpf = dest_cnpj or dest_cpf
    destinatario_nome = acessar(dados, "nfeProc", "NFe", "infNFe", "dest", "xNome")
    destinatario_ie = acessar(dados, "nfeProc", "NFe", "infNFe", "dest", "IE")

    valor_total = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vNF")
    valor_produtos = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vProd")
    valor_desconto = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vDesc")
    valor_frete = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vFrete")
    valor_seguro = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vSeg")
    valor_outras_despesas = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vOutro")
    valor_bc_icms = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vBC")
    valor_icms = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vICMS")
    valor_icms_desonerado = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vICMSDeson")
    valor_fcp = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vFCP")
    valor_bc_icms_st = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vBCST")
    valor_icms_st = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vST")
    valor_ipi = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vIPI")
    valor_pis = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vPIS")
    valor_cofins = acessar(dados, "nfeProc", "NFe", "infNFe", "total", "ICMSTot", "vCOFINS")

    valor_bc_irrf = acessar(dados, "nfeProc", "NFe", "infNFe", "retTrib", "vIRRF")

    transportadora_cnpj = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "transporta", "CNPJ")
    transportadora_cpf = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "transporta", "CPF")
    transportadora_cnpjcpf = transportadora_cnpj or transportadora_cpf
    transportadora_nome = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "transporta", "xNome")
    mod_frete = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "modFrete")
    placa_veiculo = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "veicTransp", "placa")
    uf_veiculo = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "veicTransp", "UF")
    rntc = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "veicTransp", "RNTC")
    volum_qVol = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "vol", "qVol")
    volum_esp = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "vol", "esp")
    volum_marca = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "vol", "marca")
    volum_nVol = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "vol", "nVol")
    peso_liquido = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "vol", "pesoL")
    peso_bruto = acessar(dados, "nfeProc", "NFe", "infNFe", "transp", "vol", "pesoB")

    cStat = acessar(dados, "nfeProc", "protNFe", "infProt", "cStat")
    xMotivo = acessar(dados, "nfeProc", "protNFe", "infProt", "xMotivo")
    protocolo = acessar(dados, "nfeProc", "protNFe", "infProt", "nProt")
    nRec = acessar(dados, "nfeProc", "protNFe", "infProt", "nRec")
    dhRecbto = acessar(dados, "nfeProc", "protNFe", "infProt", "dhRecbto")
    status = cStat

    qrcode_url = acessar(dados, "nfeProc", "NFe", "infNFeSupl", "qrCode")

    cobr = nfe.get("cobr", {})
    dups = cobr.get("dup", [])
    data_vencimento = "".join([dup.get("dVenc", "") for dup in dups][:1])

    det_lista = nfe["det"]
    itens_json = json.dumps(det_lista, ensure_ascii=False)

    cfop = "".join([
        item.get("prod", {}).get("CFOP", "")
        for item in det_lista
    ][:1])

    operacao = natOp

    
    print("#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#+=#")
    print(id_nfe,tipo,modelo,serie,numero,chave,cUF,uf_emit,uf_dest,tpAmb,tpNF,idDest,natOp,dhEmi,dhSaiEnt,emitente_cnpjcpf,emitente_nome,emitente_ie,destinatario_cnpjcpf,destinatario_nome,destinatario_ie,valor_total,valor_produtos,valor_desconto,valor_frete,valor_seguro,valor_outras_despesas,valor_bc_icms,valor_icms,valor_icms_desonerado,valor_fcp,valor_bc_icms_st,valor_icms_st,valor_ipi,valor_pis,valor_cofins,valor_bc_irrf,transportadora_cnpjcpf,transportadora_nome,mod_frete,placa_veiculo,uf_veiculo,rntc,volum_qVol,volum_esp,volum_marca,volum_nVol,peso_liquido,peso_bruto,cStat,xMotivo,protocolo,nRec,dhRecbto,status,qrcode_url,data_vencimento,itens_json,cfop,operacao,)

    dhSaiEnt        = None if dhSaiEnt        == "" else dhSaiEnt
    valor_bc_irrf   = None if valor_bc_irrf   == "" else valor_bc_irrf
    volum_qVol      = None if volum_qVol      == "" else volum_qVol
    volum_esp       = None if volum_esp       == "" else volum_esp
    volum_marca     = None if volum_marca     == "" else volum_marca
    volum_nVol      = None if volum_nVol      == "" else volum_nVol
    peso_liquido    = None if peso_liquido    == "" else peso_liquido
    peso_bruto      = None if peso_bruto      == "" else peso_bruto
    cStat           = None if cStat           == "" else cStat
    xMotivo         = None if xMotivo         == "" else xMotivo
    protocolo       = None if protocolo       == "" else protocolo
    nRec            = None if nRec            == "" else nRec
    data_vencimento = None if data_vencimento == "" else data_vencimento
    itens_json      = None if itens_json      == "" else itens_json
    cfop            = None if cfop            == "" else cfop
    operacao        = None if operacao        == "" else operacao

    Insere.inserir_nota_fiscal_saida(tipo,modelo,serie,numero,chave,cUF,
                                     uf_emit,uf_dest,tpAmb,tpNF,idDest,natOp,dhEmi,
                                     dhSaiEnt,emitente_cnpjcpf,emitente_nome,
                                     emitente_ie,destinatario_cnpjcpf,destinatario_nome,
                                     destinatario_ie,valor_total,valor_produtos,
                                     valor_desconto,valor_frete,valor_seguro,
                                     valor_outras_despesas,valor_bc_icms,valor_icms,
                                     valor_icms_desonerado,valor_fcp,valor_bc_icms_st,
                                     valor_icms_st,valor_ipi,valor_pis,valor_cofins,
                                     valor_bc_irrf,transportadora_cnpjcpf,transportadora_nome,
                                     mod_frete,placa_veiculo,uf_veiculo,rntc,volum_qVol,
                                     volum_esp,volum_marca,volum_nVol,peso_liquido,peso_bruto,
                                     cStat,xMotivo,protocolo,nRec,dhRecbto,status,qrcode_url,
                                     data_vencimento,itens_json,cfop,operacao, "Saída")


