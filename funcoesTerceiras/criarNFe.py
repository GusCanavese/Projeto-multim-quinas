# criarNFe.py — ACBrMonitorPLUS (dinâmico a partir das variáveis das telas)
# Mantém as funções já usadas no projeto e corrige:
# - xMun sempre preenchido em Emitente/Destinatario (derivado de cMun quando faltar)
# - Numeração Produto/ICMS/PIS/COFINS casada por item (001, 002, 003...)
# - dhEmi único
# - indIntermed conforme indPres (NT 2020.006): indIntermed=0/1 e bloco [infIntermed] quando houver marketplace
# - NOVO: nNF auto-incremental por CNPJ+Série quando não informado (evita duplicidade 539)

import sys
import os
import pathlib
import re
import time
import random
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from consultas.insert import inserir_nota_fiscal

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


# ------------------------ NOVO: Sequência nNF por CNPJ+Série ------------------------
SEQ_BASE_DIR = os.path.join("NotaFiscal", "Sequencia")

def _so_digitos(s):
    try:
        return re.sub(r'\D+', '', str(s or ""))
    except Exception:
        return ""

def _seq_path(cnpj_sem_mascara, serie_int):
    os.makedirs(SEQ_BASE_DIR, exist_ok=True)
    cnpj_txt = (cnpj_sem_mascara or "00000000000000").zfill(14)
    serie_txt = str(serie_int).zfill(3)
    return os.path.join(SEQ_BASE_DIR, f"NUM_{cnpj_txt}_{serie_txt}.seq")

def _proximo_numero_nfe(cnpj_sem_mascara, serie_int):
    """
    Retorna o próximo nNF (1..999999999) persistido em arquivo local por CNPJ+Série.
    Só é usado quando o número não foi informado manualmente nas telas.
    """
    path = _seq_path(cnpj_sem_mascara, serie_int)
    atual = 0
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                txt = f.read().strip()
                if txt.isdigit():
                    atual = int(txt)
    except Exception:
        atual = 0
    proximo = atual + 1
    if proximo > 999_999_999:
        proximo = 1  # reseta caso estoure o limite de 9 dígitos
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(proximo))
    except Exception:
        pass
    return proximo

def _max_nnf_logs(cnpj_sem_mascara, serie_int, logs_dir=r"C:\ACBrMonitorPLUS\Logs"):
    try:
        import os, glob, re
        import xml.etree.ElementTree as ET
        max_n = 0
        for pat in ("*-nfe.xml", "*-procNFe.xml"):
            for path in glob.glob(os.path.join(logs_dir, pat)):
                try:
                    tree = ET.parse(path)
                    root = tree.getroot()
                    ns = {"n": root.tag.split("}")[0].strip("{")}
                    inf = root.find(".//n:infNFe", ns)
                    if inf is None:
                        continue
                    ide = inf.find("n:ide", ns)
                    if ide is None:
                        continue
                    cnpj_el = root.find(".//n:emit/n:CNPJ", ns)
                    if cnpj_el is None:
                        continue
                    cnpj_xml = _so_digitos(cnpj_el.text)
                    if cnpj_xml != cnpj_sem_mascara:
                        continue
                    serie_xml = ide.find("n:serie", ns)
                    nnf_xml   = ide.find("n:nNF",  ns)
                    if serie_xml is None or nnf_xml is None:
                        continue
                    if int(serie_xml.text) != int(serie_int):
                        continue
                    n = int(re.sub(r"\D+", "", nnf_xml.text or "0"))
                    if n > max_n:
                        max_n = n
                except Exception:
                    continue
        return max_n
    except Exception:
        return 0

def _grava_seq(cnpj_sem_mascara, serie_int, valor):
    path = _seq_path(cnpj_sem_mascara, serie_int)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(int(valor)))
    except Exception:
        pass

def _proximo_nnf_unico(self, cnpj_sem_mascara, serie_int):
    # 1) maior nNF AUTORIZADO no banco
    mx = 0
    try:
        from db import cursor as _dbcursor
        _dbcursor.execute(
            "SELECT COALESCE(MAX(numero),0) "
            "FROM notas_fiscais "
            "WHERE emitente_cnpjcpf=%s AND modelo=55 AND serie=%s AND COALESCE(cancelada,0)=0 "
            "AND (UPPER(COALESCE(status,''))='AUTORIZADA' OR COALESCE(cStat,0) IN (100,150))",
            (cnpj_sem_mascara, int(serie_int))
        )
        row = _dbcursor.fetchone()
        mx = int(row[0] or 0)
    except Exception:
        mx = 0

    # 2) sequência local (.seq)
    seq_val = _proximo_numero_nfe(cnpj_sem_mascara, serie_int)

    # 3) maior nNF já usado nos XMLs do ACBr (Logs)
    log_max = _max_nnf_logs(cnpj_sem_mascara, serie_int)

    # 4) escolhe o maior candidato + garante persistência da sequência
    val = max(seq_val, mx + 1, log_max + 1)
    if val != seq_val:
        _grava_seq(cnpj_sem_mascara, serie_int, val)
    return val

