"""
sped_fiscal_adaptado.py
------------------------------------
Gera arquivo SPED Fiscal (EFD ICMS/IPI) **minimalista** a partir dos mesmos
campos/estruturas usados no seu criarNFe.py.

⚠️ Observações importantes
- Este gerador cobre um subconjunto comum do leiaute: Bloco 0 (0000, 0001, 0005, 0150, 0190, 0200),
  Bloco C (C001, C100, C170, C190) e Bloco 9 (9001, 9900, 9990, 9999).
- Alguns fiscos exigem mais blocos (G, H, K…), contabilista (0100) e outras particularidades.
  Preencha/estenda conforme o Guia Prático vigente (v3.1.9 em 2025).

Como usar rapidamente
---------------------
from sped_fiscal_adaptado import gerar_sped_fiscal

# self = seu objeto de emissão que já usa criarNFe.py (com os mesmos atributos)
gerar_sped_fiscal(self, caminho_txt="sped_fiscal.txt", dt_ini="20250801", dt_fin="20250831")

O arquivo final fica em "sped_fiscal.txt".
"""

from datetime import datetime
import os
import re
from collections import defaultdict, Counter

def _sd(x):
    """Somente dígitos."""
    return re.sub(r"\D", "", str(x or ""))

def _get_strvar(obj, attr, default=""):
    try:
        v = getattr(obj, attr)
        if hasattr(v, "get"):
            return (v.get() or "").strip()
        return (str(v) or "").strip()
    except Exception:
        return str(default)

def _get_float(obj, attr, default=0.0):
    try:
        v = getattr(obj, attr)
        if hasattr(v, "get"):
            v = v.get()
        v = str(v).replace(",", ".")
        return float(v or 0.0)
    except Exception:
        return float(default)

def _get_emit_dest(self):
    """
    Reaproveita o mesmo contrato de dados do criarNFe.py:
      - variavelRazaoSocialEmitente, variavelCNPJRazaoSocialEmitente, inscricaoEstadualEmitente
      - variavelRazaoSocialRemetente, variavelCNPJRazaoSocialRemetente
    """
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

def _dt_yyyymmdd(dt):
    # aceita "YYYYMMDD" ou "YYYY-MM-DD" ou "dd/MM/yyyy"
    s = (dt or "").strip()
    if re.fullmatch(r"\d{8}", s):  # YYYYMMDD
        return s
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s.replace("-", "")
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", s):
        d, m, y = s.split("/")
        return f"{y}{m}{d}"
    # fallback: hoje
    return datetime.now().strftime("%Y%m%d")

def _reg(*campos):
    return "|" + "|".join("" if c is None else str(c) for c in campos) + "|\r\n"

def _moeda(v):
    try:
        return f"{float(v):.2f}"
    except Exception:
        try:
            return f"{float(str(v).replace(',','.')):.2f}"
        except Exception:
            return "0,00"

def _coleta_unidades_e_produtos(itens):
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
    """
    Agrega por (CFOP, CST/CSOSN) como no C190 (consolidação por CFOP/tributação).
    """
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

