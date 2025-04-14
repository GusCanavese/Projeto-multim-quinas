import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from telas.telaVerPedidos import telaVerPedidos
import json

def filtrarPedidos(self, vendedor, numero, inicio, fim, checkbox):
    pedidos = Buscas.buscaPedidos(vendedor, numero, inicio, fim, checkbox)

    # Remove dados anteriores da tabela
    if hasattr(self, "dadosTelaVerPedidos"):
        for item in self.dadosTelaVerPedidos:
            item.destroy()
    # else:
    #     pass
    self.dadosTelaVerPedidos = []

    for rowPedido, pedido in enumerate(pedidos, start=1):
        if pedido[4] != "":
            corDeFundo = "#196F3D" 
            self.status = pedido[4]

        else:
            corDeFundo="#922B21"
            self.status="Não confirmado"



        dadosPedido = [pedido[0], pedido[2], pedido[1], pedido[3], self.status]
        dadosExtras = [pedido[5], pedido[6], pedido[7]]
        dadosDoProdutoDoPedido = json.loads(pedido[8])
        dadosDoProdutoDoPedidoLista = [dadosDoProdutoDoPedido[0]['descricao']]

        

        # Cria os labels com os dados do pedido
        for colNum, valor in enumerate(dadosPedido):
            label = ctk.CTkLabel( self.frameParaVendasNoRelatorio, text=valor, width=150, fg_color=corDeFundo, anchor="center" )
            label.grid(row=rowPedido, column=colNum, padx=2, pady=2)
            self.dadosTelaVerPedidos.append(label)

        # Cria botão na última coluna (coluna 5)
        def botaoVerDadosPedido(p=dadosPedido, d=dadosExtras, dl=dadosDoProdutoDoPedidoLista):
            print("Pedido selecionado:", p)
            telaVerPedidos(self, p, d, dl)
            
            

        botao = ctk.CTkButton( self.frameParaVendasNoRelatorio, text="Ver", width=60, command=botaoVerDadosPedido)
        botao.grid(row=rowPedido, column=len(dadosPedido), padx=2, pady=2)
        self.dadosTelaVerPedidos.append(botao)
