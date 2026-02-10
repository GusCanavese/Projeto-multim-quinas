import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
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

    def atualizaProdutoFiscal(quantidade, preco, custo, id):
        dataHoje = date.today()
        queryAtualizaPedido = "UPDATE produtos_fiscal SET quantidade = %s, valor_de_venda = %s, valor_de_custo = %s  WHERE id LIKE %s LIMIT 1"
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

    # >>> ALTERADO: recebe numero_original para o WHERE
    def atualizaNotaFiscal(params, numero_original):
        query = """
            UPDATE notas_fiscais
               SET status=%s, tipo=%s, operacao=%s, destinatario_nome=%s, serie=%s, valor_total=%s, cfop=%s, dhEmi=%s, numero=%s
             WHERE numero=%s
        """
        db.cursor.execute(query, (
            params[0], params[1], params[2], params[3], params[4],params[5], params[6], params[7], params[8], numero_original
        ))
        db.conn.commit()

    def confirmarContaAPagar(chave_nfe):
        query = """
            UPDATE contasapagar
               SET confirmado = 'Sim'
             WHERE chave_nfe = %s
            LIMIT 1
        """
        db.cursor.execute(query, (chave_nfe,))
        db.conn.commit()

    def atualizaContaAReceber(confirmado, vencimento, descricao, total, formaPag, qtdParcelas):
        query = """
            UPDATE contasareceber
               SET confirmado = %s
             WHERE vencimento = %s
               AND descricao = %s
               AND total = %s
               AND formaPag = %s
               AND qtdParcelas = %s
             LIMIT 1
        """
        db.cursor.execute(query, (confirmado, vencimento, descricao, total, formaPag, qtdParcelas))
        db.conn.commit()
