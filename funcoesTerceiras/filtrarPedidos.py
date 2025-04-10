import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from telas.telaVerPedidos import telaVerPedidos

def filtrarPedidos(self, vendedor, numero, inicio, fim, checkbox):
    pedidos = Buscas.buscaPedidos(vendedor, numero, inicio, fim, checkbox)

    # Remove dados anteriores da tabela
    if hasattr(self, "dados"):
        for item in self.dados:
            item.destroy()
    self.dados = []

    for rowPedido, pedido in enumerate(pedidos, start=1):
        corDeFundo = "#196F3D" if pedido[4] != "" else "#922B21"
        status = pedido[4] if pedido[4] != "" else "Não confirmado"

        dadosPedido = [pedido[0], pedido[2], pedido[1], pedido[3], status]

        # Cria os labels com os dados do pedido
        for colNum, valor in enumerate(dadosPedido):
            label = ctk.CTkLabel( self.frameParaVendasNoRelatorio, text=valor, width=150, fg_color=corDeFundo, anchor="center" )
            label.grid(row=rowPedido, column=colNum, padx=2, pady=2)
            self.dados.append(label)

        # Cria botão na última coluna (coluna 5)
        def botaoVerDadosPedido(p=dadosPedido):
            print("Pedido selecionado:", p)
            telaVerPedidos(self)
            

        botao = ctk.CTkButton( self.frameParaVendasNoRelatorio, text="Ver", width=60, command=botaoVerDadosPedido)
        botao.grid(row=rowPedido, column=len(dadosPedido), padx=2, pady=2)
        self.dados.append(botao)
