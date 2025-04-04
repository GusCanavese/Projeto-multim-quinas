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
    
    def buscaPedidos():
        queryBuscaPedidos = "SELECT numero_recibo, data_emissao, vendedor, subtotal FROM pedidos"
        db.cursor.execute(queryBuscaPedidos)
        resultado = db.cursor.fetchall()
        return resultado


