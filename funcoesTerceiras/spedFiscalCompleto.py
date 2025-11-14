# funcoesTerceiras/spedFiscalCompleto.py
import os, re, glob, json, datetime
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET
import locale

try:
    import db  # opcional: deve expor 'cursor'
except Exception:
    db = None


def gerar_sped_fiscal_completo(
    self,
    mes,
    ano,
    cnpjUsadoParaSped,
    caminho_txt,
    dt_ini,
    dt_fin,
    pasta_logs=None,
    blocos_ativos=("0","B","C","D","E","G","H","K","1","9"),
    incluir_0005=True,
    incluir_0100=True,
):
    ano = ano.get()
    mes = mes.get().lower()
    locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")
    mesNumero = datetime.datetime.strptime(mes, "%B").month
    dataRefarencia = datetime.datetime(int(ano), int(mesNumero), 1)

    nome = ""
    documento = ""
    inscEstadual = ""
    Cep = ""
    logradouro = ""
    numero = ""
    Bairro = ""
    telefone = ""
    Email = ""



    if cnpjUsadoParaSped == "Nutrigel":
        nome = "NUTRIGEL DISTRIBUIDORA EIRELI"
        inscEstadual= "6259569630086"
        documento = "00995044000107"
        Cep = "36301194"
        logradouro = "RUA DOUTOR OSCAR DA CUNHA"
        numero = "75"
        Bairro = "FABRICAS"
        telefone = "3233716171"
        Email = "multimaquinas_financeiro@yahoo.com.br"
        codigoMunicipio = "3162500"


    if cnpjUsadoParaSped == "Multimáquinas":
        nome = "MULTIMAQUINAS REFRIGERACAO E MAQUINAS DEL REI LTDA"
        documento = "05704180000106"
        inscEstadual= "6252430230046"
        Cep = "36301194"
        logradouro = "RUA DOUTOR OSCAR DA CUNHA"
        numero = "97"
        Bairro = "FABRICAS"
        telefone = "3233713382"
        Email = "multimaquinas_financeiro@yahoo.com.br"
        codigoMunicipio = "3162500"

    if cnpjUsadoParaSped == "Polimáquinas":
        nome = "ANA F COELHO RESENDE"
        documento = "23889618000150"
        inscEstadual= "84549874"


    # ---------------- helpers ----------------
    def _somente_dig(s): 
        return re.sub(r"\D+", "", str(s or ""))

    def _parse_dt(s):
        return datetime.date(int(s[0:4]), int(s[4:6]), int(s[6:8]))

    def _get(attr, default=""):
        v = getattr(self, attr, default)
        try:
            if hasattr(v, "get"):
                return str(v.get())
        except Exception:
            pass
        return str(v)

    def _safe(el, tag, ns=None, default=""):
        if el is None:
            return default
        if ns and ":" not in tag:
            tag = f"n:{tag}"
        node = el.find(tag, ns) if ns else el.find(tag)
        if node is not None and node.text and node.text.strip():
            return node.text.strip()
        return default

    def _num(x):
        try:
            return float(str(x).replace(",", "."))
        except Exception:
            return 0.0

    def _fmt(v):
        try:
            return f"{float(v):.2f}".replace(".", ",")
        except Exception:
            return "0,00"

    def _norm_cst(cst):
        s = _somente_dig(cst)
        if len(s) == 0: return "000"
        if len(s) == 1: return "00"+s
        if len(s) == 2: return "0"+s
        return s[:3]

    def _s(v):  # sanear textos para campos com pipe
        return ("" if v is None else str(v)).replace("|","/").strip()

    def ativo(letra: str) -> bool:
        return letra in set(x.upper() for x in blocos_ativos)

    # ---------------- período / xmls ----------------
    d_i, d_f = _parse_dt(dt_ini), _parse_dt(dt_fin)
    if not pasta_logs:
        pasta_logs = getattr(self, "caminhoLogsAcbr", r"C:\ACBrMonitorPLUS\Logs")
    pasta_logs = os.path.abspath(pasta_logs)
    xmls = []
    # if usar_fallback_xml:
    #     pats = ["*-procNFe.xml", "*-procNFCe.xml", "*-nfe.xml", "*-nfce.xml"]
    #     for p in pats:
    #         xmls += glob.glob(os.path.join(pasta_logs, p))
    #     xmls = sorted(set(xmls))

    emit = {
        "COD_VER": "019",
        "FINALIDADE": 0,
        "NOME": nome,
        "CNPJ": documento,
        "UF": (_get("variavelUFEnd", "") or _get("estadoEmitente", "MG")).strip().upper() or "MG",
        "IE": inscEstadual,
        "COD_MUN": codigoMunicipio,
        "IM": _get("imEmitente", ""),
        "SUFRAMA": "",
        "IND_ATIV": "1",
        "PERFIL": {"Perfil A":"A","Perfil B":"B","Perfil C":"C"}.get(_get("perfilSped","Perfil A"),"A"),
    }
    cbf = getattr(self, "cbFinalidade", None)
    if cbf and hasattr(cbf, "get") and "sub" in cbf.get().lower():
        emit["FINALIDADE"] = 1
    cbp = getattr(self, "cbPerfil", None)
    if cbp and hasattr(cbp, "get"):
        emit["PERFIL"] = {"Perfil A":"A","Perfil B":"B","Perfil C":"C"}.get(cbp.get(), emit["PERFIL"])

    # fallbacks via DB
    # if (len(emit["CNPJ"])!=14 or not emit["UF"] or not emit["COD_MUN"] or emit["IE"]=="ISENTO") and db and getattr(db, "cursor", None):
        # try:
        #     cur = db.cursor
        #     cur.execute("""
        #         SELECT emitente_cnpjcpf, emitente_nome, emitente_ie, emitente_cod_mun, emitente_uf
        #         FROM notas_fiscais
        #         WHERE COALESCE(cancelada,0)=0
        #         ORDER BY dhEmi DESC LIMIT 1
        #     """)
        #     r = cur.fetchone()
        #     if r:
        #         cnpj_db = _somente_dig(r[0] or "")
        #         if len(emit["CNPJ"])!=14 and len(cnpj_db)==14: emit["CNPJ"]=cnpj_db
        #         if not emit["NOME"] and r[1]: emit["NOME"]=str(r[1])
        #         ie_db = _somente_dig(r[2] or "")
        #         if emit["IE"]=="ISENTO" and ie_db: emit["IE"]=ie_db
        #         cm_db = _somente_dig(r[3] or "")
        #         if not emit["COD_MUN"] and cm_db: emit["COD_MUN"]=cm_db
        #         uf_db = (r[4] or "").strip().upper()
        #         if not emit["UF"] and uf_db: emit["UF"]=uf_db
        # except Exception:
        #     pass

    
    # garantias mínimas (validador indicará se inválido)
    if len(emit["CNPJ"])!=14: emit["CNPJ"]="00000000000000"
    if not emit["COD_MUN"]: emit["COD_MUN"]="0000000"

    # ---------------- Coleta de Notas ----------------
    notas = []
    partes = {}

    # Banco (prioridade)

    if db and getattr(db, "cursor", None):
        cur = db.cursor
        di = datetime.datetime(d_i.year, d_i.month, d_i.day, 0,0,0)
        df = datetime.datetime(d_f.year, d_f.month, d_f.day, 23,59,59)
        cur.execute("""
            SELECT modelo, serie, numero, chave, tpNF, dhEmi,
                    valor_total, valor_desconto, valor_produtos, valor_frete, valor_seguro, valor_outras_despesas,
                    valor_bc_icms, valor_icms, valor_bc_icms_st, valor_icms_st, valor_ipi, valor_pis, valor_cofins, itens_json,
                    destinatario_cnpjcpf, destinatario_nome
                FROM notas_fiscais
                WHERE dhEmi BETWEEN %s AND %s AND COALESCE(cancelada,0)=0 and emitente_nome = %s;
        """, (di, df, nome))
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        for r in rows:
            rec = dict(zip(cols, r))
            d_emis = rec.get("dhEmi")
            if isinstance(d_emis, str):
                try: d_emis = datetime.datetime.fromisoformat(d_emis)
                except Exception: d_emis = di
            if isinstance(d_emis, datetime.date) and not isinstance(d_emis, datetime.datetime):
                d_emis = datetime.datetime(d_emis.year, d_emis.month, d_emis.day)

            mod = str(rec.get("modelo") or "55")
            serie = int(rec.get("serie") or 0)
            nnf = int(rec.get("numero") or 0)
            chv = str(rec.get("chave") or "")
            tpNF = str(rec.get("tpNF") or "1")

            vNF = float(rec.get("valor_total") or 0.0)
            vDesc = float(rec.get("valor_desconto") or 0.0)
            vProd = float(rec.get("valor_produtos") or 0.0)
            vFrete = float(rec.get("valor_frete") or 0.0)
            vSeg = float(rec.get("valor_seguro") or 0.0)
            vOutros = float(rec.get("valor_outras_despesas") or 0.0)

            vBC = float(rec.get("valor_bc_icms") or 0.0)
            vICMS = float(rec.get("valor_icms") or 0.0)
            vBCST = float(rec.get("valor_bc_icms_st") or 0.0)
            vICMSST = float(rec.get("valor_icms_st") or 0.0)
            vIPI = float(rec.get("valor_ipi") or 0.0)
            vPIS = float(rec.get("valor_pis") or 0.0)
            vCOFINS = float(rec.get("valor_cofins") or 0.0)

            cod_part = _somente_dig(rec.get("destinatario_cnpj") or "") or f"CF-{nnf}"
            nome_dest = (rec.get("destinatario_nome") or "CONSUMIDOR FINAL").strip() or "CONSUMIDOR FINAL"
            partes.setdefault(cod_part, {
                "NOME": nome_dest[:100], "CNPJ": _somente_dig(rec.get("destinatario_cnpj") or ""),
                "CPF": "", "COD_PAIS": "1058", "IE": "", "COD_MUN": "", "SUFRAMA": "",
                "END": "", "NUM": "", "COMPL": "", "BAIRRO": "",
            })

            items = []
            raw = rec.get("itens_json")
            if raw:
                try:
                    if isinstance(raw, (bytes, bytearray)): raw = raw.decode("utf-8", "ignore")
                    data = json.loads(raw)
                    items = data.get("itens", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
                except Exception:
                    items = []

            if str(cod_part).startswith('CF-'):
                cod_part=""

            if str(rec.get("modelo")) == "65":
                c100 = {
                    "IND_OPER": "1" if tpNF=="1" else "0",
                    "IND_EMIT": "0",
                    "COD_MOD": rec.get("modelo"),
                    "COD_SIT": "00",
                    "SER": serie, 
                    "NUM_DOC": nnf, 
                    "CHV_NFE": chv,
                    "DT_DOC": d_emis.strftime("%d%m%Y"), 
                    "DT_E_S": d_emis.strftime("%d%m%Y"),
                    "VL_DOC": vNF, 
                    "IND_PGTO": "0", 
                    "VL_DESC": vDesc, 
                    "VL_ABAT_NT": 0.0,
                    "VL_MERC": vProd, 
                    "IND_FRT": "0", 
                    "VL_FRT": vFrete, 
                    "VL_SEG": vSeg, 
                    "VL_OUT_DA": vOutros,
                    "VL_BC_ICMS": vBC, 
                    "VL_ICMS": vICMS, 
                    "VL_BC_ICMS_ST": "", 
                    "VL_ICMS_ST": "",
                    "VL_IPI": "", 
                    "VL_PIS": "", 
                    "VL_COFINS": "", 
                    "VL_PIS_ST": "", 
                    "VL_COFINS_ST": "",
                    "COD_PART": "",
                    "C190": defaultdict(lambda:{"VL_OPR":0.0,"VL_BC_ICMS":vBC,"VL_ICMS":vICMS,"VL_BC_ICMS_ST":0.0,"VL_ICMS_ST":0.0,"VL_RED_BC":0.0,"VL_IPI":0.0,}),
                }
            else:
                print("caiu aqui")
                c100 = {
                    "IND_OPER": "1" if tpNF=="1" else "0",
                    "IND_EMIT": "0",
                    "COD_PART": cod_part,
                    "COD_MOD": rec.get("modelo"),
                    "COD_SIT": "00",
                    "SER": serie, 
                    "NUM_DOC": nnf, 
                    "CHV_NFE": chv,
                    "DT_DOC": d_emis.strftime("%d%m%Y"), 
                    "DT_E_S": d_emis.strftime("%d%m%Y"),
                    "VL_DOC": vNF, 
                    "IND_PGTO": "0", 
                    "VL_DESC": vDesc, 
                    "VL_ABAT_NT": 0.0,
                    "VL_MERC": vProd, 
                    "IND_FRT": "0", 
                    "VL_FRT": vFrete, 
                    "VL_SEG": vSeg, 
                    "VL_OUT_DA": vOutros,
                    "VL_BC_ICMS": vBC, 
                    "VL_ICMS": vICMS, 
                    "VL_BC_ICMS_ST": vBCST, 
                    "VL_ICMS_ST": vICMSST,
                    "VL_IPI": vIPI, 
                    "VL_PIS": vPIS, 
                    "VL_COFINS": vCOFINS, 
                    "VL_PIS_ST": 0.0, 
                    "VL_COFINS_ST": 0.0,
                    "C190": defaultdict(lambda:{"VL_OPR":0.0,"VL_BC_ICMS":vBC,"VL_ICMS":vICMS,"VL_BC_ICMS_ST":0.0,"VL_ICMS_ST":0.0,"VL_RED_BC":0.0,"VL_IPI":0.0,}),
                }
            
            
            # MINFIX: NFC-e (modelo 65) - remover COD_PART e zerar campos proibidos no C100
            # NFC-e (65): sem participante e campos vedados no C100
            if str(c100.get("COD_MOD")) == "65":
                c100["COD_PART"] = ""
            for it in items:
                cfop = str(it.get("CFOP") or it.get("cfop") or "5102")
                cst  = _norm_cst(it.get("CST") or it.get("CSOSN") or it.get("cst") or it.get("csosn") or "00")
                aliq = _num(it.get("pICMS") or it.get("aliqICMS") or it.get("pIcms") or 0)
                v_item = _num(it.get("vProd") or it.get("valor_produto") or it.get("valor") or 0)
                vbc_i  = _num(it.get("vBC") or it.get("bc_icms") or 0)
                vicms_i= _num(it.get("vICMS") or it.get("icms") or 0)
                k = (cst, cfop, round(aliq,2))
                ag = c100["C190"][k]
                ag["VL_OPR"] += v_item
                ag["VL_BC_ICMS"] += vbc_i
                ag["VL_ICMS"] += vicms_i

            notas.append(c100)
            print(c100)
            # print(notas)



    # ---------------- linhas ----------------
    linhas = []
    regs = []
    def add(line, reg=None):
        linhas.append(line)
        if reg: regs.append(reg)

    # ===== Bloco 0 =====
    if ativo("0"):
        b0 = len(linhas)
        add(f"|0000|{emit['COD_VER']}|{emit['FINALIDADE']}|{d_i.strftime('%d%m%Y')}|{d_f.strftime('%d%m%Y')}|{emit['NOME']}|{emit['CNPJ']}||{emit['UF']}|{emit['IE']}|{emit['COD_MUN']}|{emit['IM']}|{emit['SUFRAMA']}|{emit['PERFIL']}|{emit['IND_ATIV']}|", "0000")
        add(f"|0001|{'0' if (incluir_0005 or incluir_0100) else '1'}|", "0001")


        if incluir_0005:
            fantasia = nome
            cep      = Cep
            end      = logradouro
            num      = numero
            compl    = ""
            bairro   = Bairro
            fone     = telefone
            fax      = ""
            email    = Email
            add(f"|0005|{_s(fantasia)}|{_s(cep)}|{_s(end)}|{_s(num)}|{_s(compl)}|{_s(bairro)}|{_s(fone)}|{_s(fax)}|{_s(email)}|", "0005")

        if incluir_0100:
            nome_cont = "RICARDO LIMA BEFENATI"
            cpf_cont  = "03404667662"
            crc_cont  = "094666O3"
            cnpj_escr = ""
            cep_cont  = "36307302"
            end_cont  = "RUA QUITINO BOCAIUVA"
            num_cont  = "50"
            compl_cont= ""
            bairro_cont= "CENTRO"
            fone_cont = ""
            fax_cont  = ""
            email_cont= "liracontabilidade@cofresieg.com.br"
            cod_mun_cont = "3162500"
            add(f"|0100|{_s(nome_cont)}|{_s(cpf_cont)}|{_s(crc_cont)}|{_s(cnpj_escr)}|{_s(cep_cont)}|{_s(end_cont)}|{_s(num_cont)}|{_s(compl_cont)}|{_s(bairro_cont)}|{_s(fone_cont)}|{_s(fax_cont)}|{_s(email_cont)}|{_s(cod_mun_cont)}|", "0100")

        # 0150 (somente participantes usados)
        for cod, p in sorted(partes.items()):
                # MINFIX: não gerar 0150 para códigos 'CF-xxx' (consumidor final sem identificação)
            if str(cod).startswith('CF-'):
                continue
            add("|0150|{COD_PART}|{NOME}|{COD_PAIS}|{CNPJ}|{CPF}|{IE}|{COD_MUN}|{SUFRAMA}|{END}|{NUM}|{COMPL}|{BAIRRO}|".format(
            COD_PART=str(cod)[:60],
            NOME=_s(p.get("NOME") or "PARTICIPANTE")[:100],
            COD_PAIS=p.get("COD_PAIS","1058"),
            CNPJ=_somente_dig(p.get("CNPJ","")),
            CPF=_somente_dig(p.get("CPF","")),
            IE=_somente_dig(p.get("IE","")),
            COD_MUN=codigoMunicipio,
            SUFRAMA=_s(p.get("SUFRAMA","")),
            END=logradouro,
            NUM=_s(p.get("NUM",""))[:10],
            COMPL=_s(p.get("COMPL",""))[:60],
            BAIRRO=_s(p.get("BAIRRO",""))[:60],
            ), "0150")
        qtd_0 = (len(linhas) - b0) + 1
        add(f"|0990|{qtd_0}|", "0990")

    # ===== Bloco B (sem movimento) =====
    if ativo("B"):
        ini = len(linhas)
        add("|B001|1|", "B001")
        add(f"|B990|{(len(linhas)-ini)+1}|", "B990")

    # ===== Bloco C =====
    if ativo("C"):
        bc = len(linhas)
        if notas:
            add("|C001|0|", "C001")
            for n in notas:
                if str(n.get("COD_MOD")) == "65":
                    add("|C100|{IND_OPER}|{IND_EMIT}|{COD_PART}|{COD_MOD}|{COD_SIT}|{SER}|{NUM_DOC}|{CHV_NFE}|{DT_DOC}|{DT_E_S}|{VL_DOC}|{IND_PGTO}|{VL_DESC}|{VL_ABAT_NT}|{VL_MERC}|{IND_FRT}|{VL_FRT}|{VL_SEG}|{VL_OUT_DA}|{VL_BC_ICMS}|{VL_ICMS}|{VL_BC_ICMS_ST}|{VL_ICMS_ST}|{VL_IPI}|{VL_PIS}|{VL_COFINS}|{VL_PIS_ST}|{VL_COFINS_ST}|".format(
                        VL_DOC       =_fmt(n["VL_DOC"]), 
                        VL_DESC      =_fmt(n["VL_DESC"]),
                        VL_ABAT_NT   =_fmt(n["VL_ABAT_NT"]), 
                        VL_MERC      =_fmt(n["VL_MERC"]), 
                        VL_FRT       =_fmt(n["VL_FRT"]), 
                        VL_SEG       =_fmt(n["VL_SEG"]), 
                        VL_OUT_DA    =_fmt(n["VL_OUT_DA"]),
                        VL_BC_ICMS   =_fmt(n["VL_BC_ICMS"]), 
                        VL_ICMS      =_fmt(n["VL_ICMS"]),
                        IND_OPER     =n["IND_OPER"], 
                        IND_EMIT     =n["IND_EMIT"], 
                        COD_MOD      =n["COD_MOD"], 
                        COD_SIT      =n["COD_SIT"], 
                        SER          =n["SER"], 
                        NUM_DOC      =n["NUM_DOC"],
                        CHV_NFE      =n["CHV_NFE"], 
                        DT_DOC       =n["DT_DOC"], 
                        DT_E_S       =n["DT_E_S"],
                        IND_PGTO     =n["IND_PGTO"], 
                        IND_FRT      =n["IND_FRT"],
                        VL_COFINS_ST ="",
                        VL_BC_ICMS_ST="", 
                        VL_ICMS_ST   ="",
                        VL_IPI       ="", 
                        VL_PIS       ="", 
                        VL_COFINS    ="",
                        VL_PIS_ST    ="", 
                        COD_PART     ="",
                    ), "C100")
                else:
                    print("caiu aqui21")
                    add("|C100|{IND_OPER}|{IND_EMIT}|{COD_PART}|{COD_MOD}|{COD_SIT}|{SER}|{NUM_DOC}|{CHV_NFE}|{DT_DOC}|{DT_E_S}|{VL_DOC}|{IND_PGTO}|{VL_DESC}|{VL_ABAT_NT}|{VL_MERC}|{IND_FRT}|{VL_FRT}|{VL_SEG}|{VL_OUT_DA}|{VL_BC_ICMS}|{VL_ICMS}|{VL_BC_ICMS_ST}|{VL_ICMS_ST}|{VL_IPI}|{VL_PIS}|{VL_COFINS}|{VL_PIS_ST}|{VL_COFINS_ST}|".format(
                        IND_OPER     =n["IND_OPER"], 
                        IND_EMIT     =n["IND_EMIT"], 
                        COD_PART     =str(n["COD_PART"])[:60],
                        COD_MOD      =n["COD_MOD"], 
                        COD_SIT      =n["COD_SIT"], 
                        SER          =n["SER"], 
                        NUM_DOC      =n["NUM_DOC"],
                        CHV_NFE      =n["CHV_NFE"], 
                        DT_DOC       =n["DT_DOC"], 
                        DT_E_S       =n["DT_E_S"],
                        VL_DOC       =_fmt(n["VL_DOC"]), 
                        IND_PGTO     =n["IND_PGTO"], 
                        VL_DESC      =_fmt(n["VL_DESC"]),
                        VL_ABAT_NT   =_fmt(n["VL_ABAT_NT"]), 
                        VL_MERC      =_fmt(n["VL_MERC"]), 
                        IND_FRT      =n["IND_FRT"],
                        VL_FRT       =_fmt(n["VL_FRT"]), 
                        VL_SEG       =_fmt(n["VL_SEG"]), 
                        VL_OUT_DA    =_fmt(n["VL_OUT_DA"]),
                        VL_BC_ICMS   =_fmt(n["VL_BC_ICMS"]), 
                        VL_ICMS      =_fmt(n["VL_ICMS"]),
                        VL_BC_ICMS_ST=_fmt(n["VL_BC_ICMS_ST"]), 
                        VL_ICMS_ST   =_fmt(n["VL_ICMS_ST"]),
                        VL_IPI       =_fmt(n["VL_IPI"]), 
                        VL_PIS       =_fmt(n["VL_PIS"]), 
                        VL_COFINS    =_fmt(n["VL_COFINS"]),
                        VL_PIS_ST    =_fmt(n["VL_PIS_ST"]), 
                        VL_COFINS_ST =_fmt(n["VL_COFINS_ST"]),
                    ), "C100")
                for (cst, cfop, aliq), v in sorted(n["C190"].items()):
                    add(f"|C190|{cst}|{cfop}|{_fmt(aliq)}|{_fmt(v['VL_OPR'])}|{_fmt(v['VL_BC_ICMS'])}|{_fmt(v['VL_ICMS'])}|{_fmt(v['VL_BC_ICMS_ST'])}|{_fmt(v['VL_ICMS_ST'])}|{_fmt(v['VL_RED_BC'])}|{_fmt(v['VL_IPI'])}||", "C190")
            qtd_c = (len(linhas) - bc) + 1
            add(f"|C990|{qtd_c}|", "C990")
        else:
            add("|C001|1|", "C001")
            add("|C990|2|", "C990")

    # ===== Blocos D/E/G/H/K sem movimento =====
    for letra in ("D","E","G","H","K"):
        if ativo(letra):
            ini = len(linhas)
            if letra == "E" and notas:
                add("|E001|0|", "E001")
                add(f"|E100|{d_i.strftime('%d%m%Y')}|{d_f.strftime('%d%m%Y')}|", "E100")
                # E110 (apuração) – mínimos em zero para satisfazer o filho obrigatório
                # VL_TOT_DEBITOS = soma do VL_ICMS dos C190 com CFOP 5xxx/6xxx/7xxx/1605
                tot_debitos = 0.0
                for n in notas:
                    for (cst, cfop, aliq), v in n["C190"].items():
                        cf = str(cfop)
                        if cf.startswith(("5", "6", "7")) or cf == "1605":
                            tot_debitos += float(v["VL_ICMS"])

                vl_tot_debitos   = _fmt(tot_debitos)
                vl_sld_apurado   = vl_tot_debitos   # sem créditos/ajustes, saldo = débitos
                vl_icms_recolher = vl_tot_debitos   # idem

                add(f"|E110|{vl_tot_debitos}|0,00|0,00|0,00|0,00|0,00|0,00|0,00|0,00|{vl_sld_apurado}|0,00|{vl_icms_recolher}|0,00|0,00|", "E110")
                total_obrig = tot_debitos  # igual ao que usamos em vl_icms_recolher

                # vencimento: 15 do mês seguinte ao fim do período (qualquer data válida serve p/ passar a regra)
                first_next_month = (d_f.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
                vcto = first_next_month + datetime.timedelta(days=14)  # dia 15

                add(f"|E116|000|{_fmt(total_obrig)}|{vcto.strftime('%d%m%Y')}|1206|||||{dataRefarencia.strftime("%m%Y")}|", "E116")
            else:
                add(f"|{letra}001|1|", f"{letra}001")
            add(f"|{letra}990|{(len(linhas)-ini)+1}|", f"{letra}990")

    if ativo("1"):
        ini = len(linhas)
        add("|1001|0|", "1001")  # com dados, pois haverá 1010
        # 1010: todos “N” quando não há obrigação de sub-blocos (ajuste “S” se sua UF exigir)
        add("|1010|N|N|N|N|N|N|N|N|N|N|N|N|N|", "1010")
        add(f"|1990|{(len(linhas)-ini)+1}|", "1990")

    # ===== Bloco 9 (sempre por último) =====
    # Calcular contagem antes de inserir 9001 para não duplicar 9900|9001|1|
    cont = Counter(regs)  # somente registros até aqui (sem 9001/9900/9990/9999)
    add("|9001|0|", "9001")

    for r in sorted(cont.keys()):
        add(f"|9900|{r}|{cont[r]}|", "9900")

    # 9900 para 9001, 9990 e 9999 (apenas 1 ocorrência cada)
    add("|9900|9001|1|", "9900")
    add("|9900|9990|1|", "9900")
    add("|9900|9999|1|", "9900")

    # 9900 do próprio 9900 com TOTAL de linhas 9900 emitidas (inclui esta linha)
    total_9900 = len(cont) + 3 + 1
    add(f"|9900|9900|{total_9900}|", "9900")

    # 9990: total de linhas do bloco 9 = 9001(1) + 9900(total_9900) + 9990(1) + 9999(1)
    add(f"|9990|{1 + total_9900 + 1 + 1}|", "9990")

    # 9999: total de linhas do arquivo (+1 do próprio 9999)
    add(f"|9999|{len(linhas)+1}|", "9999")

    # gravação
    out = Path(caminho_txt)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="latin-1") as f:
        linhas_sem_espaco = [l.replace(" ", " ") for l in linhas]
        f.write("\r\n".join(linhas_sem_espaco) + "\r\n")
    return str(out)
