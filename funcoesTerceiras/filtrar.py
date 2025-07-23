import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
from datetime import datetime
import tkinter as tk
from telas.telaVerPedidos import telaVerPedidos
from telas.telaVercontasApagar import telaVercontasApagar
from telas.telaVer import telaVer
import json
from componentes import criaLabel, criaBotao

def filtrarPedidos(self, frame, vendedor, numero, inicio, fim, checkbox, pagina=1):
    pedidos = Buscas.buscaPedidos(vendedor, numero, inicio, fim, checkbox)

    # Remove dados anteriores da tabela
    if hasattr(self, "dadosTelaVerPedidos"):
        for item in self.dadosTelaVerPedidos:
            item.destroy()
    self.dadosTelaVerPedidos = []

    # Calcula o intervalo de pedidos a mostrar
    inicio_pedido = (pagina - 1) * 10
    fim_pedido = pagina * 10
    pedidos_pagina = pedidos[inicio_pedido:fim_pedido]

    y = 0.12
    for rowPedido, pedido in enumerate(pedidos_pagina, start=1):
        if pedido[4] != "":
            corDeFundo = "#196F3D" 
            self.status = pedido[4]
        else:
            corDeFundo = "#922B21"
            self.status = "Não confirmado"

        dadosPedido = [pedido[0], pedido[5], pedido[2], pedido[1], pedido[3], self.status]
        dadosExtras = [pedido[5], pedido[6], pedido[7]]

        dadosDoProdutoDoPedido = json.loads(pedido[8])
        descricaoProdutos = [f"{produto['descricao']} {produto['quantidade']}" for produto in dadosDoProdutoDoPedido]

        x = 0.03
        for colNum, valor in enumerate(dadosPedido):
            if colNum == 0:
                label = criaLabel(frame, valor, x, y, 0.05, corDeFundo)
                x += 0.055
                self.dadosTelaVerPedidos.append(label)
            elif colNum == 1:
                label = criaLabel(frame, valor, x, y, 0.15, corDeFundo)
                x += 0.155
                self.dadosTelaVerPedidos.append(label)
            elif colNum == 2:
                label = criaLabel(frame, valor, x, y, 0.15, corDeFundo)
                x += 0.155
                self.dadosTelaVerPedidos.append(label)
            else:
                label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
                x += 0.175
                self.dadosTelaVerPedidos.append(label)

        btn = criaBotao(frame, "Ver", 0.94, y, 0.05, lambda p=dadosPedido, d=dadosExtras, desc=descricaoProdutos: telaVerPedidos(self, p, d, desc))
        self.dadosTelaVerPedidos.append(btn)

        y += 0.07

    # Adiciona botões de navegação se houver mais pedidos
    if len(pedidos) > 10:
        params = {
            'vendedor': vendedor,
            'numero': numero,
            'inicio': inicio,
            'fim': fim,
            'checkbox': checkbox,
            'pagina': pagina
        }

        if pagina > 1:
            btnAnterior = criaBotao(frame, "← Anterior", 0.33, 1, 0.2, lambda p=params: filtrarPedidos(self, frame, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']-1))
            self.dadosTelaVerPedidos.append(btnAnterior)

        if fim_pedido < len(pedidos):
            btnProxima = criaBotao(frame, "Próximo →", 0.66, 1, 0.2, lambda p=params: filtrarPedidos(self, frame, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']+1))
            self.dadosTelaVerPedidos.append(btnProxima)






def filtrarContas(self, frame, valor, pagina=1):
    if hasattr(self, "datePickerInicio") and hasattr(self, "datePickerFim"):
        inicio = self.datePickerInicio.get()
        fim = self.datePickerFim.get()
        inicio = datetime.strptime(inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
        fim = datetime.strptime(fim, "%d/%m/%Y").strftime("%Y-%m-%d")
    else:
        inicio = None
        fim = None

    contasReceber = Buscas.buscaContasAReceber(valor, inicio, fim)
    contasPagar = Buscas.buscaContasAPagar(valor, inicio, fim)
    contas = contasReceber + contasPagar



    if hasattr(self, "dadosTelaFiltrarContas"):
        for item in self.dadosTelaFiltrarContas:
            item.destroy()
    self.dadosTelaFiltrarContas = []

    inicioContas = (pagina - 1) * 10
    fimContas = pagina * 10
    contasPagina = contas[inicioContas:fimContas]
    
    y = 0.1

    for rowProduto, conta in enumerate(contasPagina, start=1):
        corDeFundo = "#1C60A0"
        dadosProduto = [conta[0], conta[2], conta[1], conta[3], conta[4]]
        try:
            datetime.strptime(conta[1], "%d/%m/%Y")
        except:
            dataOriginal = dadosProduto[2]
            dataOriginal = str(dataOriginal)
            try:
                dataFormatada = datetime.strptime(dataOriginal, "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                dataFormatada = datetime.strptime(dataOriginal, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
            dadosProduto[2] = dataFormatada

        x = 0.03


        for colNum, valor in enumerate(dadosProduto):
            if colNum == 0:
                if "Não" in conta[0]:
                    corDeFundo = "#922B21"
                elif "Sim" in conta[2]:
                    corDeFundo = "#196F3D"
                label = criaLabel(frame, valor, x, y, 0.08, corDeFundo)
                x+=0.085
            elif colNum ==1:
                corDeFundo = "#1C60A0"
                label = criaLabel(frame, valor, x, y, 0.4, corDeFundo)
                x+=0.405
            elif colNum ==2:
                corDeFundo = "#1C60A0"
                label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
                x+=0.175
            elif colNum ==3:
                if "lançamento referente a nota" in conta[2]:
                    valor1 = conta[3]
                    valor1 = valor *-1
                    corDeFundo = "#922B21"
                    label = criaLabel(frame, valor1, x, y, 0.17, corDeFundo)
                if "lançamento referente ao pedido" in conta[2]:
                    corDeFundo = "#196F3D" 
                    label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
                
                x+=0.175

            self.dadosTelaFiltrarContas.append(label)

        btn = criaBotao(frame, "Ver", 0.937, y, 0.05, lambda p=conta: telaVercontasApagar(self, p))
        self.dadosTelaFiltrarContas.append(btn)

        y += 0.06
    
    if len(contas) > 10:

        
        params = {
            'pagina': pagina,
        }

        if pagina > 1:
            btnAnterior = criaBotao(frame, "← Anterior", 0.33, 0.6, 0.2, lambda p=params: filtrarContas(self, frame, p['pagina']-1))
            self.dadosTelaFiltrarContas.append(btnAnterior)

        if fimContas < len(contas):
            btnProxima = criaBotao(frame, "Próximo →", 0.66, 0.6, 0.2, lambda p=params: filtrarContas(self, frame, p['pagina']+1))
            self.dadosTelaFiltrarContas.append(btnProxima)






def filtrarFuncionarios(self, frame, valor, pagina=1):
    
    funcionarios = Buscas.buscaFuncionarios(valor)

    if hasattr(self, "dadosTelaFiltrarFunc"):
        for item in self.dadosTelaFiltrarFunc:
            item.destroy()
    self.dadosTelaFiltrarFunc = []

    iniciofunc = (pagina - 1) * 10
    fimfunc = pagina * 10
    contasPagina = funcionarios[iniciofunc:fimfunc]
    
    y = 0.1

    for row, funcionarios in enumerate(contasPagina, start=1):
        corDeFundo = "#1C60A0"
        dadosProduto = [funcionarios[0], funcionarios[1]]

        x = 0.03

        for colNum, valor in enumerate(dadosProduto):
            corDeFundo = "#1C60A0"
            label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
            self.dadosTelaFiltrarFunc.append(label)
            x+=0.175


        btn = criaBotao(frame, "Ver", 0.937, y, 0.05, lambda p=dadosProduto: telaVer(self, p))
        self.dadosTelaFiltrarFunc.append(btn)

        y += 0.059