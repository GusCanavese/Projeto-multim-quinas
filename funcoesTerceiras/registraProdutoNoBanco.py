import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consultas.insert import Insere
import customtkinter as ctk
from componentes import criaAviso


def registraProdutoNoBanco(self, frame):
    nome = self.nomeProduto.get()
    valorCusto = self.ValorCusto.get()
    valorVenda = self.ValorVenda.get()
    quantidade = self.Quantidade.get()
    codigoInterno = self.CodigoInterno.get()
    NCM = self.NCM.get()
    CFOP = self.CFOP.get()
    CEST = self.CEST.get()
    origemCST = self.OrigemCST.get()
    descricao = self.Descricao.get()
    CNPJ = self.CNPJ.get()


    if not(nome and valorCusto and valorVenda and quantidade and codigoInterno and NCM and CFOP and CEST and origemCST and descricao and CNPJ):
        criaAviso(self, frame, 60, 350, "Preencha os campos obrigatórios", 0.5, 0.6)

    else:
        Insere.insereProdutosNoBanco(nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ)
        frame.destroy()
