import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consultas.insert import Insere
from tkinter import messagebox 

import customtkinter as ctk


def registraProdutoNoBanco(self, frame):

    nome = self.nomeProduto.get()
    marca = self.marca.get()
    valorCusto = self.ValorCusto.get()
    valorVenda = self.ValorVenda.get()
    if not self.Quantidade.get():
        quantidade = 0
    else:
        quantidade = self.Quantidade.get()
    codigoInterno = self.CodigoInterno.get()
    NCM = self.NCM.get()
    CFOP = self.CFOP.get()
    CEST = self.CEST.get()
    origemCST = self.OrigemCST.get()
    descricao = self.Descricao.get()
    CNPJ = self.CNPJ.get()


    if not(nome and valorCusto and valorVenda and CNPJ and marca):
        messagebox.showerror("erro", "valores estão em branco")

    else:
        Insere.insereProdutosNoBanco(nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ, marca)
        frame.destroy()
