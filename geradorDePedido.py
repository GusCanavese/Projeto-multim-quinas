from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime


def gerar_recibo(nome_arquivo, dados):
    dataHora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4
    
    # Cabeçalho
    c.setFont("Helvetica-Bold", 10)
    c.drawString(250, altura - 40, "RECIBO DE VENDA")

    c.setFont("Helvetica", 10)
    c.drawString(480, altura - 40, f"{dataHora}")
    c.line(20, altura - 45, 575, altura - 45 )

    
    c.setFont("Helvetica", 10)
    c.drawString(50, altura - 70, "Máquinas e \nequipamentos")
    c.drawString(50, altura - 85, "32-33751671")
    
    c.drawString(400, altura - 70, f"Nº {dados['numero_recibo']}")
    c.drawString(400, altura - 85, f"Vendedor: {dados['vendedor']}")
    c.drawString(400, altura - 100, f"Data de Confirmação: {dados['data_confirmacao']}")
    c.drawString(400, altura - 115, f"Data de Emissão: {dados['data_emissao']}")
    c.drawString(400, altura - 130, "Página 1 de 1")
    
    # Destinatário
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, altura - 160, "DESTINATÁRIO")
    c.setFont("Helvetica", 10)
    c.drawString(50, altura - 175, f"Nome/Razão Social: {dados['destinatario']}")
    c.drawString(400, altura - 175, f"CNPJ/CPF: {dados['cpf_cnpj']}")
    c.drawString(50, altura - 190, f"Endereço: {dados['endereco']}")
    c.drawString(400, altura - 190, f"Telefone: {dados['telefone']}")
    
    # Produtos
    produtos = [["CÓDIGO", "DESCRIÇÃO DOS PRODUTOS", "UNID", "QTD", "V. UNITÁRIO", "DESC (%)", "SUBTOTAL"]]
    for produto in dados['produtos']:
        produtos.append([produto['codigo'], produto['descricao'], produto['unidade'], produto['quantidade'], produto['valor_unitario'], produto['desconto'], produto['subtotal']])
    
    tabela = Table(produtos, colWidths=[60, 200, 40, 40, 80, 60, 80])
    tabela.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER')
    ]))
    
    tabela.wrapOn(c, largura, altura)
    tabela.drawOn(c, 50, altura - 350)
    
    # Observações e Assinatura
    c.drawString(50, altura - 450, "OBSERVAÇÕES")
    c.rect(50, altura - 500, 500, 30)
    c.drawString(60, altura - 490, dados['observacoes'])
    
    c.drawString(50, altura - 530, f"Condição de Pagamento: {dados['condicao_pagamento']}")
    c.drawString(50, altura - 550, f"Entrega: {dados['entrega']}")
    
    c.line(200, altura - 580, 400, altura - 580)
    c.drawString(250, altura - 595, dados['destinatario'])
    
    c.save()

# Exemplo de dados
dados_exemplo = {
    "numero_recibo": "0001206970",
    "vendedor": "VANIA",
    "data_confirmacao": "05/02/2025 12:44",
    "data_emissao": "07/02/2025 11:39:25",
    "destinatario": "ANTONIO LOPES DE MOURA",
    "cpf_cnpj": "423.921.106-97",
    "endereco": "Rua Padre Antônio, 89 - Conceição da Barra de Minas/MG",
    "telefone": "(32) 3375-1182",
    "produtos": [
        {"codigo": "2087118514612", "descricao": "ILHA PARA CONGELADOS LIGHT 2.00M - POLAR", "unidade": "UN", "quantidade": 2, "valor_unitario": "7.076,00", "desconto": "0,00", "subtotal": "14.152,00"}
    ],
    "observacoes": "É necessário a apresentação do recibo para assistência técnica. Não devolvemos dinheiro.",
    "condicao_pagamento": "À VISTA",
    "entrega": "ENTREGAR"
}

# Gerar PDF
gerar_recibo("recibo_venda.pdf", dados_exemplo)
