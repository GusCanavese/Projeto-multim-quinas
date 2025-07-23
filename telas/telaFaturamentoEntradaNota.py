import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
from funcoesTerceiras import calculaParcelasFaturamento
from telas.telaTransporte import telaTransporte

def telaGerarFaturamentoEntradaNota(self, dadosNota):
    variavelValorLiquido = ctk.StringVar()
    variavelValorLiquido.set(dadosNota["NFe"]["infNFe"]["total"]["ICMSTot"]["vNF"]["#text"])

    self.row=1
    self.frameTelaGerarFaturamento = ctk.CTkFrame(self)
    self.frameValorTotais = ctk.CTkFrame(self.frameTelaGerarFaturamento, fg_color="#48424d")

    self.frameTelaGerarFaturamento.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)


    valores = ["Forma de pagamento", "Quantidade parcelas", "Valor"]
    opcoesPagamento = ["", "Bndes", "Boleto", "Carnê", "Crédito a vista", "Crédito parcelado", "Débito", "Cheque", "Depósito"]

    largura_label = 0.2 
    posicaoy = 0.1
    self.y= 0.138
    self.teste = 0.038
    self.yParcelas = 0.138
    self.totais = 0
    self.totaisFormasDePagamento = ctk.StringVar()
    self.totaisFormasDePagamento = variavelValorLiquido

    self.descontoTotalVindoDoPedido = ctk.StringVar()
    self.descontoTotalVindoDoPedido.set(123123) 

    self.acrescimoTotalVindoDoPedido = ctk.StringVar()
    self.acrescimoTotalVindoDoPedido.set(123123) 


    self.botaoAdicionarParcela = ctk.CTkButton(self.frameTelaGerarFaturamento, text="Adicionar Parcela", width=20, corner_radius=0, command=lambda:verificaParcelasPreenchidas(self)) 
    
    
    labelEntradasTotais = ctk.CTkLabel(self.frameValorTotais, text="Total")
    labelEntradasTotais.place(relx=0.6, rely = 0.10)
    self.entradasTotais = ctk.CTkEntry(self.frameValorTotais, textvariable=self.totaisFormasDePagamento)
    self.entradasTotais.place(relx=0.6, rely = 0.20, relwidth=0.3)
    
    labelDescontoTotal = ctk.CTkLabel(self.frameValorTotais, text="Desconto total")
    labelDescontoTotal.place(relx=0.6, rely = 0.35)
    self.descontoTotal = ctk.CTkEntry(self.frameValorTotais, textvariable=self.descontoTotalVindoDoPedido)
    self.descontoTotal.place(relx=0.6, rely = 0.45, relwidth=0.3)
    
    labelAcrescimoTotal = ctk.CTkLabel(self.frameValorTotais, text="Acrescimo total")
    labelAcrescimoTotal.place(relx=0.6, rely = 0.60)
    self.acrescimoTotal = ctk.CTkEntry(self.frameValorTotais, textvariable=self.descontoTotalVindoDoPedido)
    self.acrescimoTotal.place(relx=0.6, rely = 0.70, relwidth=0.3)



    labelValorOriginal = ctk.CTkLabel(self.frameValorTotais, text="Valor original da fatura")
    labelValorOriginal.place(relx=0.1, rely = 0.10)
    self.ValorOriginal = ctk.CTkEntry(self.frameValorTotais, textvariable=self.totaisFormasDePagamento)
    self.ValorOriginal.place(relx=0.1, rely = 0.20, relwidth=0.3)
    
    labelNumeroDaFatura = ctk.CTkLabel(self.frameValorTotais, text="Número da fatura")
    labelNumeroDaFatura.place(relx=0.1, rely = 0.35)
    self.NumeroDaFatura = ctk.CTkEntry(self.frameValorTotais, textvariable=self.descontoTotalVindoDoPedido)
    self.NumeroDaFatura.place(relx=0.1, rely = 0.45, relwidth=0.3)
    
    labelValorDaNota = ctk.CTkLabel(self.frameValorTotais, text="Valor da nota")
    labelValorDaNota.place(relx=0.1, rely = 0.60)
    self.ValorDaNota = ctk.CTkEntry(self.frameValorTotais, textvariable=self.descontoTotalVindoDoPedido)
    self.ValorDaNota.place(relx=0.1, rely = 0.70, relwidth=0.3)

    

    self.listaComboboxes = []
    self.listaEntradaQuantidade = []
    self.listaEntradaValor = []
    self.variavelQuantidade = ctk.StringVar()




    def calcularTotal():
        total = 0
        for entrada in self.listaEntradaValor:
            valor = float(entrada.get())
            total += valor
        self.totaisFormasDePagamento.set(f"{total:.2f}")



    def adicionaParcela(self):
        self.valorDoPedidoVariavel = ctk.StringVar()
        self.valorDoPedidoVariavel = variavelValorLiquido

        self.y += 0.038
        self.botaoAdicionarParcela.place(relx=0.2, rely=self.y)

        self.combobox = ctk.CTkComboBox(self.frameTelaGerarFaturamento, width=100, values=opcoesPagamento, corner_radius=0, command=lambda valor: modal(self, self.entradaValor.get()))
        self.combobox.place(relx=0.2, rely=self.yParcelas, relwidth=0.2)
        self.listaComboboxes.append(self.combobox)
        
        self.entradaQuantidade = ctk.CTkEntry(self.frameTelaGerarFaturamento, width=100, corner_radius=0, textvariable=self.variavelQuantidade)
        self.entradaQuantidade.place(relx=0.4, rely=self.yParcelas, relwidth=0.2)
        self.listaEntradaQuantidade.append(self.entradaQuantidade)

        self.entradaValor = ctk.CTkEntry(self.frameTelaGerarFaturamento, textvariable=self.valorDoPedidoVariavel, width=100, corner_radius=0)
        self.entradaValor.place(relx=0.6, rely=self.yParcelas, relwidth=0.2)
        self.entradaValor.bind("<KeyRelease>", lambda event: calcularTotal())
        self.listaEntradaValor.append(self.entradaValor)

        if len(self.listaEntradaValor) != 1:
            self.valorDoPedidoVariavel.set(0)

        for i in self.listaEntradaValor:
            print(i.get())
        self.frameValorTotais.place(relx=0.2, rely=self.y+0.1, relwidth=0.6, relheight=0.35)

    adicionaParcela(self)
    
    def removerParcela(self):
        if self.row ==1:
            self.botaoRemoverParcela.destroy()
            del self.botaoRemoverParcela
            pass
        else:
            if self.row ==1 and hasattr(self, "botaoRemoverParcela"):
                self.botaoRemoverParcela.destroy()
                del self.botaoRemoverParcela
            self.y-=0.038
            self.teste -=0.038
            self.yParcelas -=0.038
            
            self.botaoAdicionarParcela.place(relx=0.2, rely=self.y)
            self.botaoRemoverParcela.place(relx=0.8, rely=self.yParcelas)
            self.frameValorTotais.place(relx=0.2, rely=self.y+0.1, relwidth=0.6, relheight=0.35)
    

            if len(self.listaEntradaValor)>1:
                self.row -= 1
                self.listaEntradaValor[self.row].destroy()
                self.listaEntradaQuantidade[self.row].destroy()
                self.listaComboboxes[self.row].destroy()

                del self.listaEntradaValor[self.row]
                del self.listaEntradaQuantidade[self.row]
                del self.listaComboboxes[self.row]


    def verificaParcelasPreenchidas(self):
        if (self.listaComboboxes[self.row-1].get() and self.listaEntradaQuantidade[self.row-1].get() and self.listaEntradaValor[self.row-1].get()):
    
            self.row +=1
            if hasattr(self, "botaoRemoverParcela") and self.botaoRemoverParcela.winfo_exists():
                self.botaoRemoverParcela.destroy()
            self.botaoRemoverParcela = ctk.CTkButton(self.frameTelaGerarFaturamento, text="X", width=20, corner_radius=0, fg_color="red", command=lambda: removerParcela(self))
            self.yParcelas += 0.038
            self.botaoRemoverParcela.place(relx=0.8, rely=self.yParcelas)
            adicionaParcela(self)

        else:
            pass

    for i, coluna in enumerate(valores):
        posicaox = 0.2 + i * largura_label  
        colunas = ctk.CTkLabel(self.frameTelaGerarFaturamento, text=coluna, fg_color="#48424d")
        colunas.place(relx=posicaox, rely=posicaoy, relwidth=largura_label-0.001)

    proximo = ctk.CTkButton(self.frameTelaGerarFaturamento, text="Próximo - Tela de Produtos", command=lambda:telaTransporte(self, dadosNota))
    proximo.place(relx=0.25, rely=0.94, relwidth=0.15, anchor="nw")

    botaoVoltar = ctk.CTkButton(self.frameTelaGerarFaturamento, text="Voltar", command=self.frameTelaGerarFaturamento.destroy)
    botaoVoltar.place(relx=0.05, rely=0.94, relwidth=0.15, anchor="nw")


