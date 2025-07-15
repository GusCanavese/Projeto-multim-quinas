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
    
    def buscaContasAReceber(valor, inicio, fim):
        queryBuscaCliente = """SELECT confirmado, vencimento, descricao, total, formaPag, qtdParcelas FROM contasareceber
        where
        confirmado like %s
        or vencimento like %s
        or descricao like %s
        or total like %s
        or formaPag like %s
        or qtdParcelas like %s"""
        if inicio:
            queryBuscaCliente = """SELECT confirmado, vencimento, descricao, total, formaPag, qtdParcelas FROM contasareceber
            where
            confirmado like %s
            or vencimento like %s
            or descricao like %s
            or total like %s
            or formaPag like %s
            or qtdParcelas like %s"""
            queryBuscaCliente += " AND vencimento BETWEEN %s AND %s"
            db.cursor.execute(queryBuscaCliente, (f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", inicio, fim))
        else:
            queryBuscaCliente = """SELECT confirmado, vencimento, descricao, total, formaPag, qtdParcelas FROM contasareceber
            where
            confirmado like %s
            or vencimento like %s
            or descricao like %s
            or total like %s
            or formaPag like %s
            or qtdParcelas like %s"""
            db.cursor.execute(queryBuscaCliente, (f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%",))
        resultado = db.cursor.fetchall()
        return resultado
    
    def buscaContasAPagar(valor, inicio, fim):
        print(inicio, fim)
         
        if inicio:
            queryBuscaCliente = """SELECT confirmado, data_vencimento, descricao,  valor_total, numero_nfe, emitente_nome FROM contasapagar
            where
            confirmado like %s
            or descricao like %s
            or valor_total like %s
            or numero_nfe like %s"""
            queryBuscaCliente += " AND data_vencimento BETWEEN %s AND %s"
            db.cursor.execute(queryBuscaCliente, (f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", inicio, fim))
        else:
            queryBuscaCliente = """SELECT confirmado, data_vencimento, descricao, valor_total, numero_nfe, emitente_nome, chave_nfe, serie_nfe, data_emissao, data_saida, emitente_cnpj, destinatario_cnpj, destinatario_nome, valor_produtos, valor_bc_icms, valor_icms, valor_icms_desonerado, valor_bc_icms_st, valor_icms_st, valor_ipi, valor_pis, valor_cofins, valor_bc_irrf, transportadora_cnpj, transportadora_nome, itens, data_registro FROM contasapagar
            where
            confirmado like %s
            or data_vencimento like %s
            or descricao like %s
            or valor_total like %s
            or numero_nfe like %s"""
            db.cursor.execute(queryBuscaCliente, (f"%{valor}%",f"%{valor}%",f"%{valor}%",f"%{valor}%",f"%{valor}%",))

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
