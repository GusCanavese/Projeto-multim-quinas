import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
from funcoesTerceiras import calculaParcelasFaturamento

def telaGerarFaturamento(self, valorDoPedido):
    valorDoPedidoVariavel = ctk.StringVar()
    valorDoPedidoVariavel.set(valorDoPedido)
    self.row=1
    self.frameTelaGerarFaturamento = ctk.CTkFrame(self)
    self.frameTelaGerarFaturamento.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    valores = ["Forma de pagamento", "Quantidade parcelas", "Valor"]
    opcoesPagamento = ["", "Bndes", "Boleto", "Carnê", "Crédito a vista", "Crédito parcelado", "Débito", "Cheque", "Depósito"]

    largura_label = 0.2 
    posicaoy = 0.1
    self.y=0.138
    self.teste =0.038
    self.yParcelas = 0.138

    self.botaoAdicionarParcela = ctk.CTkButton(self.frameTelaGerarFaturamento, text="Adicionar Parcela", width=20, corner_radius=0, command=lambda:verificaParcelasPreenchidas(self)) 

    self.listaComboboxes = []
    self.listaEntradaQuantidade = []
    self.listaEntradaValor = []



    def adicionaParcela(self):
        self.y += 0.038
        self.botaoAdicionarParcela.place(relx=0.2, rely=self.y)  # se botao já for salvo

        self.combobox = ctk.CTkComboBox(self.frameTelaGerarFaturamento, width=100, values=opcoesPagamento, corner_radius=0, command=lambda valor: modal(self, self.entradaValor.get()))
        self.combobox.place(relx=0.2, rely=self.yParcelas, relwidth=0.2)
        self.listaComboboxes.append(self.combobox)
        

        self.entradaQuantidade = ctk.CTkEntry(self.frameTelaGerarFaturamento, width=100, corner_radius=0)
        self.entradaQuantidade.place(relx=0.4, rely=self.yParcelas, relwidth=0.2)
        self.listaEntradaQuantidade.append(self.entradaQuantidade)

        self.entradaValor = ctk.CTkEntry(self.frameTelaGerarFaturamento, textvariable=valorDoPedidoVariavel, width=100, corner_radius=0)
        self.entradaValor.place(relx=0.6, rely=self.yParcelas, relwidth=0.2)
        self.listaEntradaValor.append(self.entradaValor)
        print(self.entradaValor)

    adicionaParcela(self)

    def removerParcela(self):
        if self.row ==1:
            self.botaoRemoverParcela.destroy()
            del self.botaoRemoverParcela
            print("primeira linha ja encontrada")
            print(self.row)
            pass
        else:
            if self.row ==1 and hasattr(self, "botaoRemoverParcela"):
                self.botaoRemoverParcela.destroy()
                del self.botaoRemoverParcela
                print("teste")
            self.y-=0.038
            self.teste -=0.038
            self.yParcelas -=0.038
            
            self.botaoAdicionarParcela.place(relx=0.2, rely=self.y)
            self.botaoRemoverParcela.place(relx=0.8, rely=self.yParcelas)

            if len(self.listaEntradaValor)>1:
                self.row -= 1
                print(self.row)
                self.listaEntradaValor[self.row].destroy()
                self.listaEntradaQuantidade[self.row].destroy()
                self.listaComboboxes[self.row].destroy()

                del self.listaEntradaValor[self.row]
                del self.listaEntradaQuantidade[self.row]
                del self.listaComboboxes[self.row]


    def verificaParcelasPreenchidas(self):
        if (self.listaComboboxes[self.row-1].get() and self.listaEntradaQuantidade[self.row-1].get() and self.listaEntradaValor[self.row-1].get()):
            
            self.row +=1
            print(self.row)

            if hasattr(self, "botaoRemoverParcela") and self.botaoRemoverParcela.winfo_exists():
                self.botaoRemoverParcela.destroy()
            self.botaoRemoverParcela = ctk.CTkButton(self.frameTelaGerarFaturamento, text="X", width=20, corner_radius=0, fg_color="red", command=lambda: removerParcela(self))
            self.yParcelas += 0.038
            
            self.botaoRemoverParcela.place(relx=0.8, rely=self.yParcelas)
            adicionaParcela(self)

        else:
            print("oi")


    def obterValoresDasParcelas(self):
        for i, (combo, entradaQTD, entradaValor) in enumerate(zip(self.listaComboboxes, self.listaEntradaQuantidade, self.listaEntradaValor)):
            self.valorCombobox = combo.get()
            self.valorEntradaQuantidade = entradaQTD.get()
            self.valorEntradaValor = entradaValor.get()

            self.teste.set(self.valorEntradaValor)



    botaoteste = ctk.CTkButton(self.frameTelaGerarFaturamento, command=lambda: obterValoresDasParcelas(self))
    botaoteste.place(x=300, y=300)
  
    
    for i, coluna in enumerate(valores):
        posicaox = 0.2 + i * largura_label  
        colunas = ctk.CTkLabel(self.frameTelaGerarFaturamento, text=coluna, fg_color="#48424d")
        colunas.place(relx=posicaox, rely=posicaoy, relwidth=largura_label-0.001)

    modal(self, 50)

