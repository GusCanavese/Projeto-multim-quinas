import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import confirmarExclusaoDoProduto, confirmarAlteracoesNoProduto
from componentes import criaFrame, criaFrameJanela, criaLabelDescritivo, criaBotao, criarLabelEntry;




def telaVerProduto(self, p):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)


    

    criaLabelDescritivo(frame, "Nome do produto",             0.05, 0.07, 0.35, self.cor, ctk.StringVar(value=p[1]))
    self.quantidade = criarLabelEntry(frame, "Quantidade",    0.43, 0.08, 0.15, ctk.StringVar(value=p[0]))
    self.precoVenda = criarLabelEntry(frame, "preço de venda",0.61, 0.08, 0.15, ctk.StringVar(value=p[8]))
    criaLabelDescritivo(frame, "CNPJ",                        0.79, 0.07, 0.15, self.cor, ctk.StringVar(value=p[4]))



    criaLabelDescritivo(frame, "NCM",            0.05, 0.25, 0.15, self.cor, ctk.StringVar(value=p[5]))
    criaLabelDescritivo(frame, "CFOP",           0.25, 0.25, 0.15, self.cor, ctk.StringVar(value=p[6]))
    criaLabelDescritivo(frame, "CEST",           0.43, 0.25, 0.15, self.cor, ctk.StringVar(value=p[7]))
    
    criaLabelDescritivo(frame, "Origem CST",     0.61, 0.25, 0.15, self.cor, ctk.StringVar(value=p[8]))
    criaLabelDescritivo(frame, "Código interno", 0.79, 0.25, 0.15, self.cor, ctk.StringVar(value=p[2]))
    


    criaBotao(frame, 'salvar alterações', 0.61, 0.43, 0.15, lambda:confirmarAlteracoesNoProduto.confirmarAlteracoesNoProduto(self, frame, p[1], self.quantidade.get(), self.precoVenda.get()))
    botaoExclui = criaBotao(frame, 'Excluir pedido', 0.79, 0.43, 0.15, lambda:confirmarExclusaoDoProduto.confirmarExclusaoDoProduto(self, frame, p[1]))
    botaoExclui.configure(fg_color=self.corNegado)
    criaBotao(frame, 'Voltar', 0.15, 0.95, 0.20, lambda:frame.destroy())
    


