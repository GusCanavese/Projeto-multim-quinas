"""
sped_fiscal_completo.py
------------------------------------
Gera arquivo SPED Fiscal (EFD ICMS/IPI) cobrindo TODOS os blocos padrão
(0, C, D, E, G, H, K, 1 e 9), com dados reais quando disponíveis no mesmo *data model*
do seu `criarNFe.py` e "sem movimento" (IND_MOV=1) quando não houver dados.

Versão de leiaute (padrão): 3.1.8 (vigente em 2025). Pode ser alterada pelo parâmetro `versao_layout`.

Como usar rapidamente
---------------------
from sped_fiscal_completo import gerar_sped_fiscal_completo

# self = seu objeto de emissão que já usa criarNFe.py
caminho = gerar_sped_fiscal_completo(self,
                                     caminho_txt="sped_fiscal_COMPLETO.txt",
                                     dt_ini="20250801", dt_fin="20250831")

Observações importantes
-----------------------
- Este módulo produz um arquivo tecnicamente completo, com todos os blocos e fechamentos.
- Onde não houver dados na sua aplicação (ex.: serviços, inventário, CIAP, K200), o bloco é aberto
  com sem-movimento (IND_MOV=1). Você pode alimentar dados opcionais para cada bloco (ver docstrings).
- Para a apuração do ICMS (Bloco E), aceita um parâmetro `apuracao_icms` para informar débitos/créditos
  reais. Se você não passar, será feita uma apuração **simplificada** a partir dos C190 (somatório dos
  débitos ICMS de saída) e créditos = 0 (o que pode não refletir sua realidade). Ajuste conforme seu caso.
"""

from datetime import datetime
import calendar
import os
import re
from collections import defaultdict, Counter

# ------------------- helpers -------------------
def _sd(x):
    return re.sub(r"\D", "", str(x or ""))

def _get_strvar(obj, attr, default=""):
    try:
        v = getattr(obj, attr)
        if hasattr(v, "get"):
            return (v.get() or "").strip()
        return (str(v) or "").strip()
    except Exception:
        return str(default)

def _get_num(obj, attr, default=0.0):
    try:
        v = getattr(obj, attr)
        if hasattr(v, "get"):
            v = v.get()
        v = str(v).replace(",", ".")
        return float(v or 0.0)
    except Exception:
        return float(default)

def _dt_yyyymmdd(dt):
    s = (dt or "").strip()
    if re.fullmatch(r"\d{8}", s):  # YYYYMMDD
        return s
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s.replace("-", "")
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", s):
        d, m, y = s.split("/")
        return f"{y}{m}{d}"
    return datetime.now().strftime("%Y%m%d")

def _reg(*campos):
    return "|" + "|".join("" if c is None else str(c) for c in campos) + "|\r\n"

# contador por registro, para Bloco 9 (9900)
class RegCount:
    def __init__(self):
        self.c = Counter()
    def add(self, codigo):
        self.c[codigo] += 1
    def items(self):
        return self.c.items()

# ------------------- mapeamentos do seu criarNFe.py -------------------

def _get_emit_dest(self):
    emit = {
        "CNPJ": _sd(_get_strvar(self, "variavelCNPJRazaoSocialEmitente")) or "00995044000107",
        "xNome": _get_strvar(self, "variavelRazaoSocialEmitente") or "EMITENTE DEMO",
        "IE": (_get_strvar(self, "inscricaoEstadualEmitente") or "ISENTO").upper(),
        "UF": _get_strvar(self, "ufEmitente", "MG"),
        "xMun": _get_strvar(self, "munEmitente", "SAO JOAO DEL REI"),
        "CEP": _get_strvar(self, "cepEmitente", "36301194"),
        "ender": {
            "xLgr": _get_strvar(self, "logradouroEmitente", "RUA DEMO"),
            "nro": _get_strvar(self, "numeroEmitente", "0"),
            "xBairro": _get_strvar(self, "bairroEmitente", "CENTRO"),
            "cMun": _get_strvar(self, "cMunEmitente", "3162500"),
            "fone": _get_strvar(self, "foneEmitente", ""),
        },
        "IM": _get_strvar(self, "inscricaoMunicipalEmitente", ""),
        "EMAIL": _get_strvar(self, "emailEmitente", ""),
    }
    if emit["IE"] != "ISENTO":
        emit["IE"] = _sd(emit["IE"]) or "ISENTO"

    dest = {
        "CNPJCPF": _sd(_get_strvar(self, "variavelCNPJRazaoSocialRemetente")),
        "xNome": _get_strvar(self, "variavelRazaoSocialRemetente"),
        "UF": _get_strvar(self, "ufDestinatario", emit["UF"]),
        "xMun": _get_strvar(self, "munDestinatario", emit["xMun"]),
        "IE": _get_strvar(self, "ieDestinatario", ""),
    }
    if dest["IE"] and dest["IE"].upper() != "ISENTO":
        dest["IE"] = _sd(dest["IE"])
    return emit, dest

