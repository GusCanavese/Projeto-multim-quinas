# criarNFe.py — Integração ACBrMonitorPLUS via arquivo único enviar.txt
# Mantém o formato de envio desejado e remove código não utilizado.

import os
import re
import time
import random
from datetime import datetime

try:
    from PyQt5.QtCore import QDate
except Exception:
    try:
        from PySide6.QtCore import QDate
    except Exception:
        QDate = None


ACBR_CMD_DIR = "NotaFiscal/EnviarComando"
ACBR_RSP_DIR = "NotaFiscal/ReceberComando"

def _so_digitos(s):
    return re.sub(r"\D", "", s or "")


# ------------------------- util -------------------------

def _ler_kv(caminho):
    """Lê arquivo chave=valor simples (ignora linhas vazias/comentários)."""
    m = {}
    if not os.path.exists(caminho):
        return m
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#") or "=" not in ln:
                continue
            k, v = ln.split("=", 1)
            m[k.strip()] = v.strip()
    return m

def _carregar_emit_dest(self):
    """
    Preenche Emitente/Destinatário a partir de NotaFiscal/configuracoes.txt (se existir),
    senão usa as variáveis da UI e fallbacks seguros (homologação).
    """
    cfg = _ler_kv(os.path.join("NotaFiscal", "configuracoes.txt"))

    # Emitente (prioridade: config -> UI -> fallback)
    EMIT = {
        "CNPJ": cfg.get("CNPJ", getattr(self, "variavelCNPJRazaoSocialEmitente").get() if hasattr(self, "variavelCNPJRazaoSocialEmitente") else ""),
        "xNome": cfg.get("xNome", getattr(self, "variavelRazaoSocialEmitente").get() if hasattr(self, "variavelRazaoSocialEmitente") else ""),
        "IE": cfg.get("IE", getattr(self, "inscricaoEstadualEmitente").get() if hasattr(self, "inscricaoEstadualEmitente") else ""),
        "xLgr": cfg.get("xLgr", "R DOUTOR OSCAR DA CUNHA"),
        "nro": cfg.get("nro", "126"),
        "xBairro": cfg.get("xBairro", "FABRICAS"),
        "cMun": cfg.get("cMun", "3162500"),
        "xMun": cfg.get("xMun", "SAO JOAO DEL REI"),
        "UF": cfg.get("UF", "MG"),
        "CEP": cfg.get("CEP", "36301194"),
        "fone": cfg.get("fone", "3233713382"),
    }

    # Destinatário (usa prefixo Dest_ no configuracoes.txt; se faltar, herda emitente/valores da UI)
    DEST = {
        "CNPJ": cfg.get("Dest_CNPJ", getattr(self, "variavelCNPJRazaoSocialRemetente").get() if hasattr(self, "variavelCNPJRazaoSocialRemetente") else ""),
        "xNome": cfg.get("Dest_xNome", getattr(self, "variavelRazaoSocialRemetente").get() if hasattr(self, "variavelRazaoSocialRemetente") else ""),
        "IE": cfg.get("Dest_IE", ""),
        "indIEDest": cfg.get("Dest_indIEDest", "9"),  # 1=Contrib, 2=Isento, 9=Não contrib.
        "xLgr": cfg.get("Dest_xLgr", EMIT["xLgr"]),
        "nro": cfg.get("Dest_nro", EMIT["nro"]),
        "xBairro": cfg.get("Dest_xBairro", EMIT["xBairro"]),
        "cMun": cfg.get("Dest_cMun", EMIT["cMun"]),
        "xMun": cfg.get("Dest_xMun", EMIT["xMun"]),
        "UF": cfg.get("Dest_UF", EMIT["UF"]),
        "CEP": cfg.get("Dest_CEP", EMIT["CEP"]),
        "fone": cfg.get("Dest_fone", ""),
    }

    EMIT["CNPJ"] = _so_digitos(EMIT.get("CNPJ"))
    if len(EMIT["CNPJ"]) != 14:
        EMIT["CNPJ"] = "00995044000107"  # fallback sempre em dígitos

    # Razão social do emitente: obrigatório
    if not (EMIT.get("xNome") or "").strip():
        EMIT["xNome"] = "NUTRIGEL DISTRIBUIDORA EIRELI"

    # IE em dígitos (mantém 'ISENTO' se for o caso)
    if (EMIT.get("IE","").strip().upper() != "ISENTO"):
        EMIT["IE"] = _so_digitos(EMIT.get("IE"))

    # Destinatário (se houver)
    DEST["CNPJ"] = _so_digitos(DEST.get("CNPJ"))
    if (DEST.get("IE","").strip().upper() != "ISENTO"):
        DEST["IE"] = _so_digitos(DEST.get("IE"))

    if not EMIT.get("IE"):
        EMIT["IE"] = "ISENTO"

    # Se destinatário for isento (indIEDest=2) e IE vier vazia, define ISENTO
    if (DEST.get("indIEDest") == "2") and not DEST.get("IE"):
        DEST["IE"] = "ISENTO"

    # saneia mínimos obrigatórios
    for d in (EMIT, DEST):
        for k in ("xMun", "UF", "cMun", "CEP"):
            d[k] = (d.get(k) or "").strip()
    return EMIT, DEST

