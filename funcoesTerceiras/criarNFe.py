# criarNFe.py — ACBrMonitorPLUS (dinâmico a partir das variáveis das telas)
# Mantém as funções já usadas no projeto e corrige:
# - xMun sempre preenchido em Emitente/Destinatario (derivado de cMun quando faltar)
# - Numeração Produto/ICMS/PIS/COFINS casada por item (001, 002, 003...)
# - dhEmi único

import os
import pathlib
import re
import time
import random
from datetime import datetime


# --- helper injetado: preenche campos faltantes de endereço nos blocos [Emitente] e [Destinatario]
def _V_get(self, attr, default=""):
    val = getattr(self, attr, default)
    try:
        if hasattr(val, "get"):
            return str(val.get())
        return str(val)
    except Exception:
        return default

def _first_nonempty(*vals):
    for v in vals:
        if isinstance(v, str):
            if v.strip():
                return v.strip()
        elif v:
            return str(v)
    return ""

def _ensure_key_in_section(section_text, key, value):
    # Se não houver valor, não mexe
    if value is None or str(value).strip() == "":
        return section_text
    # Se já existir com valor, mantém
    pat_line = re.compile(rf'(?mi)^{re.escape(key)}\s*=\s*(.*)$')
    m = pat_line.search(section_text)
    if m:
        # Só preenche se estava vazio
        if m.group(1).strip() == "":
            start, end = m.span(1)
            return section_text[:start] + str(value) + section_text[end:]
        return section_text
    # Caso não exista a chave, adiciona ao final da seção
    if not section_text.endswith("\r\n"):
        section_text += "\r\n"
    section_text += f"{key}={value}\r\n"
    return section_text

def _preencher_enderecos_faltantes_arquivo(self, ini_path):
    try:
        txt = pathlib.Path(ini_path).read_text(encoding="utf-8")
    except Exception:
        return

    # Helper para editar uma seção específica
    def patch_section(txt, section_name, pairs):
        # captura a seção inteira até a próxima seção ou fim
        # preserva CRLF
        sec_pat = re.compile(rf'(\[{re.escape(section_name)}\]\r?\n)(.*?)(?=(\r?\n\[)|\Z)', re.S | re.M)
        m = sec_pat.search(txt)
        if not m:
            return txt  # seção não existe, não mexe
        header, body = m.group(1), m.group(2)
        for key, value in pairs:
            body = _ensure_key_in_section(body, key, value)
        new_sec = header + body
        start, end = m.span()
        return txt[:start] + new_sec + txt[end:]

    # Coleta valores possíveis a partir do self
    emit_xLgr = _first_nonempty(
        _V_get(self, "emit_xLgr", ""),
        _V_get(self, "variavelLogradouroEmitente", ""),
        _V_get(self, "variavelEnderecoEmitente", ""),
        _V_get(self, "variavelEnderecoRazaoSocialEmitente", "")
    )
    emit_xBairro = _first_nonempty(
        _V_get(self, "emit_xBairro", ""),
        _V_get(self, "variavelBairroEmitente", ""),
        _V_get(self, "variavelBairroRazaoSocialEmitente", "")
    )
    dest_xLgr = _first_nonempty(
        _V_get(self, "dest_xLgr", ""),
        _V_get(self, "variavelLogradouroDestinatario", ""),
        _V_get(self, "variavelEnderecoDestinatario", ""),
        _V_get(self, "variavelEnderecoCliente", "")
    )
    dest_nro = _first_nonempty(
        _V_get(self, "dest_nro", ""),
        _V_get(self, "variavelNumeroDestinatario", ""),
        _V_get(self, "variavelNumeroCliente", "")
    ) or "S/N"
    dest_xBairro = _first_nonempty(
        _V_get(self, "dest_xBairro", ""),
        _V_get(self, "variavelBairroDestinatario", ""),
        _V_get(self, "variavelBairroCliente", "")
    )

    # Fallbacks para não deixar vazio (apenas quando a tag está ausente ou vazia)
    if not emit_xLgr: emit_xLgr = "NAO INFORMADO"
    if not emit_xBairro: emit_xBairro = "NAO INFORMADO"
    if not dest_xLgr: dest_xLgr = "NAO INFORMADO"
    if not dest_xBairro: dest_xBairro = "NAO INFORMADO"
    if not dest_nro: dest_nro = "S/N"

    # Aplica patches SOMENTE se a seção existir
    txt = patch_section(txt, "Emitente", [
        ("xLgr", emit_xLgr),
        ("xBairro", emit_xBairro),
    ])
    txt = patch_section(txt, "Destinatario", [
        ("xLgr", dest_xLgr),
        ("nro", dest_nro),
        ("xBairro", dest_xBairro),
    ])

    try:
        pathlib.Path(ini_path).write_text(txt, encoding="utf-8")
    except Exception:
        pass
