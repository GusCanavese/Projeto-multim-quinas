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
    self.contadorDeLinhas =0
    self.yNovo = 0.24
    self.entradaProduto =0
    self.linhas = []



    # usuarioLogado = self.login.get()

    #pós refat 
    listaLabels = ["Item", "Produto", "Preço", "Quantidade", "Estoque", "Desconto $", "Desconto %", "Acréscimo", "Subtotal"]
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

    def buscaProduto(nomeDoProduto, entradaProduto, yNovo):
        if hasattr(self, "resultadoLabelsProduto"):
            for label in self.resultadoLabelsProduto:
                label.destroy()

        self.resultadoLabelsProduto = []

        for i, row in enumerate(Buscas.buscaProduto(nomeDoProduto)):
            if i >= 3:
                break
            label = criaBotao(frameParaItensNoFrame,row[0],0.195,yNovo + i * 0.02,0.26,lambda nome=row[0], valor=row[1], quantidade=row[2], ent=entradaProduto:selecionaProduto(nome, valor, quantidade, ent))
            label.configure(fg_color="#38343c", corner_radius=0)
            self.resultadoLabelsProduto.append(label)

    def selecionaProduto(nome, valor, quantidade, entradaProduto):
        entradaProduto.delete(0, "end")
        entradaProduto.insert(0, nome)

        # Procura a linha correta
        for linha in self.linhas:
            print(linha)
            if linha["produto"] == entradaProduto:
                linha["preco"].delete(0, "end")
                linha["preco"].insert(0, valor)

                linha["quantidade"].delete(0, "end")
                linha["quantidade"].insert(0, "0")

                linha["estoque"].delete(0, "end")
                linha["estoque"].insert(0, quantidade)

                linha["desc_real"].delete(0, "end")
                linha["desc_real"].insert(0, "0")

                linha["desc_porcentagem"].delete(0, "end")
                linha["desc_porcentagem"].insert(0, "0")

                linha["acrescimo"].delete(0, "end")
                linha["acrescimo"].insert(0, "0")

                linha["subtotal"].delete(0, "end")
                linha["subtotal"].insert(0, valor)
                break

        for label in self.resultadoLabelsProduto:
            label.destroy()
        atualizarTotalGeral()

    self.totalSubtotal=criarLabelEntry(frameTelaPedido, "TOTAL:", 0.8, 0.75, 0.15, None)
    self.totalSubtotal.configure(state="disabled")


    def atualizarTotalGeral():
        #!COLOCAR UM IF E ELSE AQUI PARA DETECTAR OS DESCONTOS EM REAL E EM PORCENTAGEM
        total = 0.0
        for linha in self.linhas:
            subtotal = float(linha["subtotal"].get().replace(",", ".") or 0)
            total += subtotal
        self.totalSubtotal.configure(state="normal")
        self.totalSubtotal.delete(0, 'end')
        self.totalSubtotal.insert(0, f"{total:.2f}")
        self.totalSubtotal.configure(state="disabled")

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

    self.botaoAdicionarItem = criaBotao(frameParaItensNoFrame, "Adicionar Item", 0.87, self.posicaoyBotao, 0.05,
        lambda: (
            messagebox.showerror("Campos vazios", "Preencha todos os campos da última linha antes de adicionar um novo item")
            if any(widget.get().strip() == "" for chave, widget in self.linhas[-1].items() if chave != "item")
            else adicionarItem(self)
        ))
    
   
    self.botaoRemoverItem = ctk.CTkButton(frameParaItensNoFrame, text="X", width=20, corner_radius=0, fg_color="red", command=lambda: removerItem(self))
    self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotao-0.04)
    

    def montarValoresDosItens():
        self.valoresDosItens = []
        for linha in self.linhas:
            produto = linha["produto"].get()
            quantidade = linha["quantidade"].get()
            preco = linha["preco"].get()
            subtotal = linha["subtotal"].get()
            estoque = linha["estoque"].get()
            acrescimo = linha["acrescimo"].get()
            desc_real = linha["desc_real"].get()
            desc_porcentagem = linha["desc_porcentagem"].get()

            if produto.strip() == "":
                continue

            item = {
                "descricao": produto,
                "quantidade": quantidade,
                "preco": preco,
                "subtotal": subtotal,
                "estoque": estoque,
                "acrescimo": acrescimo,
                "desconto_reais": desc_real,
                "desconto_porcentagem": desc_porcentagem,
            }
            self.valoresDosItens.append(item)
        salvarPedido(self)


    def adicionarItem(self):
        self.posicaoy += 0.02
        self.posicaoyBotao += 0.02
        self.posicaoyBotaoRemover += 0.02

        self.botaoAdicionarItem.place(relx=0.883, rely=self.posicaoyBotao)
        self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotaoRemover)
        linha_widgets = {}
        

        for i, coluna in enumerate(listaLabels):
            self.totalEstoque = 0
            self.quantidade = 0

            if i == 0:
                label = criaLabel(frameParaItensNoFrame, int(self.contadorDeLinhas / 9) + 1, self.posicaox, self.posicaoy, 0.040, "#38343c")
                linha_widgets["item"] = label
                self.posicaox += 0.042
            elif i == 1:
                entradaProduto = criaEntry(frameParaItensNoFrame, self.posicaox, self.posicaoy, 0.16, None)
                entradaProduto.bind("<KeyRelease>", lambda event, ent=entradaProduto, y=self.posicaoy: buscaProduto(ent.get(), ent, y))
                linha_widgets["produto"] = entradaProduto
                self.posicaox += 0.161
                self.entradaProduto = entradaProduto
            else:
                entrada = criaEntry(frameParaItensNoFrame, self.posicaox, self.posicaoy, 0.096, None)
                campo = ["preco", "quantidade", "estoque", "desc_real", "desc_porcentagem", "acrescimo", "subtotal"][i - 2]
                linha_widgets[campo] = entrada

                if campo == "quantidade":
                    entrada.bind("<KeyRelease>", lambda event, e=entrada: (
                        linha_widgets["quantidade"].delete(0, "end") or linha_widgets["quantidade"].insert(0, linha_widgets["estoque"].get())
                        if linha_widgets.get("estoque") and e.get().isdigit() and int(e.get()) > int(linha_widgets["estoque"].get() or 0)
                        else None
                    ))

                    



                if campo == 'subtotal':
                    entrada.bind("<KeyRelease>", lambda event: atualizarTotalGeral())
                
                self.posicaox += 0.0976

            self.contadorDeLinhas += 1

        self.posicaox = 0.024
        self.linhas.append(linha_widgets)
        atualizarTotalGeral()
        self.yNovo = self.posicaoy + 0.02

    adicionarItem(self)

    def removerItem(self):
        if len(self.linhas) > 1:
            ultima_linha = self.linhas.pop()  # Remove o último dicionário de entradas

            # Destroi todos os widgets da linha
            for widget in ultima_linha.values():
                widget.destroy()

            self.contadorDeLinhas -= 9  # 1 label + 8 entradas
            self.posicaoy -= 0.02
            self.posicaoyBotao -= 0.02
            self.posicaoyBotaoRemover -= 0.02

            self.botaoAdicionarItem.place(relx=0.883, rely=self.posicaoyBotao)
            self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotaoRemover)

        if len(self.linhas) == 1:
            self.botaoRemoverItem.place_forget()

        # Atualiza yNovo para ficar abaixo da nova última linha
        self.yNovo = self.posicaoy + 0.02
        atualizarTotalGeral()
    

    
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

    self.textArea1 = criaTextArea(frameTelaPedido, 0.05, 0.65, 0.2, "Observações", "É necessário a apresentação do recibo de venda para que a vendedora abra \na assistência técnica, se necessário. Não devolvemos dinheiro. \n\nCONDIÇÃO DE PAGAMENTO:\nTROCA: \nENTREGA:")
    self.textArea2 = criaTextArea(frameTelaPedido, 0.3, 0.65, 0.2, "Observações da entrega", "Dados financeiros pertinentes")

    self.totalDescontoPorcentagem = criarLabelEntry(frameTelaPedido, "Desconto total(%)", 0.55, 0.675, 0.08, None)
    self.totalDescontoReal = criarLabelEntry(frameTelaPedido, "Desconto total($)", 0.67, 0.675, 0.08, None)
    self.totalAcrescimo = criarLabelEntry(frameTelaPedido, "Acréscimo total", 0.55, 0.8, 0.08, None)
    self.valorFrete = criarLabelEntry(frameTelaPedido, "Valor frete", 0.67, 0.8, 0.08, None)



    criaBotao(frameTelaPedido, "Voltar", 0.15, 0.95, 0.20, lambda:frameTelaPedido.destroy())
    criaBotao(frameTelaPedido, "Cadastrar", 0.87, 0.95, 0.20, lambda:montarValoresDosItens())

    