def aguarda_acbr_resposta(resp_path, timeout=120, interval=1.0):
    """Aguarda enviar-resp.txt e retorna dict com cStat/xMotivo/chNFe/xml."""
    t0 = time.time()
    last = ""
    while time.time() - t0 < timeout:
        if os.path.exists(resp_path):
            try:
                with open(resp_path, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
                if txt and txt != last:
                    last = txt
                    if "[Retorno]" in txt or "CStat=" in txt or txt.startswith("OK"):
                        break
            except Exception:
                pass
        time.sleep(interval)

    if not last:
        return {"ok": False, "mensagem": "Sem resposta do ACBr no tempo limite.", "cStat": None, "resposta_bruta": ""}

    def _find(pat, default=None, flags=re.IGNORECASE):
        m = re.search(pat, last, flags)
        return m.group(1).strip() if m else default

    cstat  = _find(r"\bCStat\s*=\s*([0-9]{2,3})")
    xmot   = _find(r"\bxMotivo\s*=\s*(.+)")
    chave  = _find(r"\b(ChaveNFe|chNFe)\s*=\s*([0-9]{44})") or _find(r"\b([0-9]{44})\b")
    arqxml = _find(r"\bArquivo(?:NFe|XML)?\s*=\s*(.+)") or _find(r"\\Logs\\.*?-nfe\.xml")

    ok = cstat in {"100", "104"} or last.upper().startswith("OK")
    return {"ok": ok, "cStat": cstat, "xMotivo": (xmot or "").splitlines()[0].strip() if xmot else None,
            "chNFe": chave, "xml": arqxml, "resposta_bruta": last}

# ------------------------- geração do comando -------------------------

def criaComandoACBr(self, nome_arquivo):
    """
    Gera UM ÚNICO arquivo de comando contendo:
      NFe.CriarEnviarNFe("...INI...", 1, 1, 1, , 1)
    """
    EMIT, DEST = _carregar_emit_dest(self)
    itens = list(getattr(self, "valoresDosItens", []) or [])

    os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)
    with open(nome_arquivo, "w", encoding="utf-8", newline="\r\n") as f:
        f.write('NFe.CriarEnviarNFe(\r\n"\r\n')

        # [infNFe] + [Identificacao]
        f.write("[infNFe]\r\nversao=4.00\r\n\r\n")
        f.write("[Identificacao]\r\n")
        f.write(f"cNF={random.randint(10_000_000, 99_999_999)}\r\n")

        natop = ""
        try:
            natop = getattr(self, "variavelNatureza").get().strip()
        except Exception:
            pass
        if not natop:
            natop = "VENDA DE MERCADORIA"
        f.write(f"natOp={natop}\r\n")
        f.write("mod=55\r\n")

        # --- SERIE: 0..999, sem zeros à esquerda ---
        raw_serie = None
        if hasattr(self, "variavelSerieDaNota") and hasattr(self.variavelSerieDaNota, "get"):
            raw_serie = (self.variavelSerieDaNota.get() or "").strip()
        elif hasattr(self, "serie"):
            raw_serie = str(getattr(self, "serie"))
        if not raw_serie or not raw_serie.isdigit():
            raw_serie = "1"
        serie_int = int(raw_serie)
        if not (0 <= serie_int <= 999):
            raise ValueError(f"Série inválida: {serie_int} (esperado 0..999)")
        f.write(f"serie={serie_int}\r\n")

        # --- nNF: 1..999999999 (sem zeros à esquerda) ---
        raw_nnf = None
        if hasattr(self, "variavelNumeroDaNota") and hasattr(self.variavelNumeroDaNota, "get"):
            raw_nnf = (self.variavelNumeroDaNota.get() or "").strip()
        elif hasattr(self, "nNF"):
            raw_nnf = str(getattr(self, "nNF"))
        if not raw_nnf or not raw_nnf.isdigit() or int(raw_nnf) == 0:
            raw_nnf = "1"
        nnf_int = int(raw_nnf)
        if not (1 <= nnf_int <= 999_999_999):
            raise ValueError(f"nNF inválido: {nnf_int} (esperado 1..999999999)")
        f.write(f"nNF={nnf_int}\r\n")

        # --- dhEmi: "dd/MM/yyyy HH:mm:ss" (formato ACBrMonitor) ---
        try:
            if QDate is not None and hasattr(self, "data_emissao") and hasattr(self.data_emissao, "setDate"):
                dia = datetime.now().day
                mes = datetime.now().month
                ano = datetime.now().year
                qdate = QDate(ano, mes, dia)
                self.data_emissao.setDate(qdate)
                dataEmissaoGeral = (self.data_emissao.text() or "").strip()  # dd/MM/yyyy
                d, m, y = dataEmissaoGeral.split("/")
                data_ptbr = f"{d.zfill(2)}/{m.zfill(2)}/{y}"
            else:
                data_ptbr = datetime.now().strftime("%d/%m/%Y")
        except Exception:
            data_ptbr = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")
        f.write(f"dhEmi={data_ptbr} {hora}\r\n")







        # tpNF: 1=saída (default) | 0=entrada
        f.write(f"dhEmi={data_ptbr} {hora}\r\n")

        # tpNF: 1=saída (default) | 0=entrada
        tpnf = ""
        try:
            tpnf = getattr(self, "variavelEntradaOuSaida").get().strip()
        except Exception:
            pass
        if tpnf not in {"0", "1"}:
            tpnf = "1"
        f.write(f"tpNF={tpnf}\r\n")

        idDest = "1" if (DEST.get("UF") == EMIT.get("UF")) else "2"
        f.write(f"idDest={idDest}\r\n")

        # >>>>>>>>>>>>>> AQUI adiciona o ambiente <<<<<<<<<<<<<<
        # 1 = Produção | 2 = Homologação
        f.write("tpAmb=2\r\n")

        f.write("tpImp=1\r\n")
        f.write("tpEmis=1\r\n")
        f.write("finNFe=1\r\n")   # ajuste também: finNFe=1 para NF-e normal
        f.write("indFinal=0\r\n")
        f.write("indPres=9\r\n")
        f.write("procEmi=0\r\n")
        f.write("verProc=Sistema Python\r\n\r\n")









        # Emitente
        f.write("[Emitente]\r\n")
        cnpj_emit = _so_digitos(EMIT.get('CNPJ'))
        if len(cnpj_emit) != 14:
            cnpj_emit = "00995044000107"  # fallback somente dígitos
        f.write(f"CNPJ={cnpj_emit}\r\n")

        # Razão social
        xnome = (EMIT.get('xNome') or "").strip()
        if not xnome:
            xnome = "NUTRIGEL DISTRIBUIDORA EIRELI"
        f.write(f"xNome={xnome}\r\n")

        # IE do emitente: 2–14 dígitos ou 'ISENTO'
        ie_emit = (EMIT.get('IE', '') or '').strip()
        if ie_emit.upper() != 'ISENTO':
            ie_emit = _so_digitos(ie_emit)
        if not ie_emit:
            ie_emit = 'ISENTO'
        f.write(f"IE={ie_emit}\r\n")

        # CRT do emitente: 1=Simples; 2=Simples excesso sublimite; 3=Regime Normal
        crt = str(getattr(self, 'crt', '') or '').strip()
        if crt not in {'1', '2', '3'}:
            crt_cfg = _ler_kv(os.path.join('NotaFiscal', 'configuracoes.txt')).get('CRT', '1')
            crt = str(crt_cfg).strip()
            if crt not in {'1', '2', '3'}:
                crt = '1'
        f.write(f"CRT={crt}\r\n")

        # Endereço
        f.write(f"xLgr={EMIT.get('xLgr','R DOUTOR OSCAR DA CUNHA')}\r\n")
        f.write(f"nro={EMIT.get('nro','126')}\r\n")
        f.write("xCpl=LETRA B\r\n")
        f.write(f"xBairro={EMIT.get('xBairro','FABRICAS')}\r\n")
        f.write(f"cMun={EMIT.get('cMun','3162500')}\r\n")
        f.write(f"xMun={EMIT.get('xMun','SAO JOAO DEL REI')}\r\n")
        f.write(f"UF={EMIT.get('UF','MG')}\r\n")
        f.write(f"CEP={EMIT.get('CEP','36301194')}\r\n")
        f.write("cPais=1058\r\nxPais=BRASIL\r\n")
        f.write(f"Fone={EMIT.get('fone','3233713382')}\r\n\r\n")

        # Destinatário
        f.write("[Destinatario]\r\n")
        f.write(f"CNPJCPF={DEST.get('CNPJ','')}\r\n")
        f.write(f"xNome={DEST.get('xNome','')}\r\n")
        f.write(f"indIEDest={(DEST.get('indIEDest') or '9')}\r\n")
        ie_dest = (DEST.get('IE','') or '').strip()
        if ie_dest:
            f.write(f"IE={ie_dest}\r\n")
        f.write(f"xLgr={DEST.get('xLgr','')}\r\n")
        f.write(f"nro={DEST.get('nro','')}\r\n")
        f.write(f"xBairro={DEST.get('xBairro','')}\r\n")
        f.write(f"cMun={DEST.get('cMun','')}\r\n")
        f.write(f"xMun={DEST.get('xMun','')}\r\n")
        f.write(f"UF={DEST.get('UF','')}\r\n")
        f.write(f"CEP={DEST.get('CEP','')}\r\n")
        f.write("cPais=1058\r\nxPais=BRASIL\r\n")
        f.write(f"Fone={DEST.get('fone','')}\r\n\r\n")

        # Itens
        for i, prod in enumerate(itens, start=1):
            idx = str(i).zfill(3)

            # defaults mínimos para schema/regra
            cProd  = (prod.get("codigo")          or "1")
            xProd  = (prod.get("descricao")       or "ITEM")
            NCM    = (prod.get("ncm")             or "00000000")  # ajuste com um NCM válido
            CFOP   = (prod.get("cfop")            or "5102")
            uCom   = (prod.get("unidade")         or "UN")
            qCom   = (prod.get("quantidade")      or "1.0000")
            vUnCom = (prod.get("valor_unitario")  or "0.01")
            vProd  = (prod.get("valor_total")     or vUnCom)

            f.write(f"[Produto{idx}]\r\n")
            f.write(f"cProd={cProd}\r\n")
            f.write(f"xProd={xProd}\r\n")
            f.write(f"NCM={NCM}\r\n")
            f.write(f"CFOP={CFOP}\r\n")
            f.write(f"uCom={uCom}\r\n")
            f.write(f"qCom={qCom}\r\n")
            f.write(f"vUnCom={vUnCom}\r\n")
            f.write(f"vProd={vProd}\r\n")
            f.write("indTot=1\r\n\r\n")

            # --- ICMS por item conforme o CRT ---
            crt_item = crt  # usa o já definido
            f.write("[ICMS001]\r\n")

            if crt_item in {'1', '2'}:
                # Simples Nacional -> usar CSOSN, não usar CST
                csosn = (getattr(self, 'csosn_padrao', '') or '').strip()
                if csosn not in {'101','102','103','201','202','203','300','400','500','900'}:
                    csosn = '102'  # venda interna sem crédito
                orig = str(getattr(self, 'orig_padrao', '0')).strip() or '0'
                f.write(f"orig={orig}\r\n")
                f.write(f"CSOSN={csosn}\r\n")
                if csosn in {'101', '201', '900'}:
                    pCredSN = getattr(self, 'pCredSN', '0.00')
                    vCredICMSSN = getattr(self, 'vCredICMSSN', '0.00')
                    f.write(f"pCredSN={pCredSN}\r\n")
                    f.write(f"vCredICMSSN={vCredICMSSN}\r\n")
            else:
                # Regime Normal -> usar CST e base/aliquota/valor
                cst = (getattr(self, 'cst_padrao', '') or '').strip()
                if cst not in {'00','02','10','15','20','30','40','51','53','60'}:
                    cst = '00'  # tributação integral
                orig = str(getattr(self, 'orig_padrao', '0')).strip() or '0'
                vBC = getattr(self, 'vBC', '0.00')
                pICMS = getattr(self, 'pICMS', '0.00')
                vICMS = getattr(self, 'vICMS', '0.00')
                f.write(f"orig={orig}\r\n")
                f.write(f"CST={cst}\r\n")
                f.write(f"vBC={vBC}\r\n")
                f.write(f"pICMS={pICMS}\r\n")
                f.write(f"vICMS={vICMS}\r\n")
            # --- fim ICMS ---

            f.write(f"[PIS{idx}]\r\n")
            f.write(f"CST={(prod.get('cst_pis') or '99')}\r\n")
            f.write(f"vBC={(prod.get('bc_pis') or '0.00')}\r\n")
            f.write(f"pPIS={(prod.get('aliq_pis') or '0.00')}\r\n")
            f.write(f"vPIS={(prod.get('valor_pis') or '0.00')}\r\n\r\n")

            f.write(f"[COFINS{idx}]\r\n")
            f.write(f"CST={(prod.get('cst_cofins') or '99')}\r\n")
            f.write(f"vBC={(prod.get('bc_cofins') or '0.00')}\r\n")
            f.write(f"pCOFINS={(prod.get('aliq_cofins') or '0.00')}\r\n")
            f.write(f"vCOFINS={(prod.get('valor_cofins') or '0.00')}\r\n\r\n")

        # Totais
        f.write("[Total]\r\n")
        f.write(f"vProd={getattr(self, 'valorTotalProdutos').get()}\r\n")
        f.write(f"vNF={getattr(self, 'valorLiquido').get()}\r\n")
        f.write(f"vFrete={getattr(self, 'totalFrete').get()}\r\n")
        f.write(f"vSeg={getattr(self, 'totalSeguro').get()}\r\n")
        f.write(f"vDesc={getattr(self, 'totalDesconto').get()}\r\n")
        f.write(f"vOutro={getattr(self, 'outrasDespesas').get()}\r\n")
        f.write(f"vICMS={getattr(self, 'valorICMS').get()}\r\n")
        f.write(f"vIPI={getattr(self, 'totalIPI').get()}\r\n")
        f.write(f"vPIS={getattr(self, 'totalPIS').get()}\r\n")
        f.write(f"vCOFINS={getattr(self, 'totalCOFINS').get()}\r\n\r\n")

        # Transporte
        f.write("[Transportador]\r\n")
        f.write("modFrete=9\r\n\r\n")  # sem frete

        # Pagamento
        f.write("[pag001]\r\n")
        f.write("tpag=01\r\n")
        f.write(f"vPag={getattr(self, 'valorLiquido').get()}\r\n\r\n")

        # Fecha o comando (formato do ACBr)
        f.write('"\r\n,1,1, , ,1)')

