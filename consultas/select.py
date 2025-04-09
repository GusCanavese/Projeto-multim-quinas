import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import db


class Buscas:
    
    def buscaProduto(nomeDoProduto):
        queryBuscaProduto = "SELECT nome_do_produto, valor_de_venda, quantidade FROM produtos WHERE nome_do_produto LIKE %s"
        db.cursor.execute(queryBuscaProduto, (f"%{nomeDoProduto}%",))
        resultado = db.cursor.fetchall()
        return resultado
    
    def buscaCargoUsuarioBloqueado(usuarioBloqueado):
        queryConsultaUsuarioBloqueado = "SELECT cargo FROM funcionarios WHERE login = %s;"
        db.cursor.execute(queryConsultaUsuarioBloqueado, (usuarioBloqueado,))
        cargoUsuarioBloqueado = db.cursor.fetchall()
        return cargoUsuarioBloqueado
    
    def consultaUsuario(login, senha):
        queryConsultarLogin = "SELECT cargo FROM funcionarios WHERE login = %s AND senha= %s;"
        db.cursor.execute(queryConsultarLogin, (login, senha,))
        resultados = db.cursor.fetchall()
        return resultados
    
    def selecionaNumeroPedido():
        queryInserirNumeroDaVenda = "SELECT MAX(numero_recibo) AS maior_numero FROM pedidos"
        db.cursor.execute(queryInserirNumeroDaVenda)
        resultado = db.cursor.fetchone()
        return resultado
    
    def buscaDadosCliente(nomeDoCliente):
        queryBuscaCliente = "SELECT nome, cpf_cnpj, telefone FROM clientes WHERE nome LIKE %s"
        db.cursor.execute(queryBuscaCliente, (f"%{nomeDoCliente}%",))
        resultado = db.cursor.fetchall()
        return resultado
    
    def buscaPedidos(vendedor, numero, inicio, fim, checkbox):
        queryBuscaPedidos = "SELECT numero_recibo, data_emissao, vendedor, subtotal, data_confirmacao FROM pedidos WHERE 1=1"
        parametros = []

        if vendedor !="Nenhum":
            queryBuscaPedidos += " AND vendedor LIKE %s"
            parametros.append(f'%{vendedor}%')
            print("entrou em 1")
            print(parametros)

        if numero != '':
            queryBuscaPedidos += " AND numero_recibo LIKE %s"
            parametros.append(f'%{numero}%')
            print("entrou em 2")
            print(parametros)

        if not checkbox:
            print()
            pass

        elif (inicio and fim):
            queryBuscaPedidos += " AND data_emissao BETWEEN %s AND %s"
            parametros.extend([inicio, fim])


        print(parametros)
        db.cursor.execute(queryBuscaPedidos, parametros)
        resultado = db.cursor.fetchall()
        return resultado
    