def modal(self, teste):
    self.frame = ctk.CTkFrame(self.frameTelaGerarFaturamento)
    self.frame.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.9, anchor="center")
    self.frame.place(relx=0.5, rely=0.5, anchor="center")

    for widget in self.frameTelaGerarFaturamento.winfo_children():
        try:
            widget.configure(state="disabled")
        except:
            pass

    for widget in self.frame.winfo_children():
        try:
            widget.configure(state="normal")
        except:
            pass
    
    def destroyModal(self):
        for widget in self.frameTelaGerarFaturamento.winfo_children():
            try:
                widget.configure(state="normal")
            except:
                pass
        self.frame.destroy()

    botaoSalvarEFechar = ctk.CTkButton(self.frame, corner_radius=0, width=100, height=10, text="Salvar e fechar", command= lambda:calculaParcelasFaturamento.SalvaAlteracoesFaturamento(self, entradasLista[0].get(), entradasLista[1].get()))
    botaoSalvarEFechar.place(relx=0.14, rely=0.03)

    # campos do modal
    labels = ["Valor a pagar", "Qtd Parcelas", "repeticao", "Intervalo", "1ª parcela em:"]
    posicaoxb = 0.14
    for i, label in enumerate(labels):
        labelTituloCampo = ctk.CTkLabel(self.frame, text=label, width=100)
        labelTituloCampo.place(relx=posicaoxb, rely=0.1)
        posicaoxb += 0.15

    posicaoxb = 0.14
    entradasLista = []
    variaveis=[]

    for i in enumerate(labels):
        variavel = ctk.StringVar()
        variaveis.append(variavel)

        if i[0] == 1:
            opcoes=["1","2","3","4","5","6","7","8","9","10","11","12",]
            campo = ctk.CTkComboBox(self.frame, width=100, values=opcoes, corner_radius=0)
            campo.place(relx=posicaoxb, rely=0.15)
            posicaoxb += 0.15
            entradasLista.append(campo)
            

        elif i[0] == 2:
            opcoes=["Repetição", "Mensal", "Bimestral", "Semestral", "Anual"]
            campo = ctk.CTkComboBox(self.frame, width=100, values=opcoes, corner_radius=0)
            campo.place(relx=posicaoxb, rely=0.15)
            posicaoxb += 0.15
            entradasLista.append(campo)


        else:
            campo = ctk.CTkEntry(self.frame, width=100, textvariable=variavel, corner_radius=0)
            campo.place(relx=posicaoxb, rely=0.15)
            entradasLista.append(campo)
            posicaoxb += 0.15


    self.opcoesLabelModal=["Item", "Documento", "Valor", "Vencimento"]
    self.posicaoXLabelModal = 0.2

    for labelsModal in enumerate(self.opcoesLabelModal):
        if labelsModal[0] == 0:
            labelModal = ctk.CTkLabel(self.frame, width=60, text=labelsModal[1], fg_color="#663030")
            labelModal.place(relx=self.posicaoXLabelModal+0.028, rely=0.31)
            self.posicaoXLabelModal+=0.15


        if labelsModal[0] != 0:
            labelModal = ctk.CTkLabel(self.frame, width=120, text=labelsModal[1], fg_color="#663030")
            labelModal.place(relx=self.posicaoXLabelModal-0.04, rely=0.31)
            self.posicaoXLabelModal+=0.15
        
    botaoCalcular = ctk.CTkButton(self.frame, corner_radius=0, width=100, text="Calcular", command= lambda:calculaParcelasFaturamento.calcularParcelasTotais(self, entradasLista[1].get(), entradasLista[0].get()))
    botaoCalcular.place(relx = 0.14, rely=0.2)

    dataHoje = date.today()
    self.dataHojeFormatada = dataHoje.strftime("%d/%m/%Y")

    variaveis[0].set(teste)
    variaveis[3].set(0.00)
    variaveis[4].set(self.dataHojeFormatada)

    botaoFechar = ctk.CTkButton(self.frame, text="X", width=10, height=10, corner_radius=0, command=lambda:destroyModal(self))
    botaoFechar.place(relx=0.989, rely=0.018, anchor="center")