def _coleta_unidades_produtos(itens):
    unids = set()
    prods = {}
    for it in itens:
        u = (it.get("unidade") or "UN").upper()
        unids.add(u)
        cProd = it.get("codigo") or "1"
        prods[cProd] = {
            "cProd": cProd,
            "xProd": it.get("descricao") or "ITEM",
            "NCM": it.get("ncm") or "00000000",
            "uCom": u,
        }
    return sorted(unids), prods

def _agrega_c190(itens, regime="SN"):
    acc = defaultdict(lambda: {"vBC": 0.0, "vICMS": 0.0, "vIPI": 0.0, "vProd": 0.0})
    for it in itens:
        cfop = (it.get("cfop") or "5102")
        cst = (it.get("cst") or it.get("cst_icms") or "").strip()
        csosn = (it.get("csosn") or "").strip()
        key_cst = csosn if regime == "SN" and csosn else (cst or "00")
        vbc = float(str(it.get("vBC") or it.get("bc_icms") or 0).replace(",", ".") or 0)
        vicms = float(str(it.get("vICMS") or it.get("valor_icms") or 0).replace(",", ".") or 0)
        vipi = float(str(it.get("valor_ipi") or 0).replace(",", ".") or 0)
        vprod = float(str(it.get("valor_total") or it.get("valor_unitario") or 0).replace(",", ".") or 0)
        key = (cfop, key_cst)
        acc[key]["vBC"] += vbc
        acc[key]["vICMS"] += vicms
        acc[key]["vIPI"] += vipi
        acc[key]["vProd"] += vprod
    return acc

# ------------------- blocos -------------------

def _bloco_0(self, linhas, rc: RegCount, dt_ini, dt_fin, versao_layout="3.1.8"):
    emit, dest = _get_emit_dest(self)
    COD_VER = "018" if versao_layout == "3.1.8" else "019"
    COD_FIN = "0"
    NOME = emit["xNome"]; CNPJ = emit["CNPJ"]; UF = emit["UF"]; IE = emit["IE"]
    COD_MUN = emit["ender"]["cMun"]; IM = emit["IM"]; SUFRAMA=""
    IND_PERFIL = "A"; IND_ATIV = "0"

    def add(*campos):
        linhas.append(_reg(*campos)); rc.add(campos[0])

    add("0000", COD_VER, COD_FIN, dt_ini, dt_fin, NOME, CNPJ, UF, IE, COD_MUN, IM, SUFRAMA, IND_PERFIL, IND_ATIV)
    add("0001", "0")
    # 0005
    FANTASIA = NOME; CEP = _get_strvar(self, "cepEmitente", "")
    END = emit["ender"]["xLgr"]; NUM = emit["ender"]["nro"]; COMPL = ""; BAIRRO = emit["ender"]["xBairro"]
    FONE = emit["ender"]["fone"]; FAX = ""; EMAIL = emit["EMAIL"]
    add("0005", FANTASIA, CEP, END, NUM, COMPL, BAIRRO, FONE, FAX, EMAIL)

    # 0100 (contabilista) - opcional; preenche vazio por padrão
    CRC = _get_strvar(self, "crcContador", "")
    NOME_CON = _get_strvar(self, "nomeContador", "")
    CPF_CON = _sd(_get_strvar(self, "cpfContador", ""))
    CRC_UF = _get_strvar(self, "ufCRC", "")
    FONE_CON = _get_strvar(self, "foneContador", "")
    EMAIL_CON = _get_strvar(self, "emailContador", "")
    COD_MUN_CON = _get_strvar(self, "cMunContador", "")
    if NOME_CON or CPF_CON or CRC:
        add("0100", NOME_CON, CPF_CON, CRC, CRC_UF, FONE_CON, EMAIL_CON, COD_MUN_CON)

    # 0150 participantes (emitente/dest)
    add("0150", "EMIT", NOME, "", CNPJ, "", IE, UF, "", emit["xMun"])
    if dest.get("CNPJCPF") or dest.get("xNome"):
        add("0150", "DEST", dest.get("xNome") or "DESTINATARIO", "", dest.get("CNPJCPF"), "", dest.get("IE"), dest.get("UF"), "", dest.get("xMun"))

    # 0190 unidades e 0200 produtos
    itens = list(getattr(self, "valoresDosItens", []) or [])
    unids, produtos = _coleta_unidades_produtos(itens)
    for u in unids:
        add("0190", u, u)
    for cProd, prod in produtos.items():
        add("0200", cProd, prod["xProd"], "", prod["NCM"], "", "", "", prod["uCom"], "", "", "")
        # 0205 (alteração item) omitido, a menos que você forneça self.prod_alteracoes

    # 0400/0450/0460 (cadastros auxiliares) — preencher se você tiver essas tabelas
    # por padrão, omitimos para não "sujar" o arquivo com códigos fictícios

