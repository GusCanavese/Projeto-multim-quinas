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
    self.variavelCnpjBuscado = None
    self.variavelCtkEntry = ctk.StringVar() #esses 2 só inicializam para conseguir usar fora da função
    self.quantidadeMaximaPermitida = ctk.StringVar()
    self.variavelDefinidaDePorcentagem = ctk.StringVar()
    self.variavelDefinidaDeReal = ctk.StringVar()
    self.variavelDefinidaDeAcrescimo = ctk.StringVar()
    self.variavelDefinidaDeSubtotal = ctk.StringVar()
    self.variavelFuncionarioAtual = ctk.StringVar()
    
    self.variavelTotalDescontoReal = ctk.StringVar()
    self.variavelTotalDescontoPorcentagem = ctk.StringVar()
    self.variavelTotalAcrescimo = ctk.StringVar()
    self.variavelTotalSubtotal = ctk.StringVar()
    self.variavelnumeroDoPedido = ctk.StringVar()

    # variaveispósrefatoração
    self.dataCriacao = ctk.StringVar()
    self.variavelEmAbertoFechado = ctk.StringVar() 

    self.variavelEmAbertoFechado.set("Em aberto")
    self.dataCriacao.set(value=datetime.datetime.now().strftime("%d/%m/%y"))



    # usuarioLogado = self.login.get()
    self.numeroDoPedido = 0
    self.totalPreco = 0.0
    self.totalQuantidade = 0
    self.totalDescontoReal = 0.0
    self.totalDescontoPorcentagem = 0.0
    self.totalAcrescimo = 0.0
    self.totalSubtotal = 0.0

    # self.variavelFuncionarioAtual.set(usuarioLogado)

    self.variavelSubtotal = 0.00
    self.variavelSubtotalAux = 0.00
    
    def geraNumeroPedido():
        # self.numeroDoPedido += 1
        maiorNumero = Buscas.selecionaNumeroPedido()[0]
        
        print(maiorNumero)
        if maiorNumero == None:
            maiorNumero = 1
        else:
            maiorNumero += 1
        numeroDoPedidoSendoCriado = maiorNumero
        self.variavelnumeroDoPedido.set(numeroDoPedidoSendoCriado)

    # criação do frame
    frameTelaPedido = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
   

    # criar canva para itens adicionados

    self.frameParaItens = ctk.CTkScrollableFrame(frameTelaPedido, height=200, orientation="vertical")
    self.frameParaItens.place(relx=0.5, rely=0.5, relwidth=0.94, anchor="center")

    self.container = ctk.CTkFrame(self.frameParaItens, fg_color="red", height=1500)
    self.container.pack(fill="x", padx=0, pady=0)

    self.frameParaItensNoFrame = ctk.CTkFrame(self.frameParaItens,  height=1500)
    self.frameParaItensNoFrame.place(x=-25, y=-280, relwidth=1.06)

    def calcularTotais():
        self.totalPreco = 0.0
        self.totalQuantidade = 0
        self.totalDescontoReal = 0.0
        self.totalDescontoPorcentagem = 0.0
        self.totalAcrescimo = 0.0
        self.totalSubtotal = 0.0

        primeiroCampoDescontoReal = float(self.entradaDescontosReal.get() or 0)  
        self.totalDescontoReal += primeiroCampoDescontoReal  

        primeiroCampoDescontoPorcentagem = float(self.entradaDescontosPorcentagem.get() or 0)  
        self.totalDescontoPorcentagem += primeiroCampoDescontoPorcentagem  

        primeiroCampoAcrescimo = float(self.entradaAcrescimo.get() or 0)  
        self.totalAcrescimo += primeiroCampoAcrescimo  

        primeiroCampoSubtotal = float(self.entradaSubtotal.get() or 0)  
        self.totalSubtotal += primeiroCampoSubtotal

        primeiroCampoQuantidade = float(self.entradaQuantdadeItem.get() or 0)
        self.totalQuantidade += primeiroCampoQuantidade

        for item in self.itensCriados:
            preco = float(item[2].get() or 0)  # entradaPreco
            quantidade = int(item[3].get() or 0)  # entradaQuantidade
            descontoReal = float(item[5].get() or 0)  # entradaDescontosReal
            descontoPorcentagem = float(item[6].get() or 0)  # entradaDescontosPorcentagem
            acrescimo = float(item[7].get() or 0)  # entradaAcrescimo

            subtotalCalculado = (preco * quantidade) + acrescimo - descontoReal
            if subtotalCalculado<0:subtotalCalculado=0

            item[8].delete(0, "end")
            item[8].insert(0, f"{subtotalCalculado:.2f}")

            self.totalPreco += preco
            self.totalQuantidade += quantidade
            self.totalDescontoReal += descontoReal
            self.totalDescontoPorcentagem += descontoPorcentagem
            self.totalAcrescimo += acrescimo
            self.totalSubtotal += subtotalCalculado


        self.variavelTotalDescontoReal.set(round(self.totalDescontoReal, 2))
        self.variavelTotalAcrescimo.set(round(self.totalAcrescimo, 2))
        self.variavelTotalDescontoPorcentagem.set(round(self.totalDescontoPorcentagem, 2))
        self.variavelTotalSubtotal.set(round(self.totalSubtotal, 2))

        

        
        salvarValoresDosItens()
    
        print(self.quantidades)
    


    # frame para calcular os totais no final da pagina


    # frame valor final para finalizar o preço de tudo
    self.frameValorFinal = ctk.CTkFrame(frameTelaPedido, width=200, height=150)
    self.frameValorFinal.place(relx=0.8, rely=0.7)
    self.quantidades = []

    self.valoresDosItens = []
    self.totaisDosItens = []

    self.codigoItem = 0


    def salvarValoresDosItens():
        self.valoresDosItens = []

        # Adiciona os valores originais (campos que dão origem aos itens)
        valoresItem = {
            "codigo": "Modelo",
            "descricao": self.entradaProdutoPesquisado.get(),
            "valor_unitario": self.entradaPreco.get() or 0,
            "quantidade": self.entradaQuantdadeItem.get(),
            "unidade": self.entradaUnidadeMedida.get(),
            "desconto_real": self.descontoTotalReal.get() or 0,
            "desconto_porcentagem": self.descontoTotalPorcento.get() or 0,
            "acrescimo": self.entradaAcrescimo.get() or 0,
            "subtotal": self.entradaSubtotal.get() or 0
        }
        self.valoresDosItens.append(valoresItem)

        # Adiciona os valores dos itens já criados
        i=1
        for item in self.itensCriados:
            i+=1
            valoresItem = {
                "codigo": "Modelo",
                "descricao": item[1].get(),
                "valor_unitario": float(item[2].get() or 0),
                "unidade": item[4].get(),
                "quantidade": int(item[3].get() or 0),
                "desconto_real": float(item[5].get() or 0),
                "desconto_porcentagem": float(item[6].get() or 0),
                "acrescimo": float(item[7].get() or 0),
                "subtotal": float(item[8].get() or 0)
            }
            self.valoresDosItens.append(valoresItem)

    # pesquisa que fica aparecendo e sumindo os valores que estou pesquisando
    def buscaCliente(event=None): 
        calcularTotais()
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

    # seleciona o nome e o cpf/cnpj 
    def selecionaCliente(nome, cnpj):
        self.nomeDoClienteBuscado.delete(0, "end")
        self.nomeDoClienteBuscado.insert(0, nome)
        self.variavelCnpjBuscado = cnpj
        if cnpj:
            self.variavelCtkEntry.set(self.variavelCnpjBuscado)
        else:
            self.variavelCtkEntry.set("sem valores")
        for label in self.resultadoLabels: 
            label.destroy()

    # pesquisa que fica aparecendo quando digitamos algo no campo do produto
    def buscaProduto(event=None):
        calcularTotais()
        nomeDoProduto = self.entradaProdutoPesquisado.get()
        Buscas.buscaProduto(nomeDoProduto)

        if hasattr(self, "resultadoLabelsProduto"):
            for label in self.resultadoLabelsProduto:
                label.destroy()

        self.resultadoLabelsProduto = []
        yNovo = 0.24



        for i, row in enumerate(Buscas.buscaProduto(nomeDoProduto)):
            if i >=3: break
            label = criaBotao(self.frameParaItensNoFrame, row[0], 0.195, yNovo, 0.26, lambda nome=row[0], valor=row[1], quantidade=row[2]: selecionaProduto(nome, valor, quantidade))
            label.configure(fg_color="#38343c", corner_radius=0)
            self.resultadoLabelsProduto.append(label)
            yNovo += 0.02


        # ações realizadas quando digitamos em cada campo
        self.entradaQuantdadeItem.bind("<KeyRelease>", lambda event: verificaQuantidadeMaxima(self.quantidadeMaximaAtualOriginal))
        self.entradaAcrescimo.bind("<KeyRelease>", lambda event: calcularAlteracoes())
        self.entradaPreco.bind("<KeyRelease>", lambda event: calcularAlteracoes())
        self.entradaDescontosReal.bind("<FocusIn>", lambda event: limparCampo(event, self.entradaDescontosPorcentagem))
        self.entradaDescontosReal.bind("<KeyRelease>", lambda event: calcularAlteracoes())
        self.entradaDescontosPorcentagem.bind("<FocusIn>", lambda event: limparCampo(event, self.entradaDescontosReal))
        self.entradaDescontosPorcentagem.bind("<KeyRelease>", lambda event: calcularAlteracoes())
        self.entradaAcrescimo.bind("<KeyRelease>", lambda event: calcularTotais())
        self.entradaDescontosPorcentagem.bind("<KeyRelease>", lambda event: calcularTotais())
        self.entradaDescontosReal.bind("<KeyRelease>", lambda event: calcularTotais())
        self.entradaSubtotal.bind("<KeyRelease>", lambda event: calcularTotais())
        
    # chamado somente para deixar o campo "desconto" em branco
    def limparCampo(event, campo):
        campo.delete(0, "end")

    # ao selecionar o produto é chamada
    def selecionaProduto(nome, valor, quantidade):
        
        self.entradaProdutoPesquisado.delete(0, "end")
        self.entradaProdutoPesquisado.insert(0, nome)
        
        self.entradaQuantdadeItem.delete(0, "end")
        self.entradaQuantdadeItem.insert(0, 0)

        self.entradaPreco.delete(0,"end")
        self.entradaPreco.insert(0, valor)

        self.entradaUnidadeMedida.delete(0, "end")
        self.entradaUnidadeMedida.insert(0, "UN")

        self.variavelDefinidaDeAcrescimo.set(0.00)
        self.quantidadeMaximaAtualOriginal = quantidade 

        calcularAlteracoes()
        for label in self.resultadoLabelsProduto: 
            label.destroy()
            
        calcularTotais()
        
    # toda alteração realizada o subtotal precisa ser atualizado
    def calcularAlteracoes():
        preco = float(self.entradaPreco.get() or 0)
        acrescimo = float(self.entradaAcrescimo.get() or 0)
        descontoReal = float(self.entradaDescontosReal.get() or 0)      
        descontoPorcentagem = float(self.entradaDescontosPorcentagem.get() or 0)
        if descontoReal:
            self.variavelSubtotal = ((preco * int(self.entradaQuantdadeItem.get())) + acrescimo) - descontoReal
            self.variavelDefinidaDeSubtotal.set(self.variavelSubtotal)
        else:
            descontoPorcentagem = descontoPorcentagem/100
            self.variavelSubtotal = ((preco * int(self.entradaQuantdadeItem.get())) + acrescimo)
            self.variavelSubtotalAux = self.variavelSubtotal
            self.variavelSubtotal = ((preco * int(self.entradaQuantdadeItem.get())) + acrescimo) * descontoPorcentagem
            self.variavelSubtotalAux = self.variavelSubtotalAux - self.variavelSubtotal
            self.variavelDefinidaDeSubtotal.set(self.variavelSubtotalAux)

    # verifica se a quantidade sendo vendida é menor do que a quantidade existente no depósito
    def verificaQuantidadeMaxima(quantidade):
        if quantidade is not None and int(self.entradaQuantdadeItem.get()) >= quantidade or int(self.entradaQuantdadeItem.get())<=0 :
            self.quantidadeMaximaPermitida.set(quantidade)
            print(quantidade)
            labelValorQuanrtidadeMax = ctk.CTkLabel(self, text="Quantidade excede o estoque", fg_color="red", text_color="white", corner_radius=5)
            labelValorQuanrtidadeMax.pack(pady=10)
            self.after(3000, labelValorQuanrtidadeMax.destroy)
            calcularAlteracoes()

        else:
            calcularAlteracoes()
            print(self.variavelSubtotal)
            print("Menor, tá de boa")

    #! AO EXCLUIR OS ITENS, ELES ESTÃO SENDO EXCLUÍDOS FORA DE ORDEM FUNÇÃO COM DEFEITO
    def removerItem(index):
        if 0 <= index:  
            for widget in self.itensCriados[index-1]:
                if widget:  
                    widget.destroy()  
            self.itensCriados.pop(index-1)  

            self.yAtualBotao -= self.yFuturoBotao
            if self.itensCriados:
                ultimoItem = self.itensCriados[-1]
                if ultimoItem[-1] is None:  
                    print("oi")
                    if hasattr(self, "botaoRemover"):
                        self.botaoRemover.destroy()
                    self.botaoRemover = criaBotao(self.frameParaItensNoFrame, "x", 0.92, self.yAtualBotao, 0.02, lambda idx=len(self.itensCriados): removerItem(idx))
                    self.botaoRemover.configure(fg_color="red")

                    ultimoItem[-1] = self.botaoRemover


            if hasattr(self, "botaoAdicionarItem"):
                self.botaoAdicionarItem.destroy()
            self.botaoAdicionarItem = criaBotao(self.frameParaItensNoFrame, "Adicionar Item", 0.87, self.yAtualBotao, 0.05, lambda:adicionarItem())
    
    def adicionarItem():

        if self.itensCriados:
            ultimoItem = self.itensCriados[-1]
            camposObrigatorios = [
                ultimoItem[1].get(),  
                ultimoItem[2].get(),  
                ultimoItem[3].get(),  
                ultimoItem[4].get()   
            ]

            if any(campo == "" for campo in camposObrigatorios):
                labelValorPreenchaCampos = ctk.CTkLabel(self, text="Preencha todos os campos", fg_color="red", text_color="white", corner_radius=5)
                labelValorPreenchaCampos.pack(pady=10)
                self.after(3000, labelValorPreenchaCampos.destroy)
                return  

        numeroItem = len(self.itensCriados) + 1

        labelNumeroItem=criaLabel(self.frameParaItensNoFrame, f"{numeroItem+1}", 0.024, self.yAtualBotao, 0.040, "#38343c")
        entradaProdutoPesquisado=criaEntry(self.frameParaItensNoFrame, 0.066, self.yAtualBotao, 0.16, None)
        entradaPreco = criaEntry(self.frameParaItensNoFrame, 0.2270, self.yAtualBotao, 0.096, None)
        entradaQuantidade = criaEntry(self.frameParaItensNoFrame, 0.325, self.yAtualBotao, 0.096, None)
        entradaUnidadeMedida = criaEntry(self.frameParaItensNoFrame, 0.422, self.yAtualBotao, 0.096, None)
        entradaDescontosReal = criaEntry(self.frameParaItensNoFrame, 0.520, self.yAtualBotao, 0.096, None)
        entradaDescontosPorcentagem = criaEntry(self.frameParaItensNoFrame, 0.6175, self.yAtualBotao, 0.096, None)
        entradaAcrescimo = criaEntry(self.frameParaItensNoFrame, 0.715, self.yAtualBotao, 0.096, None)
        entradaSubtotal = criaEntry(self.frameParaItensNoFrame, 0.813, self.yAtualBotao, 0.096, None)

        self.botaoRemover = criaBotao(self.frameParaItensNoFrame,"x", 0.92, self.yAtualBotao, 0.02, lambda idx=len(self.itensCriados): removerItem(idx))
        self.botaoRemover.configure(fg_color="red")



        if self.itensCriados:
            ultimoItem = self.itensCriados[-1]
            if ultimoItem[-1]: 
                ultimoItem[-1].destroy() 
                ultimoItem[-1] = None 

        self.itensCriados.append([
            labelNumeroItem, entradaProdutoPesquisado, entradaPreco, entradaQuantidade, entradaUnidadeMedida,
            entradaDescontosReal, entradaDescontosPorcentagem, entradaAcrescimo, entradaSubtotal, self.botaoRemover
        ])

        calcularAlteracoesParaItem(numeroItem - 1)

        self.yAtualBotao += self.yFuturoBotao
        if hasattr(self, "botaoAdicionarItem"):
            self.botaoAdicionarItem.destroy()
        self.botaoAdicionarItem = criaBotao(self.frameParaItensNoFrame, "Adicionar Item", 0.87, self.yAtualBotao, 0.05, lambda:adicionarItem())


        entradaProdutoPesquisado.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: buscaProdutoParaItem(idx))
        entradaPreco.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: calcularAlteracoesParaItem(idx))
        entradaQuantidade.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: verificaQuantidadeMaximaParaItem(self.quantidadeMaximaAtualItem, idx))
        entradaDescontosReal.bind("<FocusIn>", lambda event, idx=len(self.itensCriados) - 1: limparCampo(event, self.itensCriados[idx][6]))
        entradaDescontosReal.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: calcularAlteracoesParaItem(idx))
        entradaDescontosPorcentagem.bind("<FocusIn>", lambda event, idx=len(self.itensCriados) - 1: limparCampo(event, self.itensCriados[idx][5]))
        entradaDescontosPorcentagem.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: calcularAlteracoesParaItem(idx))
        entradaAcrescimo.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: calcularAlteracoesParaItem(idx))
        calcularTotais()

    # busca o produto no banco de dados
    def buscaProdutoParaItem(index):
        nomeDoProduto = self.itensCriados[index][1].get()
        Buscas.buscaProduto(nomeDoProduto)
        print(Buscas.buscaProduto(nomeDoProduto))


        if hasattr(self, "resultadoLabelsProduto"):
            for label in self.resultadoLabelsProduto:
                label.destroy()

        self.resultadoLabelsProduto = []

        yNovo = 0.26 + (index*32)
        
        for i, row in enumerate(Buscas.buscaProduto(nomeDoProduto)):
            if i >= 3: break
            label = criaBotao(self.frameParaItensNoFrame, row[0], 0.195, yNovo, 0.26, lambda nome=row[0], valor=row[1], quantidade=row[2]: selecionaProdutoParaItem(nome, valor, quantidade, index))
            label.configure(fg_color="#38343c", corner_radius=0)
            self.quantidades.append(row[2])

            self.resultadoLabelsProduto.append(label)
            yNovo += 0.02
        calcularTotais()

    # ao clicar no produto ele é selecionado 
    def selecionaProdutoParaItem(nome, valor, quantidade, index):

        self.itensCriados[index][1].delete(0, "end")
        self.itensCriados[index][1].insert(0, nome)

        self.itensCriados[index][3].delete(0, "end")
        self.itensCriados[index][3].insert(0, 0)

        self.itensCriados[index][2].delete(0, "end")
        self.itensCriados[index][2].insert(0, valor)

        self.itensCriados[index][4].delete(0, "end")
        self.itensCriados[index][4].insert(0, "UN")

        self.itensCriados[index][7].delete(0, "end")
        self.itensCriados[index][7].insert(0, 0.00)

        self.quantidadeMaximaAtualItem = quantidade

        print(quantidade)

        calcularAlteracoesParaItem(index)

        for label in self.resultadoLabelsProduto:
            label.destroy()

        calcularTotais()

    # sempre que o campo for alterado, serão realizadas operações para modificar seu subtotal
    def calcularAlteracoesParaItem(index):
        preco = float(self.itensCriados[index][2].get() or 0)
        quantidade = int(self.itensCriados[index][3].get() or 0)
        acrescimo = float(self.itensCriados[index][7].get() or 0)
        descontoReal = float(self.itensCriados[index][5].get() or 0)
        descontoPorcentagem = float(self.itensCriados[index][6].get() or 0)

        if descontoReal:
            subtotal = ((preco * quantidade) + acrescimo) - descontoReal
        else:
            descontoPorcentagem = descontoPorcentagem / 100
            subtotal = ((preco * quantidade) + acrescimo)
            subtotalAux = subtotal
            subtotal = ((preco * quantidade) + acrescimo) * descontoPorcentagem
            subtotalAux = subtotalAux - subtotal
            subtotal = subtotalAux

        self.itensCriados[index][8].delete(0, "end")
        self.itensCriados[index][8].insert(0, f"{subtotal:.2f}")
        calcularTotais()

    # verifica se a quantidade da venda é maior que a presente do estoque
    def verificaQuantidadeMaximaParaItem(quantidade, index):
        quantidadeDigitada = int(self.itensCriados[index][3].get() or 0)

        if quantidade is not None and quantidadeDigitada > quantidade or quantidadeDigitada < 0:
            self.itensCriados[index][3].delete(0, "end")  
            self.itensCriados[index][3].insert(0, str(quantidade))  

            labelValorQuantidadeMax = ctk.CTkLabel(self, text="Quantidade excede o estoque", fg_color="red", text_color="white", corner_radius=5)
            labelValorQuantidadeMax.pack(pady=10)
            self.after(3000, labelValorQuantidadeMax.destroy)  

            calcularAlteracoesParaItem(index)
        else:
            self.quantidades.clear()
            calcularAlteracoesParaItem(index)
            print("Quantidade válida")

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
    

    self.yAtualBotao = 0.24
    self.yFuturoBotao = 0.02
    self.yInicial = 364
    self.itensCriados = []

    self.botaoAdicionarItem = criaBotao(self.frameParaItensNoFrame, "Adicionar Item", 0.87, self.yAtualBotao, 0.05, lambda:adicionarItem())


    # título
    geraNumeroPedido()


    self.numeroDeVenda = criarLabelEntry(frameTelaPedido, "Número da venda", 0.05, 0.05, 0.12, self.variavelnumeroDoPedido)
    self.dataDeCriacao = criarLabelEntry(frameTelaPedido, "Data de criação", 0.20, 0.05, 0.12, self.dataCriacao)
    self.nomeDoClienteBuscado = criarLabelEntry(frameTelaPedido, "Nome do cliente *", 0.05, 0.15, 0.27, None)
    self.nomeDoClienteBuscado.bind("<KeyRelease>", buscaCliente)

    self.dataDaVenda = criarLabelEntry(frameTelaPedido, "Data da venda",                     0.39, 0.05, 0.15, None)
    self.statusDoPedido = criarLabelEntry(frameTelaPedido, "Status",                         0.57, 0.05, 0.15, self.variavelEmAbertoFechado)
    self.funcionariaPedido = criarLabelEntry(frameTelaPedido, "Vendedor(a)",                 0.75, 0.05, 0.15, self.variavelFuncionarioAtual)
    self.CPFCliente = criarLabelEntry(frameTelaPedido, "CPF/CNPJ *",                         0.39, 0.15, 0.15, self.variavelCtkEntry)
    self.entradaCEP = criarLabelEntry(frameTelaPedido, "CEP *",                              0.57, 0.15, 0.15, None)
    self.entradaNumero = criarLabelEntry(frameTelaPedido, "Nº *",                            0.75, 0.15, 0.05, None)
    self.botaoBuscaCEP = criaBotao(frameTelaPedido, "Buscar CEP",                            0.865, 0.19, 0.07, lambda:buscaCep(self.entradaCEP.get(), self.entradaNumero.get()))
    self.entradaEnderecoNoPedido = criarLabelEntry(frameTelaPedido, "Endereço *",            0.39, 0.25, 0.33, None)
    self.entradaReferenciaEnderecoEntrega = criarLabelEntry(frameTelaPedido, "Referencia *", 0.75, 0.25, 0.15, None)





    listaLabels = ["Item", "Produto", "Preço", "Quantidade", "U.M.", "Desconto $", "Desconto %", "Acréscimo", "Subtotal"]
    entradasDosProdutos = []

    posicaoy = 0.2
    posicaox = 0.024
    for i, coluna in enumerate(listaLabels):
        if i == 0:
            criaLabel(self.frameParaItensNoFrame, coluna, posicaox, posicaoy, 0.040, "#38343c")
            label=criaLabel(self.frameParaItensNoFrame, i, posicaox, posicaoy+0.02, 0.040, "#38343c")
            entradasDosProdutos.append(label)
            posicaox +=0.042
        if i == 1:
            label = criaLabel(self.frameParaItensNoFrame, coluna, posicaox, posicaoy, 0.16, "#38343c")
            entrada = criaEntry(self.frameParaItensNoFrame, posicaox, posicaoy+0.02, 0.16, None)
            entradasDosProdutos.append(entrada)
            posicaox +=0.161
        if i!=0 and i!=1:
            label = criaLabel(self.frameParaItensNoFrame, coluna, posicaox, posicaoy, 0.096, "#38343c")
            entrada = criaEntry(self.frameParaItensNoFrame, posicaox, posicaoy+0.02, 0.096, None)
            entradasDosProdutos.append(entrada)
            posicaox +=0.0976

    

    

    self.NumeroItem                  = entradasDosProdutos[0]
    self.entradaProdutoPesquisado    = entradasDosProdutos[1]
    self.entradaPreco                = entradasDosProdutos[2]
    self.entradaQuantdadeItem        = entradasDosProdutos[3]
    self.entradaUnidadeMedida        = entradasDosProdutos[4]
    self.entradaDescontosReal        = entradasDosProdutos[5]
    self.entradaDescontosPorcentagem = entradasDosProdutos[6]
    self.entradaAcrescimo            = entradasDosProdutos[7]
    self.entradaSubtotal             = entradasDosProdutos[8]

        
    self.entradaProdutoPesquisado.bind("<KeyRelease>", buscaProduto)
    frameTelaPedido.bind("<Button-1>", lambda event: [label.destroy() for label in getattr(self, 'resultadoLabelsProduto', [])]) # exclui os valores da pesquisa de nome de usuário quando clicar em outro lgar no frame
    frameTelaPedido.bind("<Button-1>", lambda event: [label.destroy() for label in getattr(self, 'resultadoLabels', [])]) # exclui os valores da pesquisa de nome de usuário quando clicar em outro lgar no frame



    # área de texto observações
    criaTextArea(frameTelaPedido, 0.05, 0.65, 0.2, "Observações", "É necessário a apresentação do recibo de venda para que a vendedora abra \na assistência técnica, se necessário. Não devolvemos dinheiro. \n\nCONDIÇÃO DE PAGAMENTO:\nTROCA: \nENTREGA:")
    criaTextArea(frameTelaPedido, 0.3, 0.65, 0.2, "Observações da entrega", "Dados financeiros pertinentes")

    # área de totais
    self.labelAreaTotais = ctk.CTkLabel(frameTelaPedido, text="Totais", width=30, font=("Century Gothic", 15))
    self.labelAreaTotais.place(relx=0.55, rely=0.65)

    self.frameTotais = criaFrame(frameTelaPedido, 0.64, 0.787, 0.2, 0.18)

    self.descontoTotalPorcento = criarLabelEntry(self.frameTotais, "Desconto total(%)", 0.05, 0.08, 0.4, self.variavelTotalDescontoPorcentagem)
    self.descontoTotalReal = criarLabelEntry(self.frameTotais, "Desconto total($)", 0.5, 0.08, 0.4, self.variavelTotalDescontoPorcentagem)
    self.acrescimo = criarLabelEntry(self.frameTotais, "Acréscimo total", 0.05, 0.6, 0.4, self.variavelTotalDescontoPorcentagem)
    self.valorFrete = criarLabelEntry(self.frameTotais, "Valor frete", 0.5, 0.6, 0.4, self.variavelTotalDescontoPorcentagem)
        
    self.valorFrete = criarLabelEntry(self.frameValorFinal, "TOTAL:", 0.05, 0.3, 0.9, self.variavelTotalSubtotal)


    criaBotao(frameTelaPedido, "Voltar", 0.15, 0.95, 0.20, lambda:frameTelaPedido.destroy())
    criaBotao(frameTelaPedido, "Cadastrar", 0.87, 0.95, 0.20, lambda:salvarPedido(self))


    calcularTotais()

