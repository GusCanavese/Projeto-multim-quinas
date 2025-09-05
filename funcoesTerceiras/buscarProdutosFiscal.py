import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
from telas.telaVerProduto import telaVerProduto
from componentes import criaLabel, criaBotao
 
def buscarProdutosFiscal(self, frame, nome, cnpj, pagina=1):
    produtos = Buscas.buscaEstoqueProdutosFiscal(nome, cnpj)

    # Remove dados anteriores da tabela
    if hasattr(self, "dadosTelaVerProdutos"):
        for item in self.dadosTelaVerProdutos:
            item.destroy()
    self.dadosTelaVerProdutos = []

    # Calcula o intervalo de pedidos a mostrar
    inicioProduto = (pagina - 1) * 15
    fimProdutos = pagina * 15
    pedidosPagina = produtos[inicioProduto:fimProdutos]
    
    y = 0.18
    for rowProduto, produto in enumerate(pedidosPagina, start=1):
        corDeFundo = "#1C60A0" 


        dadosProduto = [produto[0], produto[10], produto[1], produto[6], produto[13]]



                        #nome      codiInterno  codBarras   codGrade      NCM         CST_A     valorVenda    custo    qtdEstoque     CFOP     estoque_MIN  estoque_MAX   CEST         cnpj
        dadosextras = [produto[0], produto[1], produto[2], produto[3], produto[4], produto[5], produto[6], produto[7], produto[8], produto[9], produto[10], produto[11], produto[12], produto[13]]




        x = 0.05
        for colNum, valor in enumerate(dadosProduto):
            if colNum == 0:
                label = criaLabel(frame, valor, x, y, 0.4, corDeFundo)
                x+=0.403
            elif colNum ==1:
                label = criaLabel(frame, valor, x, y, 0.04, corDeFundo)
                x+=0.043
            elif colNum ==2:
                label = criaLabel(frame, valor, x, y, 0.15, corDeFundo)
                x+=0.153
            elif colNum ==3:
                label = criaLabel(frame, valor, x, y, 0.10, corDeFundo)
                x+=0.103
            else:
                label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
                x+=0.178
            self.dadosTelaVerProdutos.append(label)


        btn = criaBotao(frame, "Ver", 0.95, y, 0.05, lambda p=dadosextras: telaVerProduto(self, p, 1))
        self.dadosTelaVerProdutos.append(btn) 

        y += 0.045

    # Adiciona botões de navegação se houver mais pedidos


    if len(produtos) > 10:
        
        params = {
            'nome': nome,
            'cnpj': cnpj,
            'pagina': pagina,
        }

        if pagina > 1:
            btnAnterior = criaBotao(frame, "← Anterior", 0.33, 0.85, 0.2, lambda p=params: buscarProdutosFiscal(self, frame, p['nome'], p['cnpj'], p['pagina']-1))
            self.dadosTelaVerProdutos.append(btnAnterior)

        if fimProdutos < len(produtos):
            btnProxima = criaBotao(frame, "Próximo →", 0.66, 0.85, 0.2, lambda p=params: buscarProdutosFiscal(self, frame, p['nome'], p['cnpj'], p['pagina']+1))
            self.dadosTelaVerProdutos.append(btnProxima)
