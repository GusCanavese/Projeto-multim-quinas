import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import db
from tkinter import messagebox
import gc



class Insere():


    def insereTransportadoraNoBanco(colunas, valores):
        query = f"INSERT INTO transportadoras ({', '.join(colunas)}) VALUES ({', '.join(valores)})"
        db.cursor.execute(query)
        db.conn.commit()
        messagebox.showinfo("Sucesso", "A transportadora foi cadastrado com sucesso!")


    def insereProdutosNoBanco(nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ):
        queryInserirProdutos = "INSERT INTO produtos(nome_do_produto, valor_de_custo, valor_de_venda, quantidade, codigo_interno, codigo_ncm, codigo_cfop, codigo_cest, origem_cst, descricao, CNPJ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        db.cursor.execute(queryInserirProdutos, (nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ,))
        db.conn.commit()
        messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")


    def insereUsuarioNoBanco(nome, cargo, login, senha):
        queryInserirFuncionario = "INSERT INTO funcionarios(nome, cargo, login, senha) VALUES(%s, %s, %s, %s);"
        db.cursor.execute(queryInserirFuncionario, (nome, cargo, login, senha,))
        db.conn.commit()
        messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")
    

    def registraFornecedorNoBanco(colunas, valores):
        query = f"INSERT INTO fornecedores ({', '.join(colunas)}) VALUES ({', '.join(valores)})"
        print("Query gerada:", query)
        db.cursor.execute(query)
        db.conn.commit()
        messagebox.showinfo("Sucesso", "O fornecedor foi cadastrado com sucesso!")