import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import db

class deleta:
    def deletarPedidos(numeroPedido):
        queryDeletaPedido = "DELETE FROM pedidos WHERE numero_recibo = %s;"
        print(numeroPedido)
        db.cursor.execute(queryDeletaPedido, (numeroPedido,))
        db.conn.commit()