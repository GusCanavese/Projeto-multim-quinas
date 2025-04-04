import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import json

def telaRelatorioDeVendas(self):
    self.frameTelaRelatorioDeVendas = ctk.CTkFrame(self, height=800, width=1200, corner_radius=5)
    self.frameTelaRelatorioDeVendas.place(x=40, y=50)
    
    # Frame rolável
    self.frameParaVendasNoRelatorio = ctk.CTkScrollableFrame(self.frameTelaRelatorioDeVendas, width=1160, height=730 )
    self.frameParaVendasNoRelatorio.place(x=10, y=10)




    # Cabeçalho da tabela
    colunas = ["Pedido", "Vendedor", "Data de emissão", "Subtotal"]
    for i, coluna in enumerate(colunas):
        label = ctk.CTkLabel(self.frameParaVendasNoRelatorio, text=coluna, width=150, fg_color="green", anchor="center")
        label.grid(row=0, column=i, padx=2, pady=5)  

    pedidos = Buscas.buscaPedidos()
    print(pedidos)
    
    for rowPedido, pedido in enumerate(pedidos, start=1):  

        dados = [
            pedido[0],  # Item
            pedido[2],
            pedido[1],
            pedido[3]   
        ]
        
        
        for colNum, valor in enumerate(dados):
            dado = ctk.CTkLabel(self.frameParaVendasNoRelatorio, text=valor, width=150, fg_color="#38343c", anchor="center")
            dado.grid(row=rowPedido, column=colNum, padx=2, pady=2)
    

    self.botaoVoltar = ctk.CTkButton(self.frameTelaRelatorioDeVendas, text="Voltar", width=150, command=self.frameTelaRelatorioDeVendas.destroy)
    self.botaoVoltar.place(x=950, y=760)