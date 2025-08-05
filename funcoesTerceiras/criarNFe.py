from pynfe.entidades import Emitente, Cliente, Produto, NotaFiscal
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.processamento.comunicacao import ComunicacaoSefaz
from datetime import datetime

# Configurações do certificado e SEFAZ
CERTIFICADO_PATH = "arquivos/certificado.pfx"
CERTIFICADO_SENHA = "nutri@00995"
UF = "SP"
HOMOLOGACAO = True  # True = ambiente de homologação, False = produção


# Classe de fonte de dados para SerializacaoXML
class FonteDadosNotas:
    def __init__(self, notas):
        self._notas = notas

    def obter_lista(self, _classe=None, **kwargs):
        return self._notas

    def limpar_dados(self):
        pass


def gerar_nfe():
    # Emitente
    emitente = Emitente(
        razao_social='SUA EMPRESA LTDA',
        nome_fantasia='SUA EMPRESA',
        cnpj='12345678000195',
        inscricao_estadual='123456789',
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

    # Cliente
    cliente = Cliente(
        razao_social='CLIENTE EXEMPLO LTDA',
        tipo_documento='CNPJ',
        numero_documento='12345678000195',
        inscricao_estadual='123456789',
        endereco_logradouro='Rua do Cliente',
        endereco_numero='100',
        endereco_bairro='Centro',
        endereco_municipio='São Paulo',
        endereco_uf='SP',
        endereco_cep='01001000',
        endereco_pais='1058',
        indicador_ie=1,
    )

    # Produto
    produto = Produto(
        codigo='001',
        descricao='PRODUTO EXEMPLO',
        ncm='12345678',
        cfop='5102',
        unidade_comercial='UN',
        quantidade_comercial=1.0,
        valor_unitario_comercial=100.00,
        valor_total=100.00,
        unidade_tributavel='UN',
        quantidade_tributavel=1.0,
        valor_unitario_tributavel=100.00,
        icms_modalidade='00',
        icms_origem=0,
        icms_csosn='',
        pis_modalidade='01',
        cofins_modalidade='01'
    )

    # Nota Fiscal
    nota_fiscal = NotaFiscal(
        emitente=emitente,
        cliente=cliente,
        uf=UF,
        natureza_operacao='VENDA',
        forma_pagamento=0,
        tipo_documento=1,
        modelo='55',
        serie='1',
        numero_nf='12345',
        data_emissao=datetime.now(),
        data_saida_entrada=datetime.now(),
        tipo_impressao_danfe=1,
        forma_emissao='1',
        ambiente=2 if HOMOLOGACAO else 1,
        finalidade_emissao='1',
        processo_emissao='0',
        produtos=[produto],
        valor_total=100.00,
        valor_icms=12.00,
        valor_pis=0.65,
        valor_cofins=3.00,
    )

    # Serializar XML
    fonte_dados = FonteDadosNotas([nota_fiscal])
    serializador = SerializacaoXML(fonte_dados=fonte_dados)
    xml = serializador.exportar()

    # Assinar XML
    assinatura = AssinaturaA1(CERTIFICADO_PATH, CERTIFICADO_SENHA)
    xml_assinado = assinatura.assinar(xml)

    # Enviar para SEFAZ
    con = ComunicacaoSefaz(UF, CERTIFICADO_PATH, CERTIFICADO_SENHA, HOMOLOGACAO)
    # if con:
    #     print("teria enviado")
    # else:
    envio = con.autorizacao(modelo='nfe', nota_fiscal=xml_assinado)
    print(envio)
    if envio[0].status == 100:
        print("✅ NF-e autorizada com sucesso!")
        print("Chave de acesso:", envio[0].chave)
        print("Protocolo:", envio[0].protocolo)

        # Consultar recibo
        consulta = con.consulta_recibo(modelo='nfe', numero_recibo=envio[0].protocolo)
        if consulta[0].status == 100:
            print("Consulta confirmada:", consulta[0].motivo)

            # Salvar XML autorizado
            with open(f"nfe-{envio[0].chave}-env.xml", "w", encoding="utf-8") as f:
                f.write(xml_assinado)
            with open(f"nfe-{envio[0].chave}-proc.xml", "w", encoding="utf-8") as f:
                f.write(consulta[0].protocolo)

            print("Arquivos XML salvos com sucesso.")
        else:
            print("⚠ NF-e enviada, mas problema na consulta:", consulta[0].motivo)
    else:
        print("❌ Erro no envio:", envio[0].motivo)


if __name__ == '__main__':
    gerar_nfe()
