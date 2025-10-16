import sys
import os
from tkinter import messagebox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
from funcoesTerceiras import calculaParcelasFaturamento
from componentes import criaBotaoPequeno, criaEntry, criaFrameJanela, criaLabel, criarLabelEntry, criarLabelComboBox, criarLabelLateralEntry, criaBotao
from telas.telaObservacoes import telaObservacoes
from telas.telaTotaisNota import telaTotaisNotaSaida




def acessar(dados, *caminho, default=""):
    for chave in caminho:
        if isinstance(dados, dict) and chave in dados:
            dados = dados[chave]
        else:
            return default
    if isinstance(dados, dict) and "#text" in dados:
        return dados["#text"]
    return dados if isinstance(dados, str) else default


def telaTransporteNotaSaida(self, cons):
    
    listaLabels = ["Quantidade", "Espécie",	"Marca", "Numeração", "Peso Bruto",	"Peso Líquido"]
    opcoesPagamento = ["À vista", "À prazo", "Outros"]
    opcoesTransporte = [
        "Contratação do Frete por conta do Remetente (CIF)",
        "Contratação do Frete por conta do Destinatário (FOB)",
        "Contratação do Frete por conta de Terceiros",
        "Transporte Próprio por conta do Remetente",
        "Transporte Próprio por conta do Destinatário",
        "Sem Ocorrência de Transporte"
    ]


    
    self.frametelaTransporte = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    # opções
    opcoesSerie = ["", "B", "C", "U"]
    opcoesModelo = ["", "57", "07", "08", "09", "10", "11"]
    opcoesTributacao = ["", "00", "10", "20", "30", "40", "41", "50", "51", "60", "70", "90"]

    # variáveis
    variavelModalidade = ctk.StringVar()
    variavelTransportador = ctk.StringVar()
    variavelCNPJTransportador = ctk.StringVar()
    variavelModelo = ctk.StringVar()
    variavelTributacao = ctk.StringVar()

    criarLabelComboBox(self.frametelaTransporte, "Modalidade do frete", 0.05, 0.1, 0.25, opcoesTransporte)
    criarLabelEntry(self.frametelaTransporte, "Transportador", 0.35, 0.1, 0.3, variavelTransportador)
    criarLabelEntry(self.frametelaTransporte, "CPF/CNPJ", 0.7, 0.1, 0.1, variavelCNPJTransportador)

    criarLabelEntry(self.frametelaTransporte, "Número", 0.05, 0.2, 0.05, None)
    criarLabelComboBox(self.frametelaTransporte, "Série", 0.12, 0.2, 0.05, opcoesSerie)
    criarLabelEntry(self.frametelaTransporte, "SubSérie", 0.19, 0.2, 0.05, None)
    modelo = criarLabelComboBox(self.frametelaTransporte, "Modelo", 0.26, 0.2, 0.05, opcoesModelo)
    modelo.set(variavelModelo.get())
    tribut = criarLabelComboBox(self.frametelaTransporte, "Tributação", 0.33, 0.2, 0.05, opcoesTributacao)
    tribut.set(variavelTributacao.get())
    criarLabelEntry(self.frametelaTransporte, "Chave CT-e ", 0.40, 0.2, 0.15, None)
    criarLabelEntry(self.frametelaTransporte, "Data Emissão", 0.57, 0.2, 0.10, None)
    criarLabelEntry(self.frametelaTransporte, "Data Prestação", 0.69, 0.2, 0.10, None)
    criarLabelEntry(self.frametelaTransporte, "Desconto", 0.81, 0.2, 0.05, None)
    criarLabelEntry(self.frametelaTransporte, "Total da Nota ", 0.88, 0.2, 0.05, None)

    criarLabelLateralEntry(self.frametelaTransporte, "CFOP", 0.10, 0.4, 0.08, None)
    criarLabelLateralEntry(self.frametelaTransporte, "BC Retenção ICMS", 0.40, 0.4, 0.15, None)
    criarLabelLateralEntry(self.frametelaTransporte, "Valor ICMS Retido", 0.70, 0.4, 0.15, None)
    criarLabelLateralEntry(self.frametelaTransporte, "Valor do Serviço", 0.10, 0.5, 0.15, None)
    criarLabelLateralEntry(self.frametelaTransporte, "Aliquota Ret. ICMS", 0.40, 0.5, 0.15, None)
    criarLabelLateralEntry(self.frametelaTransporte, "Município Gerador", 0.70, 0.5, 0.15, None)






    self.posicaoy = 0.6
    self.posicaox = 0.05
    self.posicaoyBotaoTransp = 0.65
    self.posicaoyBotaoRemoverTransp = 0.691
    self.contadorDeLinhas = 0
    self.yNovo = 0.24
    self.entradaProduto = 0
    self.valorSubtotal = 0
    self.linhasTransporte = []


    self.botaoRemoverItem = ctk.CTkButton(self.frametelaTransporte, text="X", width=20, corner_radius=0, fg_color="red", command=lambda: removerItem(self))
    self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotao-0.04)



    for i, coluna in enumerate(listaLabels):
        criaLabel(self.frametelaTransporte, coluna, self.posicaox, self.posicaoy, 0.145, self.cor)
        self.posicaox +=0.1453
    self.posicaox = 0.05
    self.botaoAdicionarItemTransp = criaBotaoPequeno(self.frametelaTransporte, "Adicionar item", 0.7, self.posicaoyBotaoTransp, 0.07, lambda: (adicionarItem(self)))

    def adicionarItem(self):

        self.posicaoy += 0.04
        self.posicaoyBotaoTransp += 0.04
        self.posicaoyBotaoRemoverTransp += 0.04

        self.botaoAdicionarItemTransp.place(relx=0.875, rely=self.posicaoyBotaoTransp)
        self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotaoRemoverTransp)
        linha_widgets = {}
        

        for i, coluna in enumerate(listaLabels):

            entrada = criaEntry(self.frametelaTransporte, self.posicaox, self.posicaoy, 0.145, None)
            campo = ["Quantidade", "Espécie", "Marca", "Numeração", "Peso Bruto", "Peso Líquido"][i - 2]
            linha_widgets[campo] = entrada

            self.posicaox += 0.1453


        self.posicaox = 0.05
        self.linhasTransporte.append(linha_widgets)
        self.yNovo = self.posicaoy + 0.02

    def removerItem(self):
        if len(self.linhasTransporte) > 1:
            ultima_linha = self.linhasTransporte.pop()

            for widget in ultima_linha.values():
                if hasattr(widget, "destroy"):
                    widget.destroy()

            self.contadorDeLinhas -= 9
            self.posicaoy -= 0.02
            self.posicaoyBotaoTransp -= 0.02
            self.posicaoyBotaoRemoverTransp -= 0.02

            self.botaoAdicionarItem.place(relx=0.883, rely=self.posicaoyBotao)
            self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotaoRemoverTransp)

        if len(self.linhasTransporte) == 1:
            self.botaoRemoverItem.place_forget()

        self.yNovo = self.posicaoy + 0.02
        self.entradaProduto = ""

    



    adicionarItem(self)




    criaBotao(self.frametelaTransporte, "Próximo - Tela Totais", 0.25, 0.94, 0.15, lambda: telaTotaisNotaSaida(self, cons)).place(anchor="nw")
    criaBotao(self.frametelaTransporte, "Voltar", 0.05, 0.94, 0.15, lambda: self.frametelaTransporte.destroy()).place(anchor="nw")