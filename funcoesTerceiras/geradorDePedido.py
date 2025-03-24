from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def gerar_recibo(nome_arquivo, dados):
    c = canvas.Canvas(nome_arquivo, pagesize=letter)
    width, height = letter

    # Definindo a altura inicial
    altura = height - 10

    # Cabeçalho
    c.setFont("Times-Bold", 10)
    c.drawString(250, altura - 40, "RECIBO DE VENDA")

    c.setFont("Times-Roman", 10)
    c.drawString(480, altura - 40, f"{dados['data_emissao']}")
    # Linha lado a lado
    c.line(20, altura - 45, 575+15, altura - 45)

    # Comentário, máquinas e equipamentos
    c.setFont("Times-Bold", 8)
    c.drawString(52, altura - 70, "Máquinas e")
    c.drawString(50, altura - 80, "equipamentos")
    c.drawString(52, altura - 90, "32-33751671")

    # Quadrado superior direito
    c.setFont("Times-Bold", 7)
    c.line(420, altura - 55, 575+15, altura - 55)
    c.line(420, altura - 55, 420, altura - 110)
    c.line(420, altura - 110, 575+15, altura - 110)
    c.line(575+15, altura - 55, 575+15, altura - 110)

    # Dados da venda e do vendedor, dentro do quadrado
    c.drawString(425, altura - 65, f"Nº {dados['numero_recibo']}")
    # c.drawString(425, altura - 75, f"Vendedor: {dados['vendedor']}")
    c.drawString(425, altura - 85, f"Data de Confirmação: {dados['data_confirmacao']}")
    c.drawString(425, altura - 95, f"Data de Emissão: {dados['data_emissao']}")
    c.drawString(425, altura - 105, "Página 1 de 1")

    # Destinatário
    c.rect(20, altura - 180, 570, 40, stroke=1, fill=0)

    c.setFont("Times-Bold", 9)
    c.drawString(22, altura - 135, "DESTINATÁRIO")
    c.drawString(22, altura - 150, "NOME/RAZÃO SOCIAL")
    c.setFont("Times-Roman", 9)
    c.drawString(22, altura - 165, f"{dados['destinatario']}")

    c.line(250, altura - 140, 250, altura - 180)
    c.setFont("Times-Bold", 9)
    c.drawString(252, altura - 150, "INSCRIÇÃO ESTADUAL")


    c.line(400, altura - 140, 400, altura - 180)
    c.drawString(402, altura - 150, "CNPJ")
    c.setFont("Times-Roman", 9)
    c.drawString(402, altura - 165, f"{dados['cnpj']}")

    c.setFont("Times-Bold", 9)
    c.line(500, altura - 140, 500, altura - 250)
    c.drawString(502, altura - 150, "CPF")
    c.setFont("Times-Roman", 9)
    c.drawString(502, altura - 165, f"{dados['cpf']}")

    c.rect(20, altura - 210, 570, 30, stroke=1, fill=0)

    c.setFont("Times-Bold", 9)
    c.drawString(502, altura - 190, "TELEFONE")
    c.setFont("Times-Roman", 9)
    c.drawString(502, altura - 205, f"{dados['telefone']}")

    c.setFont("Times-Bold", 9)
    c.drawString(502, altura - 220, "CEP")
    c.setFont("Times-Roman", 9)
    c.drawString(502, altura - 235, f"{dados['cep']}")

    c.setFont("Times-Bold", 9)
    c.drawString(22, altura - 190, "ENDEREÇO")
    c.setFont("Times-Roman", 9)
    c.drawString(22, altura - 200, f"Endereço: {dados['endereco']}")


    c.rect(20, altura - 250, 570, 40, stroke=1, fill=0)
    # c.line(20, altura - 230, 500, altura - 230)

    c.setFont("Times-Bold", 8)
    c.drawString(22, altura - 218, "REFERENCIA")
    c.setFont("Times-Roman", 8)
    c.drawString(22, altura - 228, f"Endereço: {dados['referencia']}")

    # Tabela de itens
    c.line(20, altura - 275, 575+15, altura - 275)
    c.line(20, altura - 275 - 15, 575+15, altura - 275 - 15)
    c.line(20, altura - 305, 575+15, altura - 305)

    c.setFont("Times-Bold", 8)
    c.drawString(30, altura - 285, "CÓDIGO")
    c.setFont("Times-Roman", 6)

    c.setFont("Times-Bold", 8)
    c.drawString(110, altura - 285, "DESCRIÇÃO DOS PRODUTOS")
    c.setFont("Times-Roman", 5)

    c.setFont("Times-Bold", 8)
    c.drawString(270, altura - 285, "UNID")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(307, altura - 285, "QTD")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(346, altura - 285, "V.UNITÁRIO")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(405, altura - 285, "DESC(%)")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(450, altura - 285, "DESC($)")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(490, altura - 285, "ACR($)")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 8)
    c.drawString(525, altura - 285, "SUBTOTAL")
    c.setFont("Times-Roman", 7)

    c.setFont("Times-Bold", 9)
    c.drawString(23, altura - 272, "DADOS DO PRODUTO")
    c.setFont("Times-Roman", 7)

    # Adiciona os itens dinamicamente
    altura_item = altura - 300  # Posição inicial dos itens
    altura_linha = 0
    for item in dados['itens']:

        c.drawString(23, altura_item, f"{item['codigo']}")
        c.drawString(82, altura_item, f"{item['descricao']}")
        c.drawString(270, altura_item, f"{item['unidade']}")
        c.drawString(300, altura_item, f"{item['quantidade']}")
        c.drawString(345, altura_item, f"{item['valor_unitario']}")
        c.drawString(405, altura_item, f"{item['desconto_porcentagem']}")
        c.drawString(450, altura_item, f"{item['desconto_real']}")
        c.drawString(490, altura_item, f"{item['acrescimo']}")
        c.drawString(525, altura_item, f"{item['subtotal']}")

        c.line(20,  altura - 275, 20,  altura - 320 + altura_linha)
        c.line(80,  altura - 275, 80,  altura - 305 + altura_linha)
        c.line(265, altura - 275, 265, altura - 320 + altura_linha)
        c.line(295, altura - 275, 295, altura - 320 + altura_linha)
        c.line(340, altura - 275, 340, altura - 320 + altura_linha)
        c.line(400, altura - 275, 400, altura - 320 + altura_linha)
        c.line(445, altura - 275, 445, altura - 320 + altura_linha)
        c.line(485, altura - 275, 485, altura - 320 + altura_linha)
        c.line(520, altura - 275, 520, altura - 320 + altura_linha)
        c.line(575+15, altura - 275, 575+15, altura - 320 + altura_linha)

        c.line(20, altura - 320 + altura_linha, 575+15, altura - 320 + altura_linha)
        
        altura_linha -= 15
        altura_item -= 15

    c.setFont("Times-Bold", 8)
    c.drawString(155, altura_item, "TOTAL DE MERCADORIAS")
    c.drawString(300, altura_item, f"{dados['total_quantidade']}")
    # c.drawString(345, altura_item, f"{dados['total_valor_unitario']}")
    c.drawString(405, altura_item, f"{dados['total_desc_porc']}")
    c.drawString(450, altura_item, f"{dados['total_desc_real']}")
    c.drawString(490, altura_item, f"{dados['total_acrescimo']}")
    c.drawString(525, altura_item, f"{dados['total_subtotal']}")


    c.setFont("Times-Bold", 9)
    c.drawString(520, altura_item -28, "VALORES")
    c.drawString(440, altura_item -115, "TOTAL")
    c.drawString(23, altura_item -28, "OBSERVAÇÕES DE ENTREGA")
    c.line(350, altura_item - 30, 350, altura_item - 120)
    c.drawString(485, altura_item -115, f"{dados['valor_total']}")


    c.setFont("Times-Roman", 8)
    c.drawString(40, altura_item -55, "ENTREGUE")
    c.rect(23, altura_item - 60, 15, 15, stroke=1, fill=0)

    c.drawString(40, altura_item -85, "ENTREGAR")
    c.rect(23, altura_item - 90, 15, 15, stroke=1, fill=0)

    c.drawString(353, altura_item -40, "TOTAIS DE MERCADORIA")
    c.drawString(353, altura_item -55, "DESCONTO NA VENDA($)")
    c.drawString(353, altura_item -70, "DESCONTO NA VENDA(%)")
    c.drawString(353, altura_item -85, "ACRESCIMO NA VENDA($)")
    c.drawString(353, altura_item -100, "FRETE")


    # c.drawString(485, altura_item -40, f"{dados['total_valor_unitario']}")
    c.drawString(485, altura_item -55, f"{dados['total_desc_real']}")
    c.drawString(485, altura_item -70, f"{dados['total_desc_porc']}")
    c.drawString(485, altura_item -85, f"{dados['total_acrescimo']}")
    c.drawString(485, altura_item -100, f"{dados['frete']}")


    c.line(480, altura_item - 30, 480, altura_item - 120)
    c.rect(20, altura_item - 30, 570, -90, stroke=1, fill=0)
    c.line(20, altura_item - 105, 575+15, altura_item - 105)

    c.setFont("Times-Bold", 9)
    c.drawString(23, altura_item -140, "OBSERVAÇÕES DO PEDIDO")
    c.drawString(450, altura_item -140, "FECHAMENTO FINANCEIRO")
    
    c.setFont("Times-Roman", 9)
    texto = c.beginText(23, altura_item - 160)  
    texto.setFont("Times-Roman", 9)
    for linha in dados['observacoes1'].split('\n'):
        texto.textLine(linha)  
    c.drawText(texto)


    texto2 = c.beginText(322, altura_item - 203)  
    texto2.setFont("Times-Roman", 9)
    for linha in dados['observacoes2'].split('\n'):
        texto2.textLine(linha)  
    c.drawText(texto2)
   

    c.setFont("Times-Roman", 7)

    c.drawString(338, altura_item -160, "PAGO")
    c.rect(322, altura_item - 165, 15, 15, stroke=1, fill=0)

    c.drawString(388, altura_item -160, "A VISTA")
    c.rect(372, altura_item - 165, 15, 15, stroke=1, fill=0)

    c.drawString(450, altura_item -160, "A PRAZO")
    c.rect(434, altura_item - 165, 15, 15, stroke=1, fill=0)

    c.drawString(510, altura_item -160, "RECEBER NA ENTREGA")
    c.rect(494, altura_item - 165, 15, 15, stroke=1, fill=0)

    c.setFont("Times-Bold", 9)
    c.drawString(322, altura_item -183, "FINANCEIRO")
    c.rect(20, altura_item - 143, (width - 50)/2 -5, -200, stroke=1, fill=0)
    c.line(314, altura_item - 175, 590, altura_item - 175)


    c.rect((width - 20)/2 + 18, altura_item - 143, (width - 50)/2 - 5, -200, stroke=1, fill=0)
    c.line(width/2-100, altura_item-390, width/2 + 100, altura_item-390)
    c.drawString(width/2-65, altura_item -400, f"{dados['destinatario']}")
    c.drawString(width/2-30, altura_item -415, f"{dados['cpf']}")

    


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
    }
],
}
    
gerar_recibo("recibo_venda.pdf", dados_exemplo)