def gerar_sped_fiscal(self, caminho_txt="sped_fiscal.txt", dt_ini=None, dt_fin=None, uf="MG"):
    """
    Gera um TXT de SPED Fiscal **simplificado** com dados do objeto `self` do seu criarNFe.py.
    - Busca itens em `self.valoresDosItens` (lista de dicionários por item)
    - Busca totais em variáveis .get(): valorTotalProdutos, valorLiquido, totalDesconto, etc.
    - Usa dados do emitente/destinatário pelos mesmos atributos usados no criarNFe.py

    Parâmetros:
        caminho_txt: onde gravar o .txt
        dt_ini/dt_fin: "YYYYMMDD" (ou "YYYY-MM-DD" ou "dd/MM/yyyy"). Se None, usa mês atual.
        uf: UF do estabelecimento (default 'MG')

    Retorna: caminho absoluto do TXT gerado.
    """
    itens = list(getattr(self, "valoresDosItens", []) or [])
    if not itens:
        raise ValueError("Sem itens em self.valoresDosItens.")

    emit, dest = _get_emit_dest(self)

    # Datas do período
    hoje = datetime.now()
    if not dt_ini or not dt_fin:
        # mês corrente
        dt_ini = hoje.replace(day=1).strftime("%Y%m01")
        # último dia do mês atual
        import calendar
        last_day = calendar.monthrange(hoje.year, hoje.month)[1]
        dt_fin = hoje.replace(day=last_day).strftime("%Y%m%d")

    dt_ini = _dt_yyyymmdd(dt_ini)
    dt_fin = _dt_yyyymmdd(dt_fin)

    # Bloco 0
    linhas = []
    # 0000 - Abertura/Identificação
    COD_VER = "019"  # exemplo de versão de leiaute (ajustar conforme o validador)
    COD_FIN = "0"    # 0=Remessa do arquivo original
    NOME = emit["xNome"]
    CNPJ = emit["CNPJ"]
    UF = emit["UF"] or uf
    IE = emit["IE"]
    COD_MUN = emit["ender"]["cMun"]
    IM = ""         # inscrição municipal (se houver)
    SUFRAMA = ""    # se houver
    IND_PERFIL = "A"  # A, B ou C
    IND_ATIV = "0"    # 0 = industrial ou equiparado; 1 = outros

    linhas.append(_reg("0000", COD_VER, COD_FIN, dt_ini, dt_fin, NOME, CNPJ, UF, IE, COD_MUN, IM, SUFRAMA, IND_PERFIL, IND_ATIV))

    # 0001 - Abertura do Bloco 0
    linhas.append(_reg("0001", "0"))  # 0 = com dados

    # 0005 - Dados complementares
    FANTASIA = NOME
    CEP = emit["CEP"]
    END = emit["ender"]["xLgr"]
    NUM = emit["ender"]["nro"]
    COMPL = ""
    BAIRRO = emit["ender"]["xBairro"]
    FONE = emit["ender"]["fone"]
    FAX = ""
    EMAIL = getattr(self, "emailEmitente", "")
    linhas.append(_reg("0005", FANTASIA, CEP, END, NUM, COMPL, BAIRRO, FONE, FAX, EMAIL))

    # 0150 - Participantes (emitente + destinatário, mínimo)
    #  Emitente
    linhas.append(_reg("0150", "EMIT", NOME, "", CNPJ, "", IE, UF, "", emit["xMun"]))
    #  Destinatário (se houver)
    if dest.get("CNPJCPF") or dest.get("xNome"):
        linhas.append(_reg("0150", "DEST", dest.get("xNome") or "DESTINATARIO", "", dest.get("CNPJCPF"), "", dest.get("IE"), dest.get("UF"), "", dest.get("xMun")))

    # 0190 - Unidades de medida
    unidades, produtos = _coleta_unidades_e_produtos(itens)
    for u in unidades:
        linhas.append(_reg("0190", u, u))

    # 0200 - Cadastro de produtos
    for cProd, prod in produtos.items():
        linhas.append(_reg("0200", cProd, prod["xProd"], "", prod["NCM"], "", "", "", prod["uCom"], "", "", ""))

    # Bloco C
    # C001 - Abertura do bloco C
    linhas.append(_reg("C001", "0"))

    # C100 - Documento NF-e (modelo 55). Pegamos da sua tela/objeto:
    mod = "55"
    ind_oper = "1" if _get_strvar(self, "variavelEntradaOuSaida", "1") == "1" else "0"  # 1=Saída, 0=Entrada
    ind_emit = "1"  # 1=Emissão própria
    cod_part = "DEST" if ind_oper == "1" else "EMIT"

    # datas documento
    # aproveita a mesma lógica do criarNFe: data_emissao (dd/MM/yyyy)
    data_emissao = _get_strvar(self, "data_emissao", "")  # pode vir "dd/MM/yyyy"
    if "/" in data_emissao:
        d, m, y = data_emissao.split("/")[:3]
        dt_e = f"{y}{m}{d}"
    else:
        dt_e = dt_ini

    vl_doc = _get_float(self, "valorLiquido", 0.0)
    vl_desc = _get_float(self, "totalDesconto", 0.0)
    vl_merc = _get_float(self, "valorTotalProdutos", 0.0)
    ind_frt = "9"  # 9=sem frete detalhado
    vl_frt = _get_float(self, "totalFrete", 0.0)
    vl_seg = _get_float(self, "totalSeguro", 0.0)
    vl_out_da = _get_float(self, "outrasDespesas", 0.0)
    vl_bc_icms = _get_float(self, "vBC", 0.0)
    vl_icms = _get_float(self, "valorICMS", 0.0)
    vl_ipi = _get_float(self, "totalIPI", 0.0)

    # chave/serie/numero se existirem
    nnf = _get_strvar(self, "variavelNumeroDaNota", "1")
    serie = _get_strvar(self, "variavelSerieDaNota", "1")
    chave = _get_strvar(self, "variavelChaveDaNota", "")

    # Campos comuns do C100 (nem todos são obrigatórios em todas as situações)
    # Estrutura (versões recentes): ver Guia Prático; aqui um conjunto mínimo prático:
    c100 = [
        "C100", ind_oper, ind_emit, cod_part, "00",  # COD_SIT = 00 regular
        mod, serie, nnf, dt_e, dt_e,  # datas emissão/entrada-saída
        "1",  # TP_NF 1 saída, 0 entrada
        "1",  # ID_DEST 1 interno
        "1",  # COD_MUN - usamos "1" placeholder aqui, pois já consta no 0000
        f"{vl_doc:.2f}", f"{vl_desc:.2f}", "0.00", f"{vl_frt:.2f}", f"{vl_seg:.2f}", f"{vl_out_da:.2f}",
        f"{vl_bc_icms:.2f}", f"{vl_icms:.2f}", "0.00",  # ST
        f"{vl_ipi:.2f}", "0.00",  # PIS/COFINS detalhados nos itens
        "", "", "",  # ICMS DIFAL/FC etc (ajustar se necessário)
        chave
    ]
    linhas.append(_reg(*c100))

    # C170 - Itens da NF
    # num_item sequencial; campos básicos
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

        c170 = [
            "C170", idx, x_prod, u, f"{q:.4f}", f"{v_un:.6f}", f"{v_prod:.2f}",
            cst, cfop, "", "",  # EX_IPI, COD_NAT, etc.
            f"{vbc:.2f}", f"{aliq_icms:.2f}", f"{vicms:.2f}",
            "0.00", "0.00", "0.00",  # ST
            "0.00", "0.00",  # FRETE/SEGURO rateado opcionalmente
            "0.00",  # DESCONTO por item se tiver
            "0.00", "0.00",  # PIS/COFINS (deixar 0; pode detalhar com C176/C195/C197 se preciso)
            "0.00",  # IPI BC
            "0.00",  # IPI ALIQ
            f"{vipi:.2f}",
        ]
        linhas.append(_reg(*c170))

    # C190 - Consolidação por CFOP/tributação (ICMS)
    regime = "SN" if str(_get_strvar(self, "crt", "1")) in ("1","2") else "NR"
    agreg = _agrega_c190(itens, regime=regime)
    for (cfop, cst_ou_csosn), tot in sorted(agreg.items()):
        c190 = [
            "C190",
            cst_ou_csosn, cfop, "0.00",  # ALIQ_ICMS agregada (informativa)
            f"{tot['vBC']:.2f}", f"{tot['vICMS']:.2f}",
            "0.00",  # vBC_ST
            "0.00",  # vST
            f"{tot['vIPI']:.2f}",
            f"{tot['vProd']:.2f}",
        ]
        linhas.append(_reg(*c190))

    # Bloco 9 - Encerramento e totalização
    # Tabela 9900: somatório de registros por tipo
    tipos = Counter()
    for ln in linhas:
        cod = ln.split("|")[1]
        tipos[cod] += 1

    linhas.append(_reg("9001", "0"))

    # 9900: um por "tipo de registro" + 9900 + 9990 + 9999
    total_9900 = 0
    for cod, qtd in sorted(tipos.items()):
        linhas.append(_reg("9900", cod, qtd))
        total_9900 += 1

    # reservar para o próprio 9900 e demais encerramentos
    linhas.append(_reg("9900", "9900", total_9900 + 3))
    linhas.append(_reg("9900", "9990", 1))
    linhas.append(_reg("9900", "9999", 1))

    # 9990 - Encerramento do bloco 9
    qtd_lin_bloco9 = 1 + (total_9900 + 3) + 1  # 9001 + (todas 9900) + 9990
    linhas.append(_reg("9990", qtd_lin_bloco9))

    # 9999 - Encerramento do arquivo
    linhas_totais = len(linhas) + 1  # + 1 do próprio 0000 (que já está somado), simples aqui
    linhas.append(_reg("9999", linhas_totais))

    # Grava
    with open(caminho_txt, "w", encoding="utf-8", newline="") as f:
        f.writelines(linhas)

    return os.path.abspath(caminho_txt)