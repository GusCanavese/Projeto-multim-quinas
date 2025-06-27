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
    
    def buscaContasAReceber():
        queryBuscaCliente = "SELECT confirmado, vencimento, descricao, total, formaPag, qtdParcelas FROM contasareceber"
        db.cursor.execute(queryBuscaCliente)
        resultado = db.cursor.fetchall()
        return resultado
    
    def buscaContasAPagar():
        queryBuscaCliente = "SELECT confirmado, vencimento, descricao, total, formaPag, qtdParcelas FROM contasapagar"
        db.cursor.execute(queryBuscaCliente)
        resultado = db.cursor.fetchall()
        return resultado
    
    def buscaPedidos(vendedor, numero, inicio, fim, checkbox):
        queryBuscaPedidos = "SELECT numero_recibo, data_emissao, vendedor, subtotal, data_confirmacao, destinatario, cpf, endereco, itens FROM pedidos WHERE 1=1"
        parametros = []

        if vendedor !="Nenhum":
            queryBuscaPedidos += " AND vendedor LIKE %s"
            parametros.append(f'%{vendedor}%')

        if numero != '':
            queryBuscaPedidos += " AND numero_recibo LIKE %s"
            parametros.append(f'%{numero}%')

        if not checkbox:
            pass

        elif (inicio and fim):
            queryBuscaPedidos += " AND data_emissao BETWEEN %s AND %s"
            parametros.extend([inicio, fim])


        print(parametros)
        db.cursor.execute(queryBuscaPedidos, parametros)
        resultado = db.cursor.fetchall()
        return resultado
    
    def buscaEstoqueProdutos(nome, codigo):
        queryBuscaProdutosEstoque = "SELECT quantidade, descricao, codigo_interno, valor_de_venda, CNPJ, codigo_ncm, codigo_cfop, codigo_cest, valor_de_venda, valor_de_custo origem_cst FROM produtos WHERE 1=1"
        parametros = []
        if nome is not None:
            queryBuscaProdutosEstoque += " AND descricao LIKE %s"
            parametros.append(f'%{nome}%')

            print(codigo)
        if codigo is not None:
            queryBuscaProdutosEstoque += " AND codigo_interno LIKE %s"
            parametros.append(f'%{codigo}%')

        queryBuscaProdutosEstoque += " ORDER BY descricao ASC"
        db.cursor.execute(queryBuscaProdutosEstoque, parametros)
        resultado = db.cursor.fetchall()

        return resultado
    



