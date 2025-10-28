import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from componentes import criaBotaoPequeno, criaEntry, criaFrameJanela, criaLabel, criarLabelEntry, criarLabelComboBox, criaBotao
from telas.telaCadastroTransportadoras import telaCadastroTransportadoras 
from telas.telaTotaisNotaSaida import telaTotaisNotaSaida

def telaTransporteNotaSaida(self, EhNotaDoConsumidor):
    self.frametelaTransporte = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    def buscaTransportador(event=None): 
        nomeDoTransportador = self.nomeTransportador.get()
        cnpjTransportador   = self.documentoTransportador.get()
        dadosTransportador  = Buscas.buscaTransportador(nomeDoTransportador, cnpjTransportador)

        if hasattr(self, 'resultadoLabels'):
            for label in self.resultadoLabels: 
                label.destroy()
        self.resultadoLabels = []
            
        yNovo = 0.16
        if len(dadosTransportador) > 0:
            for i, row in enumerate(dadosTransportador):
                if i >= 5:
                    break
                label = ctk.CTkButton(self.frametelaTransporte,  text=row[0], corner_radius=0, fg_color=self.cor, font=("Century Gothic bold", 15), command = lambda  nome=row[0], documento=row[1]: selecionaCliente(nome, documento))
                label.place(relx=0.35, rely=yNovo, relwidth=0.3)
                self.resultadoLabels.append(label)  
                yNovo += 0.0399
        else:
            print("entrou")
            label = ctk.CTkButton(self.frametelaTransporte,  text="+ Cadastrar Transportador", corner_radius=0, fg_color=self.cor, font=("Century Gothic bold", 15), command = lambda: telaCadastroTransportadoras(self))
            label.place(relx=0.35, rely=yNovo, relwidth=0.3)
            self.resultadoLabels.append(label)  
            yNovo += 0.0399
    
    def selecionaCliente(nome, documento):

        # --------------------------------------------------

        self.nomeDestinatario = nome
        self.documentoDestinatario = documento

        self.variavelRazaoSocialRemetente.set(nome)
        self.variavelCNPJRazaoSocialRemetente.set(documento)

        for label in self.resultadoLabels: 
            label.destroy()





    listaLabels = ["Quantidade", "Espécie",	"Marca", "Numeração", "Peso Bruto",	"Peso Líquido"]
    opcoesTransporte = [
        "Contratação do Frete por conta do Remetente (CIF)",
        "Contratação do Frete por conta do Destinatário (FOB)",
        "Contratação do Frete por conta de Terceiros",
        "Transporte Próprio por conta do Remetente",
        "Transporte Próprio por conta do Destinatário",
        "Sem Ocorrência de Transporte"
    ]


    
    
    # variáveis
    variavelTransportador = ctk.StringVar()
    variavelCNPJTransportador = ctk.StringVar()


    criarLabelComboBox(self.frametelaTransporte, "Modalidade do frete", 0.05, 0.1, 0.25, opcoesTransporte)
    self.nomeTransportador = criarLabelEntry(self.frametelaTransporte, "Transportador", 0.35, 0.1, 0.3, variavelTransportador)
    self.documentoTransportador = criarLabelEntry(self.frametelaTransporte, "CPF/CNPJ", 0.7, 0.1, 0.2, variavelCNPJTransportador)
    self.nomeTransportador.bind("<KeyRelease>",buscaTransportador)
    self.nomeTransportador.bind("<Button-1>",buscaTransportador)
    self.documentoTransportador.bind("<Button-1>",buscaTransportador)
    self.documentoTransportador.bind("<KeyRelease>",buscaTransportador)

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




    criaBotao(self.frametelaTransporte, "Próximo - Tela Totais", 0.25, 0.94, 0.15, lambda: telaTotaisNotaSaida(self, EhNotaDoConsumidor)).place(anchor="nw")
    criaBotao(self.frametelaTransporte, "Voltar", 0.05, 0.94, 0.15, lambda: self.frametelaTransporte.destroy()).place(anchor="nw")