# ------------------------ FIM Sequência ------------------------


# Diretórios padrão do ACBr Monitor (ajuste se necessário)
ACBR_CMD_DIR = "NotaFiscal/EnviarComando"
ACBR_RSP_DIR = "NotaFiscal/ReceberComando"

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
    try:
        serie_int = int(raw_serie)
    except:
        serie_int = 1

    # CNPJ do emitente (para sequenciar nNF quando não informado)
    cnpj_emit_for_seq = _so_digitos(V("variavelCNPJRazaoSocialEmitente", ""))

    # nNF: homologação sempre usa sequência local por CNPJ+Série (evita 539)
# homologação: força nNF único por CNPJ+Série (consulta banco + .seq)
    nnf_int = _proximo_nnf_unico(self, cnpj_emit_for_seq, serie_int)


    


    # garantir número/série visíveis para insert.py
    if hasattr(self, "variavelNumeroDaNota") and hasattr(self.variavelNumeroDaNota, "set"):
        self.variavelNumeroDaNota.set(str(nnf_int))
    else:
        self.variavelNumeroDaNota = str(nnf_int)
    if hasattr(self, "variavelSerieDaNota") and hasattr(self.variavelSerieDaNota, "set"):
        self.variavelSerieDaNota.set(str(serie_int))
    else:
        self.variavelSerieDaNota = str(serie_int)

    # Data/Hora
    data_ptbr = V("variavelDataDocumento", "")
    if not data_ptbr:
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

    data_iso = datetime.strptime(data_ptbr, "%d/%m/%Y").strftime("%Y-%m-%d")
    ent_saida = (V("variavelEntradaOuSaida", "Saída") or "Saída").lower()
    tpnf      = 0 if "entra" in ent_saida else 1  # 0=Entrada, 1=Saída

    # Indicador de presença (permite sobrescrever por variável da tela)
    indPres = (V("indPres", "") or
               V("variavelIndicadorPresenca", "") or
               "9").strip()  # 9 = operação não presencial (outros)

    # ---------------- Emitente ----------------
    xNomeEmit  = self.variavelRazaoSocialEmitente.get()
    cnpjEmit   = self.variavelCNPJRazaoSocialEmitente.get()
    ieEmit     = self.variavelInscEstadualEmitente.get()

    emit_fone    = self.variavelTelefoneEnd
    emit_CEP     = self.variavelCEPEnd
    emit_UF      = self.variavelUFEnd
    emit_xMun    = self.variavelMunicipioEnd
    emit_cMun    = self.variavelCodigoMunicipioEnd
    emit_xCpl    = self.variavelComplementoEnd
    emit_xLgr    = self.variavelLogradouroEnd
    emit_nro     = self.variavelNumeroEnd
    emit_xBairro = self.variavelBairroEnd



    # ---------------- Destinatário ----------------
    xNomeDest = V("nomeDestinatario", "")
    cnpjDest  = V("documentoDestinatario", "")
    ieDest    = self.inscricaoEstadualDestinatario.get() 
    dest_xLgr = self.ruaDestinatario
    dest_nro  = self.numeroDestinatario
    dest_xBairro = self.bairroDestinatario
    dest_cMun = ''
    dest_xMun = self.cidadeDestinatario
    dest_UF = self.estadoDestinatario
    dest_CEP = self.cepDestinatario
    dest_fone = ''

    print(xNomeDest, cnpjDest, ieDest, dest_xLgr, dest_nro, dest_xBairro, dest_cMun, dest_xMun, dest_UF, dest_CEP, dest_fone)

    cfop_hint = _so_digitos(V("variavelCFOP", ""))  # ex.: "5102", "6102", "7102"
    if cfop_hint:
        d0 = cfop_hint[0]
        if d0 in ("1", "5"):
            idDest = 1   # operação interna
        elif d0 in ("2", "6"):
            idDest = 2   # interestadual
        elif d0 in ("3", "7"):
            idDest = 3   # exterior
        else:
            idDest = 1
    else:
        # fallback por UF (quando não vier CFOP global da tela)
        if (dest_UF or "").upper() == "EX":
            idDest = 3
        elif emit_UF and dest_UF and emit_UF != dest_UF:
            idDest = 2
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

    # depois de vICMS, vProdTot...
    try:
        _icms_tot_user = float(str(vICMS).replace(",", "."))
    except:
        _icms_tot_user = 0.0
    try:
        _vprod_tot_user = float(str(vProdTot or "0").replace(",", "."))
    except:
        _vprod_tot_user = 0.0

    # Alíquota "global" (se o usuário informou total de ICMS e total de produtos)
    _aliq_icms_global = (_icms_tot_user / _vprod_tot_user * 100.0) if (_icms_tot_user > 0 and _vprod_tot_user > 0) else 0.0


    itens_base = list(getattr(self, "valoresDosItens", []) or [])

    dp = getattr(self, "dadosProdutos", None)  # pode ser dict (chaves -> item) ou list
    if isinstance(dp, dict):
        trib_list = list(dp.values())
    elif isinstance(dp, list):
        trib_list = dp
    else:
        trib_list = list(getattr(self, "dadosProduto", []) or [])  # fallback antigo

    # se não houver itens_base, monta "raso" só para casar posições
    if not itens_base and trib_list:
        itens_base = [{} for _ in trib_list]

    # Modalidade de frete
    modFrete = _so_digitos(V("variavelModalidadeFrete", "")) or "9"  # 9 = sem frete

    # ---------------- Intermediador (marketplace) ----------------
    # Captura possíveis nomes de variáveis usadas no seu app
    marketplace_cnpj = _so_digitos(
        (V("marketplace_cnpj", "") or
         V("cnpjIntermediador", "") or
         V("variavelCNPJIntermediador", "") or
         V("variavelCNPJMarketplace", "") or
         V("CNPJ_intermediador", "") or
         V("CNPJMarketplace", ""))
    )
    marketplace_id = (
        V("marketplace_id", "") or
        V("idCadIntTran", "") or
        V("variavelIdIntermediador", "") or
        V("variavelIdMarketplace", "")
    ).strip()










    ini_path     = r"C:\ACBrMonitorPLUS\ACBrMonitor.ini"


    with open(nome_arquivo, "w", encoding="utf-8", newline="") as f:
        # 2) Criar e enviar a NFe (BLOCO ÚNICO)
        f.write('NFe.CriarEnviarNFe(\r\n"\r\n')

        # [infNFe] / [Identificacao]
        f.write("[infNFe]\r\nversao=4.00\r\n\r\n")
        f.write("[Identificacao]\r\n")
        f.write(f"cNF={random.randint(10_000_000, 99_999_999)}\r\n")
        f.write(f"natOp={natop}\r\n")
        f.write("mod=55\r\n")
        f.write(f"serie={serie_int}\r\n")
        f.write(f"nNF={nnf_int}\r\n")
        f.write(f"dhEmi={data_ptbr} {hora}\r\n")
        f.write(f"tpNF={tpnf}\r\n")
        f.write(f"idDest={idDest}\r\n")
        f.write("tpAmb=2\r\n")
        f.write("tpImp=1\r\n")
        f.write("tpEmis=1\r\n")
        f.write("finNFe=1\r\n")
        f.write("indFinal=0\r\n")
        f.write(f"indPres={indPres}\r\n")
        f.write("procEmi=0\r\n")
        f.write("verProc=Sistema Python\r\n")
        # >>> NOVO: indicativo do intermediador conforme indPres
        if indPres in {"2", "3", "4", "9"}:
            if len(marketplace_cnpj) == 14:
                # Houve marketplace/intermediador
                f.write("indIntermed=1\r\n\r\n")
                f.write("[infIntermed]\r\n")
                f.write(f"CNPJ={marketplace_cnpj}\r\n")
                if marketplace_id:
                    f.write(f"idCadIntTran={marketplace_id}\r\n")
                f.write("\r\n")
            else:
                # Sem marketplace (operação não presencial direta)
                f.write("indIntermed=0\r\n\r\n")
        else:
            # Para 0,1,5 não deve enviar indIntermed
            f.write("\r\n")
        # <<< NOVO


        #  [Transp] - modalidade de frete
        try:
            _modfrete = ""
            # tenta nas variáveis que você já usa na tela nova, sem mudar a sua lógica
            for _cand in ("variavelModalidadeFrete", "variavelModalidade", "modFrete", "modalidadeFrete"):
                try:
                    _v = V(_cand)  # se sua função V existir, usa; se não existir, cai no except
                except Exception:
                    try:
                        _v = globals().get(_cand) or locals().get(_cand)
                    except Exception:
                        _v = None
                if _v not in (None, "", "None"):
                    _modfrete = str(_v).strip()
                    break
            if not _modfrete:
                _modfrete = "0"  # padrão NFe: 0=por conta do emitente
            f.write("[Transp]\r\n")
            f.write(f"modFrete={_modfrete}\r\n\r\n")
        except Exception:
            # não interrompe o fluxo caso algo não exista
            pass

        # [Transportador] - identificação (opcional, só grava se houver algum valor)
        try:
            _cnpjcpf = ""
            for _cand in ("variavelCNPJTransportador","cnpjTransportador","cpfCnpjTransportador",
                        "documentoTransportador","transportadora_cnpj","CNPJTransportador"):
                try:
                    _v = V(_cand)
                except Exception:
                    _v = globals().get(_cand) or locals().get(_cand)
                if _v not in (None,"","None"):
                    _cnpjcpf = str(_v).strip()
                    break

            _xnome = ""
            for _cand in ("variavelTransportador","nomeTransportador","transportador","transportadora_nome"):
                try:
                    _v = V(_cand)
                except Exception:
                    _v = globals().get(_cand) or locals().get(_cand)
                if _v not in (None,"","None"):
                    _xnome = str(_v).strip()
                    break

            if _cnpjcpf or _xnome:
                f.write("[Transportador]\r\n")
                if _cnpjcpf: f.write(f"CNPJCPF={_cnpjcpf}\r\n")
                if _xnome:   f.write(f"xNome={_xnome}\r\n")
                f.write("\r\n")
        except Exception:
            pass

        # [RetTransp] - retenção ICMS de transporte (opcional)
        try:
            def _norm_dec(_val):
                # mantém o estilo do seu projeto: trocar vírgula por ponto só se vier string
                if _val is None or _val == "None" or _val == "":
                    return ""
                _s = str(_val).strip()
                return _s.replace(",", ".")

            _vServ   = ""
            _vBCRet  = ""
            _pICMSRet= ""
            _vICMSRet= ""
            _CFOP    = ""
            _cMunFG  = ""

            # valores
            for _name, _store in (
                (("variavelValorServicoTransp","variavelValorServicoTransporte","vServTransp","vServ"), "_vServ"),
                (("variavelBCRetencaoICMS","vBCRetTransp","vBCRet"), "_vBCRet"),
                (("variavelAliquotaRetICMS","pICMSRetTransp","pICMSRet"), "_pICMSRet"),
                (("variavelValorICMSRetido","vICMSRetTransp","vICMSRet"), "_vICMSRet"),
                (("variavelCFOPTransporte","variavelCFOPTransp","cfopTransp","CFOPTransp","CFOP"), "_CFOP"),
                (("variavelMunicipioGerador","cMunFGTransp","municipioGeradorCod","cMunFG"), "_cMunFG"),
            ):
                _val = None
                for _cand in _name:
                    try:
                        _v = V(_cand)
                    except Exception:
                        _v = globals().get(_cand) or locals().get(_cand)
                    if _v not in (None,"","None"):
                        _val = _v
                        break
                if _store == "_vServ":    _vServ    = _norm_dec(_val)
                if _store == "_vBCRet":   _vBCRet   = _norm_dec(_val)
                if _store == "_pICMSRet": _pICMSRet = _norm_dec(_val)
                if _store == "_vICMSRet": _vICMSRet = _norm_dec(_val)
                if _store == "_CFOP":     _CFOP     = str(_val).strip() if _val not in (None,"","None") else ""
                if _store == "_cMunFG":   _cMunFG   = str(_val).strip() if _val not in (None,"","None") else ""

            if any(( _vServ, _vBCRet, _pICMSRet, _vICMSRet, _CFOP, _cMunFG )):
                f.write("[RetTransp]\r\n")
                if _vServ:     f.write(f"vServ={_vServ}\r\n")
                if _vBCRet:    f.write(f"vBCRet={_vBCRet}\r\n")
                if _pICMSRet:  f.write(f"pICMSRet={_pICMSRet}\r\n")
                if _vICMSRet:  f.write(f"vICMSRet={_vICMSRet}\r\n")
                if _CFOP:      f.write(f"CFOP={_CFOP}\r\n")
                if _cMunFG:    f.write(f"cMunFG={_cMunFG}\r\n")
                f.write("\r\n")
        except Exception:
            pass

        # <<<<< END_TRANSPORTE_PATCH (NFe) >>>>>




        # [Emitente]
        f.write("[Emitente]\r\n")
        cnpj_ok = _so_digitos(cnpjEmit)
        f.write(f"CNPJ={cnpj_ok}\r\n")
        f.write(f"xNome={xNomeEmit}\r\n")
        ie_num = _so_digitos(ieEmit)
        if ie_num and 2 <= len(ie_num) <= 14 and int(ie_num) > 0:
            f.write(f"IE={ie_num}\r\n")
        else:
            f.write("IE=ISENTO\r\n")
        # CRT se existir nas telas; se não, 1 (Simples) por padrão


        # CRT (1=SN, 2=Excesso SN, 3=Regime Normal)
        crt = (V("CRT_emitente", "") or
               V("variavelCRTEmitente", "") or
               V("variavelCRT", "") or
               V("crt", "")).strip()
        if crt not in {"1", "2", "3"}:
            crt = "3"  # se não vier da tela, regime normal por segurança
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
        f.write(f"cMun={dest_cMun or '3162500'}\r\n")
        f.write(f"xMun={dest_xMun or emit_xMun or 'SAO JOAO DEL REI'}\r\n")
        f.write(f"UF={dest_UF or emit_UF or 'MG'}\r\n")
        f.write(f"CEP={dest_CEP}\r\n")
        f.write("cPais=1058\r\nxPais=BRASIL\r\n")
        if dest_fone: f.write(f"Fone={dest_fone}\r\n")
        f.write("\r\n")

        # ---------------- [Produtos] + tributos por item ----------------
        tot_vBC = Decimal("0.00"); tot_vICMS = Decimal("0.00"); tot_vBCST = Decimal("0.00"); tot_vST = Decimal("0.00")
        tot_vProd = Decimal("0.00")
        tot_vPIS = Decimal("0.00"); tot_vCOFINS = Decimal("0.00")

        for idx, base in enumerate(itens_base, start=1):
            prod = dict(base)
            print(prod)
            if idx-1 < len(trib_list):
                try:
                    prod.update({k: v for k, v in dict(trib_list[idx-1]).items() if v not in (None, "", "None")})
                except Exception:
                    pass

            cProd  = prod.get("codigo",     prod.get("cProd",    str(idx)))
            xProd  = prod.get("descricao",  prod.get("xProd",    "ITEM"))
            NCM    = prod.get("ncm",        prod.get("NCM",      "00000000"))
            CFOP   = prod.get("cfop",       prod.get("CFOP",     V("variavelCFOP", "5102") or "5102"))

            CFOP   = prod.get("cfop", prod.get("CFOP", V("variavelCFOP", "5102") or "5102"))

            # >>> AJUSTE CFOP PARA BATER COM idDest / tpNF (EVITA 773/733)
            _cfop = _so_digitos(str(CFOP)) or "5102"
            if idDest == 3:
                # Exterior -> 7xxx (saída) ou 3xxx (entrada)
                if tpnf == 1 and _cfop[0] != "7":
                    _cfop = "7" + _cfop[1:]
                elif tpnf == 0 and _cfop[0] != "3":
                    _cfop = "3" + _cfop[1:]
            elif idDest == 2:
                # Interestadual -> 6xxx (saída) ou 2xxx (entrada)
                if tpnf == 1 and _cfop[0] != "6":
                    _cfop = "6" + _cfop[1:]
                elif tpnf == 0 and _cfop[0] != "2":
                    _cfop = "2" + _cfop[1:]
            else:
                # Interna -> 5xxx (saída) ou 1xxx (entrada)
                if tpnf == 1 and _cfop[0] != "5":
                    _cfop = "5" + _cfop[1:]
                elif tpnf == 0 and _cfop[0] != "1":
                    _cfop = "1" + _cfop[1:]
            CFOP = _cfop
