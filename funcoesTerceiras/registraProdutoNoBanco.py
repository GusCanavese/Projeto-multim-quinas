import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consultas.insert import Insere
import customtkinter as ctk


def registraProdutoNoBanco(self):
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
        self.frameProdutoNaoCadastrado = ctk.CTkFrame(self, height=60, width=300, corner_radius=5, border_width=2, border_color="red",fg_color="transparent")
        self.frameProdutoNaoCadastrado.place(relx=0.5, y=600, )
        self.ProdutoNaoCadastrado = ctk.CTkLabel(self.frameProdutoNaoCadastrado,  text="Prencha os campos obrigatórios", font=("Arial", 18))
        self.ProdutoNaoCadastrado.place(relx=0.5, y=30, anchor="center")
    else:
        Insere.insereProdutosNoBanco(nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ)
        self.frameTelaCadastroProduto.destroy()
