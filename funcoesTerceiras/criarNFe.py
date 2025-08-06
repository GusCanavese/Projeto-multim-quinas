from pynfe.entidades import Emitente, Cliente, Produto, NotaFiscal
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoSefaz
from datetime import datetime
from lxml import etree
import warnings

# Configurações
CERTIFICADO_PATH = "arquivos/certificado.pfx"
CERTIFICADO_SENHA = "nutri@00995"
UF = "SP"
HOMOLOGACAO = True  # True = homologação, False = produção

# Suprimir avisos de certificado não verificado (apenas para desenvolvimento)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

class FonteDadosNotas:
    def __init__(self, notas):
        self._notas = notas

    def obter_lista(self, _classe=None, **kwargs):
        return self._notas

    def limpar_dados(self):
        pass

def gerar_nfe():
    try:
        # 1. Emitente
        emitente = Emitente(
            razao_social='SUA EMPRESA LTDA',
            nome_fantasia='SUA EMPRESA',
            cnpj='12345678000195',  # Substitua por um CNPJ válido
            inscricao_estadual='123456789',  # IE válida para SP
            inscricao_municipal='12345',
            cnae_fiscal='6201500',
            endereco_logradouro='Rua Exemplo',
            endereco_numero='123',
            endereco_bairro='Centro',
            endereco_municipio='São Paulo',
            endereco_uf='SP',
            endereco_cep='01001000',
            endereco_pais='1058'
        )

        # 2. Cliente
        cliente = Cliente(
            razao_social='CLIENTE EXEMPLO LTDA',
            tipo_documento='CNPJ',
            numero_documento='12345678000195',  # CNPJ válido
            inscricao_estadual='123456789',  # IE válida se necessário
            endereco_logradouro='Rua do Cliente',
            endereco_numero='100',
            endereco_bairro='Centro',
            endereco_municipio='São Paulo',
            endereco_uf='SP',
            endereco_cep='01001000',
            endereco_pais='1058',
            indicador_ie=1  # 1=Contribuinte ICMS
        )

        # 3. Produto
        produto = Produto(
            codigo='001',
            descricao='PRODUTO EXEMPLO',
            ncm='12345678',  # NCM válido
            cfop='5102',  # CFOP válido para operação
            unidade_comercial='UN',
            quantidade_comercial=1.0,
            valor_unitario_comercial=100.00,
            valor_total=100.00,
            unidade_tributavel='UN',
            quantidade_tributavel=1.0,
            valor_unitario_tributavel=100.00,
            icms_modalidade='00',  # 00=Tributada integralmente
            icms_origem=0,  # 0=Nacional
            pis_modalidade='01',  # 01=Operação tributável
            cofins_modalidade='01'  # 01=Operação tributável
        )

        # 4. Nota Fiscal
        nota_fiscal = NotaFiscal(
            emitente=emitente,
            cliente=cliente,
            uf=UF,
            natureza_operacao='VENDA',
            forma_pagamento=0,  # 0=À vista
            tipo_documento=1,  # 1=Saída
            modelo='55',  # 55=NFe
            serie='1',
            numero_nf='12345',  # Número sequencial único
            data_emissao=datetime.now(),
            data_saida_entrada=datetime.now(),
            tipo_impressao_danfe=1,  # 1=DANFE normal
            forma_emissao='1',  # 1=Emissão normal
            ambiente=2 if HOMOLOGACAO else 1,  # 2=Homologação, 1=Produção
            finalidade_emissao='1',  # 1=Normal
            processo_emissao='0',  # 0=Emissão com aplicativo do contribuinte
            produtos=[produto],
            valor_total=100.00,
            valor_icms=12.00,
            valor_pis=0.65,
            valor_cofins=3.00,
            municipio_fato_gerador='3550308'  # Código IBGE de São Paulo
        )

        # 5. Serialização e assinatura
        fonte_dados = FonteDadosNotas([nota_fiscal])
        serializador = SerializacaoXML(fonte_dados=fonte_dados)
        xml = serializador.exportar()

        assinatura = AssinaturaA1(CERTIFICADO_PATH, CERTIFICADO_SENHA)
        xml_assinado = assinatura.assinar(xml)

        with open("nfe_assinada.xml", "wb") as f:
            f.write(etree.tostring(xml_assinado, encoding='UTF-8', xml_declaration=True))
        print("✅ XML assinado salvo em 'nfe_assinada.xml'")

        # 6. Comunicação com SEFAZ
        con = ComunicacaoSefaz(UF, CERTIFICADO_PATH, CERTIFICADO_SENHA, HOMOLOGACAO)
        
        # Envio para autorização
        envio = con.autorizacao(modelo='nfe', nota_fiscal=xml_assinado)
        
        # Processamento do retorno
        status_pynfe, http_response, xml_resposta = envio
        
        print("\nResposta completa da SEFAZ:")
        resposta_completa = etree.tostring(xml_resposta, encoding='unicode', pretty_print=True)
        print(resposta_completa)
        
        # Verifica se a resposta contém erros
        ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
        cStat = xml_resposta.xpath('//ns:cStat/text()', namespaces=ns)
        xMotivo = xml_resposta.xpath('//ns:xMotivo/text()', namespaces=ns)
        
        if cStat:
            print(f"\nStatus: {cStat[0]} - {xMotivo[0] if xMotivo else 'Sem mensagem'}")
            
            if cStat[0] == '103':  # Lote recebido com sucesso
                nRec = xml_resposta.xpath('//ns:infRec/ns:nRec/text()', namespaces=ns)
                if nRec:
                    print(f"📄 Número do recibo: {nRec[0]}")
                    
                    # Consulta protocolo
                    consulta = con.consulta_recibo(modelo='nfe', numero_recibo=nRec[0])
                    xml_consulta = consulta[2]
                    print("\nResposta da consulta:")
                    print(etree.tostring(xml_consulta, encoding='unicode', pretty_print=True))
                    
                    cStat_consulta = xml_consulta.xpath('//ns:cStat/text()', namespaces=ns)
                    xMotivo_consulta = xml_consulta.xpath('//ns:xMotivo/text()', namespaces=ns)
                    chNFe = xml_consulta.xpath('//ns:chNFe/text()', namespaces=ns)
                    nProt = xml_consulta.xpath('//ns:nProt/text()', namespaces=ns)
                    
                    if cStat_consulta and cStat_consulta[0] == '100':
                        print(f"\n✅ NF-e autorizada! Chave: {chNFe[0]}, Protocolo: {nProt[0]}")
                    else:
                        print(f"\n❌ Erro na consulta: {xMotivo_consulta[0] if xMotivo_consulta else 'Status desconhecido'}")
                else:
                    print("⚠ Não foi possível obter o número de recibo.")
            else:
                print("❌ Erro no envio da NFe")
        else:
            print("⚠ Resposta da SEFAZ não contém status")

    except Exception as e:
        print(f"\n❌ Erro durante o processo: {str(e)}")

if __name__ == '__main__':
    gerar_nfe()