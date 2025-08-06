import random
from datetime import datetime
from lxml import etree
from pynfe.entidades import Emitente, Cliente, Produto, NotaFiscal
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoSefaz
import os
from OpenSSL import crypto

# ===================================================================================
# CONFIGURAÇÕES (ALTERE COM SEUS DADOS)
# ===================================================================================
CERTIFICADO_PATH = "arquivos/certificado.pfx"
CERTIFICADO_SENHA = "nutri@00995"
UF = "MG"  # UF real do emitente
HOMOLOGACAO = True  # True para homologação, False para produção

# Dicionário com os códigos de UF do IBGE
CODIGO_UF = {
    'RO': '11', 'AC': '12', 'AM': '13', 'RR': '14', 'PA': '15', 'AP': '16', 'TO': '17',
    'MA': '21', 'PI': '22', 'CE': '23', 'RN': '24', 'PB': '25', 'PE': '26', 'AL': '27', 'SE': '28', 'BA': '29',
    'MG': '31', 'ES': '32', 'RJ': '33', 'SP': '35',
    'PR': '41', 'SC': '42', 'RS': '43',
    'MS': '50', 'MT': '51', 'GO': '52', 'DF': '53'
}

def gerar_chave_acesso(cnpj, serie, numero_nf, uf_code):
    """Gera a chave de acesso da NF-e."""
    data_emissao = datetime.now().strftime('%y%m')
    tipo_emissao = '1'
    codigo_numerico = str(random.randint(10000000, 99999999))
    
    chave_sem_dv = f"{uf_code}{data_emissao}{cnpj}{55:02d}{int(serie):03d}{int(numero_nf):09d}{tipo_emissao}{codigo_numerico}"
    
    # Cálculo do Dígito Verificador
    soma = 0
    peso = 2
    for char in reversed(chave_sem_dv):
        soma += int(char) * peso
        peso += 1
        if peso > 9:
            peso = 2
    
    resto = soma % 11
    dv = 0 if resto in [0, 1] else 11 - resto

    return f"{chave_sem_dv}{dv}"

