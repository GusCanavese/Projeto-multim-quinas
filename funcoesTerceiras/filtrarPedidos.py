import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from tkcalendar import DateEntry

def filtrarPedidos(self, vendedor, numero):
    print(vendedor)
    print(numero)

    pedidos = Buscas.buscaPedidos()
    print(pedidos)
    
    for rowPedido, pedido in enumerate(pedidos, start=1):  

        dados = [
            pedido[0],  # Item
            pedido[2],
            pedido[1],
            pedido[3]   
        ]
        
        # 
        # 
        
        for colNum, valor in enumerate(dados):
            dado = ctk.CTkLabel(self.frameParaVendasNoRelatorio, text=valor, width=150, fg_color="#38343c", anchor="center")
            dado.grid(row=rowPedido, column=colNum, padx=2, pady=2)
