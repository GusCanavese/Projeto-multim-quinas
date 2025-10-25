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
        queryBuscaCliente = "SELECT nome, cpf, cnpj, telefone, cep, cidade, referencia, numero, bairro, rua FROM clientes WHERE nome LIKE %s ORDER BY nome"
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
        if checkbox and inicio and fim:
            if vendedor != "Todos":
                queryBuscaPedidos = """SELECT numero_recibo, data_emissao, vendedor, subtotal, data_confirmacao, 
                                    destinatario, cpf, endereco, itens FROM pedidos 
                                WHERE
                                    data_emissao BETWEEN %s AND %s
                                    AND vendedor LIKE %s
                                    AND (
                                        destinatario LIKE %s
                                        numero_recibo LIKE %s
                                        OR subtotal LIKE %s
                                    ) 
                                ORDER BY numero_recibo ASC"""
                parametros = (inicio, fim, f"%{vendedor}%", f"%{numero}%", f"%{numero}%")
            else:
                queryBuscaPedidos = """SELECT numero_recibo, data_emissao, vendedor, subtotal, data_confirmacao,
                                    destinatario, cpf, endereco, itens FROM pedidos 
                                WHERE 
                                    data_emissao BETWEEN %s AND %s
                                    AND (
                                        destinatario LIKE %s
                                        OR vendedor LIKE %s
                                        OR numero_recibo LIKE %s
                                        OR subtotal LIKE %s
                                    )
                                ORDER BY numero_recibo ASC"""
                parametros = (inicio, fim, f"%{numero}%", f"%{numero}%", f"%{numero}%", f"%{numero}%")
        else:
            if vendedor != "Todos":
                queryBuscaPedidos = """SELECT numero_recibo, data_emissao, vendedor, subtotal, data_confirmacao,
                                    destinatario, cpf, endereco, itens FROM pedidos 
                                WHERE
                                    vendedor LIKE %s
                                    AND (
                                        destinatario LIKE %s
                                        OR numero_recibo LIKE %s
                                        OR subtotal LIKE %s
                                    )
                                ORDER BY numero_recibo ASC"""
                parametros = (f"%{vendedor}%", f"%{numero}%", f"%{numero}%", f"%{numero}%")
            else:
                queryBuscaPedidos = """SELECT numero_recibo, data_emissao, vendedor, subtotal, data_confirmacao,
                                    destinatario, cpf, endereco, itens FROM pedidos 
                                WHERE 
                                    destinatario LIKE %s
                                    OR vendedor LIKE %s
                                    OR numero_recibo LIKE %s
                                    OR subtotal LIKE %s
                                ORDER BY numero_recibo ASC"""
                parametros = (f"%{numero}%", f"%{numero}%", f"%{numero}%", f"%{numero}%")

        db.cursor.execute(queryBuscaPedidos, parametros)
        resultado = db.cursor.fetchall()
        return resultado

    def buscaEstoqueProdutos(valor, cnpj):
        if cnpj == "Todos":
            queryBuscaProdutosEstoque = """SELECT quantidade, descricao, codigo_interno, valor_de_venda, CNPJ, codigo_ncm, codigo_cfop, codigo_cest, valor_de_venda, valor_de_custo, origem_cst, nome_do_produto, marca, valor_de_custo, id FROM produtos 
            WHERE 
                descricao like %s
                or CNPJ like %s
                or quantidade like %s
                or nome_do_produto like %s
                or codigo_interno like %s
                or valor_de_venda like %s
                or marca like %s
                ORDER BY descricao ASC"""
            db.cursor.execute(queryBuscaProdutosEstoque, (f"%{valor}%", f"%{cnpj}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%"))
        else:
            queryBuscaProdutosEstoque = """SELECT quantidade, descricao, codigo_interno, valor_de_venda, CNPJ, codigo_ncm, codigo_cfop, codigo_cest, valor_de_venda, valor_de_custo, origem_cst, nome_do_produto, marca, valor_de_custo, id FROM produtos 
            WHERE 
                CNPJ like %s
                    AND (
                        descricao LIKE %s
                        OR quantidade LIKE %s
                        OR nome_do_produto LIKE %s
                        OR codigo_interno LIKE %s
                        OR valor_de_venda LIKE %s
                        OR marca LIKE %s
                    )
                ORDER BY descricao ASC"""
            db.cursor.execute(queryBuscaProdutosEstoque, (cnpj, f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%"))

        
        resultado = db.cursor.fetchall()

        return resultado
    

    def buscaEstoqueProdutosFiscal(valor, cnpj):
        if cnpj == "Todos":
            queryBuscaProdutosEstoque = """SELECT ﻿descricao_do_produto, cadigo_interno, codigo_de_barras, codigo_grade, codigo_NCM, CST_A, valor_venda, custo, quantidade_em_estoque, CFOP, estoque_MIN, estoque_MAX, CEST, cnpj FROM produtos_fiscal
            WHERE 
                ﻿descricao_do_produto LIKE %s
                OR cadigo_interno LIKE %s
                OR codigo_de_barras LIKE %s
                OR codigo_grade LIKE %s
                OR codigo_NCM LIKE %s
                OR CST_A LIKE %s
                OR valor_venda LIKE %s
                OR custo LIKE %s
                OR quantidade_em_estoque LIKE %s
                OR CFOP LIKE %s
                OR estoque_MIN LIKE %s
                OR estoque_MAX LIKE %s
                OR CEST LIKE %s
                ORDER BY ﻿descricao_do_produto ASC"""
            db.cursor.execute(queryBuscaProdutosEstoque, (f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%"))
        else:
            queryBuscaProdutosEstoque = """SELECT ﻿descricao_do_produto, cadigo_interno, codigo_de_barras, codigo_grade, codigo_NCM, CST_A, valor_venda, custo, quantidade_em_estoque, CFOP, estoque_MIN, estoque_MAX, CEST, cnpj FROM produtos_fiscal
            WHERE 
                CNPJ like %s
                    AND (
                        ﻿descricao_do_produto LIKE %s
                        OR cadigo_interno LIKE %s
                        OR codigo_de_barras LIKE %s
                        OR codigo_grade LIKE %s
                        OR codigo_NCM LIKE %s
                        OR CST_A LIKE %s
                        OR valor_venda LIKE %s
                        OR custo LIKE %s
                        OR quantidade_em_estoque LIKE %s
                        OR CFOP LIKE %s
                        OR estoque_MIN LIKE %s
                        OR estoque_MAX LIKE %s
                        OR CEST LIKE %s
                    )
                ORDER BY ﻿descricao_do_produto ASC"""
            db.cursor.execute(queryBuscaProdutosEstoque, (cnpj, f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%", f"%{valor}%"))

        
        resultado = db.cursor.fetchall()

        return resultado



    def buscaFuncionarios(valor):
        queryBuscaFuncionarios = """SELECT nome, cargo FROM funcionarios 
        WHERE 
            nome LIKE %s
            OR cargo LIKE %s"""
        db.cursor.execute(queryBuscaFuncionarios, (f"%{valor}%", f"%{valor}%"))
        resultado = db.cursor.fetchall()
        return resultado
    
    def buscaClientesFiscal(nome, cnpj):
        if cnpj:
            cnpj = cnpj.strip()
            cnpj_limpo = cnpj.replace('.', '').replace('/', '').replace('-', '')

            queryBuscaClientes = """SELECT nome_razao_social, CPF_CNPJ, inscricao_estadual, Logradouro, Numero, CEP, Bairro, Cidade, Estado
            FROM clientes_fiscal 
                WHERE 
                    REPLACE(REPLACE(REPLACE(CPF_CNPJ, '.', ''), '/', ''), '-', '') LIKE %s"""

            db.cursor.execute(queryBuscaClientes, (f"{cnpj_limpo}%",))
            resultado = db.cursor.fetchall()
            return resultado
        
        elif nome:
            queryBuscaClientes = """SELECT nome_razao_social, CPF_CNPJ, inscricao_estadual, Logradouro, Numero, CEP, Bairro, Cidade, Estado
            FROM clientes_fiscal 
                WHERE 
                    nome_razao_social LIKE %s"""

            db.cursor.execute(queryBuscaClientes, (f"{nome}%",))
            resultado = db.cursor.fetchall()
            return resultado
        else:
            queryBuscaClientes = """SELECT nome_razao_social, CPF_CNPJ, inscricao_estadual, Logradouro, Numero, CEP, Bairro, Cidade, Estado
            FROM clientes_fiscal 
                WHERE 
                    nome_razao_social OR CPF_CNPJ LIKE "%%" """

            db.cursor.execute(queryBuscaClientes)
            resultado = db.cursor.fetchall()
            return resultado