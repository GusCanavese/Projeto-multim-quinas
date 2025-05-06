from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

def gerarOrcamento(nome_arquivo, dados):
    c = canvas.Canvas(nome_arquivo, pagesize=letter)
    width, height = letter

    # Definindo a altura inicial
    altura = height - 10

    # Cabeçalho
    c.line(20, altura, 575+15, altura)
    c.setFont("Times-Bold", 12)
    c.drawString(width/4 + 10, altura - 20, "Multimáquinas, refrigeração e máquinas LTDA")
    c.setFont("Times-Roman", 8)
    c.drawString(width/4, altura - 35, "RUA DOUTOR OSCAR DA CUNHA, 97, FÁBRICAS, SÃO JOÃO DEL REI-MG")
    c.drawString(width/2.5, altura - 50, "TELEFONE: 32 3371-6171")
    
    c.line(20, altura-60, 575+15, altura-60)
    c.setFont("Times-Roman", 10)
    c.drawString(20, altura - 70, f"{dados['data_emissao']}")
    c.drawString(width/2.35, altura - 70, f"Nº {dados['numero_recibo']}")
    c.line(20, altura-75, 575+15, altura-75)

    c.setFont("Times-Roman", 8)
    c.drawString(width/3, altura - 83, "Não é documento fiscal - Não é válido como garantia")
    c.line(20, altura-86, 575+15, altura-86)

    c.drawString(22, altura - 95, "Cliente:")
    c.drawString(50, altura - 95, f"{dados['destinatario']}")

    c.drawString(22, altura - 105, "CPF:")
    c.drawString(50, altura - 105, f"{dados['cpf']}")

    c.drawString(22, altura - 115, "CNPJ:")
    c.drawString(50, altura - 115, f"{dados['cnpj']}")

    c.drawString(22, altura - 125, "Endereço:")
    c.drawString(60, altura - 125, f"{dados['endereco']}")

    c.line(20, altura-130, 575+15, altura-130)


    # Tabela de itens
    c.line(20, altura - 275+ 100, 575+15, altura - 275+ 100)
    c.line(20, altura - 275+ 100 - 15, 575+15, altura - 275 - 15+ 100)

    c.setFont("Times-Bold", 8)
    c.drawString(30, altura - 285+100, "CÓDIGO")
    c.setFont("Times-Roman", 6)

    c.setFont("Times-Bold", 8)
    c.drawString(110, altura - 285+100, "DESCRIÇÃO DOS PRODUTOS")
    c.setFont("Times-Roman", 5)

    c.setFont("Times-Bold", 8)
    c.drawString(270, altura - 285+100, "UNID")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(307, altura - 285+100, "QTD")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(346, altura - 285+100, "V.UNITÁRIO")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(405, altura - 285+100, "DESC(%)")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(450, altura - 285+100, "DESC($)")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(490, altura - 285+100, "ACR($)")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(525, altura - 285+100, "SUBTOTAL")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 9)
    c.drawString(23, altura - 272+100, "DADOS DO PRODUTO")
    c.setFont("Times-Roman", 7)

    # Adiciona os itens dinamicamente
    altura_item = altura - 300  # Posição inicial dos itens
    altura_linha = 30
    for item in dados['itens']:
        c.drawString(23, altura_item + 100, f"{item['codigo']}")
        c.drawString(82, altura_item + 100, f"{item['descricao']}")
        c.drawString(270, altura_item +100, f"{item['unidade']}")
        c.drawString(300, altura_item +100, f"{item['quantidade']}")
        c.drawString(345, altura_item +100, f"{item['valor_unitario']}")
        c.drawString(405, altura_item +100, f"{item['desconto_porcentagem']}")
        c.drawString(450, altura_item +100, f"{item['desconto_real']}")
        c.drawString(490, altura_item +100, f"{item['acrescimo']}")
        c.drawString(525, altura_item +100, f"{item['subtotal']}")



        c.line(20, altura - 320 + altura_linha + 100, 575+15, altura - 320 + altura_linha + 100)
        
        altura_linha -= 80
        altura_item -= 80


    c.setFont("Times-Bold", 8)
    c.line(20, altura_item+110, 575+15, altura_item+110)

    c.drawString(150, altura_item+100, "TOTAL DE MERCADORIAS")
    c.drawString(300, altura_item+100, f"{dados['total_quantidade']}")
    c.drawString(405, altura_item+100, f"{dados['total_desc_porc']}")
    c.drawString(450, altura_item+100, f"{dados['total_desc_real']}")
    c.drawString(490, altura_item+100, f"{dados['total_acrescimo']}")
    c.drawString(525, altura_item+100, f"{dados['total_subtotal']}")

    novaAltura = 480
    c.line(20, novaAltura+altura_item-390, 575+15, novaAltura+altura_item-390)
    c.drawString(20, novaAltura+altura_item-400, "Forma de pagamento:")
    c.drawString(100, novaAltura+altura_item-400, f"{dados['forma_pagamento']}")
    c.line(20, novaAltura+altura_item-410, 575+15, novaAltura+altura_item-410)

    c.setFont("Times-Roman", 10)
    c.drawString(20, novaAltura+altura_item-430, "Vendedor:")
    c.drawString(70, novaAltura+altura_item-430, f"{dados['vendedor']}")
    
    c.setFont("Times-Bold", 12)
    c.drawString(200, novaAltura+altura_item-430, "Itens sujeitos a disponibilidade do estoque, não reservamos mercadorias")
    c.line(20, novaAltura+altura_item-460, 575+15, novaAltura+altura_item-460)

    c.setFont("Times-Bold", 8)
    c.drawString(width/2.7, novaAltura+altura_item-470, "É vedada a autenticação deste documento")
   
    c.save()
    

