import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from tkcalendar import DateEntry


def filtrarPedidos(self, vendedor, numero, inicio, fim, checkbox):
    print(checkbox)
    pedidos = Buscas.buscaPedidos(vendedor, numero, inicio, fim, checkbox)

    if hasattr(self, "dados"):
        for self.labelDadosPedido in self.dados:
            self.labelDadosPedido.destroy()
            print("entrou")
        self.dados=[]


    print(pedidos)

    self.dados=[]
    
    for rowPedido, pedido in enumerate(pedidos, start=1):
        self.valores = [
            pedido[0], 
            pedido[2],
            pedido[1],
            pedido[3]   
        ]

        for colNum, valor in enumerate(self.valores):
            self.labelDadosPedido = ctk.CTkLabel(self.frameParaVendasNoRelatorio, text=valor, width=150, fg_color="#38343c", anchor="center")
            self.labelDadosPedido.grid(row=rowPedido, column=colNum, padx=2, pady=2)
            self.dados.append(self.labelDadosPedido)
            