def emitir_nfe():
    print("Iniciando processo de emissão de NF-e...")

    # 1. DADOS DO EMITENTE (SUA EMPRESA)
    emitente = Emitente(
        endereco_municipio='SAO JOAO DEL REI',
        endereco_codigo_municipio='3162500',
        razao_social='NUTRIGEL DISTRIBUIDORA EIRELI',
        nome_fantasia='NUTRIGEL DISTRIBUIDORA',
        cnpj='00995044000107',
        inscricao_estadual='6259569630086',  # IE real de MG
        endereco_logradouro='R DOUTOR OSCAR DA CUNHA',
        endereco_numero='126',
        endereco_complemento='LETRA B',
        endereco_bairro='FABRICAS',
        endereco_uf='MG',
        endereco_cep='36301194',
        endereco_pais='1058',
        telefone='3233713382',
        codigo_regime_tributario='1',  # 1=Simples Nacional
    )

    # 2. DADOS DO CLIENTE (DESTINATÁRIO)
    cliente = Cliente(
        razao_social='CLIENTE DE TESTE LTDA',
        tipo_documento='CNPJ',
        numero_documento='98765432000195',
        indicador_ie=9,  # 9=Não contribuinte
        endereco_logradouro='RUA DO CLIENTE',
        endereco_numero='456',
        endereco_bairro='CENTRO',
        endereco_municipio='Rio de Janeiro',
        endereco_uf='RJ',
        endereco_cep='20010010',
        endereco_pais='1058',
        email='cliente@email.com'
    )

    # 3. DADOS DO PRODUTO
    valor_produto = 150.75
    produto_1 = Produto(
        item=1,
        codigo='PROD-001',
        descricao='PRODUTO DE TESTE 1',
        ncm='84715010',
        cfop='5102',
        unidade_comercial='UN',
        quantidade_comercial=1.0,
        valor_unitario_comercial=valor_produto,
        unidade_tributavel='UN',
        quantidade_tributavel=1.0,
        valor_unitario_tributavel=valor_produto,
        valor_total=valor_produto,
        icms_modalidade='00',
        icms_origem=0,
        pis_modalidade='01',
        cofins_modalidade='01',
    )

    # 4. MONTAGEM DA NOTA FISCAL
    serie_nf = '1'
    numero_nf = str(random.randint(10000, 99999))  # Número aleatório para testes
    uf_code = CODIGO_UF[UF]
    chave_acesso = gerar_chave_acesso(emitente.cnpj, serie_nf, numero_nf, uf_code)

    nota_fiscal = NotaFiscal(
        emitente=emitente,
        cliente=cliente,
        uf=UF,
        natureza_operacao='VENDA DE MERCADORIA',
        forma_pagamento=1,
        modelo='55',
        serie=serie_nf,
        numero_nf=numero_nf,
        data_emissao=datetime.now(),
        data_saida_entrada=datetime.now(),
        tipo_documento=1,
        municipio_fato_gerador=CODIGO_UF[emitente.endereco_uf],
        tipo_impressao_danfe=1,
        forma_emissao='1',
        ambiente=2 if HOMOLOGACAO else 1,
        finalidade_emissao='1',
        processo_emissao='0',
        versao_processo_emissao='1.0',
        indicador_presenca=1,
        informacoes_adicionais_contribuinte='Documento emitido por ME ou EPP optante pelo Simples Nacional.',
        produtos=[produto_1],
        chave_acesso=chave_acesso,
        valor_total_produtos=valor_produto,
        valor_total=valor_produto,
        valor_icms=0.00,
        valor_pis=0.00,
        valor_cofins=0.00,
    )


    def corrigir_totais(xml_element):
        infNFe = xml_element.find(".//{*}infNFe")
        total = infNFe.find("{*}total/{*}ICMSTot")
        
        # Calcula totais dos produtos
        v_prod = sum(float(det.find("{*}prod/{*}vProd").text) for det in infNFe.findall("{*}det"))
        
        # Atualiza os campos
        total.find("{*}vProd").text = f"{v_prod:.2f}"
        total.find("{*}vNF").text = f"{v_prod:.2f}"
        
        return xml_element


    # Modifique a seção de serialização assim:

        
        # Classe auxiliar para fonte de dados
    class FonteDados:
        def __init__(self, notas):
            self._notas = notas
            
        def obter_lista(self, _classe=None, **kwargs):
            return self._notas
            
        def limpar_dados(self):
            pass
    

    fonte_dados = FonteDados([nota_fiscal])
    serializador = SerializacaoXML(fonte_dados=fonte_dados)
    xml_nao_assinado = serializador.exportar()

    # Aplica correções manuais
    xml_nao_assinado = corrigir_totais(xml_nao_assinado)

    # Adiciona CRT (Regime Tributário)
    emitente = xml_nao_assinado.find(".//{*}emit")
    crt = etree.SubElement(emitente, "{http://www.portalfiscal.inf.br/nfe}CRT")
    crt.text = "1"  # 1=Simples Nacional

    





















    


    print("Assinando o XML com o certificado A1...")
    assinatura = AssinaturaA1(CERTIFICADO_PATH, CERTIFICADO_SENHA)

    # Correção manual para garantir produtos no XML
    infNFe = xml_nao_assinado.find(".//{*}infNFe")
    for prod in nota_fiscal.produtos:
        det = etree.SubElement(infNFe, "{http://www.portalfiscal.inf.br/nfe}det")
        det.set("nItem", str(prod.item))
        prod_node = etree.SubElement(det, "{http://www.portalfiscal.inf.br/nfe}prod")
        etree.SubElement(prod_node, "{http://www.portalfiscal.inf.br/nfe}cProd").text = prod.codigo
        etree.SubElement(prod_node, "{http://www.portalfiscal.inf.br/nfe}xProd").text = prod.descricao
        etree.SubElement(prod_node, "{http://www.portalfiscal.inf.br/nfe}NCM").text = prod.ncm
        etree.SubElement(prod_node, "{http://www.portalfiscal.inf.br/nfe}CFOP").text = prod.cfop
        etree.SubElement(prod_node, "{http://www.portalfiscal.inf.br/nfe}uCom").text = prod.unidade_comercial
        etree.SubElement(prod_node, "{http://www.portalfiscal.inf.br/nfe}qCom").text = str(prod.quantidade_comercial)
        etree.SubElement(prod_node, "{http://www.portalfiscal.inf.br/nfe}vUnCom").text = str(prod.valor_unitario_comercial)
        etree.SubElement(prod_node, "{http://www.portalfiscal.inf.br/nfe}vProd").text = str(prod.valor_total)

    print("Assinando o XML com o certificado A1...")
    assinatura = AssinaturaA1(CERTIFICADO_PATH, CERTIFICADO_SENHA)
    xml_assinado = assinatura.assinar(xml_nao_assinado)

    # Salva XML assinado
    caminho_xml = f"nfe_{chave_acesso}_assinado.xml"
    with open(caminho_xml, "wb") as f:
        f.write(etree.tostring(xml_assinado, encoding='UTF-8', xml_declaration=True))
    print(f"XML assinado salvo em '{caminho_xml}'")

    # 6. COMUNICAÇÃO COM A SEFAZ
    print("\nIniciando comunicação com a SEFAZ...")
    con = ComunicacaoSefaz(UF, CERTIFICADO_PATH, CERTIFICADO_SENHA, HOMOLOGACAO)

    try:
        # Envio da NF-e
        envio = con.autorizacao(modelo='nfe', nota_fiscal=xml_assinado)
        status_pynfe, http_response, xml_resposta_envio = envio
        
        print("\n--- Resposta do Envio ---")
        print(etree.tostring(xml_resposta_envio, encoding='unicode', pretty_print=True))

        ns = {'ns': 'http://www.portalfiscal.inf.br/nfe', 'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        cStat_envio = xml_resposta_envio.xpath('//ns:cStat/text()', namespaces=ns)
        
        print(cStat_envio)
        if not cStat_envio:
            # Verifique a resposta bruta
            print("Resposta bruta:", etree.tostring(xml_resposta_envio, encoding='unicode'))
            return 

        if cStat_envio[0] != '103':  # 103 = Lote Recebido com Sucesso
            xMotivo_envio = xml_resposta_envio.xpath('//ns:xMotivo/text()', namespaces=ns)
            print(f"❌ Erro no recebimento do lote: {xMotivo_envio[0] if xMotivo_envio else 'Motivo desconhecido'}")
            return

        nRec = xml_resposta_envio.xpath('//ns:infRec/ns:nRec/text()', namespaces=ns)
        if not nRec:
            print("⚠ Não foi possível obter o número do recibo do lote.")
            return
        
        numero_recibo = nRec[0]
        print(f"📄 Lote recebido com sucesso! Número do recibo: {numero_recibo}")

        # Consulta do recibo
        print(f"\nConsultando o resultado do processamento do recibo {numero_recibo}...")
        consulta = con.consulta_recibo(modelo='nfe', numero_recibo=numero_recibo)
        status_pynfe, http_response, xml_resposta_consulta = consulta

        print("\n--- Resposta da Consulta do Recibo ---")
        print(etree.tostring(xml_resposta_consulta, encoding='unicode', pretty_print=True))

        cStat_recibo = xml_resposta_consulta.xpath('//ns:cStat/text()', namespaces=ns)
        xMotivo_recibo = xml_resposta_consulta.xpath('//ns:xMotivo/text()', namespaces=ns)

        if not (cStat_recibo and cStat_recibo[0] == '104'):  # 104 = Lote processado
            print(f"❌ Erro no processamento do lote: {cStat_recibo[0] if cStat_recibo else 'N/A'} - {xMotivo_recibo[0] if xMotivo_recibo else 'Motivo desconhecido'}")
            return

        # Verificação do status da NF-e
        cStat_nfe = xml_resposta_consulta.xpath('//ns:protNFe/ns:infProt/ns:cStat/text()', namespaces=ns)
        if cStat_nfe and cStat_nfe[0] == '100':  # 100 = Autorizado o uso da NF-e
            chNFe = xml_resposta_consulta.xpath('//ns:protNFe/ns:infProt/ns:chNFe/text()', namespaces=ns)
            nProt = xml_resposta_consulta.xpath('//ns:protNFe/ns:infProt/ns:nProt/text()', namespaces=ns)
            print("\n" + "="*50)
            print(f"✅ NF-e AUTORIZADA COM SUCESSO!")
            print(f"   Chave de Acesso: {chNFe[0]}")
            print(f"   Protocolo: {nProt[0]}")
            print("="*50)
        else:
            xMotivo_nfe = xml_resposta_consulta.xpath('//ns:protNFe/ns:infProt/ns:xMotivo/text()', namespaces=ns)
            print("\n" + "!"*50)
            print(f"❌ NF-e REJEITADA!")
            print(f"   Status: {cStat_nfe[0] if cStat_nfe else 'N/A'}")
            print(f"   Motivo: {xMotivo_nfe[0] if xMotivo_nfe else 'Desconhecido'}")
            print("!"*50)

    except Exception as e:
        print(f"❌ Falha crítica na comunicação com a SEFAZ: {str(e)}")

if __name__ == '__main__':
    emitir_nfe()