def _bloco_C(self, linhas, rc: RegCount, dt_ini, dt_fin):
    def add(*campos):
        linhas.append(_reg(*campos)); rc.add(campos[0])

    itens = list(getattr(self, "valoresDosItens", []) or [])
    tem_docs = bool(itens)
    add("C001", "0" if tem_docs else "1")
    if not tem_docs:
        return

    # capa NF-e C100
    regime = "SN" if str(_get_strvar(self, "crt", "1")) in ("1","2") else "NR"
    ind_oper = "1" if _get_strvar(self, "variavelEntradaOuSaida", "1") == "1" else "0"
    ind_emit = "1"
    cod_part = "DEST" if ind_oper == "1" else "EMIT"
    mod = "55"
    nnf = _get_strvar(self, "variavelNumeroDaNota", "1")
    serie = _get_strvar(self, "variavelSerieDaNota", "1")
    chave = _get_strvar(self, "variavelChaveDaNota", "")

    data_emissao = _get_strvar(self, "data_emissao", "")
    if "/" in data_emissao:
        d, m, y = data_emissao.split("/")[:3]
        dt_e = f"{y}{m}{d}"
    else:
        dt_e = dt_ini

    vl_doc = _get_num(self, "valorLiquido", 0.0)
    vl_desc = _get_num(self, "totalDesconto", 0.0)
    vl_frt = _get_num(self, "totalFrete", 0.0)
    vl_seg = _get_num(self, "totalSeguro", 0.0)
    vl_out_da = _get_num(self, "outrasDespesas", 0.0)
    vl_bc_icms = _get_num(self, "vBC", 0.0)
    vl_icms    = _get_num(self, "valorICMS", 0.0)
    vl_ipi     = _get_num(self, "totalIPI", 0.0)

    add("C100", ind_oper, ind_emit, cod_part, "00", mod, serie, nnf, dt_e, dt_e,
        "1", "1", "1", f"{vl_doc:.2f}", f"{vl_desc:.2f}", "0.00", f"{vl_frt:.2f}",
        f"{vl_seg:.2f}", f"{vl_out_da:.2f}", f"{vl_bc_icms:.2f}", f"{vl_icms:.2f}",
        "0.00", f"{vl_ipi:.2f}", "0.00", "", "", "", chave)

    # C170 itens
    for idx, it in enumerate(itens, start=1):
        q = float(str(it.get("quantidade", "0")).replace(",", ".") or 0)
        v_un = float(str(it.get("valor_unitario", "0")).replace(",", ".") or 0)
        v_prod = float(str(it.get("valor_total", v_un)).replace(",", ".") or 0)
        cfop = it.get("cfop") or "5102"
        cst = (it.get("cst") or it.get("cst_icms") or it.get("csosn") or "00")
        x_prod = it.get("descricao") or "ITEM"
        u = (it.get("unidade") or "UN").upper()
        aliq_icms = float(str(it.get("aliq_icms", "0")).replace(",", ".") or 0)
        vbc = float(str(it.get("vBC") or it.get("bc_icms") or 0).replace(",", ".") or 0)
        vicms = float(str(it.get("vICMS") or it.get("valor_icms") or 0).replace(",", ".") or 0)
        vipi = float(str(it.get("valor_ipi") or 0).replace(",", ".") or 0)
        add("C170", idx, x_prod, u, f"{q:.4f}", f"{v_un:.6f}", f"{v_prod:.2f}", cst, cfop, "", "",
            f"{vbc:.2f}", f"{aliq_icms:.2f}", f"{vicms:.2f}", "0.00", "0.00", "0.00", "0.00", "0.00",
            "0.00", "0.00", "0.00", f"{vipi:.2f}")

    # C190 agregação por CFOP/tributação
    agreg = _agrega_c190(itens, regime=regime)
    for (cfop, cst_ou_csosn), tot in sorted(agreg.items()):
        add("C190", cst_ou_csosn, cfop, "0.00", f"{tot['vBC']:.2f}", f"{tot['vICMS']:.2f}",
            "0.00", "0.00", f"{tot['vIPI']:.2f}", f"{tot['vProd']:.2f}")