# --- fim helper injetado ---

# Diretórios padrão do ACBr Monitor (ajuste se necessário)
ACBR_CMD_DIR = "NotaFiscal/EnviarComando"
ACBR_RSP_DIR = "NotaFiscal/ReceberComando"

# ------------------------ UTIL ------------------------

def _so_digitos(s):
    try:
        return re.sub(r'\D+', '', str(s or ""))
    except Exception:
        return ""

# ------------------------ ACBr I/O ------------------------

def aguarda_acbr_resposta(resp_path, timeout=120, interval=0.5):
    """
    Espera o arquivo .../enviar-resp.txt que o Monitor grava.
    Retorna dict com {ok, cStat, xMotivo, xml, resposta_bruta}.
    """
    t0 = time.time()
    ultimo = ""
    while time.time() - t0 < timeout:
        if os.path.exists(resp_path):
            try:
                with open(resp_path, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
                if txt and txt != ultimo:
                    ultimo = txt
                    if ("[Retorno]" in txt) or ("CStat=" in txt) or txt.startswith("OK"):
                        break
            except Exception:
                pass
        time.sleep(interval)

    if not ultimo:
        return {"ok": False, "mensagem": "Sem resposta do ACBr no tempo limite.", "cStat": None, "xMotivo": None, "xml": None, "resposta_bruta": ""}

    def _find(pat, default=None, flags=re.IGNORECASE):
        m = re.search(pat, ultimo, flags)
        return m.group(1).strip() if m else default

    cstat = _find(r"\bCStat\s*=\s*([0-9]{2,3})")
    xmot  = _find(r"\bxMotivo\s*=\s*(.+)")
    xml   = _find(r"\bArquivo\s*=\s*(.+)")
    return {"ok": True, "cStat": cstat, "xMotivo": xmot, "xml": xml, "resposta_bruta": ultimo}

# ------------------------ COMANDO ------------------------

def criaComandoACBr(self, nome_arquivo):
    """
    Gera um ÚNICO arquivo de comando contendo:
        NFe.CriarEnviarNFe("...INI...", 1, 1, 1, , 1)
    usando SOMENTE as variáveis já preenchidas no fluxo das telas.
    """

    os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)

    # atalho para pegar StringVar/valores das telas
    def V(attr, default=""):
        val = getattr(self, attr, default)
        try:
            if hasattr(val, "get"):
                return str(val.get())
            return str(val)
        except Exception:
            return str(default)

    # ---------------- Cabeçalho / Identificacao ----------------
    natop     = V("variavelNatureza", "VENDA DE MERCADORIA") or "VENDA DE MERCADORIA"
    raw_serie = V("variavelSerieDaNota", "") or V("serie", "") or "1"
    raw_nnf   = V("variavelNumeroDaNota", "") or V("nNF", "") or "1"
    try:    serie_int = int(raw_serie)
    except: serie_int = 1
    try:    nnf_int   = int(raw_nnf)
    except: nnf_int   = 1

    # Data/Hora
    data_ptbr = V("variavelDataDocumento", "")
    if not data_ptbr:
        # tenta QDate (ex.: self.data_emissao)
        try:
            d = getattr(self, "data_emissao")
            if hasattr(d, "date"):
                d = d.date()
            if hasattr(d, "toString"):
                data_ptbr = d.toString("dd/MM/yyyy")
        except Exception:
            data_ptbr = ""
    if not data_ptbr:
        data_ptbr = datetime.now().strftime("%d/%m/%Y")
    hora = V("variavelHoraEntradaSaida", "") or datetime.now().strftime("%H:%M:%S")

    ent_saida = (V("variavelEntradaOuSaida", "Saída") or "Saída").lower()
    tpnf      = 0 if "entra" in ent_saida else 1  # 0=Entrada, 1=Saída

    # ---------------- Emitente ----------------
    xNomeEmit    = V("variavelRazaoSocialEmitente")
    cnpjEmit     = _so_digitos(V("variavelCNPJRazaoSocialEmitente"))
    ieEmit       = V("variavelInscEstadualEmitente") or "ISENTO"

    emit_xLgr    = V("emit_xLgr")
    emit_nro     = V("emit_nro")
    emit_xCpl    = V("emit_xCpl")
    emit_xBairro = V("emit_xBairro")
    emit_cMun    = _so_digitos(V("emit_cMun"))
    emit_xMun    = V("emit_xMun")
    emit_UF      = V("emit_UF")
    emit_CEP     = _so_digitos(V("emit_CEP"))
    emit_fone    = _so_digitos(V("emit_fone"))

    # ---------------- Destinatário ----------------
    xNomeDest    = V("variavelRazaoSocialRemetente")
    cnpjDest     = _so_digitos(V("variavelCNPJRazaoSocialRemetente"))
    ieDest       = V("variavelInscEstadualRemetente") or "ISENTO"

    dest_xLgr    = V("dest_xLgr")
    dest_nro     = V("dest_nro")
    dest_xBairro = V("dest_xBairro")
    dest_cMun    = _so_digitos(V("dest_cMun"))
    dest_xMun    = V("dest_xMun")
    dest_UF      = V("dest_UF")
    dest_CEP     = _so_digitos(V("dest_CEP"))
    dest_fone    = _so_digitos(V("dest_fone"))

    # idDest: 1=op. interna, 2=interestadual, 3=exterior
    if emit_UF and dest_UF and emit_UF != dest_UF:
        idDest = 2
    elif dest_UF:
        idDest = 1
    else:
        idDest = 1

    # --------- Garantia de xMun (derivando de cMun quando necessário) ----------
    # Mapeamento mínimo; adicione os municípios que você usa:
    _IBGE2MUN = {
        "3162500": "SAO JOAO DEL REI",
        "3106200": "BELO HORIZONTE",
    }
    # Emitente
    if not emit_xMun:
        if emit_cMun and emit_cMun in _IBGE2MUN:
            emit_xMun = _IBGE2MUN[emit_cMun]
    emit_xMun = re.sub(r"[^ -ÿ]", "", (emit_xMun or "").upper()).strip()

    # Destinatário
    if not dest_xMun:
        if dest_cMun and dest_cMun in _IBGE2MUN:
            dest_xMun = _IBGE2MUN[dest_cMun]
        elif not dest_cMun and emit_cMun:
            dest_cMun = emit_cMun
            dest_xMun = _IBGE2MUN.get(dest_cMun, emit_xMun)
    dest_xMun = re.sub(r"[^ -ÿ]", "", (dest_xMun or "").upper()).strip()

    # ---------------- Totais / Pagamento ----------------
    vNF      = V("valorLiquido", "0.00") or "0.00"
    vDesc    = V("totalDesconto", "0.00") or "0.00"
    vFrete   = V("totalFrete", "0.00") or "0.00"
    vSeg     = V("totalSeguro", "0.00") or "0.00"
    vOutro   = V("outrasDespesas", "0.00") or "0.00"
    vICMS    = V("valorICMS", "0.00") or V("totalICMS", "0.00") or "0.00"
    vIPI     = V("totalIPI", "0.00") or "0.00"
    vPIS     = V("totalPIS", "0.00") or "0.00"
    vCOFINS  = V("totalCOFINS", "0.00") or "0.00"
    vProdTot = V("valorTotalProdutos", "") or V("valorSubtotal", "")  # pode vir vazio

    itens    = list(getattr(self, "valoresDosItens", []) or [])
    dadosTrib = list(getattr(self, "dadosProduto", []) or [])  # opcional

    # Modalidade de frete
    modFrete = _so_digitos(V("variavelModalidadeFrete", "")) or "9"  # 9 = sem frete

    # ---------------- Escrever arquivo ----------------
    with open(nome_arquivo, "w", encoding="utf-8", newline="\r\n") as f:
        f.write('NFe.CriarEnviarNFe(\r\n"\r\n')

        # [infNFe] / [Identificacao]
        f.write("[infNFe]\r\nversao=4.00\r\n\r\n")
        f.write("[Identificacao]\r\n")
        f.write(f"cNF={random.randint(10_000_000, 99_999_999)}\r\n")
        f.write(f"natOp={natop}\r\n")
        f.write("mod=55\r\n")
        f.write(f"serie={serie_int}\r\n")
        f.write(f"nNF={nnf_int}\r\n")
        f.write(f"dhEmi={data_ptbr} {hora}\r\n")  # única ocorrência
        f.write(f"tpNF={tpnf}\r\n")
        f.write(f"idDest={idDest}\r\n")
        f.write("tpAmb=2\r\n")
        f.write("tpImp=1\r\n")
        f.write("tpEmis=1\r\n")
        f.write("finNFe=1\r\n")
        f.write("indFinal=0\r\n")
        f.write("indPres=9\r\n")
        f.write("procEmi=0\r\n")
        f.write("verProc=Sistema Python\r\n\r\n")

        # [Emitente]
        f.write("[Emitente]\r\n")
        cnpj_ok = cnpjEmit if len(cnpjEmit) == 14 else ""
        f.write(f"CNPJ={cnpj_ok}\r\n")
        f.write(f"xNome={xNomeEmit}\r\n")
        ie_num = _so_digitos(ieEmit)
        if ie_num and 2 <= len(ie_num) <= 14 and int(ie_num) > 0:
            f.write(f"IE={ie_num}\r\n")
        else:
            f.write("IE=ISENTO\r\n")
        # CRT se existir nas telas; se não, 1 (Simples) por padrão
        crt = str(getattr(self, "crt", "") or "").strip()
        if crt not in {"1", "2", "3"}:
            crt = "1"
        f.write(f"CRT={crt}\r\n")
        if emit_xLgr:    f.write(f"xLgr={emit_xLgr}\r\n")
        if emit_nro:     f.write(f"nro={emit_nro}\r\n")
        if emit_xCpl:    f.write(f"xCpl={emit_xCpl}\r\n")
        if emit_xBairro: f.write(f"xBairro={emit_xBairro}\r\n")
        f.write(f"cMun={emit_cMun or '3162500'}\r\n")
        f.write(f"xMun={emit_xMun or 'SAO JOAO DEL REI'}\r\n")
        f.write(f"UF={emit_UF or 'MG'}\r\n")
        f.write(f"CEP={emit_CEP}\r\n")
        f.write("cPais=1058\r\nxPais=BRASIL\r\n")
        if emit_fone: f.write(f"Fone={emit_fone}\r\n")
        f.write("\r\n")

        # [Destinatario]
        f.write("[Destinatario]\r\n")
        if cnpjDest:
            f.write(f"CNPJCPF={cnpjDest}\r\n")
        f.write(f"xNome={xNomeDest}\r\n")
        ie_dest_num = _so_digitos(ieDest)
        if ie_dest_num and 2 <= len(ie_dest_num) <= 14 and int(ie_dest_num) > 0:
            indIEDest = "1" if cnpjDest else "9"
            f.write(f"indIEDest={indIEDest}\r\n")
            f.write(f"IE={ie_dest_num}\r\n")
        else:
            f.write("indIEDest=2\r\n")
        if dest_xLgr:    f.write(f"xLgr={dest_xLgr}\r\n")
        if dest_nro:     f.write(f"nro={dest_nro}\r\n")
        if dest_xBairro: f.write(f"xBairro={dest_xBairro}\r\n")
        f.write(f"cMun={dest_cMun or emit_cMun or '3162500'}\r\n")
        f.write(f"xMun={dest_xMun or emit_xMun or 'SAO JOAO DEL REI'}\r\n")
        f.write(f"UF={dest_UF or emit_UF or 'MG'}\r\n")
        f.write(f"CEP={dest_CEP}\r\n")
        f.write("cPais=1058\r\nxPais=BRASIL\r\n")
        if dest_fone: f.write(f"Fone={dest_fone}\r\n")
        f.write("\r\n")

        # ---------------- [Produtos] + tributos por item ----------------
        for idx, base in enumerate(itens, start=1):
            prod = dict(base)
            # mescla tributação paralela se houver
            if idx-1 < len(dadosTrib):
                try:
                    trib = dict(dadosTrib[idx-1])
                    for k,v in trib.items():
                        if v not in (None, "", "None"):
                            prod[k] = v
                except Exception:
                    pass

            cProd  = prod.get("codigo",     prod.get("cProd",    str(idx)))
            xProd  = prod.get("descricao",  prod.get("xProd",    "ITEM"))
            NCM    = prod.get("ncm",        prod.get("NCM",      "00000000"))
            CFOP   = prod.get("cfop",       prod.get("CFOP",     V("variavelCFOP", "5102") or "5102"))
            uCom   = prod.get("unidade",    prod.get("uCom",     "UN"))
            qCom   = prod.get("quantidade", prod.get("qCom",     "1"))
            vUnCom = prod.get("valor_unitario", prod.get("vUnCom",  "0.01"))
            vProd  = prod.get("valor_total",    prod.get("vProd",   vUnCom))

            f.write(f"[Produto{idx:03d}]\r\n")
            f.write(f"cProd={cProd}\r\n")
            f.write(f"xProd={xProd}\r\n")
            f.write(f"NCM={NCM}\r\n")
            f.write(f"CFOP={CFOP}\r\n")
            f.write(f"uCom={uCom}\r\n")
            f.write(f"qCom={qCom}\r\n")
            f.write(f"vUnCom={vUnCom}\r\n")
            f.write(f"vProd={vProd}\r\n")
            f.write("indTot=1\r\n\r\n")

            # ---- ICMS
            orig  = prod.get("orig",  prod.get("origem", "0"))
            csosn = prod.get("csosn") or prod.get("CSOSN")
            cst   = prod.get("cst")   or prod.get("CST")

            f.write(f"[ICMS{idx:03d}]\r\n")
            f.write(f"orig={orig}\r\n")
            # Corrigido: respeita CRT do Emitente
            if crt in ("1", "2"):  # Simples Nacional
                csosn_val = csosn or str(getattr(self, "csosn_padrao", "") or "102")
                f.write(f"CSOSN={csosn_val}\r\n\r\n")
            else:  # Regime Normal
                vBC   = prod.get("vBC",   prod.get("bc_icms", "0.00"))
                pICMS = prod.get("pICMS", prod.get("aliq_icms", "0.00"))
                vICMS = prod.get("vICMS", prod.get("valor_icms", "0.00"))
                f.write(f"CST={cst or '00'}\r\n")
                f.write(f"vBC={vBC}\r\n")
                f.write(f"pICMS={pICMS}\r\n")
                f.write(f"vICMS={vICMS}\r\n\r\n")

            # ---- PIS
            f.write(f"[PIS{idx:03d}]\r\n")
            f.write(f"CST={(prod.get('cst_pis') or prod.get('CST_PIS') or '99')}\r\n")
            f.write(f"vBC={(prod.get('bc_pis') or prod.get('vBC_PIS') or '0.00')}\r\n")
            f.write(f"pPIS={(prod.get('aliq_pis') or prod.get('pPIS') or '0.00')}\r\n")
            f.write(f"vPIS={(prod.get('valor_pis') or prod.get('vPIS') or '0.00')}\r\n\r\n")

            # ---- COFINS
            f.write(f"[COFINS{idx:03d}]\r\n")
            f.write(f"CST={(prod.get('cst_cofins') or prod.get('CST_COFINS') or '99')}\r\n")
            f.write(f"vBC={(prod.get('bc_cofins') or prod.get('vBC_COFINS') or '0.00')}\r\n")
            f.write(f"pCOFINS={(prod.get('aliq_cofins') or prod.get('pCOFINS') or '0.00')}\r\n")
            f.write(f"vCOFINS={(prod.get('valor_cofins') or prod.get('vCOFINS') or '0.00')}\r\n\r\n")

        # ---------------- [Total] ----------------
        f.write("[Total]\r\n")
        if vProdTot:
            f.write(f"vProd={vProdTot}\r\n")
        f.write(f"vNF={vNF}\r\n")
        f.write(f"vFrete={vFrete}\r\n")
        f.write(f"vSeg={vSeg}\r\n")
        f.write(f"vDesc={vDesc}\r\n")
        f.write(f"vOutro={vOutro}\r\n")
        f.write(f"vICMS={vICMS}\r\n")
        f.write(f"vIPI={vIPI}\r\n")
        f.write(f"vPIS={vPIS}\r\n")
        f.write(f"vCOFINS={vCOFINS}\r\n\r\n")

        # ---------------- [Transportador] ----------------
        f.write("[Transportador]\r\n")
        f.write(f"modFrete={modFrete}\r\n\r\n")

        # ---------------- [pag001] ----------------
        f.write("[pag001]\r\n")
        f.write("tpag=01\r\n")
        f.write(f"vPag={vNF}\r\n\r\n")

        # Encerramento do comando
        f.write('"\r\n,1,1, , ,1)')

def criarNFE(self):
    """
    Cria NotaFiscal/EnviarComando/enviar.txt (CriarEnviarNFe),
    garante normalizações essenciais e aguarda o retorno do ACBr.
    """
    os.makedirs(ACBR_CMD_DIR, exist_ok=True)
    os.makedirs(ACBR_RSP_DIR, exist_ok=True)

    cmd_path  = os.path.join(ACBR_CMD_DIR, "enviar.txt")
    resp_path = os.path.join(ACBR_RSP_DIR, "enviar-resp.txt")
    try:
        if os.path.exists(resp_path):
            os.remove(resp_path)
    except Exception:
        pass

    criaComandoACBr(self, cmd_path)
    # >>> PATCH: preenche campos faltantes de endereço
    _preencher_enderecos_faltantes_arquivo(self, cmd_path)
    # <<< PATCH
    # pequeno delay para o Monitor consumir
    time.sleep(0.5)

    resultado = aguarda_acbr_resposta(resp_path, timeout=120, interval=0.5)
    return resultado

# compatibilidade (se alguma parte do seu app ainda chamar gerarNFe)
gerarNFe = criarNFE
