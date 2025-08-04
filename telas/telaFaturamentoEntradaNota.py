import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
from telas.telaTransporte import telaTransporte
from funcoesTerceiras import calculaParcelasFaturamento
from funcoesTerceiras.confirmarSalvamentoDoFaturamento import confirmarSalvamentoDoFaturamento
from componentes import criaFrameJanela, criaBotao

def telaGerarFaturamentoEntradaNota(self, DadosNota, valorDaNota):
    self.variavelRepeticao = 0
    self.row = 1
    self.frameTelaGerarFaturamento = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    self.frameValorTotais = ctk.CTkFrame(self.frameTelaGerarFaturamento, fg_color=self.cor)

    valores = ["Forma de pagamento", "Quantidade parcelas", "Valor"]
    opcoesPagamento = ["", "Bndes", "Boleto", "Carnê", "Crédito a vista", "Crédito parcelado", "Débito", "Cheque", "Depósito"]

    largura_label = 0.2
    posicaoy = 0.1
    self.y = 0.138
    self.teste = 0.038
    self.yParcelas = 0.138
    self.totais = 0
    self.totaisFormasDePagamento = ctk.StringVar()
    self.totaisFormasDePagamento.set(self.totais)

    self.descontoTotalVindoDoPedido = ctk.StringVar()
    self.acrescimoTotalVindoDoPedido = ctk.StringVar()

    self.botaoAdicionarParcela = ctk.CTkButton(
        self.frameTelaGerarFaturamento, 
        text="Adicionar Parcela", 
        width=20, 
        corner_radius=0, 
        command=lambda: verificaParcelasPreenchidas(self)
    )

    # Campos de totais
    labelEntradasTotais = ctk.CTkLabel(self.frameValorTotais, text="Total")
    labelEntradasTotais.place(relx=0.6, rely=0.10)
    self.entradasTotais = ctk.CTkEntry(self.frameValorTotais, textvariable=self.totaisFormasDePagamento)
    self.entradasTotais.place(relx=0.6, rely=0.20, relwidth=0.3)

    labelDescontoTotal = ctk.CTkLabel(self.frameValorTotais, text="Desconto total")
    labelDescontoTotal.place(relx=0.6, rely=0.35)
    self.descontoTotal = ctk.CTkEntry(self.frameValorTotais, textvariable=self.descontoTotalVindoDoPedido)
    self.descontoTotal.place(relx=0.6, rely=0.45, relwidth=0.3)

    labelAcrescimoTotal = ctk.CTkLabel(self.frameValorTotais, text="Acrescimo total")
    labelAcrescimoTotal.place(relx=0.6, rely=0.60)
    self.acrescimoTotal = ctk.CTkEntry(self.frameValorTotais, textvariable=self.acrescimoTotalVindoDoPedido)
    self.acrescimoTotal.place(relx=0.6, rely=0.70, relwidth=0.3)

    labelValorOriginal = ctk.CTkLabel(self.frameValorTotais, text="Valor original da fatura")
    labelValorOriginal.place(relx=0.1, rely=0.10)
    self.ValorOriginal = ctk.CTkEntry(self.frameValorTotais, textvariable=self.totaisFormasDePagamento)
    self.ValorOriginal.place(relx=0.1, rely=0.20, relwidth=0.3)

    labelNumeroDaFatura = ctk.CTkLabel(self.frameValorTotais, text="Número da fatura")
    labelNumeroDaFatura.place(relx=0.1, rely=0.35)
    self.NumeroDaFatura = ctk.CTkEntry(self.frameValorTotais)
    self.NumeroDaFatura.place(relx=0.1, rely=0.45, relwidth=0.3)

    labelValorDaNota = ctk.CTkLabel(self.frameValorTotais, text="Valor da nota")
    labelValorDaNota.place(relx=0.1, rely=0.60)
    self.ValorDaNota = ctk.CTkEntry(self.frameValorTotais, textvariable=valorDaNota)
    self.ValorDaNota.place(relx=0.1, rely=0.70, relwidth=0.3)

    self.listaComboboxes = []
    self.listaEntradaQuantidade = []
    self.listaVariaveisQuantidade = []
    self.listaEntradaValor = []
    self.variavelQuantidade = ctk.StringVar()

    def calcularTotal():
        total = 0
        for entrada in self.listaEntradaValor:
            try:
                valor = float(entrada.get())
            except ValueError:
                valor = 0
            total += valor

        try:
            desconto = float(self.descontoTotalVindoDoPedido.get()) if self.descontoTotalVindoDoPedido.get() else 0
        except ValueError:
            desconto = 0

        try:
            acrescimo = float(self.acrescimoTotalVindoDoPedido.get()) if self.acrescimoTotalVindoDoPedido.get() else 0
        except ValueError:
            acrescimo = 0

        total = total - desconto + acrescimo
        self.totaisFormasDePagamento.set(f"{total:.2f}")

    self.calcularTotal = calcularTotal

    def adicionaParcela(self):
        self.valorDoPedidoVariavel = ctk.StringVar()
        self.valorDoPedidoVariavel.set(valorDaNota.get())

        self.y += 0.038
        self.botaoAdicionarParcela.place(relx=0.2, rely=self.y)

        self.combobox = ctk.CTkComboBox(self.frameTelaGerarFaturamento, width=100, values=opcoesPagamento, corner_radius=0, command=lambda valor: modal(self, self.entradaValor.get()))
        self.combobox.place(relx=0.2, rely=self.yParcelas, relwidth=0.2)
        self.listaComboboxes.append(self.combobox)

        variavelQuantidade = ctk.StringVar()
        self.listaVariaveisQuantidade.append(variavelQuantidade)
        self.entradaQuantidade = ctk.CTkEntry(self.frameTelaGerarFaturamento, width=100, corner_radius=0, textvariable=variavelQuantidade)
        self.entradaQuantidade.place(relx=0.4, rely=self.yParcelas, relwidth=0.2)
        self.listaEntradaQuantidade.append(self.entradaQuantidade)

        self.entradaValor = ctk.CTkEntry(self.frameTelaGerarFaturamento, textvariable=self.valorDoPedidoVariavel, width=100, corner_radius=0)
        self.entradaValor.place(relx=0.6, rely=self.yParcelas, relwidth=0.2)
        self.entradaValor.bind("<KeyRelease>", lambda event: calcularTotal())
        self.listaEntradaValor.append(self.entradaValor)

        if len(self.listaEntradaValor) != 1:
            self.valorDoPedidoVariavel.set(0)

        self.frameValorTotais.place(relx=0.2, rely=self.y+0.1, relwidth=0.6, relheight=0.35)

    adicionaParcela(self)

    def removerParcela(self):
        if self.row == 1:
            self.botaoRemoverParcela.destroy()
            del self.botaoRemoverParcela
        else:
            if self.row == 1 and hasattr(self, "botaoRemoverParcela"):
                self.botaoRemoverParcela.destroy()
                del self.botaoRemoverParcela
            self.y -= 0.038
            self.teste -= 0.038
            self.yParcelas -= 0.038

            self.botaoAdicionarParcela.place(relx=0.2, rely=self.y)
            self.botaoRemoverParcela.place(relx=0.8, rely=self.yParcelas)
            self.frameValorTotais.place(relx=0.2, rely=self.y+0.1, relwidth=0.6, relheight=0.35)

            if len(self.listaEntradaValor) > 1:
                self.row -= 1
                self.listaEntradaValor[self.row].destroy()
                self.listaEntradaQuantidade[self.row].destroy()
                self.listaComboboxes[self.row].destroy()

                del self.listaEntradaValor[self.row]
                del self.listaEntradaQuantidade[self.row]
                del self.listaComboboxes[self.row]
                del self.listaVariaveisQuantidade[self.row]

            self.calcularTotal()

    def verificaParcelasPreenchidas(self):
        if self.listaComboboxes[self.row-1].get() and self.listaEntradaQuantidade[self.row-1].get() and self.listaEntradaValor[self.row-1].get():
            self.row += 1
            if hasattr(self, "botaoRemoverParcela") and self.botaoRemoverParcela.winfo_exists():
                self.botaoRemoverParcela.destroy()
            self.botaoRemoverParcela = ctk.CTkButton(self.frameTelaGerarFaturamento, text="X", width=20, corner_radius=0, fg_color="red", command=lambda: removerParcela(self))
            self.yParcelas += 0.038
            self.botaoRemoverParcela.place(relx=0.8, rely=self.yParcelas)
            adicionaParcela(self)

    for i, coluna in enumerate(valores):
        posicaox = 0.2 + i * largura_label
        colunas = ctk.CTkLabel(self.frameTelaGerarFaturamento, text=coluna, fg_color=self.cor)
        colunas.place(relx=posicaox, rely=posicaoy, relwidth=largura_label-0.001)

    criaBotao(self.frameTelaGerarFaturamento, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaGerarFaturamento.destroy()).place(anchor="nw")
    criaBotao(self.frameTelaGerarFaturamento, "Próximo - Transporte", 0.25, 0.94, 0.15, lambda: telaTransporte(self, DadosNota)).place(anchor="nw")

    def salvarEFechar(self):
        confirmarSalvamentoDoFaturamento(self, self.listaEntradaQuantidade, self.listaEntradaValor, self.listaComboboxes, self.data, self.variavelRepeticao)
        self.frameTelaGerarFaturamento.destroy()

    self.descontoTotal.bind("<KeyRelease>", lambda event: self.calcularTotal())
    self.acrescimoTotal.bind("<KeyRelease>", lambda event: self.calcularTotal())
    self.entradasTotais.bind("<KeyRelease>", lambda event: self.calcularTotal())
    self.ValorOriginal.bind("<KeyRelease>", lambda event: self.calcularTotal())