dados_exemplo = {
"numero_recibo": "0001206970",
"total_quantidade": "pass",
"total_desc_porc": "pass",
"total_desc_real": "pass",
"total_acrescimo": "pass",
"total_subtotal": "pass",
"valor_total": "pass",
"frete": "200,00",
"forma_pagamento":"5 parcelas",
"vendedor": "VANIA",
"data_confirmacao": "05/02/2025 12:44",
"data_emissao": "07/02/2025 11:39:25",
"destinatario": "ANTONIO LOPES DE MOURA",
"cpf": "423.921.106-97",
"cnpj": "58.990.672/0001-71",
"cep": "36360-000",
"endereco": "Rua Padre Antônio, 89 - Conceição da Barra de Minas/MG",
"referencia": "Rua Padre antônio",
"telefone": "(32) 3375-1182",
"observacoes1": "teste",
"observacoes2": "teste",
"itens": [
    {
        "codigo": "2087118514612",
        "descricao": "ILHA PARA CONGELADOS LIGHT 2.00M - POLAR",
        "unidade": "UN",
        "quantidade": 2,
        "valor_unitario": "7.076,00",
        "desconto_real": "0,00",
        "desconto_porcentagem": "0,00",
        "acrescimo": "0,00",
        "subtotal": "14.152,00"
    },



    {
        "codigo": "2087118514613",
        "descricao": "FREEZER VERTICAL 500L - POLAR",
        "unidade": "UN",
        "quantidade": 1,
        "valor_unitario": "3.500,00",
        "desconto_real": "0,00",
        "desconto_porcentagem": "0,00",
        "acrescimo": "0,00",
        "subtotal": "3.500,00"
    },
    # {
    #     "codigo": "2087118514612",
    #     "descricao": "ILHA PARA CONGELADOS LIGHT 2.00M - POLAR",
    #     "unidade": "UN",
    #     "quantidade": 2,
    #     "valor_unitario": "7.076,00",
    #     "desconto_real": "0,00",
    #     "desconto_porcentagem": "0,00",
    #     "acrescimo": "0,00",
    #     "subtotal": "14.152,00"
    # },
    # {
    #     "codigo": "2087118514612",
    #     "descricao": "ILHA PARA CONGELADOS LIGHT 2.00M - POLAR",
    #     "unidade": "UN",
    #     "quantidade": 2,
    #     "valor_unitario": "7.076,00",
    #     "desconto_real": "0,00",
    #     "desconto_porcentagem": "0,00",
    #     "acrescimo": "0,00",
    #     "subtotal": "14.152,00"

    # },
    # {
    #     "codigo": "2087118514613",
    #     "descricao": "FREEZER VERTICAL 500L - POLAR",
    #     "unidade": "UN",
    #     "quantidade": 1,
    #     "valor_unitario": "3.500,00",
    #     "desconto_real": "0,00",
    #     "desconto_porcentagem": "0,00",
    #     "acrescimo": "0,00",
    #     "subtotal": "3.500,00"
    # },
    # {
    #     "codigo": "2087118514612",
    #     "descricao": "ILHA PARA CONGELADOS LIGHT 2.00M - POLAR",
    #     "unidade": "UN",
    #     "quantidade": 2,
    #     "valor_unitario": "7.076,00",
    #     "desconto_real": "0,00",
    #     "desconto_porcentagem": "0,00",
    #     "acrescimo": "0,00",
    #     "subtotal": "14.152,00"
    # },
    # {
    #     "codigo": "2087118514613",
    #     "descricao": "FREEZER VERTICAL 500L - POLAR",
    #     "unidade": "UN",
    #     "quantidade": 1,
    #     "valor_unitario": "3.500,00",
    #     "desconto_real": "0,00",
    #     "desconto_porcentagem": "0,00",
    #     "acrescimo": "0,00",
    #     "subtotal": "3.500,00"
    # },
    # {
    #     "codigo": "2087118514613",
    #     "descricao": "FREEZER VERTICAL 500L - POLAR",
    #     "unidade": "UN",
    #     "quantidade": 1,
    #     "valor_unitario": "3.500,00",
    #     "desconto_real": "0,00",
    #     "desconto_porcentagem": "0,00",
    #     "acrescimo": "0,00",
    #     "subtotal": "3.500,00"
    # }
],
}
    
gerarOrcamento("Orcamento.pdf", dados_exemplo)