def modal(self, teste):
    frame = ctk.CTkFrame(self.frameTelaGerarFaturamento)
    frame.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.9, anchor="center")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    for widget in self.frameTelaGerarFaturamento.winfo_children():
        try:
            widget.configure(state="disabled")
        except:
            pass

    for widget in frame.winfo_children():
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
        frame.destroy()


    # colunasParcelas = ["Item Documento,", "Valor", "Vencimento", "Informação 1", "Informação 2", "Informação 3"]
    # posicaoxa = 0.1
    # for i, coluna in enumerate(colunasParcelas):
    #     colunas = ctk.CTkLabel(frame, text=coluna)
    #     colunas.place(relx=posicaoxa, rely=0.5, anchor="center")
    #     posicaoxa += 0.1 +0.2


    # campos do modal
    labels = ["Valor a pagar", "Qtd Parcelas", "repeticao", "Intervalo", "1ª parcela em:"]
    posicaoxb = 0.14
    for i, label in enumerate(labels):
        labelTituloCampo = ctk.CTkLabel(frame, text=label, width=100)
        labelTituloCampo.place(relx=posicaoxb, rely=0.05)
        posicaoxb += 0.15

    posicaoxb = 0.14
    entradasLista = []
    variaveis=[]
    for i in enumerate(labels):
        variavel = ctk.StringVar()
        variaveis.append(variavel)

        if i[0] == 1:
            opcoes=["1","2","3","4","5","6","7","8","9","10","11","12",]
            campo = ctk.CTkComboBox(frame, width=100, values=opcoes, corner_radius=0)
            campo.place(relx=posicaoxb, rely=0.1)
            posicaoxb += 0.15
            entradasLista.append(campo)
            


        elif i[0] == 2:
            opcoes=["Repetição", "Mensal", "Bimestral", "Semestral", "Anual"]
            campo = ctk.CTkComboBox(frame, width=100, values=opcoes, corner_radius=0)
            campo.place(relx=posicaoxb, rely=0.1)
            posicaoxb += 0.15
            entradasLista.append(campo)


        else:
            campo = ctk.CTkEntry(frame, width=100, textvariable=variavel, corner_radius=0)
            campo.place(relx=posicaoxb, rely=0.1)
            entradasLista.append(campo)
            posicaoxb += 0.15

    dataHoje = date.today()
    dataHojeFormatada = dataHoje.strftime("%d/%m/%Y")



    variaveis[0].set(teste)
    variaveis[3].set(0.00)
    variaveis[4].set(dataHojeFormatada)


    def getEntradas():
        ValorAPagar = entradasLista[0].get()
        quantidade = entradasLista[1].get()
        juros = entradasLista[2].get()
        taxa = entradasLista[3].get()
        repeticao = entradasLista[4].get()
        intervalo = entradasLista[5].get()
        primeiraParcela = entradasLista[5].get()

    botaoCalcular = ctk.CTkButton(frame, corner_radius=0, width=100, text="Calcular", command= lambda:calculaParcelasFaturamento.calculaParcelasFaturamento(self))
    botaoCalcular.place(relx = 0.14, rely=0.15)
  
    

    
    botao = ctk.CTkButton(frame, command=lambda:getEntradas())
    botao.place(x=300, y=300)


    botao_fechar = ctk.CTkButton(frame, text="X", width=10, height=10, corner_radius=0, command=lambda:destroyModal(self))
    botao_fechar.place(relx=0.989, rely=0.018, anchor="center")