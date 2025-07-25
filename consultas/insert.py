import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import db
from tkinter import messagebox
import json



class Insere:


    def insereTransportadoraNoBanco(dados):
        colunas = list(dados.keys())
        valores = [f"'{str(valor)}'" for valor in dados.values()]
        query = f"INSERT INTO transportadoras ({', '.join(colunas)}) VALUES ({', '.join(valores)})"
        db.cursor.execute(query)
        db.conn.commit()



    def insereProdutosNoBanco(nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ):
        queryInserirProdutos = "INSERT INTO produtos(nome_do_produto, valor_de_custo, valor_de_venda, quantidade, codigo_interno, codigo_ncm, codigo_cfop, codigo_cest, origem_cst, descricao, CNPJ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        db.cursor.execute(queryInserirProdutos, (nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ,))
        db.conn.commit()
        messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")


    def insereUsuarioNoBanco(nome, cargo, login, senha):
        queryInserirFuncionario = "INSERT INTO funcionarios(nome, cargo, login, senha) VALUES(%s, %s, %s, %s);"
        db.cursor.execute(queryInserirFuncionario, (nome, cargo, login, senha,))
        db.conn.commit()
        messagebox.showinfo(title="Info", message="Registrado com Sucesso")
    

    def registraFornecedorNoBanco(dados):
        colunas = list(dados.keys())
        valores = [f"'{str(valor)}'" for valor in dados.values()]
        query = f"INSERT INTO fornecedores ({', '.join(colunas)}) VALUES ({', '.join(valores)})"
        db.cursor.execute(query)
        db.conn.commit()



    def insereClienteNoBanco(nome, cpf, cnpj, IE, RG, CEP, rua, numero, bairro, cidade, estado, referencia, telefone):
        queryInserirCliente = "INSERT INTO clientes(nome, cpf, cnpj, IE, RG, CEP, rua, numero, bairro, cidade, estado, referencia, telefone) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        db.cursor.execute(queryInserirCliente, (nome, cpf, cnpj, IE, RG, CEP, rua, numero, bairro, cidade, estado, referencia, telefone, ))
        db.conn.commit()
        messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")


    def registraFaturamentoNoBanco(confirmado, vencimento, descricao, total, formaPag, qtdParcelas):
        queryInserirCliente = "INSERT INTO contasareceber(confirmado, vencimento, descricao, total, formaPag, qtdParcelas) VALUES(%s, %s, %s, %s, %s, %s);"
        db.cursor.execute(queryInserirCliente, (confirmado, vencimento, descricao, total, formaPag, qtdParcelas))
        db.conn.commit()

    
    def registraPedidoNoBanco(dadosPedido):     
        itens_json = json.dumps(dadosPedido['itens'])

        db.cursor.execute("""INSERT INTO pedidos (
                numero_recibo, data_emissao, data_confirmacao, destinatario,
                cpf, cnpj, telefone, endereco, referencia, cep, vendedor,
                frete, valor_total, total_subtotal, total_acrescimo,
                total_desc_real, total_desc_porc,
                subtotal, itens
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
            (
                dadosPedido['numero_recibo'],
                dadosPedido['data_emissao'],
                dadosPedido.get('data_confirmacao', ''),
                dadosPedido['destinatario'],
                dadosPedido.get('cpf', ''),
                dadosPedido.get('cnpj', ''),
                dadosPedido.get('telefone', ''),
                dadosPedido['endereco'],
                dadosPedido.get('referencia', ''),
                dadosPedido.get('cep', ''),
                dadosPedido.get('vendedor', ''),
                float(dadosPedido.get('frete', 0.0) or 0.0),
                float(dadosPedido.get('valor_total') or 0.0),
                float(dadosPedido.get('total_subtotal') or 0.0),
                float(dadosPedido.get('total_acrescimo') or 0.0),
                float(dadosPedido.get('total_desc_real') or 0.0),
                float(dadosPedido.get('total_desc_porc') or 0.0),
                # int(dadosPedido.get('total_quantidade') or 0),
                float(dadosPedido.get('subtotal') or 0.0),
                itens_json
            )
        )

        db.conn.commit()

    def inserir_nota_fiscal(chave_nfe, numero_nfe, serie_nfe, data_emissao, data_saida,
                       emitente_cnpj, emitente_nome, destinatario_cnpj, destinatario_nome,
                       valor_total, valor_produtos, valor_bc_icms, valor_icms,
                       valor_icms_desonerado, valor_bc_icms_st, valor_icms_st,
                       valor_ipi, valor_pis, valor_cofins, valor_bc_irrf,
                       transportadora_cnpj, transportadora_nome, itens_json, data_vencimento):
        
        resposta = messagebox.askquestion("Aviso", "Você tem certeza que deseja inserir essa nota fiscal?")
        if resposta == 'yes':
            descricao = f"lançamento referente a nota {numero_nfe}, com o fornecedor {emitente_nome}"
            confirmado = "Não"

            query = """INSERT INTO contasapagar (
                chave_nfe, numero_nfe, serie_nfe, data_emissao, data_saida,
                emitente_cnpj, emitente_nome, destinatario_cnpj, destinatario_nome,
                valor_total, valor_produtos, valor_bc_icms, valor_icms,
                valor_icms_desonerado, valor_bc_icms_st, valor_icms_st,
                valor_ipi, valor_pis, valor_cofins, valor_bc_irrf,
                transportadora_cnpj, transportadora_nome, itens, data_vencimento, confirmado, descricao 
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            
            dados = (
                chave_nfe, numero_nfe, serie_nfe, data_emissao, data_saida,
                emitente_cnpj, emitente_nome, destinatario_cnpj, destinatario_nome,
                valor_total, valor_produtos, valor_bc_icms, valor_icms,
                valor_icms_desonerado, valor_bc_icms_st, valor_icms_st,
                valor_ipi, valor_pis, valor_cofins, valor_bc_irrf,
                transportadora_cnpj, transportadora_nome, itens_json, data_vencimento, confirmado, descricao, 
            )
            
            db.cursor.execute(query, dados)
            db.conn.commit()
            messagebox.showinfo("Sucesso", "Nota fiscal inserida com sucesso!")


        else:
            pass
        