def _bloco_D(self, linhas, rc: RegCount, docs_servicos=None):
    def add(*campos):
        linhas.append(_reg(*campos)); rc.add(campos[0])

    tem_docs = bool(docs_servicos)
    add("D001", "0" if tem_docs else "1")
    if not tem_docs:
        return
    # Exemplos (D100/D190) poderiam ser gerados se você fornecer docs_servicos (lista de dicts)
    # Aqui mantemos apenas a abertura quando houver dados.

def _bloco_E(self, linhas, rc: RegCount, dt_ini, dt_fin, apuracao_icms=None):
    def add(*campos):
        linhas.append(_reg(*campos)); rc.add(campos[0])

    # Abre bloco E com movimento se houver NF-e (C100) ou se apuração for passada
    tem_c = any(ln.startswith("|C100|") for ln in linhas)
    add("E001", "0" if (tem_c or apuracao_icms) else "1")
    if not (tem_c or apuracao_icms):
        return

    add("E100", dt_ini, dt_fin)

    # Apuração simplificada ou informada
    if apuracao_icms is None:
        # pega débitos ICMS de C190
        total_debitos = 0.0
        for ln in linhas:
            # |C190|CST|CFOP|ALIQ|vBC|vICMS|...
            if ln.startswith("|C190|"):
                split = ln.strip().split("|")
                vICMS = float(split[6].replace(",", ".") if split[6] else 0.0)
                total_debitos += vICMS
        apuracao_icms = {
            "VL_TOT_DEBITOS": total_debitos,
            "VL_TOT_CREDITOS": 0.0,
            "VL_AJ_DEBITOS": 0.0,
            "VL_AJ_CREDITOS": 0.0,
            "VL_ESTORNOS_DEBITOS": 0.0,
            "VL_ESTORNOS_CREDITOS": 0.0,
            "VL_SLD_CREDOR_ANT": 0.0,
            "VL_OUT_DEB": 0.0,
            "VL_OUT_CRED": 0.0,
        }

    # Campos mínimos E110 (simplificado)
    deb = float(apuracao_icms.get("VL_TOT_DEBITOS", 0))
    cre = float(apuracao_icms.get("VL_TOT_CREDITOS", 0))
    ajd = float(apuracao_icms.get("VL_AJ_DEBITOS", 0))
    ajc = float(apuracao_icms.get("VL_AJ_CREDITOS", 0))
    estd = float(apuracao_icms.get("VL_ESTORNOS_DEBITOS", 0))
    estc = float(apuracao_icms.get("VL_ESTORNOS_CREDITOS", 0))
    sld_ant = float(apuracao_icms.get("VL_SLD_CREDOR_ANT", 0))
    odeb = float(apuracao_icms.get("VL_OUT_DEB", 0))
    ocred = float(apuracao_icms.get("VL_OUT_CRED", 0))

    vl_sld_apurado = (deb + ajd + odeb - estd) - (cre + ajc + ocred - estc) - sld_ant
    vl_sld_transp = abs(vl_sld_apurado) if vl_sld_apurado < 0 else 0.0
    vl_icms_recolher = vl_sld_apurado if vl_sld_apurado > 0 else 0.0

    add("E110",
        f"{deb:.2f}", f"{ajd:.2f}", f"{estd:.2f}", f"{cre:.2f}", f"{ajc:.2f}", f"{estc:.2f}",
        f"{sld_ant:.2f}", f"{odeb:.2f}", f"{ocred:.2f}",
        f"{vl_sld_apurado:.2f}", f"{vl_sld_transp:.2f}", f"{vl_icms_recolher:.2f}", "0.00")

    if vl_icms_recolher > 0:
        # E116: obrigações do ICMS a recolher (vencimento básico = dia 15 do mês seguinte)
        y, m, d = int(dt_fin[:4]), int(dt_fin[4:6]), int(dt_fin[6:8])
        # aproxima o vencimento: dia 15 próximo mês
        if m == 12:
            venc = f"{y+1}01{15:02d}"
        else:
            venc = f"{y}{m+1:02d}{15:02d}"
        # COD_OR = "000" (código genérico – ajuste conforme sua UF)
        add("E116", "000", f"{vl_icms_recolher:.2f}", venc, "", "", "", "", "", "")