def modal(self, teste):
    self.frame = criaFrameJanela(self.frameTelaGerarFaturamento, 0.5, 0.5, 0.6, 0.9, self.corModal)


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


    # campos do modal
    labels = ["Valor a pagar", "Qtd Parcelas", "Repetição", "Intervalo", "1ª parcela em:"]
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
        print(variaveis[i[0]].get())

        if i[0] == 1:
            opcoes=["1", "2", "3", "4", "5", "6","7", "8", "9", "10", "11", "12"]
            campo = ctk.CTkComboBox(self.frame, width=100, values=opcoes, corner_radius=0)
            campo.place(relx=posicaoxb, rely=0.15)
            posicaoxb += 0.15
            entradasLista.append(campo)
            

        elif i[0] == 2:
            opcoes=["Mensal", "Bimestral", "Semestral", "Anual"]
            self.campoRepeticao = ctk.CTkComboBox(self.frame, width=100, values=opcoes, corner_radius=0)
            self.campoRepeticao.place(relx=posicaoxb, rely=0.15)
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
            labelModal = ctk.CTkLabel(self.frame, width=60, text=labelsModal[1], fg_color=self.cor)
            labelModal.place(relx=self.posicaoXLabelModal+0.028, rely=0.31)
            self.posicaoXLabelModal+=0.15


        if labelsModal[0] != 0:
            labelModal = ctk.CTkLabel(self.frame, width=120, text=labelsModal[1], fg_color=self.cor)
            labelModal.place(relx=self.posicaoXLabelModal-0.04, rely=0.31)
            self.posicaoXLabelModal+=0.15
        
    botaoCalcular = ctk.CTkButton(self.frame, corner_radius=0, width=100, text="Calcular", command= lambda:calculaParcelasFaturamento.calcularParcelasTotais(self, entradasLista[1].get(), entradasLista[0].get(), self.campoRepeticao.get()))
    botaoCalcular.place(relx = 0.14, rely=0.2)

    dataHoje = date.today()
    self.dataHojeFormatada = dataHoje.strftime("%d/%m/%Y")

    variaveis[0].set(teste)
    variaveis[3].set(0.00)
    variaveis[4].set(self.dataHojeFormatada)

    botaoSalvarEFechar = ctk.CTkButton(
        self.frame,
        corner_radius=0,
        width=100,
        height=10,
        text="Salvar e fechar",
        command=lambda: [
            self.listaVariaveisQuantidade[-1].set(entradasLista[1].get()),
            calculaParcelasFaturamento.SalvaAlteracoesFaturamento(self, entradasLista[0].get(), entradasLista[1].get(), variaveis),
            self.calcularTotal(),
            self.frame.destroy()
        ]
    )
    botaoSalvarEFechar.place(relx=0.14, rely=0.03)

    botaoFechar = ctk.CTkButton(self.frame, text="X", width=10, height=10, corner_radius=0, command=lambda:destroyModal(self))
    botaoFechar.place(relx=0.989, rely=0.018, anchor="center")


