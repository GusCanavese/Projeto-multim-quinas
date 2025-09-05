import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import confirmarExclusaoDoProduto, confirmarAlteracoesNoProduto
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criaLabelDescritivo, criaBotao, criarLabelEntry;




def telaVerProduto(self, p, fiscal):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)


    

    criaLabelDescritivo(frame, "Nome do produto",             0.05, 0.07, 0.35, self.cor, ctk.StringVar(value=p[1]))
    self.quantidade = criarLabelEntry(frame, "Quantidade",    0.43, 0.08, 0.05, ctk.StringVar(value=p[0]))
    self.precoVenda = criarLabelEntry(frame, "preço de venda",0.51, 0.08, 0.10, ctk.StringVar(value=p[8]))
    self.precoCusto = criarLabelEntry(frame, "preço de custo",0.64, 0.08, 0.10, ctk.StringVar(value=p[8]))
    criaLabelDescritivo(frame, "CNPJ",                        0.77, 0.07, 0.17, self.cor, ctk.StringVar(value=p[4]))



    criaLabelDescritivo(frame, "NCM",                 0.05, 0.25, 0.15, self.cor, ctk.StringVar(value=p[5]))
    criaLabelDescritivo(frame, "CFOP",                0.25, 0.25, 0.15, self.cor, ctk.StringVar(value=p[6]))
    criaLabelDescritivo(frame, "CEST",                0.43, 0.25, 0.15, self.cor, ctk.StringVar(value=p[7]))
    
    criaLabelDescritivo(frame, "Origem CST",          0.61, 0.25, 0.15, self.cor, ctk.StringVar(value=p[8]))
    criaLabelDescritivo(frame, "Código interno",      0.79, 0.25, 0.15, self.cor, ctk.StringVar(value=p[2]))
    criaLabelDescritivo(frame, "Marca",               0.05, 0.43, 0.15, self.cor, ctk.StringVar(value=p[9]))
    

    if fiscal:
        criaBotao(frame, 'salvar alterações', 0.61, 0.43, 0.15, lambda:confirmarAlteracoesNoProduto.confirmarAlteracoesNoProduto(self, frame, p[11], self.quantidade.get(), self.precoVenda.get(), self.precoCusto.get()))
        print(p[0])
        botaoExclui = criaBotao(frame, 'Excluir produto', 0.79, 0.43, 0.15, lambda:confirmarExclusaoDoProduto.confirmarExclusaoDoProdutoFiscal(self, frame, p[11]))
        botaoExclui.configure(fg_color=self.corNegado)
        criaBotao(frame, 'Voltar', 0.15, 0.95, 0.20, lambda:frame.destroy())
    else:
        criaBotao(frame, 'salvar alterações', 0.61, 0.43, 0.15, lambda:confirmarAlteracoesNoProduto.confirmarAlteracoesNoProduto(self, frame, p[11], self.quantidade.get(), self.precoVenda.get(), self.precoCusto.get()))
        print(p[0])
        botaoExclui = criaBotao(frame, 'Excluir produto', 0.79, 0.43, 0.15, lambda:confirmarExclusaoDoProduto.confirmarExclusaoDoProduto(self, frame, p[11]))
        botaoExclui.configure(fg_color=self.corNegado)
        criaBotao(frame, 'Voltar', 0.15, 0.95, 0.20, lambda:frame.destroy())
    


