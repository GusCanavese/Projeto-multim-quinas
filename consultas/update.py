import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import db
from datetime import date

class Atualiza():
    def atualizaPedido(identificador):
        print(identificador)
        dataHoje = date.today()

        queryAtualizaPedido = "UPDATE pedidos SET data_confirmacao = %s WHERE numero_recibo = %s"
        db.cursor.execute(queryAtualizaPedido, (dataHoje.strftime("%d/%m/%Y") ,identificador,))
        print("atualizado com sucesso")