# ------------------------- execução -------------------------

def gerarNFe(self):
    """
    Cria NotaFiscal/EnviarComando/enviar.txt (CriarEnviarNFe) e
    aguarda NotaFiscal/ReceberComando/enviar-resp.txt.
    """
    os.makedirs(ACBR_CMD_DIR, exist_ok=True)
    os.makedirs(ACBR_RSP_DIR, exist_ok=True)

    resp_path = os.path.join(ACBR_RSP_DIR, "enviar-resp.txt")
    try:
        if os.path.exists(resp_path):
            os.remove(resp_path)
    except Exception:
        pass

    cmd_path = os.path.join(ACBR_CMD_DIR, "enviar.txt")

    itens = list(getattr(self, "valoresDosItens", []) or [])
    if len(itens) == 0:
        return {"ok": False, "mensagem": "NF-e sem itens: adicione ao menos 1 produto antes de enviar."}

    criaComandoACBr(self, cmd_path)

    # Debugs úteis
    with open(cmd_path, "r", encoding="utf-8", errors="ignore") as _f:
        _txt = _f.read()
    print("DEBUG: enviar.txt absoluto:", os.path.abspath(cmd_path))
    _dhemi = re.findall(r"^dhEmi=(.*)$", _txt, flags=re.MULTILINE)
    print("DEBUG: dhEmi encontrado:", _dhemi)

    resultado = aguarda_acbr_resposta(resp_path)
    print(f"↩️ cStat={resultado.get('cStat')} - {resultado.get('xMotivo')}")
    if resultado.get("xml"):
        print(f"📄 XML: {resultado['xml']}")
    if not resultado["ok"]:
        print("❌ Falha no envio. Veja 'resposta_bruta' para diagnóstico.")
    return resultado