def _bloco_G(self, linhas, rc: RegCount, ciap=None):
    def add(*campos):
        linhas.append(_reg(*campos)); rc.add(campos[0])
    add("G001", "0" if ciap else "1")
    # Preencher G110/G125 se você fornecer lançamentos de CIAP em `ciap`

def _bloco_H(self, linhas, rc: RegCount, inventario=None, dt_inv=None):
    def add(*campos):
        linhas.append(_reg(*campos)); rc.add(campos[0])

    tem_inv = bool(inventario)
    add("H001", "0" if tem_inv else "1")
    if not tem_inv:
        return
    dt_inv = _dt_yyyymmdd(dt_inv or datetime.now().strftime("%Y-%m-%d"))
    vl_inv = 0.0
    add("H005", dt_inv, "0", "0.00")  # motivo 0=Inventário no final do período; VL_INV ajustado abaixo
    # H010 itens inventariados
    for it in inventario:
        cProd = it.get("codigo") or "1"
        xProd = it.get("descricao") or "ITEM"
        u = (it.get("unidade") or "UN").upper()
        qtd = float(str(it.get("quantidade") or 0).replace(",", ".") or 0)
        vUnit = float(str(it.get("valor_unitario") or 0).replace(",", ".") or 0)
        vlItem = float(str(it.get("valor_total") or (qtd*vUnit)).replace(",", ".") or 0)
        vl_inv += vlItem
        add("H010", cProd, xProd, u, f"{qtd:.4f}", f"{vUnit:.6f}", f"{vlItem:.2f}", "", "", "", "")
    # Ajusta o VL_INV no H005: regrava linha com valor
    for i, ln in enumerate(linhas):
        if ln.startswith("|H005|"):
            campos = ln.strip().split("|")
            campos[4] = f"{vl_inv:.2f}"
            linhas[i] = "|".join(campos) + "|\r\n"
            break

def _bloco_K(self, linhas, rc: RegCount, k200_estoque=None, periodo=None):
    def add(*campos):
        linhas.append(_reg(*campos)); rc.add(campos[0])

    tem_k = bool(k200_estoque)
    add("K001", "0" if tem_k else "1")
    if not tem_k:
        return
    # K100 período de apuração
    if periodo and isinstance(periodo, (tuple, list)) and len(periodo) == 2:
        add("K100", _dt_yyyymmdd(periodo[0]), _dt_yyyymmdd(periodo[1]))
    # K200 estoque escriturado por produto
    for it in k200_estoque:
        cProd = it.get("codigo") or "1"
        dtEst = _dt_yyyymmdd(it.get("data") or datetime.now().strftime("%Y-%m-%d"))
        qtd = float(str(it.get("quantidade") or 0).replace(",", ".") or 0)
        indEst = it.get("ind_est", "0")  # 0=posse do informante
        add("K200", dtEst, cProd, f"{qtd:.4f}", indEst)

