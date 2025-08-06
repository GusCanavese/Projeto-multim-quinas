import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import db
from datetime import date

class Atualiza:
    def atualizaPedido(identificador):
        dataHoje = date.today()
        queryAtualizaPedido = "UPDATE pedidos SET data_confirmacao = %s WHERE numero_recibo = %s LIMIT 1"
        db.cursor.execute(queryAtualizaPedido, (dataHoje.strftime("%d/%m/%Y") ,identificador,))
        db.conn.commit()

    def atualizaProduto(quantidade, preco, custo, id):
        dataHoje = date.today()
        queryAtualizaPedido = "UPDATE produtos SET quantidade = %s, valor_de_venda = %s, valor_de_custo = %s  WHERE id LIKE %s LIMIT 1"
        db.cursor.execute(queryAtualizaPedido, (quantidade, preco, custo, id))
        db.conn.commit()

    def removeUnidadesDeProdutos(desc):
        for i in desc:
            partes = i.rsplit(' ', 1)
            quantidade = partes[1]
            nomeDoProduto = partes[0]

        queryRemoveProduto = "UPDATE produtos SET quantidade = quantidade - %s WHERE nome_do_produto LIKE %s"
        db.cursor.execute(queryRemoveProduto, (quantidade, nomeDoProduto,))
        db.conn.commit()


    def retornaProdutoParaOEstoque(desc):
        for i in desc:
            partes = i.rsplit(' ', 1)
            quantidade = partes[1]
            nomeDoProduto = partes[0]

        queryRemoveProduto = "UPDATE produtos SET quantidade = quantidade + %s WHERE nome_do_produto LIKE %s"
        db.cursor.execute(queryRemoveProduto, (quantidade, nomeDoProduto,))
        db.conn.commit()


