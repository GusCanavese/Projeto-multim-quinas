import xml.dom.minidom as minidom
import random
from datetime import datetime
import random
import datetime
from xml.dom.minidom import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from signxml import XMLSigner
from cryptography.hazmat.primitives.serialization import pkcs12
from signxml import XMLSigner
from cryptography.hazmat.primitives.serialization import pkcs12
from lxml import etree
from signxml import XMLSigner, methods

from brazilfiscalreport.danfe import Danfe

def gerarEnvioLote(self, xml_assinado_path="base_assinado.xml", output_path="envio_lote.xml"):
    """Gera o XML de envio de lote (enviNFe) para envio ao WebService"""
    
    # Carrega o XML assinado
    with open(xml_assinado_path, "r", encoding="utf-8") as f:
        xml_content = f.read()
    
    # Cria o documento XML do lote
    doc = Document()
    
    # Elemento raiz
    enviNFe = doc.createElement("enviNFe")
    enviNFe.setAttribute("xmlns", "http://www.portalfiscal.inf.br/nfe")
    enviNFe.setAttribute("versao", "4.00")
    doc.appendChild(enviNFe)
    
    # ID do lote (gerar um número aleatório)
    idLote = doc.createElement("idLote")
    idLote.appendChild(doc.createTextNode(str(random.randint(100000000, 999999999))))
    enviNFe.appendChild(idLote)
    
    # Indicador de sincronização (1 para sincrono)
    indSinc = doc.createElement("indSinc")
    indSinc.appendChild(doc.createTextNode("1"))
    enviNFe.appendChild(indSinc)
    
    # Adiciona a NFe assinada ao lote
    nfe = doc.createElement("NFe")
    nfe_xml = minidom.parseString(xml_content)
    nfe.appendChild(doc.importNode(nfe_xml.documentElement, True))
    enviNFe.appendChild(nfe)
    
    # Salva o arquivo
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(doc.toprettyxml(indent="  "))
    
    print(f"Arquivo de lote gerado em: {output_path}")

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