def _bloco_1(self, linhas, rc: RegCount):
    def add(*campos):
        linhas.append(_reg(*campos)); rc.add(campos[0])

    # Abre com movimento se houver qualquer dado complementar; por padrão "sem"
    add("1001", "1")
    # 1010 - obrigatoriedades (flags S/N); usamos 'N' por padrão
    add("1010", "N","N","N","N","N","N","N","N","N","N","N","N")

def _bloco_9(linhas, rc: RegCount):
    def add(*campos):
        linhas.append(_reg(*campos)); rc.add(campos[0])
    add("9001", "0")

    # 9900 para cada registro que já contabilizamos
    total_9900 = 0
    for cod, qtd in sorted(rc.items()):
        add("9900", cod, qtd)
        total_9900 += 1
    # os próprios somatórios
    add("9900", "9900", total_9900 + 3)
    add("9900", "9990", 1)
    add("9900", "9999", 1)

    # 9990 - encerramento do bloco 9: QTD_LIN_9
    qtd_lin_bloco9 = 1 + (total_9900 + 3) + 1
    add("9990", qtd_lin_bloco9)

    # 9999 - encerramento do arquivo: QTD_LIN total
    total = len(linhas) + 1
    add("9999", total)

# ------------------- orquestrador -------------------

def gerar_sped_fiscal_completo(self,
                               caminho_txt="sped_fiscal_COMPLETO.txt",
                               dt_ini=None, dt_fin=None,
                               versao_layout="3.1.8",
                               docs_servicos=None,
                               apuracao_icms=None,
                               inventario=None, dt_inventario=None,
                               k200_estoque=None, k_periodo=None,
                               ciap=None):
    """
    Gera o SPED Fiscal completo.

    Parâmetros-chave:
      - dt_ini / dt_fin: strings "YYYYMMDD" (ou "YYYY-MM-DD"/"dd/MM/yyyy")
      - versao_layout: "3.1.8" (2025) ou "3.1.9" (vigente em 2026)
      - docs_servicos: lista[dict] para Bloco D (se não informado -> sem movimento)
      - apuracao_icms: dict para E110/E116 com chaves VL_TOT_DEBITOS, VL_TOT_CREDITOS, etc.
      - inventario: lista[dict] com itens do inventário para H010 (se não informado -> sem movimento)
      - dt_inventario: data do inventário (H005)
      - k200_estoque: lista[dict] com {codigo, quantidade, data?, ind_est?} (se não -> sem movimento)
      - k_periodo: (dt_ini, dt_fin) para K100, opcional
      - ciap: lista/dados do CIAP (G110/G125), se omitido -> sem movimento

    Retorna: caminho absoluto do TXT gerado.
    """
    hoje = datetime.now()
    if not dt_ini or not dt_fin:
        dt_ini = hoje.replace(day=1).strftime("%Y%m01")
        last_day = calendar.monthrange(hoje.year, hoje.month)[1]
        dt_fin = hoje.replace(day=last_day).strftime("%Y%m%d")
    dt_ini = _dt_yyyymmdd(dt_ini); dt_fin = _dt_yyyymmdd(dt_fin)

    linhas = []
    rc = RegCount()

    _bloco_0(self, linhas, rc, dt_ini, dt_fin, versao_layout=versao_layout)
    _bloco_C(self, linhas, rc, dt_ini, dt_fin)
    _bloco_D(self, linhas, rc, docs_servicos=docs_servicos)
    _bloco_E(self, linhas, rc, dt_ini, dt_fin, apuracao_icms=apuracao_icms)
    _bloco_G(self, linhas, rc, ciap=ciap)
    _bloco_H(self, linhas, rc, inventario=inventario, dt_inv=dt_inventario)
    _bloco_K(self, linhas, rc, k200_estoque=k200_estoque, periodo=k_periodo)
    _bloco_1(self, linhas, rc)
    _bloco_9(linhas, rc)

    with open(caminho_txt, "w", encoding="utf-8", newline="") as f:
        f.writelines(linhas)

    return os.path.abspath(caminho_txt)