# <<< FIM AJUSTE


            uCom   = prod.get("unidade",    prod.get("uCom",     "UN"))
                        # --- NORMALIZAÇÃO qCom / vUnCom / vProd (evita Rejeição 629) ---
            _raw_q = str(prod.get("quantidade") or prod.get("qCom") or "").replace(",", ".").strip()
            _raw_u = str(prod.get("preco") or prod.get("valor_unitario") or prod.get("vUnCom") or "0.01").replace(",", ".").strip()
            _raw_t = str(prod.get("subtotal") or prod.get("valor_total") or prod.get("vProd") or _raw_u).replace(",", ".").strip()

            def _to_float(s, default):
                try:
                    return float(s)
                except Exception:
                    return float(default)

            q = _to_float(_raw_q, 0 if _raw_q != "" else 0)
            u = _to_float(_raw_u, 0.01)
            t = _to_float(_raw_t, u)

            # Se quantidade vier vazia/zero, calcula a partir do total e unitário; se não der, assume 1
            if q <= 0:
                if u > 0 and t > 0:
                    q = t / u
                else:
                    q = 1.0

            # Garante consistência exata: q * u (2 casas) = t
            if q > 0 and t > 0:
                u = t / q

            # Formatação nos padrões da NF-e
            qCom   = f"{q:.4f}"
            vUnCom = f"{u:.10f}"
            vProd  = f"{t:.2f}"
            try:
                tot_vProd += Decimal(str(vProd).replace(",", ".")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            except:
                pass

            f.write(f"[Produto{idx:03d}]\r\n")
            f.write(f"cProd={cProd}\r\nxProd={xProd}\r\nNCM={NCM}\r\nCFOP={CFOP}\r\n")
            f.write(f"uCom={uCom}\r\nqCom={qCom}\r\nvUnCom={vUnCom}\r\nvProd={vProd}\r\nindTot=1\r\n\r\n")
            # --- FIM NORMALIZAÇÃO ---

            # ===== ICMS por item =====
            orig  = prod.get("orig",  prod.get("origem", "0"))
            csosn = prod.get("csosn") or prod.get("CSOSN")
            cst   = prod.get("cst")   or prod.get("CST")

            # mapeia chaves usadas na tela de totais
            # --- injeta tributação salva por CHAVE do produto (não perder bc_icms) ---
            chave = prod.get('cProd') or prod.get('xProd')
            if isinstance(getattr(self, 'dadosProdutos', None), dict) and chave in self.dadosProdutos:
                try:
                    prod.update({k: v for k, v in dict(self.dadosProdutos[chave]).items() if v not in (None, '', 'None')})
                except Exception:
                    prod.update(self.dadosProdutos[chave])
            # --- fim injeção por chave ---
            vBC = prod.get('vBC')
            if vBC is None and 'bc_icms' in prod:
                vBC = prod['bc_icms']
            if vBC is None and 'vBC_ICMS' in prod:
                vBC = prod['vBC_ICMS']
            if vBC is None:
                vBC = '0.00'
            pICMS = prod.get("pICMS") or prod.get("aliq_icms") or "0.00"
            vICMS = prod.get("vICMS") or prod.get("vr_icms") or prod.get("valor_icms") or "0.00"

            vBCST   = prod.get("vBCST") or prod.get("bc_icms_st") or prod.get("vr_bc_icms_st_ret") or ""
            vICMSST = prod.get("vICMSST") or prod.get("vr_icms_st") or prod.get("vr_icms_subst") or prod.get("vr_icms_st_ret") or ""

            # f.write(f"[ICMS{idx:03d}]\r\n")



            # ---- ICMS (decide por item)

            orig      = prod.get("orig",  prod.get("origem", "0"))
            csosn_txt = (prod.get("csosn") or prod.get("CSOSN") or "").strip()
            cst_b_fallback = (prod.get("cst_b_produto") or prod.get("cst_b") or "").strip()
            cst_txt   = (prod.get("cst")   or prod.get("CST")   or "").strip()
            vBC       = prod['bc_icms'] or prod['vBC_ICMS'] or prod.get("vBC")
            print(vBC)
            pICMS     = prod.get("pICMS")     or prod.get("aliq_icms")      or "0.00"
            vICMS     = prod.get("vICMS")     or prod.get("vr_icms")        or prod.get("valor_icms") or "0.00"
            vBCST     = prod.get("vBCST")     or prod.get("bc_icms_st")     or prod.get("vr_bc_icms_st_ret") or ""
            vICMSST   = prod.get("vICMSST")   or prod.get("vr_icms_st")     or prod.get("vr_icms_subst")     or prod.get("vr_icms_st_ret") or ""
            
            f.write(f"[ICMS{idx:03d}]\r\n")
            f.write(f"orig={orig}\r\n")

            if False:
                # Se veio CSOSN no item, escreve CSOSN e não força CST nem valores de ICMS padrão
                f.write(f"CSOSN={csosn_txt}\r\n\r\n")
            elif cst_txt:
                _num = lambda x: float(str(x).replace(",", ".").strip() or "0")
                bc_num    = _num(vBC)
                aliq_num  = _num(pICMS)
                vicms_num = _num(vICMS)
                vprod_num = _num(vProd)

                if cst_txt == "00":
                    vBCST = ""
                    vICMSST = ""
                    # Base do ICMS do item = vProd (se não informada)
                    if bc_num <= 0:
                        bc_num = vprod_num
                        print(bc_num)
                        vBC = f"{bc_num:.2f}"

                    # Se tudo veio zerado, use a alíquota global (se existir) para fechar com o total
                    if aliq_num <= 0 and vicms_num <= 0 and _aliq_icms_global > 0:
                        aliq_num  = _aliq_icms_global
                        pICMS     = f"{aliq_num:.4f}"
                        vicms_num = bc_num * aliq_num / 100.0
                        vICMS     = f"{vicms_num:.2f}"

                    # Casos parciais
                    if aliq_num > 0 and vicms_num <= 0:
                        vicms_num = bc_num * aliq_num / 100.0
                        vICMS = f"{vicms_num:.2f}"
                    if vicms_num > 0 and aliq_num <= 0 and bc_num > 0:
                        aliq_num = (vicms_num / bc_num) * 100.0
                        pICMS = f"{aliq_num:.4f}"

                f.write(f"CST={cst_txt}\r\n")
                f.write("modBC=3\r\n")  # <<< troque 0 por 3 (valor da operação)
                _bc = str(vBC).strip().replace(',', '.')
                if not _bc:
                    _bc = bc_num
                f.write(f"vBC={_bc}\r\n")
                
                f.write(f"pICMS={pICMS}\r\n")
                f.write(f"vICMS={vICMS}\r\n")
                if vBCST:   f.write(f"vBCST={vBCST}\r\n")
                if vICMSST: f.write(f"vICMSST={vICMSST}\r\n")
                f.write("\r\n")

            
            else:
                vBCST = ""
                vICMSST = ""
                if crt in ("1", "2"):   # Simples
                    f.write(f"CSOSN={(getattr(self, 'csosn_padrao', '') or '102')}\r\n\r\n")
                else:                    # Regime Normal
                    _num = lambda x: float(str(x).replace(",", ".").strip() or "0")
                    if _num(vBC) <= 0:
                        vBC = vProd   # usa o vProd já calculado acima como base do item

                    f.write("CST=00\r\n")
                    f.write("modBC=3\r\n")  # <<< aqui também 3
                _bc = str(vBC).strip().replace(',', '.')
                if not _bc:
                    _bc = '0.00'
                f.write(f"vBC={_bc}\r\n")
                f.write(f"pICMS={pICMS}\r\n")
                f.write(f"vICMS={vICMS}\r\n")
                if vBCST:   f.write(f"vBCST={vBCST}\r\n")
                if vICMSST: f.write(f"vICMSST={vICMSST}\r\n")
                f.write("\r\n")
                
            def _fnum(x):
                try:
                    d = Decimal(str(x).replace(",", "."))
                    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                except:
                    return Decimal("0.00")

            tot_vBC   += _fnum(vBC)
            tot_vICMS += _fnum(vICMS)
            tot_vBCST += _fnum(vBCST)
            tot_vST   += _fnum(vICMSST)


            # ===== PIS por item =====
            pis_cst = (prod.get('cst_pis') or prod.get('CST_PIS') or '99')
            pis_vbc = (prod.get('bc_pis')  or prod.get('vBC_PIS') or '0.00')
            pis_ppc = (prod.get('aliq_pis') or prod.get('pPIS') or '0.00')
            pis_vvl = (prod.get('vr_pis') or prod.get('valor_pis') or prod.get('vPIS'))

            if not pis_vvl:  # calcula vPIS = vBC * pPIS/100
                try:
                    pis_vvl = f"{(float(str(pis_vbc).replace(',','.')) * float(str(pis_ppc).replace(',','.'))/100):.2f}"
                except:
                    pis_vvl = "0.00"

            f.write(f"[PIS{idx:03d}]\r\n")
            f.write(f"CST={pis_cst}\r\n")
            f.write(f"vBC={pis_vbc}\r\n")
            f.write(f"pPIS={pis_ppc}\r\n")
            f.write(f"vPIS={pis_vvl}\r\n\r\n")

            # +++ NOVO: acumula total PIS
            tot_vPIS += _fnum(pis_vvl)


            # ===== COFINS por item =====
            cof_cst = (prod.get('cst_cofins') or prod.get('CST_COFINS') or '99')
            cof_vbc = (prod.get('bc_cofins')  or prod.get('vBC_COFINS') or '0.00')
            cof_ppc = (prod.get('aliq_cofins') or prod.get('pCOFINS') or '0.00')
            cof_vvl = (prod.get('vr_cofins') or prod.get('valor_cofins') or prod.get('vCOFINS'))

            if not cof_vvl:  # calcula vCOFINS = vBC * pCOFINS/100
                try:
                    cof_vvl = f"{(float(str(cof_vbc).replace(',','.')) * float(str(cof_ppc).replace(',','.'))/100):.2f}"
                except:
                    cof_vvl = "0.00"

            f.write(f"[COFINS{idx:03d}]\r\n")
            f.write(f"CST={cof_cst}\r\n")
            f.write(f"vBC={cof_vbc}\r\n")
            f.write(f"pCOFINS={cof_ppc}\r\n")
            f.write(f"vCOFINS={cof_vvl}\r\n\r\n")

            # +++ NOVO: acumula total COFINS
            tot_vCOFINS += _fnum(cof_vvl)

        try: frete = _fnum(vFrete)
        except: frete = Decimal("0.00")
        try: seg = _fnum(vSeg)
        except: seg = Decimal("0.00")
        try: outro = _fnum(vOutro)
        except: outro = Decimal("0.00")
        try: ipi = _fnum(vIPI)
        except: ipi = Decimal("0.00")
        try: desc = _fnum(vDesc)
        except: desc = Decimal("0.00")
        # ST total já está em tot_vST; se for 0, não impacta
        vNF_calc = (tot_vProd - desc) + frete + seg + outro + ipi + tot_vST
        vNF_calc = vNF_calc.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Se vNF vier vazio/zero ou diferente do calculado, força o correto
        try:
            vNF_num = _fnum(vNF)
        except:
            vNF_num = Decimal("0.00")
        if (vNF_num <= Decimal("0.00")) or (abs(vNF_num - vNF_calc) > Decimal("0.01")):
            vNF = f"{vNF_calc:.2f}"

        # Fallback: se vPIS/vCOFINS vier vazio ou zero, soma pelos itens
        def _soma(lista, chave):
            from decimal import Decimal
            tot = Decimal("0.00")
            for p in (lista or []):
                v = p.get(chave) or p.get(chave.upper()) or "0"
                try:
                    tot += Decimal(str(v).replace(",", "."))
                except:
                    pass
            return f"{tot:.2f}"

        if not str(vPIS).strip() or str(vPIS).strip() in {"0", "0.0", "0.00"}:
            vPIS = f"{tot_vPIS:.2f}"

        if not str(vCOFINS).strip() or str(vCOFINS).strip() in {"0", "0.0", "0.00"}:
            vCOFINS = f"{tot_vCOFINS:.2f}"


        # ---------------- [Total] ----------------
        f.write("[Total]\r\n")
        # usa a soma dos itens (garante consistência com o detalhamento)
        f.write(f"vBC={tot_vBC:.2f}\r\n")
        f.write(f"vBCST={tot_vBCST:.2f}\r\n")
        f.write(f"vST={tot_vST:.2f}\r\n")

        # mantém seus demais campos
        f.write(f"vProd={tot_vProd:.2f}\r\n")
        f.write(f"vNF={vNF}\r\n")
        f.write(f"vFrete={vFrete}\r\n")
        f.write(f"vSeg={vSeg}\r\n")
        f.write(f"vDesc={vDesc}\r\n")
        f.write(f"vOutro={vOutro}\r\n")

        # ICMS total também pela soma dos itens (evita divergência)
        f.write(f"vICMS={tot_vICMS:.2f}\r\n")

        f.write(f"vIPI={vIPI}\r\n")
        f.write(f"vPIS={vPIS}\r\n")
        f.write(f"vCOFINS={vCOFINS}\r\n\r\n")
        # campos que o insert.py lê
        self.variavelValorTotalNota = str(vNF)
        self.variavelValorProdutos  = f"{tot_vProd:.2f}"
        self.variavelValorDesconto  = str(vDesc)
        self.variavelValorFrete     = str(vFrete)
        self.variavelValorSeguro    = str(vSeg)
        self.variavelOutros         = str(vOutro)
        self.variavelBaseICMS       = f"{tot_vBC:.2f}"
        self.variavelValorICMS      = f"{tot_vICMS:.2f}"
        self.variavelBaseICMSST     = f"{tot_vBCST:.2f}"
        self.variavelValorICMSST    = f"{tot_vST:.2f}"
        self.variavelValorIPI       = str(vIPI)
        self.variavelValorPIS       = str(vPIS)
        self.variavelValorCOFINS    = str(vCOFINS)
        
        # destinatário para insert.py
        self.variavelNomeRazaoDestinatario = xNomeDest
        self.variavelCNPJDestinatario      = cnpjDest

        self.variavelDataEmissao    = f"{data_iso} {hora}"
        self.variavelDataSaida      = f"{data_iso} {hora}"



        # ---------------- [Transportador] ----------------
        f.write("[Transportador]\r\n")
        f.write(f"modFrete={modFrete}\r\n\r\n")

        # ---------------- [pag001] ----------------
        f.write("[pag001]\r\n")
        f.write("tpag=01\r\n")
        f.write(f"vPag={vNF}\r\n\r\n")

        # Encerramento do comando
        f.write('"\r\n,1,1,1, ,1)')

def criarNFE(self):
    os.makedirs(ACBR_CMD_DIR, exist_ok=True)
    os.makedirs(ACBR_RSP_DIR, exist_ok=True)

    # 1) SET CERTIFICADO (COMANDO ISOLADO)
    cert_cmd  = os.path.join(ACBR_CMD_DIR, "cert.txt")
    cert_resp = os.path.join(ACBR_RSP_DIR, "cert-resp.txt")
    try:
        if os.path.exists(cert_resp):
            os.remove(cert_resp)
    except Exception:
        pass

    with open(cert_cmd, "w", encoding="utf-8", newline="") as f:
        f.write(f'NFe.SetCertificado("{self.caminhoCertificado}","{self.senhaCertificado}")\r\n')

    r1 = aguarda_acbr_resposta(cert_resp, timeout=60, interval=0.2)
    if not r1.get("ok"):
        return r1  # se falhou o certificado, para aqui

    # 2) CRIAR/ENVIAR NFe (COMANDO COMPLETO)
    cmd_path  = os.path.join(ACBR_CMD_DIR, "enviar.txt")
    resp_path = os.path.join(ACBR_RSP_DIR, "enviar-resp.txt")
    try:
        if os.path.exists(resp_path):
            os.remove(resp_path)
    except Exception:
        pass

    criaComandoACBr(self, cmd_path)  # agora escreve só o CriarEnviarNFe(...)
    _preencher_enderecos_faltantes_arquivo(self, cmd_path)

    resultado = aguarda_acbr_resposta(resp_path, timeout=120, interval=0.5)

        
    status = "AUTORIZADA" if str(resultado.get("cStat")) in ("100", "150") else "GERADA"
    xml_path = resultado.get("xml") or ""
    inserir_nota_fiscal(self, tipo="NFe", xml_path=xml_path, status=status)
    return resultado


# compatibilidade (se alguma parte do seu app ainda chamar gerarNFe)
gerarNFe = criarNFE