def criaXML_ACBr(self, nome_arquivo):
    doc = Document()

    # Elemento raiz
    nfeProc = doc.createElement("nfeProc")
    nfeProc.setAttribute("xmlns", "http://www.portalfiscal.inf.br/nfe")
    nfeProc.setAttribute("versao", "4.00")
    doc.appendChild(nfeProc)

    NFe = doc.createElement("NFe")
    nfeProc.appendChild(NFe)

    infNFe = doc.createElement("infNFe")
    NFe.appendChild(infNFe)

    # ================== Geração da chave de acesso ==================
    uf = getattr(self, "cUF", "35")  # exemplo SP
    ano_mes = datetime.datetime.now().strftime("%y%m")
    cnpj = getattr(self, "cnpjEmitente", "00000000000000").get() if hasattr(self, "cnpjEmitente") else "00000000000000"
    mod = "55"
    serie = str(getattr(self, "serie", "1").get() if hasattr(self, "serie") else "1").zfill(3)
    nNF = str(getattr(self, "nNF", "1").get() if hasattr(self, "nNF") else "1").zfill(9)
    cNF = str(random.randint(10000000, 99999999)).zfill(8)

    chave_sem_dv = uf + ano_mes + cnpj.zfill(14) + mod + serie + nNF + cNF
    dv = str(sum(int(d) for d in chave_sem_dv) % 11 % 10)  # cálculo simples de DV

    chave_acesso = chave_sem_dv + dv
    infNFe.setAttribute("Id", f"NFe{chave_acesso}")
    infNFe.setAttribute("versao", "4.00")

    # ================== ide ==================
    ide = doc.createElement("ide"); infNFe.appendChild(ide)
    elementos_ide = {
        "cUF": uf,
        "cNF": cNF,
        "natOp": getattr(self, "naturezaOperacao", "VENDA").get() if hasattr(self, "naturezaOperacao") else "VENDA",
        "mod": mod,
        "serie": serie,
        "nNF": nNF,
        "dhEmi": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00"),
        "tpNF": "1",
        "idDest": "1",
        "cMunFG": getattr(self, "cMunFG", "3550308"),  # SP São Paulo
        "tpImp": "1",
        "tpEmis": "1",
        "cDV": dv,
        "tpAmb": "2",  # homologação
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

    # ================== emit ==================
    emit = doc.createElement("emit"); infNFe.appendChild(emit)
    elementos_emit = {
        "CNPJ": cnpj,
        "xNome": getattr(self, "razaoSocialEmitente", "Empresa Exemplo LTDA").get() if hasattr(self, "razaoSocialEmitente") else "Empresa Exemplo LTDA",
        "IE": getattr(self, "inscricaoEstadualEmitente", "123456789").get() if hasattr(self, "inscricaoEstadualEmitente") else "123456789"
    }
    for k, v in elementos_emit.items():
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        emit.appendChild(el)

    # Endereço do emitente
    enderEmit = doc.createElement("enderEmit"); emit.appendChild(enderEmit)
    end_emit_dict = {
        "xLgr": "Rua Exemplo",
        "nro": "100",
        "xBairro": "Centro",
        "cMun": "3550308",
        "xMun": "São Paulo",
        "UF": "SP",
        "CEP": "01000000",
        "cPais": "1058",
        "xPais": "BRASIL",
        "fone": "11999999999"
    }
    for k, v in end_emit_dict.items():
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        enderEmit.appendChild(el)

    # ================== dest ==================
    dest = doc.createElement("dest"); infNFe.appendChild(dest)
    elementos_dest = {
        "CNPJ": getattr(self, "cnpjDestinatario", "11111111111111").get() if hasattr(self, "cnpjDestinatario") else "11111111111111",
        "xNome": getattr(self, "nomeDestinatario", "Cliente Teste").get() if hasattr(self, "nomeDestinatario") else "Cliente Teste",
        "indIEDest": "9"
    }
    for k, v in elementos_dest.items():
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        dest.appendChild(el)

    enderDest = doc.createElement("enderDest"); dest.appendChild(enderDest)
    end_dest_dict = {
        "xLgr": "Rua Cliente",
        "nro": "200",
        "xBairro": "Bairro Teste",
        "cMun": "3550308",
        "xMun": "São Paulo",
        "UF": "SP",
        "CEP": "02000000",
        "cPais": "1058",
        "xPais": "BRASIL",
        "fone": "1188888888"
    }
    for k, v in end_dest_dict.items():
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        enderDest.appendChild(el)

    # ================== Produtos ==================
    total_vProd = 0
    for i, prod in enumerate(getattr(self, "valoresDosItens", []), start=1):
        det = doc.createElement("det")
        det.setAttribute("nItem", str(i))
        infNFe.appendChild(det)

        prodEl = doc.createElement("prod"); det.appendChild(prodEl)
        campos_prod = {
            "cProd": prod.get("codigo", f"P{i}"),
            "xProd": prod.get("descricao", ""),
            "NCM": prod.get("ncm", "00000000"),
            "CFOP": prod.get("cfop", "5102"),
            "uCom": prod.get("unidade", "UN"),
            "qCom": prod.get("quantidade", "1"),
            "vUnCom": prod.get("valorUnitario", "0.00"),
            "vProd": prod.get("valorTotal", "0.00")
        }
        total_vProd += float(campos_prod["vProd"])
        for k, v in campos_prod.items():
            el = doc.createElement(k)
            el.appendChild(doc.createTextNode(str(v)))
            prodEl.appendChild(el)

    # ================== Totais ==================
    total = doc.createElement("total"); infNFe.appendChild(total)
    icmsTot = doc.createElement("ICMSTot"); total.appendChild(icmsTot)
    campos_totais = {
        "vBC": "0.00",
        "vICMS": "0.00",
        "vICMSDeson": "0.00",
        "vProd": f"{total_vProd:.2f}",
        "vFrete": str(getattr(self, "totalFrete", 0)),
        "vSeg": str(getattr(self, "totalSeguro", 0)),
        "vDesc": str(getattr(self, "totalDesconto", 0)),
        "vII": "0.00",
        "vIPI": "0.00",
        "vPIS": "0.00",
        "vCOFINS": "0.00",
        "vOutro": str(getattr(self, "outrasDespesas", 0)),
        "vNF": f"{total_vProd:.2f}"
    }
    for k, v in campos_totais.items():
        el = doc.createElement(k)
        el.appendChild(doc.createTextNode(str(v)))
        icmsTot.appendChild(el)

    # ================== Transporte ==================
    transp = doc.createElement("transp"); infNFe.appendChild(transp)
    modFrete = doc.createElement("modFrete")
    modFrete.appendChild(doc.createTextNode("9"))
    transp.appendChild(modFrete)

    # ================== Pagamento ==================
    pag = doc.createElement("pag"); infNFe.appendChild(pag)
    detPag = doc.createElement("detPag"); pag.appendChild(detPag)
    tPag = doc.createElement("tPag"); tPag.appendChild(doc.createTextNode("01"))
    detPag.appendChild(tPag)
    vPag = doc.createElement("vPag"); vPag.appendChild(doc.createTextNode(f"{total_vProd:.2f}"))
    detPag.appendChild(vPag)

    # ================== Salvando arquivo ==================
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(doc.toprettyxml(indent="  "))

def gerarNFe(self):
    print("chegou no gerarNfe")
    criaTXT_ACBr(self, "base.txt")
    criaXML_ACBr(self, "base.xml")
    criaComandoACBr(self, "NotaFiscal/EnviarComando/enviar.txt")  # Novo

    # Carregar certificado .pfx
    with open("arquivos/certificado.pfx", "rb") as f:
        pfx_data = f.read()

    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(pfx_data, b"nutri@00995")

    # Carregar XML da NFe
    xml_tree = etree.parse("base.xml")

    # Localizar nó <infNFe>
    infNFe = xml_tree.find(".//{http://www.portalfiscal.inf.br/nfe}infNFe")

    # Assinar o XML (nó infNFe)
    signer = XMLSigner(
        method=methods.enveloped,
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256",
        c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
    )
   
    signed_xml = signer.sign(infNFe, key=private_key, cert=[certificate])

    # Substituir o nó no XML original
    xml_tree.getroot().insert(0, signed_xml)

    # Salvar XML assinado
    with open("base_assinado.xml", "wb") as f:
        f.write(etree.tostring(xml_tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))

    print("XML assinado com sucesso!")




    # xml_file_path = "base.xml"   # seu XML de prévia

    # with open(xml_file_path, "r", encoding="utf-8") as f:
    #     xml_content = f.read()

    # danfe = Danfe(xml=xml_content)
    # danfe.output("danfe_preview.pdf")  # gera o PDF da DANFE


