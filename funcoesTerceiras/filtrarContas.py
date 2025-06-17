import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from telas.telaVerPedidos import telaVerPedidos
import json
from componentes import criaLabel, criaBotao

def filtrarContas():
    contas = Buscas.buscaPedidos(vendedor, numero, inicio, fim, checkbox)

    # Remove dados anteriores da tabela
    if hasattr(self, "dadosTelaVerPedidos"):
        for item in self.dadosTelaVerPedidos:
            item.destroy()
    self.dadosTelaVerPedidos = []

    # Calcula o intervalo de pedidos a mostrar
    inicio_pedido = (pagina - 1) * 10
    fim_pedido = pagina * 10
    pedidos_pagina = pedidos[inicio_pedido:fim_pedido]

    y = 0.1
    for rowPedido, pedido in enumerate(pedidos_pagina, start=1):
        if pedido[4] != "":
            corDeFundo = "#196F3D" 
            self.status = pedido[4]
        else:
            corDeFundo = "#922B21"
            self.status = "Não confirmado"

        dadosPedido = [pedido[0], pedido[2], pedido[1], pedido[3], self.status]
        dadosExtras = [pedido[5], pedido[6], pedido[7]]

        dadosDoProdutoDoPedido = json.loads(pedido[8])
        descricaoProdutos = [f"{produto['descricao']} {produto['quantidade']}" for produto in dadosDoProdutoDoPedido]

        x = 0.03
        for colNum, valor in enumerate(dadosPedido):
            label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
            x += 0.175
            self.dadosTelaVerPedidos.append(label)

        btn = criaBotao(frame, "Ver", 0.927, y, 0.05, lambda p=dadosPedido, d=dadosExtras, desc=descricaoProdutos: telaVerPedidos(self, p, d, desc))
        self.dadosTelaVerPedidos.append(btn)

        y += 0.045

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
            btnAnterior = criaBotao(frame, "← Anterior", 0.33, 0.6, 0.2, lambda p=params: filtrarPedidos(self, frame, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']-1))
            self.dadosTelaVerPedidos.append(btnAnterior)

        if fim_pedido < len(pedidos):
            btnProxima = criaBotao(frame, "Próximo →", 0.66, 0.6, 0.2, lambda p=params: filtrarPedidos(self, frame, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']+1))
            self.dadosTelaVerPedidos.append(btnProxima)