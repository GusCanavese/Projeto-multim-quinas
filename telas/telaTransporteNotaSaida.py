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

    # variáveis
    variavelTransportador = ctk.StringVar()
    variavelCNPJTransportador = ctk.StringVar()


    criarLabelComboBox(self.frametelaTransporte, "Modalidade do frete", 0.05, 0.1, 0.25, opcoesTransporte)
    criarLabelEntry(self.frametelaTransporte, "Transportador", 0.35, 0.1, 0.3, variavelTransportador)
    criarLabelEntry(self.frametelaTransporte, "CPF/CNPJ", 0.7, 0.1, 0.1, variavelCNPJTransportador)



    self.posicaoy = 0.3
    self.posicaox = 0.05
    self.posicaoyBotaoTransp = 0.35
    self.posicaoyBotaoRemoverTransp = 0.284
    self.valorSubtotal = 0
    self.linhasTransporte = []


    self.botaoRemoverItem = ctk.CTkButton(self.frametelaTransporte, text="X", width=20, corner_radius=0, fg_color="red", command=lambda: removerItem(self))
    self.botaoRemoverItem.place(relx=0.80, rely=self.posicaoyBotao-0.04)



    for i, coluna in enumerate(listaLabels):
        criaLabel(self.frametelaTransporte, coluna, self.posicaox, self.posicaoy, 0.145, self.cor)
        self.posicaox +=0.1453
    self.posicaox = 0.05
    self.botaoAdicionarItemTransp = criaBotaoPequeno(self.frametelaTransporte, "Adicionar item", 0.7, self.posicaoyBotaoTransp, 0.07, lambda: (adicionarItem(self)))

    def adicionarItem(self):
        print(f"removi, tamanho: {self.posicaoyBotaoTransp}")
        self.posicaoy += 0.04
        self.posicaoyBotaoTransp += 0.04
        self.posicaoyBotaoRemoverTransp += 0.04

        self.botaoRemoverItem.place(relx=0.93, rely=self.posicaoyBotaoRemoverTransp)
        self.botaoAdicionarItemTransp.place(relx=0.883, rely=self.posicaoyBotaoTransp)
        
        linha_widgets = {}
        
        for i, coluna in enumerate(listaLabels):
            entrada = criaEntry(self.frametelaTransporte, self.posicaox, self.posicaoy, 0.145, None)
            campo = ["Quantidade", "Espécie", "Marca", "Numeração", "Peso Bruto", "Peso Líquido"][i - 2]
            linha_widgets[campo] = entrada
            self.posicaox += 0.1453

        self.posicaox = 0.05
        self.linhasTransporte.append(linha_widgets)





    def removerItem(self):
        print(f"removi, tamanho: {self.posicaoyBotaoTransp}")
        if len(self.linhasTransporte) > 1:
            ultima_linha = self.linhasTransporte.pop()

            for widget in ultima_linha.values():
                if hasattr(widget, "destroy"):
                    widget.destroy()

            self.posicaoy -= 0.04
            self.posicaoyBotaoTransp -= 0.04
            self.posicaoyBotaoRemoverTransp -= 0.04
            
            self.botaoAdicionarItemTransp.place(relx=0.883, rely=self.posicaoyBotaoTransp)
            self.botaoRemoverItem.place(relx=0.93, rely=self.posicaoyBotaoRemoverTransp)

        if len(self.linhasTransporte) == 1:
            self.botaoRemoverItem.place_forget()


    
    adicionarItem(self)




    criaBotao(self.frametelaTransporte, "Próximo - Tela Totais", 0.25, 0.94, 0.15, lambda: telaTotaisNotaSaida(self, cons)).place(anchor="nw")
    criaBotao(self.frametelaTransporte, "Voltar", 0.05, 0.94, 0.15, lambda: self.frametelaTransporte.destroy()).place(anchor="nw")