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

    def deletarNotaFiscal(numero):
        queryDeletaNota = "DELETE FROM notas_fiscais WHERE numero = %s;"
        db.cursor.execute(queryDeletaNota, (numero,))
        db.conn.commit()

    def deletarContaAPagar(chave_nfe):
        query = "DELETE FROM contasapagar WHERE chave_nfe = %s LIMIT 1;"
        db.cursor.execute(query, (chave_nfe,))
        db.conn.commit()
