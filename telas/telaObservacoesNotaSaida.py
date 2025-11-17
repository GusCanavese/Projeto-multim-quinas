import customtkinter as ctk
from tkinter import messagebox
from componentes import criaFrameJanela, criaBotao, criaTextArea, criarLabelEntry
from funcoesTerceiras import criarNFe, criarNFCe


def acessar(dados, *caminho, default=""):
    atual = dados
    for chave in caminho:
        if isinstance(atual, dict) and chave in atual:
            atual = atual[chave]
        else:
            return default
    if isinstance(atual, dict) and "#text" in atual:
        atual = atual["#text"]
    if atual in (None, ""):
        return default
    return str(atual)


def telaObservacoesNotaSaida(self, EhNotaDoConsumidor):
    self.frameTelaObservacoes = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    numeroPedidoVinculado = ctk.StringVar()
    self.numeroPedidoVinculadoVar = numeroPedidoVinculado

    dados_nfe = getattr(self, "dadosNota", None)
    texto_contribuinte = acessar(dados_nfe, "NFe", "infNFe", "infAdic", "infCpl", default=" ")
    texto_fisco = acessar(dados_nfe, "NFe", "infNFe", "infAdic", "infAdFisco", default=" ")

    area1 = criaTextArea(
        self.frameTelaObservacoes,
        0.5,
        0.15,
        0.4,
        "INFORMAÇÕES DO INTERESSE DO CONTRIBUINTE",
        texto_contribuinte,
    )
    area1.place(relheight=0.3)
    area2 = criaTextArea(
        self.frameTelaObservacoes,
        0.05,
        0.15,
        0.4,
        "INFORMAÇÕES DO INTERESSE DO FISCO",
        texto_fisco,
    )
    area2.place(relheight=0.3)

    self.variavelObservacoes = ctk.StringVar()
    self.variavelObservacoes.set(0)

    self.observacaoContribuinteTexto = texto_contribuinte.strip()
    self.observacaoFiscoTexto = texto_fisco.strip()
    self.observacoesNotaImportada = {
        "contribuinte": self.observacaoContribuinteTexto,
        "fisco": self.observacaoFiscoTexto,
    }

    def atualizar_observacoes():
        self.observacaoContribuinteTexto = area1.get("1.0", "end").strip()
        self.observacaoFiscoTexto = area2.get("1.0", "end").strip()
        self.numeroPedidoVinculadoValor = numeroPedidoVinculado.get().strip()
        self.observacoesNotaImportada = {
            "contribuinte": self.observacaoContribuinteTexto,
            "fisco": self.observacaoFiscoTexto,
        }

    def salvar_e_gerar(modulo):
        atualizar_observacoes()
        modulo.gerarNFe(self)

    if EhNotaDoConsumidor:
        criaBotao(
            self.frameTelaObservacoes,
            "Salvar e gerar nfc-e",
            0.40,
            0.94,
            0.15,
            lambda: salvar_e_gerar(criarNFCe),
        ).place(anchor="nw")
    else:
        criaBotao(
            self.frameTelaObservacoes,
            "Salvar e gerar nf-e",
            0.25,
            0.94,
            0.15,
            lambda: salvar_e_gerar(criarNFe),
        ).place(anchor="nw")
        criarLabelEntry(self.frameTelaObservacoes, "Número pedido vinculado", 0.05, 0.58, 0.15, numeroPedidoVinculado)


    # criaBotao(self.frameTelaObservacoes, "consultar", 0.55, 0.94, 0.15, lambda: criarNFe.consultar_ultimo_recibo(self)).place(anchor="nw")
    criaBotao(self.frameTelaObservacoes, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaObservacoes.destroy()).place(anchor="nw")


# COLOCAR O CAMINHO CORRETO DOS CERTIFICADOS