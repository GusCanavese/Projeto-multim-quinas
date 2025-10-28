import customtkinter as ctk
from tkinter import messagebox
from componentes import criaFrameJanela, criaBotao, criaTextArea, criarLabelEntry
from funcoesTerceiras import criarNFe, criarNFCe


def telaObservacoesNotaSaida(self, EhNotaDoConsumidor):
    self.frameTelaObservacoes = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    numeroPedidoVinculado = ctk.StringVar()

    area1 = criaTextArea(self.frameTelaObservacoes, 0.5, 0.15, 0.4, "INFORMAÇÕES DO INTERESSE DO CONTRIBUINTE", " ")
    area1.place(relheight=0.3)
    area2 = criaTextArea(self.frameTelaObservacoes, 0.05, 0.15, 0.4, "INFORMAÇÕES DO INTERESSE DO FISCO", " ")
    area2.place(relheight=0.3)

    self.variavelObservacoes = ctk.StringVar()
    self.variavelObservacoes.set(0)
    
    if EhNotaDoConsumidor:
        criaBotao(self.frameTelaObservacoes, "Salvar e gerar nfc-e", 0.40, 0.94, 0.15, lambda: criarNFCe.gerarNFe(self)).place(anchor="nw")
    else:
        criaBotao(self.frameTelaObservacoes, "Salvar e gerar nf-e", 0.25, 0.94, 0.15, lambda: criarNFe.gerarNFe(self)).place(anchor="nw")
        criarLabelEntry(self.frameTelaObservacoes, "Número pedido vinculado", 0.05, 0.58, 0.15, numeroPedidoVinculado)


    # criaBotao(self.frameTelaObservacoes, "consultar", 0.55, 0.94, 0.15, lambda: criarNFe.consultar_ultimo_recibo(self)).place(anchor="nw")
    criaBotao(self.frameTelaObservacoes, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaObservacoes.destroy()).place(anchor="nw")


# COLOCAR O CAMINHO CORRETO DOS CERTIFICADOS