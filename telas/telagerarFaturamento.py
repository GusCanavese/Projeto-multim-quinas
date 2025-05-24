import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk

def telaGerarFaturamento(self):
    self.row=1
    self.frameTelaGerarFaturamento = ctk.CTkFrame(self)
    self.frameTelaGerarFaturamento.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    valores = ["Forma de pagamento", "Quantidade parcelas", "Valor"]
    opcoesPagamento = ["", "Bndes", "Boleto", "Carnê", "Crédito a vista", "Crédito parcelado", "Débito", "Cheque", "Depósito"]

    largura_label = 0.2 
    posicaoy = 0.1
    self.y=0.138
    self.teste =0.038
    self.yParcelas = 0.1

    self.botaoAdicionarParcela = ctk.CTkButton(self.frameTelaGerarFaturamento, text="Adicionar Parcela", width=20, corner_radius=0, command=lambda:verificaParcelasPreenchidas(self)) 

    self.listaComboboxes = []
    self.listaEntradaQuantidade = []
    self.listaEntradaValor = []



    def adicionaParcela(self):
        self.y += 0.038
        self.yParcelas += 0.038
        self.botaoAdicionarParcela.place(relx=0.2, rely=self.y)  # se botao já for salvo

        self.combobox = ctk.CTkComboBox(self.frameTelaGerarFaturamento, width=100, values=opcoesPagamento, corner_radius=0, command=lambda valor: modal(self, valor))
        self.combobox.place(relx=0.2, rely=self.yParcelas, relwidth=0.2)
        self.listaComboboxes.append(self.combobox)

        self.entradaQuantidade = ctk.CTkEntry(self.frameTelaGerarFaturamento, width=100, corner_radius=0)
        self.entradaQuantidade.place(relx=0.4, rely=self.yParcelas, relwidth=0.2)
        self.listaEntradaQuantidade.append(self.entradaQuantidade)

        self.entradaValor = ctk.CTkEntry(self.frameTelaGerarFaturamento, width=100, corner_radius=0)
        self.entradaValor.place(relx=0.6, rely=self.yParcelas, relwidth=0.2)
        self.listaEntradaValor.append(self.entradaValor)
    adicionaParcela(self)

    def removerParcela(self):
        if self.row <2:
            print("primeira linha ja encontrada")
            print(self.row)
            pass
        else:
            
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
            print(self.row)
            self.row +=1

            if hasattr(self, "botaoRemoverParcela") and self.botaoRemoverParcela.winfo_exists():
                self.botaoRemoverParcela.destroy()
            self.botaoRemoverParcela = ctk.CTkButton(self.frameTelaGerarFaturamento, text="X", width=20, corner_radius=0, fg_color="red", command=lambda: removerParcela(self))
            self.botaoRemoverParcela.place(relx=0.8, rely=self.yParcelas + self.teste)
            adicionaParcela(self)

        else:
            print("oi")

    def obterValoresDasParcelas(self):
        for i, (combo, entradaQTD, entradaValor) in enumerate(zip(self.listaComboboxes, self.listaEntradaQuantidade, self.listaEntradaValor)):
            valorCombobox = combo.get()
            valorEntradaQuantidade = entradaQTD.get()
            valorEntradaValor = entradaValor.get()

            print(f"forma de pagamento: {valorCombobox}, quantidade:{valorEntradaQuantidade}, valor:{valorEntradaValor}")

    botaoteste = ctk.CTkButton(self.frameTelaGerarFaturamento, command=lambda: obterValoresDasParcelas(self))
    botaoteste.place(x=300, y=300)
  
    
    for i, coluna in enumerate(valores):
        posicaox = 0.2 + i * largura_label  
        colunas = ctk.CTkLabel(self.frameTelaGerarFaturamento, text=coluna, fg_color="#48424d")
        colunas.place(relx=posicaox, rely=posicaoy, relwidth=largura_label-0.001)

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


    colunasParcelas = ["Item Documento,", "Valor", "Vencimento", "Informação 1", "Informação 2", "Informação 3"]
    posicaoxa = 0.1
    for i, coluna in enumerate(colunasParcelas):
        colunas = ctk.CTkLabel(frame, text=coluna)
        colunas.place(relx=posicaoxa, rely=0.5, anchor="center")
        posicaoxa += 0.1 +0.2


    # campos do modal
    labels = ["Valor a pagar", "Qtd Parcelas", "%juros a.m.", "taxa p. parcela", "repeticao", "Intervalo", "1ª parcela em:"]
    posicaoxb = 0.05
    for i, label in enumerate(labels):
        labelTituloCampo = ctk.CTkLabel(frame, text=label, width=80)
        labelTituloCampo.place(relx=posicaoxb, rely=0.05)
        posicaoxb += 0.13

    posicaoxb = 0.05
    entradasLista = []
    for i in enumerate(labels):
        campo = ctk.CTkEntry(frame, width=80, corner_radius=0)
        campo.place(relx=posicaoxb, rely=0.1)
        entradasLista.append(campo)
        posicaoxb += 0.13


    def getEntradas():
        ValorAPagar = entradasLista[0].get()
        quantidade = entradasLista[1].get()
        juros = entradasLista[2].get()
        taxa = entradasLista[3].get()
        repeticao = entradasLista[4].get()
        intervalo = entradasLista[5].get()
        primeiraParcela = entradasLista[5].get()
  
    

    
    botao = ctk.CTkButton(frame, command=lambda:getEntradas())
        
    botao.place(x=300, y=300)


    botao_fechar = ctk.CTkButton(frame, text="Fechar", command=lambda:destroyModal(self))
    botao_fechar.place(relx=0.5, rely=0.7, anchor="center")