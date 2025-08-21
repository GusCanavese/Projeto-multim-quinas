import re
import xml.dom.minidom as minidom
import datetime
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
    doc = Document()

    # Elemento raiz
    NFe = doc.createElement("NFe")
    NFe.setAttribute("xmlns", "http://www.portalfiscal.inf.br/nfe")
    doc.appendChild(NFe)

    infNFe = doc.createElement("infNFe")
    NFe.appendChild(infNFe)

    uf = getattr(self, "cUF", "31")
    ano_mes = datetime.datetime.now().strftime("%y%m")
    cnpj = getattr(self, "cnpjEmitente", "00000000000000").get() if hasattr(self, "cnpjEmitente") else "00000000000000"

    # serie e nNF: sem zeros à esquerda na TAG, com zeros na chave
    serie_raw = getattr(self, "serie", "1").get() if hasattr(self, "serie") else "1"
    serie_num = max(1, int(serie_raw))
    serie_xml = str(serie_num)
    serie_key = serie_xml.zfill(3)

    nNF_raw = getattr(self, "nNF", "1").get() if hasattr(self, "nNF") else "1"
    nNF_xml = str(int(nNF_raw))
    nNF_key = nNF_xml.zfill(9)

    mod = "55"
    tpEmis = "1"
    cNF = str(random.randint(10000000, 99999999))

    # chave sem DV (43 dígitos) + DV
    chave_sem_dv = uf + ano_mes + cnpj.zfill(14) + mod + serie_key + nNF_key + tpEmis + cNF

    def calcula_dv(chave):
        pesos = [2,3,4,5,6,7,8,9]
        soma = 0
        for i, d in enumerate(reversed(chave)):
            soma += int(d) * pesos[i % len(pesos)]
        resto = soma % 11
        dv = 11 - resto
        return "0" if dv >= 10 else str(dv)

    dv = calcula_dv(chave_sem_dv)
    chave_acesso = chave_sem_dv + dv

    # Atributos do infNFe
    infNFe.setAttribute("Id", f"NFe{chave_acesso}")
    infNFe.setAttribute("versao", "4.00")

    # =============== ide ===============
    ide = doc.createElement("ide")
    infNFe.appendChild(ide)
    elementos_ide = {
        "cUF": uf,
        "cNF": cNF,
        "natOp": getattr(self, "naturezaOperacao", "VENDA").get() if hasattr(self, "naturezaOperacao") else "VENDA",
        "mod": mod,
        "serie": serie_xml,
        "nNF": nNF_xml,
        "dhEmi": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00"),
        "tpNF": "1",
        "idDest": "1",
        "cMunFG": getattr(self, "cMunFG", "3106200"),
        "tpImp": "1",
        "tpEmis": "1",
        "cDV": dv,
        "tpAmb": "2",
        "finNFe": "1",
        "indFinal": "1",
        "indPres": "1",
        "procEmi": "0",
        "verProc": "MeuSistema_1.0"
    }
    for k, v in elementos_ide.items():
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        ide.appendChild(el)

    # =============== emit ===============
    emit = doc.createElement("emit")
    infNFe.appendChild(emit)
    for k in ["CNPJ", "xNome", "xFant"]:
        if k == "CNPJ":
            v = cnpj
        elif k == "xNome":
            v = getattr(self, "razaoSocialEmitente", "Empresa Exemplo LTDA").get() if hasattr(self, "razaoSocialEmitente") else "Empresa Exemplo LTDA"
        else:
            v = "Teste"
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        emit.appendChild(el)

    enderEmit = doc.createElement("enderEmit")
    emit.appendChild(enderEmit)
    end_emit_dict = {
        "xLgr": "Rua Exemplo",
        "nro": "100",
        "xBairro": "Centro",
        "cMun": "3106200",
        "xMun": "Belo Horizonte",
        "UF": "MG",
        "CEP": "30000000",
        "cPais": "1058",
        "xPais": "BRASIL",
        "fone": "3133333333"
    }
    for k, v in end_emit_dict.items():
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        enderEmit.appendChild(el)

    for k, v in {"IE": getattr(self, "inscricaoEstadualEmitente", "123456789").get() if hasattr(self, "inscricaoEstadualEmitente") else "123456789",
                 "CRT": "1"}.items():
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        emit.appendChild(el)

    # =============== dest ===============
    dest = doc.createElement("dest")
    infNFe.appendChild(dest)
    for k in ["CNPJ", "xNome"]:
        v = getattr(self, "cnpjDestinatario", "11111111111111").get() if (k=="CNPJ" and hasattr(self,"cnpjDestinatario")) else (
            getattr(self, "nomeDestinatario", "Cliente Teste").get() if (k=="xNome" and hasattr(self,"nomeDestinatario")) else ("11111111111111" if k=="CNPJ" else "Cliente Teste")
        )
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        dest.appendChild(el)

    enderDest = doc.createElement("enderDest")
    dest.appendChild(enderDest)
    end_dest_dict = {
        "xLgr": "Rua Cliente",
        "nro": "200",
        "xBairro": "Bairro Teste",
        "cMun": "3106200",
        "xMun": "Belo Horizonte",
        "UF": "MG",
        "CEP": "30000000",
        "cPais": "1058",
        "xPais": "BRASIL",
        "fone": "3133333333"
    }
    for k, v in end_dest_dict.items():
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        enderDest.appendChild(el)

    for k, v in {"indIEDest": "9", "email": "cliente@email.com"}.items():
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        dest.appendChild(el)

    # =============== det/prod ===============
    total_vProd = 0.0

    def add_produto(prod_dict, index):
        nonlocal total_vProd
        det = doc.createElement("det")
        det.setAttribute("nItem", str(index))
        infNFe.appendChild(det)

        prodEl = doc.createElement("prod")
        det.appendChild(prodEl)

        # ORDEM **OBRIGATÓRIA**
        seq = [
            ("cProd",    prod_dict.get("codigo", f"P{index}")),
            ("cEAN",     prod_dict.get("ean", "SEM GTIN") or "SEM GTIN"),
            ("xProd",    prod_dict.get("descricao", "Produto")),
            ("NCM",      prod_dict.get("ncm", "00000000")),
            # ("CEST",   prod_dict.get("cest","")),  # se tiver, insira aqui
            ("CFOP",     prod_dict.get("cfop", "5102")),
            ("uCom",     prod_dict.get("unidade", "UN")),
            ("qCom",     f"{float(prod_dict.get('quantidade', 1)):.4f}"),
            ("vUnCom",   f"{float(prod_dict.get('valorUnitario', prod_dict.get('valor_unitario', 0))) :.10f}"),
            ("vProd",    f"{float(prod_dict.get('valorTotal',  prod_dict.get('valor_total',   0))) :.2f}"),
            ("cEANTrib", prod_dict.get("ean_trib", "SEM GTIN") or "SEM GTIN"),
            ("uTrib",    prod_dict.get("unidade", "UN")),
            ("qTrib",    f"{float(prod_dict.get('quantidade', 1)):.4f}"),
            ("vUnTrib",  f"{float(prod_dict.get('valorUnitario', prod_dict.get('valor_unitario', 0))) :.10f}"),
            ("indTot",   "1"),
        ]
        vprod_value = 0.0
        for tag, valor in seq:
            el = doc.createElement(tag)
            el.appendChild(doc.createTextNode(str(valor).strip()))
            prodEl.appendChild(el)
            if tag == "vProd":
                try:
                    vprod_value = float(str(valor).replace(",", "."))
                except:
                    vprod_value = 0.0

        total_vProd += vprod_value

        # ====== impostos (mínimo para schema) ======
        imposto = doc.createElement("imposto")
        det.appendChild(imposto)

        icms = doc.createElement("ICMS")
        imposto.appendChild(icms)

        icms00 = doc.createElement("ICMS00")
        icms.appendChild(icms00)

        for k, v in {
            "orig": "0",
            "CST": "00",
            "modBC": "0",
            "vBC": "0.00",
            "pICMS": "0.00",
            "vICMS": "0.00"
        }.items():
            el = doc.createElement(k)
            el.appendChild(doc.createTextNode(v))
            icms00.appendChild(el)

    itens = getattr(self, "valoresDosItens", [])
    if itens:
        for i, prod in enumerate(itens, start=1):
            add_produto(prod, i)
    else:
        # Produto default também na ORDEM correta e com cEAN/cEANTrib
        add_produto({
            "codigo": "000",
            "descricao": "Produto Default",
            "ncm": "00000000",
            "cfop": "5102",
            "unidade": "UN",
            "quantidade": 1,
            "valorUnitario": 0.00,
            "valorTotal": 0.00,
            "ean": "SEM GTIN",
            "ean_trib": "SEM GTIN",
        }, 1)

    # =============== total ===============
    total = doc.createElement("total")
    infNFe.appendChild(total)

    icmsTot = doc.createElement("ICMSTot")
    total.appendChild(icmsTot)

    for k, v in {
        "vBC": "0.00",
        "vICMS": "0.00",
        "vICMSDeson": "0.00",
        "vFCP": "0.00",
        "vBCST": "0.00",
        "vST": "0.00",
        "vFCPST": "0.00",
        "vFCPSTRet": "0.00",
        "vProd": f"{total_vProd:.2f}",
        "vFrete": "0.00",
        "vSeg": "0.00",
        "vDesc": "0.00",
        "vII": "0.00",
        "vIPI": "0.00",
        "vIPIDevol": "0.00",
        "vPIS": "0.00",
        "vCOFINS": "0.00",
        "vOutro": "0.00",
        "vNF": f"{total_vProd:.2f}",
        "vTotTrib": "0.00"
    }.items():
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(v))
        icmsTot.appendChild(el)

    # =============== transp ===============
    transp = doc.createElement("transp")
    infNFe.appendChild(transp)
    modFrete = doc.createElement("modFrete")
    modFrete.appendChild(doc.createTextNode("9"))
    transp.appendChild(modFrete)

    # =============== pag ===============
    pag = doc.createElement("pag")
    infNFe.appendChild(pag)
    detPag = doc.createElement("detPag")
    pag.appendChild(detPag)
    tPag = doc.createElement("tPag")
    tPag.appendChild(doc.createTextNode("01"))
    detPag.appendChild(tPag)
    vPag = doc.createElement("vPag")
    vPag.appendChild(doc.createTextNode(f"{total_vProd:.2f}"))
    detPag.appendChild(vPag)

    # Salvar arquivo
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
    # 1. Carregar o certificado PFX
    # ============================
    with open("arquivos/certificado.pfx", "rb") as f:
        pfx_data = f.read()

    private_key, certificate, _ = load_key_and_certificates(
        pfx_data, b"nutri@00995"  # senha do PFX
    )

    # Criar arquivos temporários PEM e KEY
    cert_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
    key_file = tempfile.NamedTemporaryFile(delete=False, suffix=".key")

    cert_file.write(certificate.public_bytes(Encoding.PEM))
    key_file.write(private_key.private_bytes(
        Encoding.PEM,
        PrivateFormat.TraditionalOpenSSL,
        NoEncryption()
    ))
    cert_file.close()
    key_file.close()

    # ============================
    # 2. Assinar o XML da NFe
    # ============================

    xml_tree = etree.parse("arquivos/NotaFiscal/base.xml")

    # Localiza <NFe> e <infNFe> ignorando namespaces
    nfe_list = xml_tree.xpath('//*[local-name()="NFe" and ./*[local-name()="infNFe"]]')
    if not nfe_list:
        raise ValueError("Não encontrei <NFe> com filho <infNFe> no XML.")
    nfe = nfe_list[0]

    infNFe_list = nfe.xpath('./*[local-name()="infNFe"]')
    if not infNFe_list:
        raise ValueError("Não encontrei <infNFe> dentro de <NFe>.")
    infNFe = infNFe_list[0]

    # Id do infNFe (obrigatório)
    nfe_id = infNFe.get("Id")
    if not nfe_id:
        raise ValueError('O atributo Id de <infNFe> é obrigatório (ex.: Id="NFe3519...").')

    

    # Assinador com algoritmos exigidos pelo schema da NFe 4.00
    signer = XMLSignerWithSHA1(
        method=methods.enveloped,  # <Signature> dentro de <NFe>
        signature_algorithm=SignatureMethod.RSA_SHA1,  # URI rsa-sha1
        digest_algorithm=DigestAlgorithm.SHA1,         # URI sha1
        c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
    )

    signed_nfe = signer.sign(
        nfe,
        key=private_key,
        cert=[certificate],
        reference_uri=f"#{nfe_id}",  # referencia o Id do <infNFe>
    )

    # Substitui a árvore
    nfe_parent = nfe.getparent()
    if nfe_parent is None:
        xml_tree._setroot(signed_nfe)
    else:
        nfe_parent.replace(nfe, signed_nfe)

    # Salva sem mexer nos prefixos ds:
    xml_tree.write(
        "arquivos/NotaFiscal/base_assinado.xml",
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    )

    print("✅ Assinado com rsa-sha1/sha1, c14n 20010315; <Signature> em <NFe>; Reference -> #Id do infNFe.")

    # ============================
    # 3. Montar envelope enviNFe
    # ============================
    # Carregar o XML assinado
    xml_tree_assinado = etree.parse("arquivos/NotaFiscal/base_assinado.xml")
    xml_root = xml_tree_assinado.getroot()  # ← DEFINIR xml_root AQUI

    enviNFe = etree.Element("enviNFe", xmlns="http://www.portalfiscal.inf.br/nfe", versao="4.00")

    idLote = etree.SubElement(enviNFe, "idLote")
    idLote.text = str(random.randint(100000000000000, 999999999999999))

    indSinc = etree.SubElement(enviNFe, "indSinc")
    indSinc.text = "1"  # síncrono

    # Insere o nó <NFe> assinado
    enviNFe.append(xml_root)  # ← AGORA xml_root ESTÁ DEFINIDO

    # Salva o envelope de envio
    tree_env = etree.ElementTree(enviNFe)
    tree_env.write("arquivos/NotaFiscal/enviNFe.xml", encoding="utf-8", xml_declaration=True)
    # ============================
    # 4. Enviar para SEFAZ
    # ============================
    parser = etree.XMLParser(remove_blank_text=True)

    # enviNFe é o elemento já com <NFe> assinado dentro
    xml_envio_content = etree.tostring(
        enviNFe, encoding="utf-8", xml_declaration=False, pretty_print=False, with_tail=False
    ).decode("utf-8")

    xml_envio_content = re.sub(r">\s+<", "><", xml_envio_content.strip())

    # Criar o envelope SOAP adequado
    soap_envelope = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap12:Envelope xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">'
        '<soap12:Header>'
            '<nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NFeAutorizacao4">'
            '<cUF>31</cUF>'
            '<versaoDados>4.00</versaoDados>'
            '</nfeCabecMsg>'
        '</soap12:Header>'
        '<soap12:Body>'
            '<nfeAutorizacaoLote xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NFeAutorizacao4">'
            '<nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe">'
                + xml_envio_content +
            '</nfeDadosMsg>'
            '</nfeAutorizacaoLote>'
        '</soap12:Body>'
        '</soap12:Envelope>'
    )
    url = "https://hnfe.fazenda.mg.gov.br/nfe2/services/NFeAutorizacao4"
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "SOAPAction": "http://www.portalfiscal.inf.br/nfe/wsdl/NFeAutorizacao4/nfeAutorizacaoLote",  # opcional no SOAP 1.2
    }

    # Certificado A1 (já convertido em .pem e .key)
    cert = (cert_file.name, key_file.name)

    response = requests.post(url, data=soap_envelope.encode("utf-8"), headers=headers, cert=cert, verify=False)

   # --- ENVIO ---
    response = requests.post(
        url,
        data=soap_envelope.encode("utf-8"),
        headers=headers,
        cert=cert,
        verify=False
    )

    print("📨 Resposta SEFAZ (envio):")
    print(response.text)

    # Extrai número do recibo
    tree = etree.fromstring(response.content)
    nRec_nodes = tree.xpath('//ns:nRec', namespaces={'ns': 'http://www.portalfiscal.inf.br/nfe'})
    if not nRec_nodes:
        print("❌ Nenhum número de recibo retornado. Verifique se a nota foi aceita.")
        return

    nRec = nRec_nodes[0].text
    print("📌 Número do recibo:", nRec)

    # --- CONSULTA RECIBO ---
    soap_consulta = f"""
    <soap12:Envelope xmlns:soap12="http://www.w3.org/2003/05/soap-envelope" xmlns:nfe4="http://www.portalfiscal.inf.br/nfe/wsdl/NFeRetAutorizacao4">
    <soap12:Header>
        <nfe4:nfeCabecMsg>
        <nfe4:cUF>31</nfe4:cUF>
        <nfe4:versaoDados>4.00</nfe4:versaoDados>
        </nfe4:nfeCabecMsg>
    </soap12:Header>
    <soap12:Body>
        <nfe4:nfeRetAutorizacaoLote>
        <nfe4:nfeDadosMsg>
            <![CDATA[
            <consReciNFe xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
            <tpAmb>2</tpAmb>
            <nRec>{nRec}</nRec>
            </consReciNFe>
            ]]>
        </nfe4:nfeDadosMsg>
        </nfe4:nfeRetAutorizacaoLote>
    </soap12:Body>
    </soap12:Envelope>
    """

    url_consulta = "https://hnfe.fazenda.mg.gov.br/nfe2/services/NFeRetAutorizacao4"

    response_consulta = requests.post(
        url_consulta,
        data=soap_consulta.encode("utf-8"),
        headers={"Content-Type": "application/soap+xml; charset=utf-8"},
        cert=cert,
        verify=False
    )

    print("📨 Resposta SEFAZ (consulta recibo):")
    print(response_consulta.text)

    # Extrai código e motivo
    tree_consulta = etree.fromstring(response_consulta.content)
    cStat_nodes = tree_consulta.xpath('//ns:cStat', namespaces={'ns': 'http://www.portalfiscal.inf.br/nfe'})
    xMotivo_nodes = tree_consulta.xpath('//ns:xMotivo', namespaces={'ns': 'http://www.portalfiscal.inf.br/nfe'})

    cStat = cStat_nodes[0].text if cStat_nodes else "???"
    xMotivo = xMotivo_nodes[0].text if xMotivo_nodes else "???"

    print(f"✅ Status da NFe: {cStat} - {xMotivo}")