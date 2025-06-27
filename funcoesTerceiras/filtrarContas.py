import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 
import tkinter as tk
from telas.telaVerPedidos import telaVerPedidos
import json
from componentes import criaLabel, criaBotao

def filtrarContas(self, frame, pagina=1):
    contasReceber = Buscas.buscaContasAReceber()
    contasPagar = Buscas.buscaContasAPagar()
    contas = contasReceber + contasPagar

    print(len(contas))

    if hasattr(self, "dadosTelaFiltrarContas"):
        for item in self.dadosTelaFiltrarContas:
            item.destroy()
    self.dadosTelaFiltrarContas = []

    # Calcula o intervalo de pedidos a mostrar
    inicioContas = (pagina - 1) * 10
    fimContas = pagina * 10
    contasPagina = contas[inicioContas:fimContas]
    
    y = 0.1
    for rowProduto, conta in enumerate(contasPagina, start=1):
        corDeFundo = "#1C60A0"
        dadosProduto = [conta[0], conta[2], conta[1], conta[3], conta[4]]
        dadosextras = [conta[0], conta[1], conta[2], conta[3], conta[4], conta[5]]


        x = 0.03
        for colNum, valor in enumerate(dadosProduto):
            if colNum == 0:
                label = criaLabel(frame, valor, x, y, 0.08, corDeFundo)
                x+=0.085
            elif colNum ==1:
                label = criaLabel(frame, valor, x, y, 0.4, corDeFundo)
                x+=0.405
            elif colNum ==2:
                label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
                x+=0.175
            elif colNum ==3:
                label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
                x+=0.175

            self.dadosTelaFiltrarContas.append(label)

        btn = criaBotao(frame, "Ver", 0.937, y, 0.05, lambda p=dadosextras: print("aopa"))
        self.dadosTelaFiltrarContas.append(btn)

        y += 0.045
    
    print(len(contasPagina))
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
