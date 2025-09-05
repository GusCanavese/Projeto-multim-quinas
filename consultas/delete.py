import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import db

class deleta:
    def deletarPedidos(numeroPedido):
        queryDeletaPedido = "DELETE FROM pedidos WHERE numero_recibo = %s;"
        db.cursor.execute(queryDeletaPedido, (numeroPedido,))
        db.conn.commit()

    def deletarProduto(descricao):
        queryDeletaPedido = "DELETE FROM produtos WHERE nome_do_produto LIKE %s;"
        db.cursor.execute(queryDeletaPedido, (descricao,))
        db.conn.commit()

    def deletarProdutoFiscal(descricao):
        queryDeletaPedido = "DELETE FROM produtos_fiscal WHERE nome_do_produto LIKE %s;"
        db.cursor.execute(queryDeletaPedido, (descricao,))
        db.conn.commit()