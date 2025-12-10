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
            corDeFundo = self.corAfirma
            self.status = pedido[4]
        else:
            corDeFundo = self.corNegado
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
            btnAnterior = criaBotao(frame, "← Anterior", 0.33, 0.9, 0.2, lambda p=params: filtrarPedidos(self, frame, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']-1))
            self.dadosTelaVerPedidos.append(btnAnterior)

        if fim_pedido < len(pedidos):
            btnProxima = criaBotao(frame, "Próximo →", 0.66, 0.9, 0.2, lambda p=params: filtrarPedidos(self, frame, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']+1))
            self.dadosTelaVerPedidos.append(btnProxima)


def _aplicar_filtro_periodo(self):
    if hasattr(self, "datePickerInicio") and hasattr(self, "datePickerFim"):
        inicio = self.datePickerInicio.get()
        fim = self.datePickerFim.get()
        inicio = datetime.strptime(inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
        fim = datetime.strptime(fim, "%d/%m/%Y").strftime("%Y-%m-%d")
    else:
        inicio = None
        fim = None
    return inicio, fim


def _renderizar_contas(self, frame, contas, pagina, atributo_lista):
    if hasattr(self, atributo_lista):
        for item in getattr(self, atributo_lista):
            item.destroy()
    setattr(self, atributo_lista, [])

    inicio_contas = (pagina - 1) * 10
    fim_contas = pagina * 10
    contas_pagina = contas[inicio_contas:fim_contas]

    y = 0.1

    for conta in contas_pagina:
        corDeFundo = "#1C60A0"
        dadosContas = [conta[0], conta[2], conta[1], conta[3]]
        x = 0.03

        for colNum, valor in enumerate(dadosContas):
            if colNum == 0:
                if "Não" in conta[0]:
                    corDeFundo = self.corNegado
                elif "Sim" in conta[0]:
                    corDeFundo = self.corAfirma
                label = criaLabel(frame, valor, x, y, 0.08, corDeFundo)
                x += 0.085
            elif colNum == 1:
                corDeFundo = "#1C60A0"
                label = criaLabel(frame, valor, x, y, 0.4, corDeFundo)
                x += 0.405
            elif colNum == 2:
                corDeFundo = "#1C60A0"
                label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
                x += 0.175
            elif colNum == 3:
                if "lançamento referente a nota" in conta[2]:
                    valor_ajustado = valor * -1
                    corDeFundo = self.corNegado
                    label = criaLabel(frame, valor_ajustado, x, y, 0.17, corDeFundo)
                else:
                    corDeFundo = self.corAfirma
                    label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
                x += 0.175

            getattr(self, atributo_lista).append(label)

        btn = criaBotao(frame, "Ver", 0.937, y, 0.05, lambda p=conta: telaVercontasApagar(self, p))
        getattr(self, atributo_lista).append(btn)

        y += 0.06

    if len(contas) > 10:
        if pagina > 1:
            btnAnterior = criaBotao(frame, "← Anterior", 0.33, 0.75, 0.2, lambda: _renderizar_contas(self, frame, contas, pagina - 1, atributo_lista))
            getattr(self, atributo_lista).append(btnAnterior)

        if fim_contas < len(contas):
            btnProxima = criaBotao(frame, "Próximo →", 0.66, 0.75, 0.2, lambda: _renderizar_contas(self, frame, contas, pagina + 1, atributo_lista))
            getattr(self, atributo_lista).append(btnProxima)


def filtrarContasAReceber(self, frame, valor, inicio=None, pagina=1):
    self.valorAtualFiltroContas = valor
    inicio, fim = _aplicar_filtro_periodo(self)
    contas = Buscas.buscaContasAReceber(valor, inicio, fim)
    _renderizar_contas(self, frame, contas, pagina, "dadosTelaFiltrarContasReceber")


def filtrarContasAPagar(self, frame, valor, inicio=None, pagina=1):
    self.valorAtualFiltroContas = valor
    inicio, fim = _aplicar_filtro_periodo(self)
    contas = Buscas.buscaContasAPagar(valor, inicio, fim)
    _renderizar_contas(self, frame, contas, pagina, "dadosTelaFiltrarContasPagar")


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
        dadosContas = [funcionarios[0], funcionarios[1]]

        x = 0.03

        for colNum, valor in enumerate(dadosContas):
            corDeFundo = "#1C60A0"
            label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
            self.dadosTelaFiltrarFunc.append(label)
            x+=0.175


        btn = criaBotao(frame, "Ver", 0.937, y, 0.05, lambda p=dadosContas: telaVer(self, p))
        self.dadosTelaFiltrarFunc.append(btn)

        y += 0.059


def filtrarNotasFiscais(self, frame, valor, pagina=1):
    notas = Buscas.buscaNotasFiscais(valor)

    if hasattr(self, "dadosTelaFiltrarFunc"):
        for item in self.dadosTelaFiltrarFunc:
            item.destroy()
    self.dadosTelaFiltrarFunc = []

    iniciofunc = (pagina - 1) * 10
    fimfunc = pagina * 10
    contasPagina = notas[iniciofunc:fimfunc]

    totalNotas = len(notas)
    mostrarPaginacao = totalNotas > 10
    temProxima = fimfunc < totalNotas
    filtro_valor = valor

    y = 0.1

    for row, notas in enumerate(contasPagina, start=1):
        corDeFundo = "#1C60A0"
        dadosContas = [notas[0], notas[1], notas[2], notas[3], notas[4], notas[5], notas[6], notas[7], notas[8]]

        x = 0.03

        for colNum, valor in enumerate(dadosContas):
            if colNum == 0:
                corDeFundo = "#1C60A0"
                label = criaLabel(frame, valor, x, y, 0.07, corDeFundo)
                self.dadosTelaFiltrarFunc.append(label)
                x += 0.075
            elif colNum == 1 or colNum == 2:
                corDeFundo = "#1C60A0"
                label = criaLabel(frame, valor, x, y, 0.05, corDeFundo)
                self.dadosTelaFiltrarFunc.append(label)
                x += 0.055
            elif colNum == 3:
                corDeFundo = "#1C60A0"
                label = criaLabel(frame, valor, x, y, 0.2, corDeFundo)
                self.dadosTelaFiltrarFunc.append(label)
                x += 0.205
            elif colNum == 4:
                corDeFundo = "#1C60A0"
                label = criaLabel(frame, valor, x, y, 0.05, corDeFundo)
                self.dadosTelaFiltrarFunc.append(label)
                x += 0.055
            else:
                corDeFundo = "#1C60A0"
                label = criaLabel(frame, valor, x, y, 0.1, corDeFundo)
                self.dadosTelaFiltrarFunc.append(label)
                x += 0.105

        btn = criaBotao(frame, "Ver", 0.937, y, 0.05, lambda p=dadosContas: telaVer(self, p))
        self.dadosTelaFiltrarFunc.append(btn)

        y += 0.059

    if mostrarPaginacao:
        if pagina > 1:
            btnAnterior = criaBotao(
                frame, "← Anterior", 0.33, 0.9, 0.2,
                lambda v=filtro_valor: filtrarNotasFiscais(self, frame, v, pagina - 1)
            )
            self.dadosTelaFiltrarFunc.append(btnAnterior)

        if temProxima:
            btnProxima = criaBotao(
                frame, "Próximo →", 0.66, 0.9, 0.2,
                lambda v=filtro_valor: filtrarNotasFiscais(self, frame, v, pagina + 1)
            )
            self.dadosTelaFiltrarFunc.append(btnProxima)
