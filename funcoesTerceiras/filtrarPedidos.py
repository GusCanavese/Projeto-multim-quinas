import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from telas.telaVerPedidos import telaVerPedidos
import json

def filtrarPedidos(self, vendedor, numero, inicio, fim, checkbox, pagina=1):
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

    for rowPedido, pedido in enumerate(pedidos_pagina, start=1):
        if pedido[4] != "":
            corDeFundo = "#196F3D" 
            self.status = pedido[4]
        else:
            corDeFundo="#922B21"
            self.status="Não confirmado"

        dadosPedido = [pedido[0], pedido[2], pedido[1], pedido[3], self.status]
        
        dadosExtras = [pedido[5], pedido[6], pedido[7]]
        dadosDoProdutoDoPedido = json.loads(pedido[8])
        descricaoProdutos = [f"{produto['descricao']} {produto['quantidade']}" for produto in dadosDoProdutoDoPedido]

        # Cria os labels com os dados do pedido
        for colNum, valor in enumerate(dadosPedido):
            label = ctk.CTkLabel(self.frameParaVendasNoRelatorio, text=valor, width=150, fg_color=corDeFundo, anchor="center")
            label.grid(row=rowPedido, column=colNum, padx=2, pady=2)
            self.dadosTelaVerPedidos.append(label)

        # Cria botão na última coluna (coluna 5)
        def botaoVerDadosPedido(p=dadosPedido, d=dadosExtras, desc=descricaoProdutos):
            print("Pedido selecionado:", p)
            telaVerPedidos(self, p, d, desc)

        botao = ctk.CTkButton(self.frameParaVendasNoRelatorio, text="Ver", width=60, command=botaoVerDadosPedido)
        botao.grid(row=rowPedido, column=len(dadosPedido), padx=2, pady=2)
        self.dadosTelaVerPedidos.append(botao)

    # Adiciona botões de navegação se houver mais pedidos
    if len(pedidos) > 10:
        frame_navegacao = ctk.CTkFrame(self.frameParaVendasNoRelatorio)
        frame_navegacao.grid(row=12, column=0, columnspan=6, pady=5)
        self.dadosTelaVerPedidos.append(frame_navegacao)

        # Armazena os parâmetros em variáveis locais para usar nos callbacks
        params = {
            'vendedor': vendedor,
            'numero': numero,
            'inicio': inicio,
            'fim': fim,
            'checkbox': checkbox,
            'pagina': pagina
        }

        if pagina > 1:
            btn_anterior = ctk.CTkButton(
                frame_navegacao, 
                text="← Anterior", 
                width=100,
                command=lambda p=params: filtrarPedidos(self, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']-1)
            )
            btn_anterior.pack(side="left", padx=5)
            self.dadosTelaVerPedidos.append(btn_anterior)

        if fim_pedido < len(pedidos):
            btn_proximo = ctk.CTkButton(
                frame_navegacao, 
                text="Próximo →", 
                width=100,
                command=lambda p=params: filtrarPedidos(self, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']+1)
            )
            btn_proximo.pack(side="right", padx=5)
            self.dadosTelaVerPedidos.append(btn_proximo)