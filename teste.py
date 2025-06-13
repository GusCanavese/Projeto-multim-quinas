import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from telas.telaVerPedidos import telaVerPedidos
import json
from componentes import criaLabel, criaBotao

def filtrarPedidos(self, frame, vendedor, numero, inicio, fim, checkbox, pagina=1):
    pedidos = Buscas.buscaPedidos(vendedor, numero, inicio, fim, checkbox)
    print(pedidos)

    # Remove dados anteriores da tabela
    if hasattr(self, "dadosTelaVerPedidos"):
        for item in self.dadosTelaVerPedidos:
            item.destroy()
    self.dadosTelaVerPedidos = []

    # Calcula o intervalo de pedidos a mostrar
    inicio_pedido = (pagina - 1) * 10
    fim_pedido = pagina * 10
    pedidos_pagina = pedidos[inicio_pedido:fim_pedido]

    y = 0.15
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
            btnAnterior = criaBotao(frame, "← Anterior", 0.25, 0.7, 0.2, lambda p=params: filtrarPedidos(self, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']-1))
            self.dadosTelaVerPedidos.append(btnAnterior)

        if fim_pedido < len(pedidos):
            btnProxima = criaBotao(frame, "Próximo →", 0.5, 0.7, 0.2, lambda p=params: filtrarPedidos(self, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']-1))
            self.dadosTelaVerPedidos.append(btnProxima)









































import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import filtrarPedidos, verificaSeQuerFiltrarPorPeriodo
from componentes import criaFrame, criarLabelEntry, criarLabelComboBox, criaBotao, criaLabel



def telaRelatorioDeVendas(self):


    # Frame rolável (conteúdo principal)

    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    frameVendas = criaFrame(frame, 0.65, 0.5, 0.68, 0.93)
    opcoes = ["Nenhum", "Yara", "Camila", "Jenifer", "Bruna", "Ana Flávia", "Maurício"]


    self.filtrarPorNumero = criarLabelEntry(frame,"Filtrar pelo Nº", 0.03, 0.05, 0.22, None)
    self.filtrarPorVendedor = criarLabelComboBox(frame, "Filtrar por vendedor(a)", 0.03, 0.14, 0.22, opcoes)
    
    self.selecionarPeriodo = ctk.CTkCheckBox(frame, text="Selecionar período")
    self.selecionarPeriodo.place(relx=0.03, rely=0.27, anchor="nw")
    self.selecionarPeriodo.bind("<Button-1>", command=lambda event: verificaSeQuerFiltrarPorPeriodo.verificaSeQuerFiltrarPorPeriodo(self, self.selecionarPeriodo.get(), event))
    

    # Botões
    
    
    criaBotao(frame, "Buscar", 0.15, 0.55, 0.15, lambda:filtrarPedidos.filtrarPedidos( self, frameVendas, self.filtrarPorVendedor.get(), self.filtrarPorNumero.get(), self.datePickerInicio.get() if hasattr(self, "datePickerInicio") else None, self.datePickerFim.get() if hasattr(self, "datePickerFim") else None, self.selecionarPeriodo.get()))
    criaBotao(frame, "Atualizar", 0.15, 0.63, 0.15, lambda:filtrarPedidos.filtrarPedidos( self, frameVendas, self.filtrarPorVendedor.get(), self.filtrarPorNumero.get(), self.datePickerInicio.get() if hasattr(self, "datePickerInicio") else None, self.datePickerFim.get() if hasattr(self, "datePickerFim") else None, self.selecionarPeriodo.get()))
    criaBotao(frame, "Voltar", 0.15, 0.94, 0.15, lambda:frame.destroy())

    # Cabeçalhos da tabela
    colunas = ["Pedido", "Vendedor", "Data de emissão", "Subtotal", "Confirmação da venda"]
    x = 0.03
    y = 0.1

    for i, coluna in enumerate(colunas):
        criaLabel(frameVendas, coluna, x, y, 0.17, "#2C3E50")
        x+=0.175
        # label = ctk.CTkLabel(frameVendas, text=coluna, width=150, fg_color="#2C3E50", anchor="center")
        # label.grid(row=0, column=i, padx=2, pady=5)
        # label.grid_columnconfigure(0, minsize=20)
