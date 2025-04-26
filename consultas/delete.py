import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import db

# class deleta:
    # def deletarPedidos():
    #     queryDeletaPedido = "DELETE from PEDIDOS "



    #     dataHoje = date.today()
    #     queryAtualizaPedido = "UPDATE pedidos SET data_confirmacao = %s WHERE numero_recibo = %s LIMIT 1"
    #     db.cursor.execute(queryAtualizaPedido, (dataHoje.strftime("%d/%m/%Y") ,identificador,))
    #     db.conn.commit()