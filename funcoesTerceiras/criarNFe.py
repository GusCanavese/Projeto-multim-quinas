from pynfe.entidades import Emitente, Cliente, Produto, NotaFiscal
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoSefaz
from datetime import datetime
from lxml import etree
import random

def emitir_nfe_funcional():
    # 1. Configuração do Emitente com todos campos obrigatórios
    emitente = Emitente(
        razao_social='NUTRIGEL DISTRIBUIDORA EIRELI',
        nome_fantasia='NUTRIGEL DISTRIBUIDORA',
        cnpj='00995044000107',
        inscricao_estadual='6259569630086',
        endereco_logradouro='R DOUTOR OSCAR DA CUNHA',
        endereco_numero='126',
        endereco_complemento='LETRA B',
        endereco_bairro='FABRICAS',
        endereco_municipio='SAO JOAO DEL REI',
        endereco_codigo_municipio='3162500',  # Código IBGE (7 dígitos)
        endereco_uf='MG',
        endereco_cep='36301194',
        endereco_pais='1058',
        telefone='3233713382',
        codigo_regime_tributario='1'  # 1=Simples Nacional
    )

    # 2. Configuração do Cliente
    cliente = Cliente(
        razao_social='CLIENTE DE TESTE LTDA',
        tipo_documento='CNPJ',
        numero_documento='98765432000195',
        endereco_logradouro='RUA DO CLIENTE',
        endereco_numero='456',
        endereco_bairro='CENTRO',
        endereco_municipio='Rio de Janeiro',
        endereco_uf='RJ',
        endereco_cep='20010010',
        endereco_pais='1058',
        indicador_ie='9'  # 9=Não contribuinte
    )

    # 3. Configuração do Produto
    produto = Produto(
        codigo='001',
        descricao='PRODUTO EXEMPLO',
        ncm='84715010',
        cfop='5102',
        unidade_comercial='UN',
        quantidade_comercial=1.0,
        valor_unitario_comercial=100.00,
        valor_total=100.00,
        icms_modalidade='00',
        icms_origem=0,
        pis_modalidade='01',
        cofins_modalidade='01'
    )

    # 4. Configuração da Nota Fiscal
    nota_fiscal = NotaFiscal(
        emitente=emitente,
        cliente=cliente,
        uf='MG',
        natureza_operacao='VENDA',
        forma_pagamento=0,
        tipo_documento=1,
        modelo='55',
        serie='1',
        numero_nf=str(random.randint(10000, 99999)),
        data_emissao=datetime.now(),
        data_saida_entrada=datetime.now(),
        tipo_impressao_danfe=1,
        forma_emissao='1',
        ambiente=2,  # 2=Homologação
        finalidade_emissao='1',
        processo_emissao='0',
        produtos=[produto],
        valor_total=100.00,
        municipio_fato_gerador='3162500'  # Código IBGE
    )

    # 5. Serialização
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

    # 6. Namespace para busca
    NS = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

    # 7. Correções manuais no XML
    def corrigir_xml(xml_element):
        # Encontra a tag infNFe
        infNFe = xml_element.find('.//ns:infNFe', namespaces=NS)
        if infNFe is None:
            raise ValueError("Tag infNFe não encontrada no XML")

        # Adiciona cMunFG (Código do município de ocorrência do fato gerador)
        cMunFG = etree.SubElement(infNFe, '{http://www.portalfiscal.inf.br/nfe}cMunFG')
        cMunFG.text = '3162500'

        # Adiciona CRT (Código de Regime Tributário)
        emit = infNFe.find('.//ns:emit', namespaces=NS)
        if emit is not None:
            crt = etree.SubElement(emit, '{http://www.portalfiscal.inf.br/nfe}CRT')
            crt.text = '1'  # 1=Simples Nacional

        # Adiciona idDest (Identificador de destino da operação)
        dest = infNFe.find('.//ns:dest', namespaces=NS)
        if dest is not None:
            id_dest = etree.SubElement(dest, '{http://www.portalfiscal.inf.br/nfe}idDest')
            id_dest.text = '2'  # 2=Operação interestadual

        return xml_element

    # Aplica as correções
    xml_corrigido = corrigir_xml(xml_nao_assinado)

    # 8. Assinatura
    certificado_path = "arquivos/certificado.pfx"
    certificado_senha = "nutri@00995"
    assinatura = AssinaturaA1(certificado_path, certificado_senha)
    xml_assinado = assinatura.assinar(xml_corrigido)

    # 9. Salvar XML
    with open("nfe_emitida.xml", "wb") as f:
        f.write(etree.tostring(xml_assinado, encoding='UTF-8', xml_declaration=True))

    print("✅ XML gerado e assinado com sucesso: nfe_emitida.xml")

    # 10. Envio para SEFAZ (opcional)
    con = ComunicacaoSefaz('MG', certificado_path, certificado_senha, homologacao=True)
    try:
        envio = con.autorizacao(modelo='nfe', nota_fiscal=xml_assinado)
        print("Resposta da SEFAZ:", envio)
    except Exception as e:
        print(f"⚠ Erro ao enviar para SEFAZ: {str(e)}")

if __name__ == '__main__':
    emitir_nfe_funcional()