import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from tkinter import messagebox
import requests
from PIL import Image
import datetime
from funcoesTerceiras.verificaSeQuerSalvar import salvarPedido
from componentes import criaFrame, criaBotao, criarLabelEntry, criaLabel, criaEntry, criaTextArea


def telaGerarPedido(self):
    self.row=1
    self.posicaoy = 0.2
    self.posicaox = 0.024
    self.posicaoyBotao = 0.231
    self.posicaoyBotaoRemover = 0.191
    linhas_widgets = []


    # usuarioLogado = self.login.get()

    #pós refat 
    listaLabels = ["Item", "Produto", "Preço", "Quantidade", "U.M.", "Desconto $", "Desconto %", "Acréscimo", "Subtotal"]
    entradasDosProdutos = []

    variavelCtkEntry = ctk.StringVar() 
    variavelFuncionarioAtual = ctk.StringVar()
    variavelDefinidaDeAcrescimo = ctk.StringVar()
    variavelValorSubtotal = ctk.StringVar()
    dataCriacao = ctk.StringVar()
    variavelEmAbertoFechado = ctk.StringVar() 

    # variavelFuncionarioAtual.set(usuarioLogado)
    variavelEmAbertoFechado.set("Em aberto")
    dataCriacao.set(value=datetime.datetime.now().strftime("%d/%m/%y"))

    frameTelaPedido = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    frameParaItens = ctk.CTkScrollableFrame(frameTelaPedido, height=200, orientation="vertical")
    frameParaItens.place(relx=0.5, rely=0.5, relwidth=0.94, anchor="center")
    container = ctk.CTkFrame(frameParaItens, fg_color="red", height=1500)
    container.pack(fill="x", padx=0, pady=0)
    frameParaItensNoFrame = ctk.CTkFrame(frameParaItens,  height=1500)
    frameParaItensNoFrame.place(x=-25, y=-280, relwidth=1.06)

    def buscaCliente(event=None): 
        nomeDoCliente = self.nomeDoClienteBuscado.get()
        dadosCliente = Buscas.buscaDadosCliente(nomeDoCliente)

        if hasattr(self, 'resultadoLabels'):
            for label in self.resultadoLabels: 
                label.destroy()

        self.resultadoLabels = []
        
        yNovo = 0.21  
        for i, row in enumerate(dadosCliente):
            if i >= 5:
                break
            label = ctk.CTkButton(frameTelaPedido,  text=row[0], corner_radius=0,fg_color="#38343c", font=("Century Gothic bold", 15), command=lambda  nome=row[0], cnpj=row[1]: selecionaCliente(nome, cnpj))
            label.place(relx=0.05, rely=yNovo, relwidth=0.27)
            self.resultadoLabels.append(label)  
            yNovo += 0.039

    def selecionaCliente(nome, cnpj):
        self.nomeDoClienteBuscado.delete(0, "end")
        self.nomeDoClienteBuscado.insert(0, nome)
        variavelCnpjBuscado = cnpj
        if cnpj:
            variavelCtkEntry.set(variavelCnpjBuscado)
        else:
            variavelCtkEntry.set("sem valores")
        for label in self.resultadoLabels: 
            label.destroy()

    def buscaProduto(event=None):
        nomeDoProduto = entradaProdutoPesquisado.get()
        Buscas.buscaProduto(nomeDoProduto)

        if hasattr(self, "resultadoLabelsProduto"):
            for label in self.resultadoLabelsProduto:
                label.destroy()

        self.resultadoLabelsProduto = []
        yNovo = 0.24

        for i, row in enumerate(Buscas.buscaProduto(nomeDoProduto)):
            if i >=3: break
            label = criaBotao(frameParaItensNoFrame, row[0], 0.195, yNovo, 0.26, lambda nome=row[0], valor=row[1], quantidade=row[2]: selecionaProduto(nome, valor, quantidade))
            label.configure(fg_color="#38343c", corner_radius=0)
            self.resultadoLabelsProduto.append(label)
            yNovo += 0.02

        entradaQuantdadeItem.bind("<KeyRelease>", lambda event: verificaQuantidadeMaxima(self.quantidadeMaximaAtualOriginal))

    def selecionaProduto(nome, valor, quantidade):
        
        entradaProdutoPesquisado.delete(0, "end")
        entradaProdutoPesquisado.insert(0, nome)
        
        entradaQuantdadeItem.delete(0, "end")
        entradaQuantdadeItem.insert(0, 0)

        entradaPreco.delete(0,"end")
        entradaPreco.insert(0, valor)

        entradaUnidadeMedida.delete(0, "end")
        entradaUnidadeMedida.insert(0, "UN")

        variavelDefinidaDeAcrescimo.set(0.00)

        variavelValorSubtotal.set(valor)
        self.quantidadeMaximaAtualOriginal = quantidade 

        for label in self.resultadoLabelsProduto: 
            label.destroy()

    def verificaQuantidadeMaxima(quantidade):
        if quantidade is not None and int(entradaQuantdadeItem.get()) >= quantidade or int(entradaQuantdadeItem.get())<=0 :
            self.quantidadeMaximaPermitida.set(quantidade)
            print(quantidade)
            labelValorQuanrtidadeMax = ctk.CTkLabel(self, text="Quantidade excede o estoque", fg_color="red", text_color="white", corner_radius=5)
            labelValorQuanrtidadeMax.pack(pady=10)
            self.after(3000, labelValorQuanrtidadeMax.destroy)

        else:
            print(self.variavelSubtotal)
            print("Menor, tá de boa")

    def buscaCep(cepPassado, numero):
        url = f"https://cep.awesomeapi.com.br/json/{cepPassado}"
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            endereco_completo = f"{dados.get('address', '')} - {numero} - {dados.get('district', '')} - {dados.get('city', '')} - {dados.get('state', '')}"
            if numero == '':
                messagebox.showerror(title="Não encontrado", message="Campo 'Número não deve ficar em branco'")
            else:
                self.entradaEnderecoNoPedido.delete(0, ctk.END)
                self.entradaEnderecoNoPedido.insert(0, endereco_completo)
        else:
            messagebox.showerror(title="Não encontrado", message="CEP não foi encontrado")
    
    def verificaItensPreenchidos(self, entradasDosProdutos):
        if any(campo.get() == '' for i, campo in enumerate(entradasDosProdutos)):
            messagebox.showerror("campos vazios", "preencha todos os campos antes de adicionar um novo item")
        else:
            self.row +=1
            if hasattr(self, "botaoRemoverItem") and self.botaoRemoverItem.winfo_exists():
                self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotao)

            # self.posicaoyBotao += 0.02
            adicionarItem(self)


    for i, coluna in enumerate(listaLabels):
        if i == 0:
            criaLabel(frameParaItensNoFrame, coluna, self.posicaox, self.posicaoy, 0.040, "#38343c")
            self.posicaox +=0.042
        if i == 1:
            criaLabel(frameParaItensNoFrame, coluna, self.posicaox, self.posicaoy, 0.16, "#38343c")
            self.posicaox +=0.161
        if i!=0 and i!=1:
            criaLabel(frameParaItensNoFrame, coluna, self.posicaox, self.posicaoy, 0.096, "#38343c")
            self.posicaox +=0.0976
    self.posicaox = 0.024
    self.botaoAdicionarItem = criaBotao(frameParaItensNoFrame, "Adicionar Item", 0.87, self.posicaoyBotao, 0.05, lambda:verificaItensPreenchidos(self, entradasDosProdutos))
    self.botaoRemoverItem = ctk.CTkButton(frameParaItensNoFrame, text="X", width=20, corner_radius=0, fg_color="red", command=lambda: removerItem(self))
    self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotao-0.04)  # Posiciona imediatamente
    

    def adicionarItem(self):
        self.posicaoy += 0.02
        self.posicaoyBotao += 0.02  # Garante que o botão de adicionar desça
        self.posicaoyBotaoRemover += 0.02  
        
        self.botaoAdicionarItem.place(relx=0.883, rely=self.posicaoyBotao)
        self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotaoRemover)  # Atualiza o botão de remoção também


        linha_widgets = []  # Lista para armazenar os widgets da linha

        for i, coluna in enumerate(listaLabels):
            if i == 0:
                label = criaLabel(frameParaItensNoFrame, i, self.posicaox, self.posicaoy, 0.040, "#38343c")
                linha_widgets.append(label)
                self.posicaox += 0.042
            elif i == 1:
                entrada = criaEntry(frameParaItensNoFrame, self.posicaox, self.posicaoy, 0.16, None)
                entradasDosProdutos.append(entrada)
                linha_widgets.append(entrada)
                self.posicaox += 0.161
            else:
                entrada = criaEntry(frameParaItensNoFrame, self.posicaox, self.posicaoy, 0.096, None)
                entradasDosProdutos.append(entrada)
                linha_widgets.append(entrada)
                self.posicaox += 0.0976

        self.posicaox = 0.024
        linhas_widgets.append(linha_widgets)

        # Mapear entradas
        entradaProdutoPesquisado    = entradasDosProdutos[-8]
        entradaPreco                = entradasDosProdutos[-7]
        entradaQuantdadeItem        = entradasDosProdutos[-6]
        entradaUnidadeMedida        = entradasDosProdutos[-5]
        entradaDescontosReal        = entradasDosProdutos[-4]
        entradaDescontosPorcentagem = entradasDosProdutos[-3]
        entradaAcrescimo            = entradasDosProdutos[-2]
        entradaSubtotal             = entradasDosProdutos[-1]

        # Valores padrão
        entradaProdutoPesquisado.insert(0, "teste")
        entradaPreco.insert(0, "teste")
        entradaQuantdadeItem.insert(0, "teste")
        entradaUnidadeMedida.insert(0, "teste")
        entradaDescontosReal.insert(0, "teste")
        entradaDescontosPorcentagem.insert(0, "teste")
        entradaAcrescimo.insert(0, "teste")
        entradaSubtotal.insert(0, "teste")

        entradaProdutoPesquisado.bind("<KeyRelease>", buscaProduto)
        frameTelaPedido.bind("<Button-1>", lambda event: [label.destroy() for label in getattr(self, 'resultadoLabelsProduto', [])])
        frameTelaPedido.bind("<Button-1>", lambda event: [label.destroy() for label in getattr(self, 'resultadoLabels', [])])

    
    
    
    adicionarItem(self)





    def removerItem(self):
        if len(linhas_widgets) > 1:
            ultima_linha = linhas_widgets.pop()
            
            for _ in range(8):
                if entradasDosProdutos:
                    entradasDosProdutos.pop()
            
            for widget in ultima_linha:
                widget.destroy()
            
            self.posicaoy -= 0.02
            self.posicaoyBotao -= 0.02
            self.posicaoyBotaoRemover -= 0.02
            
            self.botaoAdicionarItem.place(relx=0.883, rely=self.posicaoyBotao)
            self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotaoRemover)
        
        if len(linhas_widgets) == 1:
            self.botaoRemoverItem.place_forget()



    self.numeroDeVenda = criarLabelEntry(frameTelaPedido, "Número da venda", 0.05, 0.05, 0.12, None)
    self.dataDeCriacao = criarLabelEntry(frameTelaPedido, "Data de criação", 0.20, 0.05, 0.12, dataCriacao)
    self.nomeDoClienteBuscado = criarLabelEntry(frameTelaPedido, "Nome do cliente *", 0.05, 0.15, 0.27, None)
    self.nomeDoClienteBuscado.bind("<KeyRelease>", buscaCliente)

    self.dataDaVenda = criarLabelEntry(frameTelaPedido, "Data da venda", 0.39, 0.05, 0.15, None)
    self.statusDoPedido = criarLabelEntry(frameTelaPedido, "Status", 0.57, 0.05, 0.15, variavelEmAbertoFechado)
    self.funcionariaPedido = criarLabelEntry(frameTelaPedido, "Vendedor(a)", 0.75, 0.05, 0.15, variavelFuncionarioAtual)
    self.CPFCliente = criarLabelEntry(frameTelaPedido, "CPF/CNPJ *", 0.39, 0.15, 0.15, variavelCtkEntry)
    self.entradaCEP = criarLabelEntry(frameTelaPedido, "CEP *", 0.57, 0.15, 0.15, None)
    self.entradaNumero = criarLabelEntry(frameTelaPedido, "Nº *", 0.75, 0.15, 0.05, None)
    self.botaoBuscaCEP = criaBotao(frameTelaPedido, "Buscar CEP", 0.865, 0.19, 0.07, lambda:buscaCep(self.entradaCEP.get(), self.entradaNumero.get()))
    self.entradaEnderecoNoPedido = criarLabelEntry(frameTelaPedido, "Endereço *", 0.39, 0.25, 0.33, None)
    self.entradaReferenciaEnderecoEntrega = criarLabelEntry(frameTelaPedido, "Referencia *", 0.75, 0.25, 0.15, None)

    # área de texto observações
    criaTextArea(frameTelaPedido, 0.05, 0.65, 0.2, "Observações", "É necessário a apresentação do recibo de venda para que a vendedora abra \na assistência técnica, se necessário. Não devolvemos dinheiro. \n\nCONDIÇÃO DE PAGAMENTO:\nTROCA: \nENTREGA:")
    criaTextArea(frameTelaPedido, 0.3, 0.65, 0.2, "Observações da entrega", "Dados financeiros pertinentes")

    criaBotao(frameTelaPedido, "Voltar", 0.15, 0.95, 0.20, lambda:frameTelaPedido.destroy())
    criaBotao(frameTelaPedido, "Cadastrar", 0.87, 0.95, 0.20, lambda:salvarPedido(self))



