import json
import sys
import os
import re
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
    return dados



def _remover_prefixos_namespace(dados):
    """Remove prefixos de namespace (ex.: "nfe:infNFe") para facilitar o acesso."""

    if isinstance(dados, dict):
        normalizado = {}
        for chave, valor in dados.items():
            chave_normalizada = chave.split(":", 1)[-1] if ":" in chave else chave
            normalizado[chave_normalizada] = _remover_prefixos_namespace(valor)
        return normalizado
    if isinstance(dados, list):
        return [_remover_prefixos_namespace(item) for item in dados]
    return dados


def _buscar_primeira_ocorrencia(dados, chave_procurada):
    """Retorna a primeira ocorrência de uma chave (ignorando prefixos) em qualquer nível."""

    if isinstance(dados, dict):
        for chave, valor in dados.items():
            chave_normalizada = chave.split(":", 1)[-1] if ":" in chave else chave
            if chave_normalizada == chave_procurada:
                return valor
            encontrado = _buscar_primeira_ocorrencia(valor, chave_procurada)
            if encontrado is not None:
                return encontrado
    elif isinstance(dados, list):
        for item in dados:
            encontrado = _buscar_primeira_ocorrencia(item, chave_procurada)
            if encontrado is not None:
                return encontrado
    return None


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
    dados = _remover_prefixos_namespace(dados)
    # print(dados)

    if "nfeProc" in dados and isinstance(dados.get("nfeProc"), dict):
        nfe_proc = dados["nfeProc"]
    elif "NFe" in dados and isinstance(dados.get("NFe"), dict):
        nfe_proc = {"NFe": dados["NFe"], "protNFe": dados.get("protNFe", {})}
    elif "infNFe" in dados and isinstance(dados.get("infNFe"), dict):
        nfe_proc = {"NFe": {"infNFe": dados["infNFe"]}, "protNFe": dados.get("protNFe", {})}
    else:
        inf_nfe = _buscar_primeira_ocorrencia(dados, "infNFe")
        prot_nfe = _buscar_primeira_ocorrencia(dados, "protNFe") or {}

        if isinstance(inf_nfe, dict):
            nfe_proc = {"NFe": {"infNFe": inf_nfe}, "protNFe": prot_nfe}
        else:
            raise KeyError(
                "Estrutura de XML inválida: não foi possível localizar os dados de infNFe."
            )
    print("aqui começa o nfe_proc: ",nfe_proc)
    nfe = acessar(nfe_proc, "NFe", "infNFe", default=None)
    print("o caminho da nota {}", nfe)
    if isinstance(nfe, list):
        nfe = nfe[0] if nfe else None
    if not isinstance(nfe, dict):
        raise KeyError(
            "Estrutura de XML inválida: não foi possível localizar os dados de infNFe."
        )

    id_nfe = acessar(nfe_proc, "NFe", "infNFe", "@Id")
    modelo = acessar(nfe_proc, "NFe", "infNFe", "ide", "mod")
    tipo = {"55": "NF-e", "65": "NFC-e"}.get(modelo, "")

    serie = acessar(nfe_proc, "NFe", "infNFe", "ide", "serie")
    numero = acessar(nfe_proc, "NFe", "infNFe", "ide", "nNF")
    chave = acessar(nfe_proc, "protNFe", "infProt", "chNFe") or ""

    # Fallbacks para garantir a chave de acesso mesmo quando o protocolo não estiver presente
    chave = re.sub(r"\D+", "", str(chave))
    if not chave:
        if id_nfe:
            m = re.search(r"([0-9]{44})", str(id_nfe))
            if m:
                chave = m.group(1)
        if not chave:
            m = re.search(r"<chNFe>([0-9]{44})</chNFe>", xml_conteudo)
            if m:
                chave = m.group(1)
    if not chave:
        raise ValueError("Não foi possível identificar a chave de acesso da NF-e gerada.")

    cUF = acessar(nfe_proc, "NFe", "infNFe", "ide", "cUF")
    uf_emit = acessar(nfe_proc, "NFe", "infNFe", "emit", "enderEmit", "UF")
    uf_dest = acessar(nfe_proc, "NFe", "infNFe", "dest", "enderDest", "UF")
    tpAmb = acessar(nfe_proc, "NFe", "infNFe", "ide", "tpAmb")
    tpNF = acessar(nfe_proc, "NFe", "infNFe", "ide", "tpNF")
    idDest = acessar(nfe_proc, "NFe", "infNFe", "ide", "idDest")
    natOp = acessar(nfe_proc, "NFe", "infNFe", "ide", "natOp")
    dhEmi = acessar(nfe_proc, "NFe", "infNFe", "ide", "dhEmi")
    dhSaiEnt = acessar(nfe_proc, "NFe", "infNFe", "ide", "dhSaiEnt")

    emit_cnpj = acessar(nfe_proc, "NFe", "infNFe", "emit", "CNPJ")
    emit_cpf = acessar(nfe_proc, "NFe", "infNFe", "emit", "CPF")
    emitente_cnpjcpf = emit_cnpj or emit_cpf
    emitente_nome = acessar(nfe_proc, "NFe", "infNFe", "emit", "xNome")
    emitente_ie = acessar(nfe_proc, "NFe", "infNFe", "emit", "IE")

    dest_cnpj = acessar(nfe_proc, "NFe", "infNFe", "dest", "CNPJ")
    dest_cpf = acessar(nfe_proc, "NFe", "infNFe", "dest", "CPF")
    destinatario_cnpjcpf = dest_cnpj or dest_cpf
    destinatario_nome = acessar(nfe_proc, "NFe", "infNFe", "dest", "xNome")
    destinatario_ie = acessar(nfe_proc, "NFe", "infNFe", "dest", "IE")

    valor_total = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vNF")
    valor_produtos = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vProd")
    valor_desconto = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vDesc")
    valor_frete = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vFrete")
    valor_seguro = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vSeg")
    valor_outras_despesas = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vOutro")
    valor_bc_icms = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vBC")
    valor_icms = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vICMS")
    valor_icms_desonerado = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vICMSDeson")
    valor_fcp = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vFCP")
    valor_bc_icms_st = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vBCST")
    valor_icms_st = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vST")
    valor_ipi = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vIPI")
    valor_pis = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vPIS")
    valor_cofins = acessar(nfe_proc, "NFe", "infNFe", "total", "ICMSTot", "vCOFINS")

    valor_bc_irrf = acessar(nfe_proc, "NFe", "infNFe", "retTrib", "vIRRF")

    transportadora_cnpj = acessar(nfe_proc, "NFe", "infNFe", "transp", "transporta", "CNPJ")
    transportadora_cpf = acessar(nfe_proc, "NFe", "infNFe", "transp", "transporta", "CPF")
    transportadora_cnpjcpf = transportadora_cnpj or transportadora_cpf
    transportadora_nome = acessar(nfe_proc, "NFe", "infNFe", "transp", "transporta", "xNome")
    mod_frete = acessar(nfe_proc, "NFe", "infNFe", "transp", "modFrete")
    placa_veiculo = acessar(nfe_proc, "NFe", "infNFe", "transp", "veicTransp", "placa")
    uf_veiculo = acessar(nfe_proc, "NFe", "infNFe", "transp", "veicTransp", "UF")
    rntc = acessar(nfe_proc, "NFe", "infNFe", "transp", "veicTransp", "RNTC")
    volum_qVol = acessar(nfe_proc, "NFe", "infNFe", "transp", "vol", "qVol")
    volum_esp = acessar(nfe_proc, "NFe", "infNFe", "transp", "vol", "esp")
    volum_marca = acessar(nfe_proc, "NFe", "infNFe", "transp", "vol", "marca")
    volum_nVol = acessar(nfe_proc, "NFe", "infNFe", "transp", "vol", "nVol")
    peso_liquido = acessar(nfe_proc, "NFe", "infNFe", "transp", "vol", "pesoL")
    peso_bruto = acessar(nfe_proc, "NFe", "infNFe", "transp", "vol", "pesoB")

    cStat = acessar(nfe_proc, "protNFe", "infProt", "cStat")
    xMotivo = acessar(nfe_proc, "protNFe", "infProt", "xMotivo")
    protocolo = acessar(nfe_proc, "protNFe", "infProt", "nProt")
    nRec = acessar(nfe_proc, "protNFe", "infProt", "nRec")
    dhRecbto = acessar(nfe_proc, "protNFe", "infProt", "dhRecbto")
    status = cStat

    try:
        self.chave_nfe = chave
        self.numero_nfe = numero
        self.serie_nfe = serie
        self.emitente_cnpj = emitente_cnpjcpf
        self.destinatario_cnpj = destinatario_cnpjcpf
        if hasattr(self, "variavelChaveDaNota") and hasattr(self.variavelChaveDaNota, "set"):
            self.variavelChaveDaNota.set(chave)
    except Exception:
        pass

    qrcode_url = acessar(nfe_proc, "NFe", "infNFeSupl", "qrCode")

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

    Insere.inserir_nota_fiscal(
        chave,
        numero,
        serie,
        dhEmi,
        dhSaiEnt,
        emitente_cnpjcpf,
        emitente_nome,
        destinatario_cnpjcpf,
        destinatario_nome,
        valor_total,
        valor_produtos,
        valor_bc_icms,
        valor_icms,
        valor_icms_desonerado,
        valor_bc_icms_st,
        valor_icms_st,
        valor_ipi,
        valor_pis,
        valor_cofins,
        valor_bc_irrf,
        transportadora_cnpjcpf,
        transportadora_nome,
        itens_json,
        data_vencimento,
    )


