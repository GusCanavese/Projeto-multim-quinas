import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from tkinter import messagebox
import requests
from PIL import Image
import datetime
from funcoesTerceiras.verificaSeQuerSalvarPedido import salvarPedido


def telaGerarPedido(self):
    self.variavelCnpjBuscado = None
    self.variavelCtkEntry = ctk.StringVar() #esses 2 só inicializam para conseguir usar fora da função
    self.variavelIndiceDoProduto = ctk.StringVar()
    self.quantidadeMaximaPermitida = ctk.StringVar()
    self.variavelDefinidaDePorcentagem = ctk.StringVar()
    self.variavelDefinidaDeReal = ctk.StringVar()
    self.variavelDefinidaDeAcrescimo = ctk.StringVar()
    self.variavelDefinidaDeSubtotal = ctk.StringVar()
    self.variavelDefinidaDeUnidadeDeMedida = ctk.StringVar()
    self.variavelFuncionarioAtual = ctk.StringVar()
    
    self.variavelTotalDescontoReal = ctk.StringVar()
    self.variavelTotalDescontoPorcentagem = ctk.StringVar()
    self.variavelTotalAcrescimo = ctk.StringVar()
    self.variavelTotalSubtotal = ctk.StringVar()
    self.variavelnumeroDoPedido = ctk.StringVar()

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
    self.frameTelaGerarPedido = ctk.CTkFrame(self, height=800, width=1200, corner_radius=5)
    
    self.frameTelaGerarPedido.place(x=40, y=50)      

    # criar canva para itens adicionados
    self.frameParaItens = ctk.CTkScrollableFrame(self.frameTelaGerarPedido, width=1150, height=200, orientation="vertical")
    self.frameParaItens.place(relx=0.5, y=450, anchor="center")

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
    
    self.container = ctk.CTkFrame(self.frameParaItens, height=1500)
    self.container.pack(fill="x", padx=1, pady=1)

    self.frameParaItensNoFrame = ctk.CTkFrame(self.frameParaItens, width=1250, height=1500)
    self.frameParaItensNoFrame.place(x=-25, y=-280)

    # frame para calcular os totais no final da pagina
    self.frameTotais = ctk.CTkFrame(self.frameTelaGerarPedido, width=250, height=150)
    self.frameTotais.place(x=650, y=600)

    # frame valor final para finalizar o preço de tudo
    self.frameValorFinal = ctk.CTkFrame(self.frameTelaGerarPedido, width=200, height=150)
    self.frameValorFinal.place(x=950, y=600)
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
                "quantidade": int(item[3].get()),
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
        
        yNovo = 210  
        for i, row in enumerate(dadosCliente):
            if i >= 5:
                break
            label = ctk.CTkButton(self.frameTelaGerarPedido, width=370, text=row[0], fg_color="#38343c", font=("Century Gothic bold", 15), command=lambda  nome=row[0], cnpj=row[1]: selecionaCliente(nome, cnpj))
            label.place(x=60, y=yNovo)
            self.resultadoLabels.append(label)  
            yNovo += 30

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
        yNovo = 362
        
        for i, row in enumerate(Buscas.buscaProduto(nomeDoProduto)):
            if i >=3: break
            label = ctk.CTkButton(self.frameParaItensNoFrame, width=300, text=row[0], fg_color="#38343c", font=("Century Gothic bold", 15), command=lambda nome = row[0], valor = row[1], quantidade=row[2]: selecionaProduto(nome, valor, quantidade))
            label.place(x=82, y=yNovo)
            self.resultadoLabelsProduto.append(label)
            yNovo += 29

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
        self.entradaQuantdadeItem.insert(0, 1)

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

    # remove cada item, e o coloca novamente no seu lugar e no seu index na lista
    def removerItem(index):
        if 0 <= index < len(self.itensCriados):  
            for widget in self.itensCriados[index]:
                if widget:  
                    widget.destroy()  
            self.itensCriados.pop(index)  

            
            for i in range(index, len(self.itensCriados)):
                y_pos = self.yInicial + (i * self.yFuturoBotao)
                self.itensCriados[i][0].place(y=y_pos)
                for widget in self.itensCriados[i][1:]:  
                    if widget:
                        widget.place(y=y_pos)

            
            if self.itensCriados:
                ultimoItem = self.itensCriados[-1]
                if ultimoItem[-1] is None:  
                    botaoRemover = ctk.CTkButton(
                        self.frameParaItensNoFrame, text="X", width=30, height=30, fg_color="red", 
                        corner_radius=5, command=lambda idx=len(self.itensCriados) - 1: removerItem(idx)
                    )
                    botaoRemover.place(x=1140, y=self.yInicial + ((len(self.itensCriados) - 1) * self.yFuturoBotao))
                    ultimoItem[-1] = botaoRemover  
            self.yAtualBotao -= self.yFuturoBotao
            self.botaoAdicionarItem.place(x=1011, y=self.yAtualBotao + 40)
    
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

        labelNumeroItem = ctk.CTkLabel(self.frameParaItensNoFrame, text=f"{numeroItem+1}", fg_color="#38343c", height=30, width=50, corner_radius=0)
        labelNumeroItem.place(x=30, y=self.yAtualBotao)

        entradaProdutoPesquisado = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=200, corner_radius=0)
        entradaProdutoPesquisado.place(x=82, y=self.yAtualBotao)

        entradaPreco = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
        entradaPreco.place(x=284, y=self.yAtualBotao)

        entradaQuantidade = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
        entradaQuantidade.place(x=406, y=self.yAtualBotao)

        entradaUnidadeMedida = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
        entradaUnidadeMedida.place(x=528, y=self.yAtualBotao)

        entradaDescontosReal = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
        entradaDescontosReal.place(x=650, y=self.yAtualBotao)

        entradaDescontosPorcentagem = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
        entradaDescontosPorcentagem.place(x=772, y=self.yAtualBotao)

        entradaAcrescimo = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
        entradaAcrescimo.place(x=894, y=self.yAtualBotao)

        entradaSubtotal = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
        entradaSubtotal.place(x=1016, y=self.yAtualBotao)

        botaoRemover = ctk.CTkButton(self.frameParaItensNoFrame, text="X", width=30, height=30, fg_color="red", corner_radius=5, command=lambda idx=len(self.itensCriados): removerItem(idx))
        botaoRemover.place(x=1140, y=self.yAtualBotao)

        if self.itensCriados:
            ultimoItem = self.itensCriados[-1]
            if ultimoItem[-1]: 
                ultimoItem[-1].destroy() 
                ultimoItem[-1] = None 

        self.itensCriados.append([
            labelNumeroItem, entradaProdutoPesquisado, entradaPreco, entradaQuantidade, entradaUnidadeMedida,
            entradaDescontosReal, entradaDescontosPorcentagem, entradaAcrescimo, entradaSubtotal, botaoRemover
        ])

        calcularAlteracoesParaItem(numeroItem - 1)

        self.yAtualBotao += self.yFuturoBotao
        self.botaoAdicionarItem.place(x=1011, y=self.yAtualBotao + 20)

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

        yNovo = 394 + (index*32)
        
        for i, row in enumerate(Buscas.buscaProduto(nomeDoProduto)):
            if i >= 3: break
            label = ctk.CTkButton(self.frameParaItensNoFrame, width=300, text=row[0], fg_color="#38343c", font=("Century Gothic bold", 15), command=lambda nome=row[0], valor=row[1], quantidade=row[2]: selecionaProdutoParaItem(nome, valor, quantidade, index))
            label.place(x=82, y=yNovo)
            self.quantidades.append(row[2])

            self.resultadoLabelsProduto.append(label)
            yNovo += 29
        calcularTotais()

    # ao clicar no produto ele é selecionado 
    def selecionaProdutoParaItem(nome, valor, quantidade, index):

        self.itensCriados[index][1].delete(0, "end")
        self.itensCriados[index][1].insert(0, nome)

        self.itensCriados[index][3].delete(0, "end")
        self.itensCriados[index][3].insert(0, 1)

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
    

    self.yAtualBotao = 364
    self.yFuturoBotao = 32
    self.yInicial = 364
    self.itensCriados = []

    self.botaoAdicionarItem = ctk.CTkButton(self.frameParaItensNoFrame, text="Adicionar Item", width=130, height=20, corner_radius=5, font=("Arial", 15), command=adicionarItem)
    self.botaoAdicionarItem.place(x=1011, y=380)

    # título
    geraNumeroPedido()
    self.textoGerarPedido = ctk.CTkLabel(self.frameTelaGerarPedido,  text="Gerar pedido", font=("Century Gothic bold", 30))
    self.textoGerarPedido.place(relx=0.5, y=40, anchor="center")

    # entrada da do número da venda
    self.labelNumeroDataVenda = ctk.CTkLabel(self.frameTelaGerarPedido,  text="Número da venda", font=("Century Gothic bold", 14))
    self.labelNumeroDataVenda.place(x=30, y=75)
    self.numeroDeVenda = ctk.CTkEntry(self.frameTelaGerarPedido, textvariable = self.variavelnumeroDoPedido, placeholder_text="Número", width=180, corner_radius=5, font=("Arial", 15))
    self.numeroDeVenda.place(x=30, y=100)

    # entrada da data da criação do pedido
    self.labelDataDeCriacao = ctk.CTkLabel(self.frameTelaGerarPedido,  text="Data de criação", font=("Century Gothic bold", 14))
    self.labelDataDeCriacao.place(x=250, y=75)
    self.dataDeCriacao = ctk.CTkEntry(self.frameTelaGerarPedido, textvariable=ctk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%y")), width=180, corner_radius=5, font=("Arial", 15))
    self.dataDeCriacao.place(x=250, y=100)

    # entrada da data da venda
    self.labelDataDaVenda = ctk.CTkLabel(self.frameTelaGerarPedido,  text="Data da venda", font=("Century Gothic bold", 14))
    self.labelDataDaVenda.place(x=470, y=75)
    self.dataDaVenda = ctk.CTkEntry(self.frameTelaGerarPedido, placeholder_text="DD/MM/AAAA",  width=180, corner_radius=5, font=("Arial", 15))
    self.dataDaVenda.place(x=470, y=100)

    # Status da venda
    self.variavelEmAbertoFechado = "Em aberto"
    self.labelStatusDoPedido = ctk.CTkLabel(self.frameTelaGerarPedido, text="Status", font=("Century Gothic bold", 14))
    self.labelStatusDoPedido.place(x=690, y=75)
    self.statusDoPedido = ctk.CTkEntry(self.frameTelaGerarPedido, textvariable=ctk.StringVar(value=self.variavelEmAbertoFechado), placeholder_text="DD/MM/AAAA", width=180, corner_radius=5, font=("Arial", 15))
    self.statusDoPedido.place(x=690, y=100)

    # qual funcionaria ta fazendo a venda? #! PEGAR O USUÁRIO QUE ESTÁ LOGADO
    self.labelFuncionaria = ctk.CTkLabel(self.frameTelaGerarPedido, text="Vendedor(a)", font=("Century Gothic bold", 15))
    self.labelFuncionaria.place(x=910, y=75)
    self.funcionariaPedido = ctk.CTkEntry(self.frameTelaGerarPedido, textvariable=self.variavelFuncionarioAtual, width=180, corner_radius=5, font=("Century Gothic bold", 15))
    self.funcionariaPedido.place(x=910, y=100)

    iconeLupa = ctk.CTkImage(light_image=Image.open("arquivos/search.png"), size=(20, 20))
    labelIcone = ctk.CTkButton(self.frameTelaGerarPedido, image=iconeLupa, fg_color="#38343c", width=30, corner_radius=5, command=buscaCliente)
    labelIcone.place(x=30, y=180)

    # nome do cliente
    self.labelNomeDoCliente = ctk.CTkLabel(self.frameTelaGerarPedido, text="Nome do cliente *", font=("Century Gothic", 14))
    self.labelNomeDoCliente.place(x=30, y=150)
    self.nomeDoClienteBuscado = ctk.CTkEntry(self.frameTelaGerarPedido,  placeholder_text="Nome do Cliente", width=370, corner_radius=5, font=("Arial", 15))
    self.nomeDoClienteBuscado.place(x=60, y=180)
    self.nomeDoClienteBuscado.bind("<KeyRelease>", buscaCliente)  # Chama a busca ao digitar
    self.frameTelaGerarPedido.bind("<Button-1>", lambda event: [label.destroy() for label in getattr(self, 'resultadoLabels', [])]) # exclui os valores da pesquisa de nome de usuário quando clicar em outro lgar no frame

    # cpf ou cnpj do cliente
    self.labelCPFCliente = ctk.CTkLabel(self.frameTelaGerarPedido,  text="CPF/CNPJ *", font=("Century Gothic bold", 14))
    self.labelCPFCliente.place(x=470, y=150)
    self.CPFCliente = ctk.CTkEntry(self.frameTelaGerarPedido, textvariable=self.variavelCtkEntry, width=180, corner_radius=5, font=("Arial", 15))
    self.CPFCliente.place(x=470, y=180)

    # cep paraa buscar endereço
    self.labelCEP = ctk.CTkLabel(self.frameTelaGerarPedido, text="CEP *", font=("Century Gothic bold", 14))
    self.labelCEP.place(x=690, y=150)
    self.entradaCEP = ctk.CTkEntry(self.frameTelaGerarPedido, width=180, corner_radius=5, font=("Arial", 15))
    self.entradaCEP.place(x=690, y=180)

    self.labelNumero = ctk.CTkLabel(self.frameTelaGerarPedido, text="Nº *", font=("Century Gothic bold", 14))
    self.labelNumero.place(x=910, y=150)
    self.entradaNumero = ctk.CTkEntry(self.frameTelaGerarPedido, width=60, corner_radius=5, font=("Arial", 15))
    self.entradaNumero.place(x=910, y=180)

    # cep paraa buscar endereço
    self.labelEnderecoNoPedido = ctk.CTkLabel(self.frameTelaGerarPedido, text="Endereço *", font=("Century Gothic bold", 14))
    self.labelEnderecoNoPedido.place(x=470, y=235)
    self.entradaEnderecoNoPedido = ctk.CTkEntry(self.frameTelaGerarPedido, width=400, corner_radius=5, font=("Arial", 13))
    self.entradaEnderecoNoPedido.place(x=470, y=260)


    # REFERENCIA    
    self.labelReferenciaEnderecoEntrega = ctk.CTkLabel(self.frameTelaGerarPedido, text="Referencia *", font=("Century Gothic bold", 14))
    self.labelReferenciaEnderecoEntrega.place(x=910, y=235)
    self.entradaReferenciaEnderecoEntrega = ctk.CTkEntry(self.frameTelaGerarPedido, width=180, corner_radius=5, font=("Arial", 13))
    self.entradaReferenciaEnderecoEntrega.place(x=910, y=260)



        

    # botão buscacep
    self.botaoBuscaCEP = ctk.CTkButton(self.frameTelaGerarPedido, text="Buscar CEP", width=30, corner_radius=5, command=lambda:buscaCep(self.entradaCEP.get(), self.entradaNumero.get()))
    self.botaoBuscaCEP.place(x=1015, y=180)




    # item
    self.labelNumeroItem = ctk.CTkLabel(self.frameParaItensNoFrame, text="Item", fg_color="#38343c",  height=30, width=50, corner_radius=0)
    self.labelNumeroItem.place(x=30, y=300)
    self.NumeroItem = ctk.CTkLabel(self.frameParaItensNoFrame, text="1", fg_color="#38343c",  height=30, width=50, corner_radius=0)
    self.NumeroItem.place(x=30, y=332)

    # produto
    self.LabelProdutoPesquisado = ctk.CTkLabel(self.frameParaItensNoFrame, text="Produto", fg_color="#38343c",  height=30, width=200, corner_radius=0)
    self.LabelProdutoPesquisado.place(x=82, y=300)
    self.entradaProdutoPesquisado = ctk.CTkEntry(self.frameParaItensNoFrame,  height=30, width=200, corner_radius=0)
    self.entradaProdutoPesquisado.place(x=82, y=332)
    self.entradaProdutoPesquisado.bind("<KeyRelease>", buscaProduto)
    self.frameTelaGerarPedido.bind("<Button-1>", lambda event: [label.destroy() for label in getattr(self, 'resultadoLabelsProduto', [])]) # exclui os valores da pesquisa de nome de usuário quando clicar em outro lgar no frame


    # detalhes
    self.labelPreco = ctk.CTkLabel(self.frameParaItensNoFrame, text="Preço", fg_color="#38343c",  height=30, width=120, corner_radius=0)
    self.labelPreco.place(x=284, y=300)
    self.entradaPreco = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
    self.entradaPreco.place(x=284, y=332)

    # Quantidade
    self.labelQuantdadeItem = ctk.CTkLabel(self.frameParaItensNoFrame, text="Quantidade", fg_color="#38343c",  height=30, width=120, corner_radius=0)
    self.labelQuantdadeItem.place(x=406, y=300)
    self.entradaQuantdadeItem = ctk.CTkEntry(self.frameParaItensNoFrame, textvariable=self.quantidadeMaximaPermitida, height=30, width=120, corner_radius=0)
    self.entradaQuantdadeItem.place(x=406, y=332)


    # Unidade de Medida
    self.labelUnidadeMedida = ctk.CTkLabel(self.frameParaItensNoFrame,  text="Unidade de medida", fg_color="#38343c",  height=30, width=120, corner_radius=0)
    self.labelUnidadeMedida.place(x=528, y=300)
    self.entradaUnidadeMedida = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
    self.entradaUnidadeMedida.place(x=528, y=332)

    # Desconto Real
    self.labelDescontosReal = ctk.CTkLabel(self.frameParaItensNoFrame, text="Desconto($)", fg_color="#38343c",  height=30, width=120, corner_radius=0)
    self.labelDescontosReal.place(x=650, y=300)
    self.entradaDescontosReal = ctk.CTkEntry(self.frameParaItensNoFrame, textvariable=self.variavelDefinidaDeReal, height=30, width=120, corner_radius=0)
    self.entradaDescontosReal.place(x=650, y=332)

    # Desconto porcentagem
    self.labelDescontosPorcentagem = ctk.CTkLabel(self.frameParaItensNoFrame, text="Desconto(%)", fg_color="#38343c",  height=30, width=120, corner_radius=0)
    self.labelDescontosPorcentagem.place(x=772, y=300)
    self.entradaDescontosPorcentagem = ctk.CTkEntry(self.frameParaItensNoFrame, textvariable=self.variavelDefinidaDePorcentagem, height=30, width=120, corner_radius=0)
    self.entradaDescontosPorcentagem.place(x=772, y=332)

    # Acrescimo
    self.labelAcrescimo = ctk.CTkLabel(self.frameParaItensNoFrame, text="Acrescimo", fg_color="#38343c",  height=30, width=120, corner_radius=0)
    self.labelAcrescimo.place(x=894, y=300)
    self.entradaAcrescimo = ctk.CTkEntry(self.frameParaItensNoFrame, textvariable=self.variavelDefinidaDeAcrescimo, height=30, width=120, corner_radius=0)
    self.entradaAcrescimo.place(x=894, y=332)

    # Subtotal
    self.labelSubtotal = ctk.CTkLabel(self.frameParaItensNoFrame, text="Subtotal", fg_color="#38343c",  height=30, width=120, corner_radius=0)
    self.labelSubtotal.place(x=1016, y=300)
    self.entradaSubtotal = ctk.CTkEntry(self.frameParaItensNoFrame, textvariable=self.variavelDefinidaDeSubtotal, height=30, width=120, corner_radius=0)
    self.entradaSubtotal.place(x=1016, y=332)


    # área de texto observações
    self.labelAreaTexto = ctk.CTkLabel(self.frameTelaGerarPedido, text="Observações", height=30, font=("Century Gothic", 15))
    self.labelAreaTexto.place(x=30, y=570)
    self.textArea1 = ctk.CTkTextbox(self.frameTelaGerarPedido, width=300, height=150, corner_radius=8, wrap="word")
    self.textArea1.insert("0.0","É necessário a apresentação do recibo de venda para que a vendedora abra \na assistência técnica, se necessário. Não devolvemos dinheiro. \n\nCONDIÇÃO DE PAGAMENTO:\nTROCA: \nENTREGA:")
    self.textArea1.place(x=30, y=600)

    # área de texto enrtrega
    self.labelAreaTexto = ctk.CTkLabel(self.frameTelaGerarPedido, text="Observações da entrega", height=30, font=("Century Gothic", 15))
    self.labelAreaTexto.place(x=360, y=570)
    self.textArea2 = ctk.CTkTextbox(self.frameTelaGerarPedido, width=250, height=150, corner_radius=8, wrap="word")
    self.textArea2.insert("0.0","Dados financeiros pertinentes")
    self.textArea2.place(x=360, y=600)

    # área de totais
    self.labelAreaTotais = ctk.CTkLabel(self.frameTelaGerarPedido, text="Totais", font=("Century Gothic", 15))
    self.labelAreaTotais.place(x=650, y=570)

    self.labelDescontoTotalPorcento = ctk.CTkLabel(self.frameTotais, text="Desconto total(%)", font=("Century Gothic", 11))
    self.labelDescontoTotalPorcento.place(x=10, y=-3)
    self.descontoTotalPorcento = ctk.CTkEntry(self.frameTotais, state="readonly", textvariable=self.variavelTotalDescontoPorcentagem, height=20, width=100, corner_radius=0)
    self.descontoTotalPorcento.place(x=10, y=20)

    self.labelDescontoTotalReal = ctk.CTkLabel(self.frameTotais, text="Desconto total($)", font=("Century Gothic", 11))
    self.labelDescontoTotalReal.place(x=140, y=-3)
    self.descontoTotalReal = ctk.CTkEntry(self.frameTotais, state="readonly", textvariable=self.variavelTotalDescontoReal, height=20, width=100, corner_radius=0)
    self.descontoTotalReal.place(x=140, y=20)

    self.labelDescontoTotalPorcento = ctk.CTkLabel(self.frameTotais, text="Acréscimo total",  font=("Century Gothic", 11))
    self.labelDescontoTotalPorcento.place(x=10, y=43)
    self.descontoTotalPorcento = ctk.CTkEntry(self.frameTotais, state="readonly", textvariable=self.variavelTotalAcrescimo, height=20, width=100, corner_radius=0)
    self.descontoTotalPorcento.place(x=10, y=65)

    self.labelValorFrete = ctk.CTkLabel(self.frameTotais, text="Valor frete",  font=("Century Gothic", 11))
    self.labelValorFrete.place(x=140, y=43)
    self.valorFrete = ctk.CTkEntry(self.frameTotais, height=20, width=100, corner_radius=0)
    self.valorFrete.place(x=140, y=65)

    self.labelValorFinal = ctk.CTkLabel(self.frameValorFinal, text="TOTAL:", font=("Century Gothic", 20))
    self.labelValorFinal.place(x=0, y=0)
    self.valorFinal = ctk.CTkEntry(self.frameValorFinal, textvariable=self.variavelTotalSubtotal, corner_radius=0, height=40, width=180)
    self.valorFinal.place(x=10, y=50)

    # voltar
    self.botaoVoltarTelaGerarPedido = ctk.CTkButton(self.frameTelaGerarPedido, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaGerarPedido.destroy)
    self.botaoVoltarTelaGerarPedido.place(x=30, y=760)

    # gerar pedido
    self.botaoGerarPedido = ctk.CTkButton(self.frameTelaGerarPedido, text="Gerar pedido", width=200, corner_radius=5, font=("Arial", 15), command=lambda:salvarPedido(self))
    self.botaoGerarPedido.place(x=950, y=760)
    calcularTotais()

