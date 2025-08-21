import re
import xml.dom.minidom as minidom
import datetime
from xml.etree.ElementTree import QName
from attr import s
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from cryptography.hazmat.primitives.serialization import pkcs12
from signxml import XMLSigner, methods, SignatureMethod, DigestAlgorithm
from brazilfiscalreport.danfe import Danfe
from lxml import etree
from xml.dom.minidom import Document, parseString
from zeep import Client
from zeep.transports import Transport
import requests, random, os
import tempfile
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
import warnings
from requests_pkcs12 import Pkcs12Adapter


class XMLSignerWithSHA1(XMLSigner):
    # Desabilita o bloqueio interno de SHA1 do signxml
    def check_deprecated_methods(self):
        pass


def criaComandoACBr(self, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        # Inicia o comando ACBr
        f.write('NFe.CriarEnviarNFe("\n')
        
        # ------------------- Identificacao -------------------
        f.write("[infNFe]\n")
        f.write("versao=4.00\n\n")
        
        f.write("[Identificacao]\n")
        f.write(f"cNF={str(random.randint(10000000, 99999999))}\n")
        f.write(f"natOp={self.variavelNatureza.get()}\n")
        f.write(f"mod=55\n")
        f.write(f"serie={self.variavelSerieDaNota.get()}\n")
        f.write(f"nNF={self.variavelNumeroDaNota.get()}\n")
        f.write(f"dhEmi={self.variavelDataDocumento.get()} {self.variavelHoraEntradaSaida.get()}\n")
        f.write(f"tpNF={self.variavelEntradaOuSaida.get()}\n")
        f.write(f"idDest=1\n")
        f.write(f"tpImp=1\n")
        f.write(f"tpEmis=1\n")
        f.write(f"finNFe=0\n")
        f.write(f"indFinal=0\n")
        f.write(f"indPres=9\n")
        f.write(f"procEmi=0\n")
        f.write(f"verProc=Sistema Python\n\n")

        # ------------------- Emitente -------------------
        f.write("[Emitente]\n")
        f.write(f"CNPJCPF={self.variavelCNPJRazaoSocialEmitente.get()}\n")
        f.write(f"xNome={self.variavelRazaoSocialEmitente.get()}\n")
        f.write(f"IE=\n")
        f.write(f"xLgr=\n")
        f.write(f"nro=\n")
        f.write(f"xBairro=\n")
        f.write(f"cMun=\n")
        f.write(f"xMun=\n")
        f.write(f"UF=\n")
        f.write(f"CEP=\n")
        f.write(f"cPais=1058\n")
        f.write(f"xPais=BRASIL\n")
        f.write(f"Fone=\n\n")

        # ------------------- Destinatario -------------------
        f.write("[Destinatario]\n")
        f.write(f"CNPJCPF={self.variavelCNPJRazaoSocialRemetente.get()}\n")
        f.write(f"xNome={self.variavelRazaoSocialRemetente.get()}\n")
        f.write(f"indIEDest=3\n")
        f.write(f"IE=\n")
        f.write(f"xLgr=\n")
        f.write(f"nro=\n")
        f.write(f"xBairro=\n")
        f.write(f"cMun=\n")
        f.write(f"xMun=\n")
        f.write(f"UF=\n")
        f.write(f"CEP=\n")
        f.write(f"cPais=1058\n")
        f.write(f"xPais=BRASIL\n")
        f.write(f"Fone=\n\n")

        # ------------------- Produtos -------------------
        for i, prod in enumerate(getattr(self, "valoresDosItens", []), start=1):
            idx = str(i).zfill(3)
            
            f.write(f"[Produto{idx}]\n")
            f.write(f"cProd={prod.get('codigo','')}\n")
            f.write(f"xProd={prod.get('descricao','')}\n")
            f.write(f"NCM={prod.get('ncm','')}\n")
            f.write(f"CFOP={prod.get('cfop','')}\n")
            f.write(f"uCom={prod.get('unidade','')}\n")
            f.write(f"qCom={prod.get('quantidade','')}\n")
            f.write(f"vUnCom={prod.get('valor_unitario','')}\n")
            f.write(f"vProd={prod.get('valor_total','')}\n")
            f.write(f"indTot=1\n\n")
            
            f.write(f"[ICMS{idx}]\n")
            f.write(f"CSOSN={prod.get('csosn','')}\n")
            f.write(f"orig={prod.get('origem','')}\n")
            f.write(f"CST={prod.get('cst','')}\n")
            f.write(f"vBC={prod.get('bc_icms','')}\n")
            f.write(f"pICMS={prod.get('aliq_icms','')}\n")
            f.write(f"vICMS={prod.get('valor_icms','')}\n\n")
            
            f.write(f"[PIS{idx}]\n")
            f.write(f"CST={prod.get('cst_pis','')}\n")
            f.write(f"vBC={prod.get('bc_pis','')}\n")
            f.write(f"pPIS={prod.get('aliq_pis','')}\n")
            f.write(f"vPIS={prod.get('valor_pis','')}\n\n")
            
            f.write(f"[COFINS{idx}]\n")
            f.write(f"CST={prod.get('cst_cofins','')}\n")
            f.write(f"vBC={prod.get('bc_cofins','')}\n")
            f.write(f"pCOFINS={prod.get('aliq_cofins','')}\n")
            f.write(f"vCOFINS={prod.get('valor_cofins','')}\n\n")

        # ------------------- Total -------------------
        f.write("[Total]\n")
        f.write(f"vProd={self.valorTotalProdutos.get()}\n")
        f.write(f"vNF={self.valorLiquido.get()}\n")
        f.write(f"vFrete={self.totalFrete.get()}\n")
        f.write(f"vSeg={self.totalSeguro.get()}\n")
        f.write(f"vDesc={self.totalDesconto.get()}\n")
        f.write(f"vOutro={self.outrasDespesas.get()}\n")
        f.write(f"vICMS={self.valorICMS.get()}\n")
        f.write(f"vIPI={self.totalIPI.get()}\n")
        f.write(f"vPIS={self.totalPIS.get()}\n")
        f.write(f"vCOFINS={self.totalCOFINS.get()}\n\n")

        # ------------------- Transporte -------------------
        f.write("[Transportador]\n")
        f.write("modFrete=9\n\n")

        # ------------------- Pagamento -------------------
        f.write("[pag001]\n")
        f.write("tpag=01\n")
        f.write(f"vPag={self.valorLiquido.get()}\n\n")

        # Finaliza o comando ACBr
        f.write('"\n,1,1, , ,1)')

# 1ª executado
def criaTXT_ACBr(self, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        
        # ------------------- Identificacao -------------------
        f.write("[Identificacao]\n")
        f.write(f"cNF=\n")  # Código aleatório de 8 dígitos - você pode gerar se quiser
        f.write(f"natOp={self.variavelNatureza.get()}\n")
        f.write(f"indPag=0\n")
        f.write(f"mod=55\n")
        f.write(f"serie={self.variavelSerieDaNota.get()}\n")
        f.write(f"nNF={self.variavelNumeroDaNota.get()}\n")
        f.write(f"dhEmi={self.variavelDataDocumento.get()} {self.variavelHoraEntradaSaida.get()}\n")
        f.write(f"tpNF={self.variavelEntradaOuSaida.get()}\n")
        f.write(f"idDest=1\n")
        f.write(f"tpAmb=2\n")
        f.write(f"tpImp=1\n")
        f.write(f"tpEmis=1\n")
        f.write(f"finNFe=0\n")
        f.write(f"indFinal=0\n")
        f.write(f"indPres=9\n")
        f.write(f"procEmi=0\n")
        f.write(f"verProc=Sistema Python\n\n")

        # ------------------- Emitente -------------------
        f.write("[Emitente]\n")
        f.write(f"CNPJCPF={self.variavelCNPJRazaoSocialEmitente.get()}\n")
        f.write(f"xNome={self.variavelRazaoSocialEmitente.get()}\n")
        f.write(f"xFant=\n")
        f.write(f"IE=\n")
        f.write(f"xLgr=\n")
        f.write(f"nro=\n")
        f.write(f"xBairro=\n")
        f.write(f"cMun=\n")
        f.write(f"xMun=\n")
        f.write(f"UF=\n")
        f.write(f"CEP=\n")
        f.write(f"cPais=1058\n")
        f.write(f"xPais=BRASIL\n")
        f.write(f"Fone=\n\n")

        # ------------------- Destinatario -------------------
        f.write("[Destinatario]\n")
        f.write(f"CNPJCPF={self.variavelCNPJRazaoSocialRemetente.get()}\n")
        f.write(f"xNome={self.variavelRazaoSocialRemetente.get()}\n")
        f.write(f"indIEDest=3\n")
        f.write(f"IE=\n")
        f.write(f"xLgr=\n")
        f.write(f"nro=\n")
        f.write(f"xBairro=\n")
        f.write(f"cMun=\n")
        f.write(f"xMun=\n")
        f.write(f"UF=\n")
        f.write(f"CEP=\n")
        f.write(f"cPais=1058\n")
        f.write(f"xPais=BRASIL\n")
        f.write(f"Fone=\n\n")

        # ------------------- Produtos e Tributos -------------------
        produtos_completos = []
        for i, prod_basico in enumerate(getattr(self, "valoresDosItens", []), start=1):
            tributacao = {}
            if hasattr(self, "dadosProduto") and (i-1) < len(self.dadosProduto):
                tributacao = self.dadosProduto[i-1]
            produto_final = {**prod_basico, **tributacao}
            produtos_completos.append(produto_final)

            idx = str(i).zfill(3)

            # Produto
            f.write(f"[Produto{idx}]\n")
            f.write(f"cProd={produto_final.get('codigo','')}\n")
            f.write(f"xProd={produto_final.get('descricao','')}\n")
            f.write(f"NCM={produto_final.get('ncm','')}\n")
            f.write(f"CFOP={produto_final.get('cfop','')}\n")
            f.write(f"uCom={produto_final.get('unidade','')}\n")
            f.write(f"qCom={produto_final.get('quantidade','')}\n")
            f.write(f"vUnCom={produto_final.get('valor_unitario','')}\n")
            f.write(f"vProd={produto_final.get('valor_total','')}\n")
            f.write(f"indTot=1\n\n")

            # ICMS
            f.write(f"[ICMS{idx}]\n")
            f.write(f"CSOSN={produto_final.get('csosn','')}\n")
            f.write(f"orig={produto_final.get('origem','')}\n")
            f.write(f"CST={produto_final.get('cst','')}\n")
            f.write(f"vBC={produto_final.get('bc_icms','')}\n")
            f.write(f"pICMS={produto_final.get('aliq_icms','')}\n")
            f.write(f"vICMS={produto_final.get('valor_icms','')}\n\n")

            # PIS
            f.write(f"[PIS{idx}]\n")
            f.write(f"CST={produto_final.get('cst_pis','')}\n")
            f.write(f"vBC={produto_final.get('bc_pis','')}\n")
            f.write(f"pPIS={produto_final.get('aliq_pis','')}\n")
            f.write(f"vPIS={produto_final.get('valor_pis','')}\n\n")

            # COFINS
            f.write(f"[COFINS{idx}]\n")
            f.write(f"CST={produto_final.get('cst_cofins','')}\n")
            f.write(f"vBC={produto_final.get('bc_cofins','')}\n")
            f.write(f"pCOFINS={produto_final.get('aliq_cofins','')}\n")
            f.write(f"vCOFINS={produto_final.get('valor_cofins','')}\n\n")

        # ------------------- Total -------------------
        f.write("[Total]\n")
        f.write(f"vProd={self.valorTotalProdutos.get()}\n")
        f.write(f"vNF={self.valorLiquido.get()}\n")
        f.write(f"vFrete={self.totalFrete.get()}\n")
        f.write(f"vSeg={self.totalSeguro.get()}\n")
        f.write(f"vDesc={self.totalDesconto.get()}\n")
        f.write(f"vOutro={self.outrasDespesas.get()}\n")
        f.write(f"vICMS={self.valorICMS.get()}\n")
        f.write(f"vIPI={self.totalIPI.get()}\n")
        f.write(f"vPIS={self.totalPIS.get()}\n")
        f.write(f"vCOFINS={self.totalCOFINS.get()}\n\n")

# 2ª executado
def criaXML_ACBr(self, nome_arquivo):
    """
    NFe 4.00 (Homologação)
    - Evita 225: ordem correta de tags em <prod> e campos obrigatórios.
    - Evita 209: IE do emitente obrigatória, numérica e obtida com segurança (sem depender do atributo existir).
    - Evita 232: destinatário com indIEDest/IE consistentes (padrão: ISENTO).
    - Simples Nacional: ICMS via ICMSSN102 (CSOSN=102).
    - PIS/COFINS mínimos (PISNT/COFINSNT).
    """
    import datetime, random, re
    from xml.dom.minidom import Document

    # ---------------- Helpers ----------------
    def only_digits(s): return re.sub(r"\D", "", str(s or ""))

    def txt(tag, val, parent):
        el = doc.createElement(tag)
        el.appendChild(doc.createTextNode(str(val)))
        parent.appendChild(el)
        return el

    def fmt2(x):  return f"{float(str(x).replace(',', '.')):.2f}"
    def fmt4(x):  return f"{float(str(x).replace(',', '.')):.4f}"
    def fmt10(x): return f"{float(str(x).replace(',', '.')):.10f}"

    # ---------------- Emitente (preencha IE real se quiser fixar aqui) ----------------
    EMIT = {
        "CNPJ": "00995044000107",                  # 14 dígitos
        "xNome": "NUTRIGEL DISTRIBUIDORA EIRELI",
        "xLgr": "R DOUTOR OSCAR DA CUNHA",
        "nro": "126",
        "xBairro": "FABRICAS",
        "cMun": "3162500",                         # IBGE São João del-Rei
        "xMun": "SAO JOAO DEL REI",
        "UF": "MG",
        "CEP": "36301194",
        "cPais": "1058",
        "xPais": "BRASIL",
        "fone": "3233713382",
        "IE": "6259569630086",  # <- se quiser, coloque a IE verdadeira aqui como string numérica; senão pegamos da UI
    }

    # ---------------- Raiz ----------------
    doc = Document()
    NFe = doc.createElement("NFe")
    NFe.setAttribute("xmlns", "http://www.portalfiscal.inf.br/nfe")
    doc.appendChild(NFe)

    infNFe = doc.createElement("infNFe")
    infNFe.setAttribute("versao", "4.00")
    NFe.appendChild(infNFe)

    # ---------------- Chave de acesso ----------------
    cUF = getattr(self, "cUF", "31")  # MG
    ano_mes = datetime.datetime.now().strftime("%y%m")
    cnpj_emit = only_digits(EMIT["CNPJ"]).zfill(14)
    mod = "55"

    # série
    try:
        serie_raw = self.serie.get()
    except Exception:
        serie_raw = getattr(self, "serie", "1")
    serie_xml = str(max(1, int(str(serie_raw or "1"))))
    serie_key = serie_xml.zfill(3)

    # número
    try:
        nNF_raw = self.nNF.get()
    except Exception:
        nNF_raw = getattr(self, "nNF", "1")
    nNF_xml = str(int(str(nNF_raw or "1")))
    nNF_key = nNF_xml.zfill(9)

    tpEmis = "1"
    cNF = str(random.randint(10000000, 99999999))
    chave_sem_dv = cUF + ano_mes + cnpj_emit + mod + serie_key + nNF_key + tpEmis + cNF

    def calc_dv(ch):
        pesos = [2,3,4,5,6,7,8,9]; soma = 0
        for i, d in enumerate(reversed(ch)):
            soma += int(d) * pesos[i % len(pesos)]
        dv = 11 - (soma % 11)
        return "0" if dv >= 10 else str(dv)

    dv = calc_dv(chave_sem_dv)
    infNFe.setAttribute("Id", f"NFe{chave_sem_dv}{dv}")

    # ---------------- ide ----------------
    ide = doc.createElement("ide"); infNFe.appendChild(ide)
    now_iso = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")
    for k, v in [
        ("cUF", cUF),
        ("cNF", cNF),
        ("natOp", (self.naturezaOperacao.get() if hasattr(self, "naturezaOperacao") and hasattr(self.naturezaOperacao, "get")
                   else getattr(self, "naturezaOperacao", "VENDA")) or "VENDA"),
        ("mod", mod),
        ("serie", serie_xml),
        ("nNF", nNF_xml),
        ("dhEmi", now_iso),
        ("tpNF", "1"),
        ("idDest", "1"),
        ("cMunFG", EMIT["cMun"]),
        ("tpImp", "1"),
        ("tpEmis", tpEmis),
        ("cDV", dv),
        ("tpAmb", "2"),
        ("finNFe", "1"),
        ("indFinal", "1"),
        ("indPres", "1"),
        ("procEmi", "0"),
        ("verProc", "MeuSistema_1.0"),
    ]:
        txt(k, v, ide)

    # ---------------- emit ----------------
    emit = doc.createElement("emit")
    infNFe.appendChild(emit)

    txt("CNPJ", cnpj_emit, emit)
    txt("xNome", EMIT["xNome"], emit)
    txt("xFant", EMIT["xNome"], emit)

    # Endereço do emitente
    enderEmit = doc.createElement("enderEmit")
    emit.appendChild(enderEmit)
    for k, v in [
        ("xLgr", EMIT["xLgr"]), ("nro", EMIT["nro"]), ("xBairro", EMIT["xBairro"]),
        ("cMun", EMIT["cMun"]), ("xMun", EMIT["xMun"]), ("UF", EMIT["UF"]),
        ("CEP", EMIT["CEP"]), ("cPais", EMIT["cPais"]), ("xPais", EMIT["xPais"]),
        ("fone", EMIT["fone"]),
    ]:
        txt(k, v, enderEmit)

    # ▼ COLE AQUI (IE do emitente)
    ie_emit = None
    if hasattr(self, "inscricaoEstadualEmitente"):
        try:
            ie_emit = self.inscricaoEstadualEmitente.get()
        except Exception:
            ie_emit = getattr(self, "inscricaoEstadualEmitente", None)
    if not ie_emit:
        ie_emit = EMIT["IE"]  # caso tenha definido acima

    ie_emit = only_digits(ie_emit)
    if not ie_emit:
        # Melhor falhar aqui do que tomar 209 no SEFAZ
        raise ValueError("IE do emitente ausente. Defina a IE real (apenas números) em self.inscricaoEstadualEmitente ou EMIT['IE'].")

    txt("IE", ie_emit, emit)   # <-- ANTES do CRT
    txt("CRT", "1", emit)      # Simples Nacional

    # ---------------- dest (Homologação) ----------------
    xNomeDest = "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL"
    cnpj_dest = cnpj_emit  # CNPJ válido só para passar validação em homologação
    dest = doc.createElement("dest")
    infNFe.appendChild(dest)

    txt("CNPJ", only_digits(cnpj_dest).zfill(14), dest)
    txt("xNome", xNomeDest, dest)

    # Endereço do destinatário
    enderDest = doc.createElement("enderDest")
    dest.appendChild(enderDest)
    for k, v in [
        ("xLgr", EMIT["xLgr"]), ("nro", EMIT["nro"]), ("xBairro", EMIT["xBairro"]),
        ("cMun", EMIT["cMun"]), ("xMun", EMIT["xMun"]), ("UF", EMIT["UF"]),
        ("CEP", EMIT["CEP"]), ("cPais", EMIT["cPais"]), ("xPais", EMIT["xPais"]),
    ]:
        txt(k, v, enderDest)

    # ▼▼▼ COLE ESTE BLOCO AQUI ▼▼▼

    # Homologação: tratar destinatário como NÃO CONTRIBUINTE (indIEDest=9)
    # txt("indIEDest", "1", dest)
    # txt("IE", ie_emit, dest)

    # Garantir que NENHUMA tag <IE> fique no destinatário (evita 232/225)
    txt("indIEDest", "1", dest)

    # Use a MESMA IE numérica que você já usou no <emit> (ex.: a variável ie_emit)
    txt("IE", ie_emit, dest)

    # ▲▲▲ FIM DO BLOCO ▲▲▲

    # ---------------- det/prod ----------------
    total_vProd = 0.0

    def add_item(idx, prod_dict):
        nonlocal total_vProd
        det = doc.createElement("det"); det.setAttribute("nItem", str(idx)); infNFe.appendChild(det)

        prod = doc.createElement("prod"); det.appendChild(prod)

        cProd = prod_dict.get("codigo", f"P{idx}")
        cEAN = prod_dict.get("ean", "") or "SEM GTIN"
        xProd = prod_dict.get("descricao", "PRODUTO")
        NCM = prod_dict.get("ncm", "00000000")
        CFOP = prod_dict.get("cfop", "5102")
        uCom = prod_dict.get("unidade", "UN")
        qCom = prod_dict.get("quantidade", 1)
        vUnCom = prod_dict.get("valorUnitario", prod_dict.get("valor_unitario", 0))
        vProd_val = prod_dict.get("valorTotal", float(qCom) * float(vUnCom))
        cEANTrib = prod_dict.get("ean_trib", "") or "SEM GTIN"
        uTrib = uCom; qTrib = qCom; vUnTrib = vUnCom

        for k, v in [
            ("cProd", cProd),
            ("cEAN", cEAN),
            ("xProd", xProd),
            ("NCM", NCM),
            ("CFOP", CFOP),
            ("uCom", uCom),
            ("qCom", fmt4(qCom)),
            ("vUnCom", fmt10(vUnCom)),
            ("vProd", fmt2(vProd_val)),
            ("cEANTrib", cEANTrib),
            ("uTrib", uTrib),
            ("qTrib", fmt4(qTrib)),
            ("vUnTrib", fmt10(vUnTrib)),
            ("indTot", "1"),
        ]:
            txt(k, v, prod)

        try: total_vProd += float(str(vProd_val).replace(",", "."))
        except Exception: pass

        # Impostos
        imposto = doc.createElement("imposto"); det.appendChild(imposto)

        ICMS = doc.createElement("ICMS"); imposto.appendChild(ICMS)
        ICMSSN102 = doc.createElement("ICMSSN102"); ICMS.appendChild(ICMSSN102)
        txt("orig", "0", ICMSSN102); txt("CSOSN", "102", ICMSSN102)

        PIS = doc.createElement("PIS"); imposto.appendChild(PIS)
        PISNT = doc.createElement("PISNT"); PIS.appendChild(PISNT)
        txt("CST", "07", PISNT)

        COFINS = doc.createElement("COFINS"); imposto.appendChild(COFINS)
        COFINSNT = doc.createElement("COFINSNT"); COFINS.appendChild(COFINSNT)
        txt("CST", "07", COFINSNT)

    itens = getattr(self, "valoresDosItens", [])
    if isinstance(itens, list) and itens:
        for i, p in enumerate(itens, start=1): add_item(i, p or {})
    else:
        add_item(1, {
            "codigo": "0001", "descricao": "PRODUTO TESTE",
            "ncm": "00000000", "cfop": "5102", "unidade": "UN",
            "quantidade": 1, "valorUnitario": 1.00, "valorTotal": 1.00,
            "ean": "SEM GTIN", "ean_trib": "SEM GTIN",
        })

    # ---------------- total/ICMSTot ----------------
    total = doc.createElement("total"); infNFe.appendChild(total)
    ICMSTot = doc.createElement("ICMSTot"); total.appendChild(ICMSTot)
    for k, v in [
        ("vBC", "0.00"), ("vICMS", "0.00"), ("vICMSDeson", "0.00"),
        ("vFCP", "0.00"), ("vBCST", "0.00"), ("vST", "0.00"),
        ("vFCPST", "0.00"), ("vFCPSTRet", "0.00"),
        ("vProd", fmt2(total_vProd)),
        ("vFrete", "0.00"), ("vSeg", "0.00"), ("vDesc", "0.00"),
        ("vII", "0.00"), ("vIPI", "0.00"), ("vIPIDevol", "0.00"),
        ("vPIS", "0.00"), ("vCOFINS", "0.00"),
        ("vOutro", "0.00"), ("vNF", fmt2(total_vProd)),
        ("vTotTrib", "0.00"),
    ]: txt(k, v, ICMSTot)

    # ---------------- transp ----------------
    transp = doc.createElement("transp"); infNFe.appendChild(transp)
    txt("modFrete", "9", transp)

    # ---------------- pag ----------------
    pag = doc.createElement("pag"); infNFe.appendChild(pag)
    detPag = doc.createElement("detPag"); pag.appendChild(detPag)
    txt("tPag", "01", detPag)
    txt("vPag", fmt2(total_vProd), detPag)

    # ---------------- infAdic ----------------
    infAdic = doc.createElement("infAdic"); infNFe.appendChild(infAdic)
    txt("infCpl", "DOCUMENTO EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL", infAdic)

    # ---------------- salvar ----------------
    with open(nome_arquivo, "wb") as f:
        f.write(doc.toprettyxml(indent="  ", encoding="utf-8"))

# 3ª executado
def gerarEnvioLote(self, xml_assinado_path="arquivos/NotaFiscal/base_assinado.xml", output_path="arquivos/NotaFiscal/envio_lote.xml"):
    """Gera o XML de envio de lote (enviNFe) para envio ao WebService"""
    
    # Carrega o XML assinado
    with open(xml_assinado_path, "r", encoding="utf-8") as f:
        xml_content = f.read()
    
    nfe_xml = minidom.parseString(xml_content)
    nfe_node = nfe_xml.documentElement  # aqui pega diretamente o <NFe>
    
    doc = Document()
    
    # Elemento raiz
    enviNFe = doc.createElement("enviNFe")
    enviNFe.setAttribute("xmlns", "http://www.portalfiscal.inf.br/nfe")
    enviNFe.setAttribute("versao", "4.00")
    doc.appendChild(enviNFe)
    
    # ID do lote
    idLote = doc.createElement("idLote")
    idLote.appendChild(doc.createTextNode(str(random.randint(100000000, 999999999))))
    enviNFe.appendChild(idLote)
    
    # Indicador síncrono
    indSinc = doc.createElement("indSinc")
    indSinc.appendChild(doc.createTextNode("1"))
    enviNFe.appendChild(indSinc)
    
    # Insere o nó <NFe> assinado diretamente
    enviNFe.appendChild(doc.importNode(nfe_node, True))
    
    # Salva o arquivo
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(doc.toprettyxml(indent="  "))
    
    print(f"Arquivo de lote gerado em: {output_path}")


def get_cert_and_key_from_pfx(pfx_path, pfx_password):
    """Carrega o .pfx e gera arquivos temporários .pem e .key"""
    with open(pfx_path, "rb") as f:
        pfx_data = f.read()

    # Carrega chave privada + certificado público
    private_key, certificate, _ = load_key_and_certificates(pfx_data, pfx_password.encode())

    # Arquivos temporários
    cert_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
    key_file = tempfile.NamedTemporaryFile(delete=False, suffix=".key")

    # Escreve o certificado
    cert_file.write(certificate.public_bytes(Encoding.PEM))
    cert_file.flush()

    # Escreve a chave privada
    key_file.write(private_key.private_bytes(
        Encoding.PEM,
        PrivateFormat.TraditionalOpenSSL,
        NoEncryption()
    ))
    key_file.flush()

    return cert_file.name, key_file.name




def gerarNFe(self):
    print("chegou no gerarNfe")
    criaTXT_ACBr(self, "arquivos/NotaFiscal/base.txt")
    criaXML_ACBr(self, "arquivos/NotaFiscal/base.xml")
    criaComandoACBr(self, "arquivos/NotaFiscal/enviar.txt")

    # ============================
    # 1) Carregar CHAVE e CERT (PEM) para ASSINAR a NFe
    # ============================
    from cryptography.hazmat.primitives import serialization
    from cryptography import x509

    with open("arquivos/chave.key", "rb") as f:
        key_data = f.read()
    # Se sua chave estiver protegida por senha, passe password=b"SENHA_AQUI"
    private_key = serialization.load_pem_private_key(key_data, password=None)

    with open("arquivos/certificado.pem", "rb") as f:
        cert_pem = f.read()
    certificate = x509.load_pem_x509_certificate(cert_pem)

    # ============================
    # 2) Assinar o XML da NFe (rsa-sha1 / sha1 / c14n20010315)
    # ============================
    xml_tree = etree.parse("arquivos/NotaFiscal/base.xml")

    nfe_list = xml_tree.xpath('//*[local-name()="NFe" and ./*[local-name()="infNFe"]]')
    if not nfe_list:
        raise ValueError("Não encontrei <NFe> com filho <infNFe> no XML.")
    nfe = nfe_list[0]

    infNFe_list = nfe.xpath('./*[local-name()="infNFe"]')
    if not infNFe_list:
        raise ValueError("Não encontrei <infNFe> dentro de <NFe>.")
    infNFe = infNFe_list[0]

    nfe_id = infNFe.get("Id")
    if not nfe_id:
        raise ValueError('O atributo Id de <infNFe> é obrigatório (ex.: Id="NFe3519...").')

    signer = XMLSignerWithSHA1(
        method=methods.enveloped,
        signature_algorithm=SignatureMethod.RSA_SHA1,
        digest_algorithm=DigestAlgorithm.SHA1,
        c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
    )

    # Aqui usamos a CHAVE privada e o CERTIFICADO em PEM para assinar
    signed_nfe = signer.sign(
        nfe,
        key=private_key,
        cert=cert_pem,  # passa o certificado em PEM (bytes)
        reference_uri=f"#{nfe_id}",
    )

    nfe_parent = nfe.getparent()
    if nfe_parent is None:
        xml_tree._setroot(signed_nfe)
    else:
        nfe_parent.replace(nfe, signed_nfe)

    xml_tree.write(
        "arquivos/NotaFiscal/base_assinado.xml",
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    )
    print("✅ Assinado com rsa-sha1/sha1; c14n 20010315; Reference -> #Id de infNFe.")

    # ============================
    # 3) Montar enviNFe (lote)
    # ============================
    xml_tree_assinado = etree.parse("arquivos/NotaFiscal/base_assinado.xml")
    xml_root = xml_tree_assinado.getroot()  # <NFe> assinado

    enviNFe = etree.Element("enviNFe", xmlns="http://www.portalfiscal.inf.br/nfe", versao="4.00")

    idLote = etree.SubElement(enviNFe, "idLote")
    idLote.text = str(random.randint(10**14, 10**15 - 1))  # 15 dígitos

    indSinc = etree.SubElement(enviNFe, "indSinc")
    indSinc.text = "1"  # síncrono (pode retornar 104 direto)

    enviNFe.append(xml_root)

    tree_env = etree.ElementTree(enviNFe)
    tree_env.write("arquivos/NotaFiscal/enviNFe.xml", encoding="utf-8", xml_declaration=True)

    # Normaliza o conteúdo do enviNFe para colocar dentro do nfeDadosMsg (sem prólogo)
    xml_envio_content_bytes = open("arquivos/NotaFiscal/enviNFe.xml", "rb").read()
    _envi = etree.fromstring(xml_envio_content_bytes)
    xml_envio_content = etree.tostring(_envi, encoding="unicode", xml_declaration=False)

    # ============================
    # 4) Enviar para SEFAZ - Autorização 4.00 (robusto com QNames)
    # ============================
        # ============================
    # 4) Enviar para SEFAZ - Autorização 4.00 (apenas SOAP 1.2)
    # ============================


    SOAP12_NS = "http://www.w3.org/2003/05/soap-envelope"
    WSDL_AUT  = "http://www.portalfiscal.inf.br/nfe/wsdl/NFeAutorizacao4"

    # payload_elem já é o seu enviNFe normalizado:
    payload_elem = etree.fromstring(
        xml_envio_content if isinstance(xml_envio_content, (bytes, bytearray))
        else xml_envio_content.encode("utf-8")
    )

    SOAP12_NS = "http://www.w3.org/2003/05/soap-envelope"
    WSDL_AUT  = "http://www.portalfiscal.inf.br/nfe/wsdl/NFeAutorizacao4"

    def build_envelope_soap12_prefix(payload_el):
        # Usa Clark notation: "{NS}Tag"
        env  = etree.Element(f"{{{SOAP12_NS}}}Envelope", nsmap={"soap12": SOAP12_NS, "nfe4": WSDL_AUT})
        hdr  = etree.SubElement(env,  f"{{{SOAP12_NS}}}Header")
        cab  = etree.SubElement(hdr,  f"{{{WSDL_AUT}}}nfeCabecMsg")
        etree.SubElement(cab,        f"{{{WSDL_AUT}}}cUF").text = "31"
        etree.SubElement(cab,        f"{{{WSDL_AUT}}}versaoDados").text = "4.00"
        body = etree.SubElement(env, f"{{{SOAP12_NS}}}Body")
        op = etree.SubElement(body, f"{{{WSDL_AUT}}}nfeAutorizacaoLoteRequest")
        dados= etree.SubElement(op,  f"{{{WSDL_AUT}}}nfeDadosMsg")
        dados.append(payload_el)  # seu <enviNFe ... xmlns="http://www.portalfiscal.inf.br/nfe">
        return env

    url = "https://hnfe.fazenda.mg.gov.br/nfe2/services/NFeAutorizacao4"
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Accept": "application/soap+xml",
    }

    # Cert mTLS (PEM + KEY)
    cert = ("arquivos/certificado.pem", "arquivos/chave.key")

    # Monta o envelope (apenas 1 variação)
    env_elem = build_envelope_soap12_prefix(payload_elem)
    soap_envelope = etree.tostring(env_elem, encoding="utf-8", xml_declaration=True).decode("utf-8")
    open("arquivos/NotaFiscal/ultimo_envelope_enviado.xml", "w", encoding="utf-8").write(soap_envelope)

    # POST
    try:
        response = requests.post(
            url,
            data=soap_envelope.encode("utf-8"),
            headers=headers,
            cert=cert,
            verify=False,   # em prod, use cadeia ICP-Brasil
            timeout=30
        )
    except Exception as e:
        open("arquivos/NotaFiscal/ultimo_erro_envio.txt", "w", encoding="utf-8").write(f"{type(e).__name__}: {e}")
        print("❌ Erro no POST (mTLS/conexão). Detalhes em arquivos/NotaFiscal/ultimo_erro_envio.txt")
        return

    # Guarda a resposta
    open("arquivos/NotaFiscal/ultima_resposta_sefaz.xml", "w", encoding="utf-8").write(response.text or "")

    print("HTTP:", response.status_code, response.headers.get("Content-Type"))
    if not response.text:
        print("⚠️ Corpo da resposta vazio. Verifique Content-Type/headers no envio.")
        return

    # Se houver SOAP Fault, mostre e pare
    if "<Fault" in response.text or "<S:Fault" in response.text or "<soapenv:Fault" in response.text:
        print("📨 Resposta SEFAZ (envio) — primeiras linhas:")
        print(response.text[:1500])
        print("❌ SOAP Fault. Abra os arquivos de depuração para comparar com o WSDL:")
        print("   - arquivos/NotaFiscal/ultimo_envelope_enviado.xml")
        print("   - arquivos/NotaFiscal/ultima_resposta_sefaz.xml")
        return

    print("📨 Resposta SEFAZ (envio) — primeiras linhas:")
    print(response.text[:1500])
    # ============================
    # 5) Interpretar retorno da Autorização
    # ============================
    try:
        root = etree.fromstring(response.content)
    except Exception as e:
        print("❌ Resposta inválida:", e)
        return

    cStat_nodes = root.xpath('//*[local-name()="cStat"]')
    xMotivo_nodes = root.xpath('//*[local-name()="xMotivo"]')
    cStat = cStat_nodes[0].text if cStat_nodes else None
    xMotivo = xMotivo_nodes[0].text if xMotivo_nodes else None
    if cStat and xMotivo:
        print(f"↩️ cStat={cStat} - {xMotivo}")

    if cStat == "104":
        prot = root.xpath('//*[local-name()="protNFe"]')
        if prot:
            open("arquivos/NotaFiscal/protocolo_autorizacao.xml", "wb").write(etree.tostring(prot[0], encoding="utf-8", pretty_print=True))
            print("✅ Lote processado (104). Protocolo salvo em arquivos/NotaFiscal/protocolo_autorizacao.xml")
            return

    # Se tiver número do recibo, consulta no RetAutorizacao
    nRec_nodes = root.xpath('//*[local-name()="nRec"]')
    if not nRec_nodes:
        print("❌ Nenhum número de recibo retornado. Verifique os arquivos de depuração:")
        print("   - arquivos/NotaFiscal/ultimo_envelope_enviado.xml")
        print("   - arquivos/NotaFiscal/ultima_resposta_sefaz.xml")
        return

    nRec = nRec_nodes[0].text
    print("📌 Número do recibo:", nRec)

    # ============================
    # 6) Consultar recibo (RetAutorizacao4)
    # ============================
    url_ret = "https://hnfe.fazenda.mg.gov.br/nfe2/services/NFeRetAutorizacao4"
    cons = f'''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"
                 xmlns:nfe4="http://www.portalfiscal.inf.br/nfe/wsdl/NFeRetAutorizacao4">
  <soap12:Header>
    <nfe4:nfeCabecMsg>
      <nfe4:cUF>31</nfe4:cUF>
      <nfe4:versaoDados>4.00</nfe4:versaoDados>
    </nfe4:nfeCabecMsg>
  </soap12:Header>
  <soap12:Body>
    <nfe4:nfeRetAutorizacaoLoteRequest>
      <nfe4:nfeDadosMsg>
        <consReciNFe xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
          <tpAmb>2</tpAmb>
          <nRec>{nRec}</nRec>
        </consReciNFe>
      </nfe4:nfeDadosMsg>
    </nfe4:nfeRetAutorizacaoLoteRequest>
  </soap12:Body>
</soap12:Envelope>'''

    hdr_ret = {
        "Content-Type": 'application/soap+xml; charset=utf-8; action="http://www.portalfiscal.inf.br/nfe/wsdl/NFeRetAutorizacao4/nfeRetAutorizacaoLoteRequest"',
        "SOAPAction": "http://www.portalfiscal.inf.br/nfe/wsdl/NFeRetAutorizacao4/nfeRetAutorizacaoLoteRequest",
        "Accept": "application/soap+xml",
    }

    open("arquivos/NotaFiscal/ultimo_envelope_enviado_consulta.xml", "w", encoding="utf-8").write(cons)
    r2 = requests.post(url_ret, data=cons.encode("utf-8"), headers=hdr_ret, cert=cert, verify=False, timeout=30)
    open("arquivos/NotaFiscal/ultima_resposta_sefaz_consulta.xml", "w", encoding="utf-8").write(r2.text or "")

    print("📨 Resposta SEFAZ (consulta recibo) — primeiras linhas:")
    print((r2.text or "")[:1500])

    root2 = etree.fromstring(r2.content)
    cStat2 = (root2.xpath('//*[local-name()="cStat"]')[0].text) if root2.xpath('//*[local-name()="cStat"]') else "???"
    xMotivo2 = (root2.xpath('//*[local-name()="xMotivo"]')[0].text) if root2.xpath('//*[local-name()="xMotivo"]') else "???"
    print(f"🔎 RetAutorizacao: {cStat2} - {xMotivo2}")

    prot = root2.xpath('//*[local-name()="protNFe"]')
    if prot:
        open("arquivos/NotaFiscal/protocolo_autorizacao.xml", "wb").write(etree.tostring(prot[0], encoding="utf-8", pretty_print=True))
        print("✅ Protocolo salvo em arquivos/NotaFiscal/protocolo_autorizacao.xml")
    else:
        print("ℹ️ Sem <protNFe> no retorno da consulta. Veja os arquivos de depuração.")
