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
from componentes import criaFrameJanela, criaFrameJanela, criaBotao, criaBotaoPequeno, criarLabelEntry, criaLabel, criaEntry, criaTextArea
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries
from telas.telaCadastroClientes import telaCadastroClientes


def telaGerarPedido(self):
    self.row=1
    self.posicaoy = 0.2
    self.posicaox = 0.024
    self.posicaoyBotao = 0.231
    self.posicaoyBotaoRemover = 0.191
    self.contadorDeLinhas = 0
    self.yNovo = 0.24
    self.entradaProduto = 0
    self.valorSubtotal = 0
    self.linhas = []



    usuarioLogado = self.logado
    usuarioLogado = Buscas.buscaNomeFuncionario(usuarioLogado).capitalize()

    #pós refat 
    listaLabels = ["Item", "Produto", "Preço", "Quantidade", "Estoque", "Desconto $", "Desconto %", "Acréscimo", "Subtotal"]

    variavelCtkEntry = ctk.StringVar() 
    variavelFuncionarioAtual = ctk.StringVar()
    dataCriacao = ctk.StringVar()
    variavelnumeroDoPedido = ctk.StringVar()
    variavelEmAbertoFechado = ctk.StringVar() 
    variavelCep = ctk.StringVar()
    variavelEndereco = ctk.StringVar()
    variavelNumero = ctk.StringVar()
    variavelReferencia = ctk.StringVar()
    # enderecoCliente = ctk.StringVar()

    variavelFuncionarioAtual.set(usuarioLogado)
    variavelEmAbertoFechado.set("Em aberto")
    dataCriacao.set(value=datetime.datetime.now().strftime("%d/%m/%y"))

    frameTelaPedido = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    frameParaItens = ctk.CTkScrollableFrame(frameTelaPedido, height=200, orientation="vertical", fg_color=self.corFundo)
    frameParaItens.place(relx=0.5, rely=0.5, relwidth=0.94, anchor="center")
    container = ctk.CTkFrame(frameParaItens, fg_color="red", height=1500)
    container.pack(fill="x", padx=0, pady=0)
    frameParaItensNoFrame = ctk.CTkFrame(frameParaItens, height=1500, fg_color=self.corFundo)
    frameParaItensNoFrame.place(x=-25, y=-280, relwidth=1.06)
 
    def formatar_moeda(event):
        entrada = event.widget  # widget que disparou o evento
        texto = entrada.get()

        texto_numerico = ''.join(filter(str.isdigit, texto))

        if not texto_numerico:
            texto_numerico = "0"

        while len(texto_numerico) < 3:
            texto_numerico = "0" + texto_numerico

        reais = texto_numerico[:-2]
        centavos = texto_numerico[-2:]

        valor = f"{int(reais)},{centavos}"

        # Evita piscar o cursor para o final
        entrada.delete(0, "end")
        entrada.insert(0, valor)

    self.typing_job = None  # precisa estar aqui antes

    def on_stop_typing(event=None):
        print("Parou de digitar")
        buscaCliente()

    def on_key_release(event):
        if self.typing_job is not None:
            self.after_cancel(self.typing_job)
        self.typing_job = self.after(300, on_stop_typing)



    def geraNumeroPedido():
            # self.numeroDoPedido += 1
            maiorNumero = Buscas.selecionaNumeroPedido()[0]
            
            if maiorNumero == None:
                maiorNumero = 1
            else:
                maiorNumero += 1
            numeroDoPedidoSendoCriado = maiorNumero
            variavelnumeroDoPedido.set(numeroDoPedidoSendoCriado)

    def buscaCliente(event=None): 
        nomeDoCliente = self.nomeDoClienteBuscado.get()
        dadosCliente = Buscas.buscaDadosCliente(nomeDoCliente)

        if hasattr(self, 'resultadoLabels'):
            for label in self.resultadoLabels: 
                label.destroy()

        self.resultadoLabels = []
        
        yNovo = 0.21  

        if len(dadosCliente) > 0:
            for i, row in enumerate(dadosCliente):
                if i >= 5:
                    break
                label = ctk.CTkButton(frameTelaPedido,  text=row[0], corner_radius=0,fg_color=self.cor, font=("Century Gothic bold", 15), command=lambda  nome=row[0], cpf=row[1], cnpj=row[2], cep=row[4], endereco=row[5], referencia=row[6], num=row[7], bairro=row[8], rua=row[9]: selecionaCliente(nome, cpf, cnpj, cep, endereco, referencia, num, bairro, rua))
                label.place(relx=0.05, rely=yNovo, relwidth=0.27)
                self.resultadoLabels.append(label)  
                yNovo += 0.0399
        else:
            label = ctk.CTkButton(frameTelaPedido, text="+ Cadastrar cliente", corner_radius=0, fg_color=self.cor, font=("Century Gothic bold", 15), command=lambda: telaCadastroClientes(self, 1))
            label.place(relx=0.05, rely=yNovo, relwidth=0.27)
            self.resultadoLabels.append(label)

    def selecionaCliente(nome, cpf, cnpj, cep, endereco, referencia, numero, bairro, rua):

        enderecoCliente = f"{rua} - {numero} - {bairro} - {endereco}"
        self.nomeDoClienteBuscado.delete(0, "end")
        self.nomeDoClienteBuscado.insert(0, nome)
        if cnpj:
            variavelCtkEntry.set(cnpj)
        elif cpf:
            variavelCtkEntry.set(cpf)
        else:
            variavelCtkEntry.set("sem valores")
        
        self.entradaCEP.delete(0, "end")
        self.entradaEnderecoNoPedido.delete(0, "end")
        self.entradaNumero.delete(0, "end")
        self.entradaReferenciaEnderecoEntrega.delete(0, "end")
        if referencia == None:
            referencia = ""


        variavelCep.set(cep)
        variavelEndereco.set(enderecoCliente)
        variavelReferencia.set(referencia)
        variavelNumero.set(numero)
        for label in self.resultadoLabels: 
            label.destroy()

    def buscaProduto(nomeDoProduto, entradaProduto, yNovo):
        if hasattr(self, "resultadoLabelsProduto"):
            for label in self.resultadoLabelsProduto:
                label.destroy()

        self.resultadoLabelsProduto = []

        for i, row in enumerate(Buscas.buscaProduto(nomeDoProduto)):
            if i >= 5:
                break
            label = criaBotao(frameParaItensNoFrame,row[0],0.195,yNovo+0.02 + i * 0.02,0.26,lambda nome=row[0], valor=row[1], quantidade=row[2], ent=entradaProduto:selecionaProduto(nome, valor, quantidade, ent))
            label.configure(fg_color=self.cor, corner_radius=0, font=("TkDefaultFont", 14))
            self.resultadoLabelsProduto.append(label)

    def selecionaProduto(nome, valor, quantidade, entradaProduto):
        entradaProduto.delete(0, "end")
        entradaProduto.insert(0, nome)

        # Procura a linha correta
        for linha in self.linhas:
            if linha["produto"] == entradaProduto:
                linha["preco"].delete(0, "end")
                linha["preco"].insert(0, valor)
                linha["preco"].configure(state="disabled")


                linha["quantidade"].delete(0, "end")
                linha["quantidade"].insert(0, "0")

                linha["estoque"].delete(0, "end")
                linha["estoque"].insert(0, quantidade)
                linha["estoque"].configure(state="disabled")

                linha["desc_real"].delete(0, "end")
                linha["desc_real"].insert(0, "0")

                linha["desc_porcentagem"].delete(0, "end")
                linha["desc_porcentagem"].insert(0, "0")

                linha["acrescimo"].delete(0, "end")
                linha["acrescimo"].insert(0, "0")

                linha["subtotal"].delete(0, "end")
                linha["subtotal"].insert(0, valor)
                linha["subtotal_original"] = float(valor)

                break

        for label in self.resultadoLabelsProduto:
            label.destroy()
        atualizarTotalGeral()

    self.totalSubtotal=criarLabelEntry(frameTelaPedido, "TOTAL:", 0.8, 0.75, 0.15, None)
    self.totalSubtotal.configure(state="disabled")

    def fechar_resultados(event):
        if hasattr(self, 'resultadoLabels'):
            for label in self.resultadoLabels:
                label.destroy()
        if hasattr(self, 'resultadoLabelsProduto'):
            for label in self.resultadoLabelsProduto:
                label.destroy()

    frameParaItens.bind("<Button-1>", fechar_resultados)
    frameParaItensNoFrame.bind("<Button-1>", fechar_resultados)
    frameTelaPedido.bind("<Button-1>", fechar_resultados)

    def atualizarTotalGeral():
        total = 0.0

        for linha in self.linhas:
            entry_descPorc = linha["desc_porcentagem"]
            entry_descReal = linha["desc_real"]
            entry_subtotal = linha["subtotal"]
            entry_quantida = linha["quantidade"]
            entry_acrescim = linha["acrescimo"]
            
            
            descReal = float(entry_descReal.get().replace(",", ".") or 0)
            descPorc = float(entry_descPorc.get().replace(",", ".") or 0)
            quantida = float(entry_quantida.get() or 0)
            acrescim = float(entry_acrescim.get().replace(",", ".") or 0)
            descPorc = descPorc/100

            valorSubtotal = linha.get("subtotal_original", float(entry_subtotal.get().replace(",", ".") or 0))

            descReal = float(entry_descReal.get().replace(",", ".") or 0)

            novo_subtotal = valorSubtotal - descReal if descReal > 0 else valorSubtotal

            if descReal:
                entry_descPorc.delete(0, "end")
                entry_descPorc.insert(0, "0")
                novo_subtotal = valorSubtotal - descReal if descReal > 0 else valorSubtotal

            if descPorc:
                entry_descReal.delete(0, "end")
                entry_descReal.insert(0, "0")
                desconto = valorSubtotal *descPorc if descPorc > 0 and descPorc < 100 else valorSubtotal
                novo_subtotal = valorSubtotal - desconto


            if quantida >0:
                novo_subtotal = novo_subtotal*quantida+acrescim
                
            entry_subtotal.delete(0, "end")
            entry_subtotal.insert(0, f"{novo_subtotal:.2f}")

            total += novo_subtotal

            
       
            desconto_total_porc = float(self.totalDescontoPorcentagem.get().replace(",", ".") or 0)
            total -= total * (desconto_total_porc / 100)

            desconto_total_real = float(self.totalDescontoReal.get().replace(",", ".") or 0)
            total -= desconto_total_real

            acrescimo_total = float(self.totalAcrescimo.get().replace(",", ".") or 0)
            total += acrescimo_total

            frete = float(self.valorFrete.get().replace(",", ".") or 0)
            total += frete

        # Exibe o TOTAL formatado
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
            criaLabel(frameParaItensNoFrame, coluna, self.posicaox, self.posicaoy, 0.040, self.cor)
            self.posicaox +=0.042
        if i == 1:
            criaLabel(frameParaItensNoFrame, coluna, self.posicaox, self.posicaoy, 0.16, self.cor)
            self.posicaox +=0.161
        if i!=0 and i!=1:
            criaLabel(frameParaItensNoFrame, coluna, self.posicaox, self.posicaoy, 0.096, self.cor)
            self.posicaox +=0.0976
    self.posicaox = 0.024
    campos_obrigatorios = {"quantidade", "valor", "nome"}

    self.botaoAdicionarItem = criaBotaoPequeno(frameParaItensNoFrame, "Adicionar item", 0.7, self.posicaoyBotao, 0.07,
        lambda: (
            messagebox.showerror("Campos vazios", "Preencha todos os campos da última linha antes de adicionar um novo item")
            if any(
                hasattr(widget, "get") and widget.get().strip() == ""
                for chave, widget in self.linhas[-1].items()
                if chave in campos_obrigatorios
            )
            else adicionarItem(self)
        ))
    
   
    self.botaoRemoverItem = ctk.CTkButton(frameParaItensNoFrame, text="X", width=20, corner_radius=0, fg_color="red", command=lambda: removerItem(self))
    self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotao-0.04)
    

    def montarValoresDosItens(frame):
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
        salvarPedido(self, frame)


    def adicionarItem(self):
        self.posicaoy += 0.02
        self.posicaoyBotao += 0.02
        self.posicaoyBotaoRemover += 0.02

        self.botaoAdicionarItem.place(relx=0.875, rely=self.posicaoyBotao)
        self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotaoRemover)
        linha_widgets = {}
        

        for i, coluna in enumerate(listaLabels):
            if i == 0:
                label = criaLabel(frameParaItensNoFrame, int(self.contadorDeLinhas / 9) + 1, self.posicaox, self.posicaoy, 0.040, self.cor)
                linha_widgets["item"] = label
                self.posicaox += 0.042
            elif i == 1:
                entradaProduto = criaEntry(frameParaItensNoFrame, self.posicaox, self.posicaoy, 0.16, None)
                entradaProduto.bind("<KeyRelease>", lambda event, ent=entradaProduto, y=self.posicaoy: buscaProduto(ent.get(), ent, y))
                entradaProduto.bind("<Button-1>", lambda event, ent=entradaProduto, y=self.posicaoy: buscaProduto(ent.get(), ent, y))
                linha_widgets["produto"] = entradaProduto
                self.posicaox += 0.161
                self.entradaProduto = entradaProduto
            else:
                entrada = criaEntry(frameParaItensNoFrame, self.posicaox, self.posicaoy, 0.096, None)
                campo = ["preco", "quantidade", "estoque", "desc_real", "desc_porcentagem", "acrescimo", "subtotal"][i - 2]
                linha_widgets[campo] = entrada
                

                if campo == "desc_real":
                    entrada.bind("<KeyRelease>", lambda event, e=entrada: atualizarTotalGeral())
                    entrada.bind("<FocusIn>", lambda event: event.widget.delete(0, "end"))

                if campo == "desc_porcentagem":
                    entrada.bind("<KeyRelease>", lambda event, e=entrada: atualizarTotalGeral())
                    entrada.bind("<FocusIn>", lambda event: event.widget.delete(0, "end"))

                if campo == 'quantidade':
                    entrada.bind("<KeyRelease>", lambda event, e=entrada: atualizarTotalGeral())
                    entrada.bind("<FocusIn>", lambda event: event.widget.delete(0, "end"))

                if campo == 'acrescimo':
                    entrada.bind("<KeyRelease>", lambda event, e=entrada: atualizarTotalGeral())
                    entrada.bind("<FocusIn>", lambda event: event.widget.delete(0, "end"))

                if campo == 'subtotal':
                    entrada.bind("<KeyRelease>", lambda event: atualizarTotalGeral())


                
                self.posicaox += 0.0976

            self.contadorDeLinhas += 1

        self.posicaox = 0.024
        self.linhas.append(linha_widgets)
        # atualizarTotalGeral()
        self.yNovo = self.posicaoy + 0.02

    adicionarItem(self)

    def removerItem(self):
        if len(self.linhas) > 1:
            ultima_linha = self.linhas.pop()

            for widget in ultima_linha.values():
                if hasattr(widget, "destroy"):
                    widget.destroy()

            self.contadorDeLinhas -= 9
            self.posicaoy -= 0.02
            self.posicaoyBotao -= 0.02
            self.posicaoyBotaoRemover -= 0.02

            self.botaoAdicionarItem.place(relx=0.883, rely=self.posicaoyBotao)
            self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotaoRemover)

        if len(self.linhas) == 1:
            self.botaoRemoverItem.place_forget()

        self.yNovo = self.posicaoy + 0.02
        print("destruiu")
        self.entradaProduto = ""
        print("destruiu")

        atualizarTotalGeral()
    

    geraNumeroPedido()
    self.numeroDeVenda = criarLabelEntry(frameTelaPedido, "Número da venda", 0.05, 0.05, 0.12, variavelnumeroDoPedido)
    self.dataDeCriacao = criarLabelEntry(frameTelaPedido, "Data de criação", 0.20, 0.05, 0.12, dataCriacao)
    self.nomeDoClienteBuscado = criarLabelEntry(frameTelaPedido, "Nome do cliente *", 0.05, 0.15, 0.27, None)
    self.nomeDoClienteBuscado.bind("<KeyRelease>", on_key_release)
    self.nomeDoClienteBuscado.bind("<Button-1>", buscaCliente)

    self.statusDoPedido = criarLabelEntry(frameTelaPedido, "Status", 0.39, 0.05, 0.33, variavelEmAbertoFechado)
    self.statusDoPedido.configure(state="disabled")
    self.funcionariaPedido = criarLabelEntry(frameTelaPedido, "Vendedor(a)", 0.75, 0.05, 0.15, variavelFuncionarioAtual)
    self.CPFCliente = criarLabelEntry(frameTelaPedido, "CPF/CNPJ *", 0.39, 0.15, 0.15, variavelCtkEntry)
    self.entradaCEP = criarLabelEntry(frameTelaPedido, "CEP *", 0.57, 0.15, 0.15, variavelCep)
    self.entradaNumero = criarLabelEntry(frameTelaPedido, "Nº *", 0.75, 0.15, 0.05, variavelNumero)
    self.botaoBuscaCEP = criaBotaoPequeno(frameTelaPedido, "Buscar CEP", 0.865, 0.205, 0.07, lambda:buscaCep(self.entradaCEP.get(), self.entradaNumero.get()))
    self.entradaEnderecoNoPedido = criarLabelEntry(frameTelaPedido, "Endereço *", 0.39, 0.25, 0.33, variavelEndereco)
    self.entradaReferenciaEnderecoEntrega = criarLabelEntry(frameTelaPedido, "Referencia *", 0.75, 0.25, 0.15, variavelReferencia)

    self.textArea1 = criaTextArea(frameTelaPedido, 0.05, 0.65, 0.2, "Observações", "É necessário a apresentação do recibo de venda para que a vendedora abra \na assistência técnica, se necessário. Não devolvemos dinheiro. \n\nCONDIÇÃO DE PAGAMENTO:\n\nTROCA: \n\nENTREGA:")
    self.textArea2 = criaTextArea(frameTelaPedido, 0.3, 0.65, 0.2, "Observações da entrega", "Dados financeiros pertinentes")

    self.totalDescontoPorcentagem = criarLabelEntry(frameTelaPedido, "Desconto total(%)", 0.55, 0.675, 0.08, None)
    self.totalDescontoReal = criarLabelEntry(frameTelaPedido, "Desconto total($)", 0.67, 0.675, 0.08, None)
    self.totalAcrescimo = criarLabelEntry(frameTelaPedido, "Acréscimo total", 0.55, 0.8, 0.08, None)
    self.valorFrete = criarLabelEntry(frameTelaPedido, "Valor frete", 0.67, 0.8, 0.08, None)

    self.totalDescontoPorcentagem.bind("<KeyRelease>", lambda event,:(atualizarTotalGeral()))
    self.totalDescontoReal.bind("<KeyRelease>", lambda event,:(atualizarTotalGeral()))
    self.totalAcrescimo.bind("<KeyRelease>", lambda event,:(atualizarTotalGeral()))
    self.valorFrete.bind("<KeyRelease>", lambda event,:(atualizarTotalGeral()))



    criaBotao(frameTelaPedido, "Voltar", 0.15, 0.95, 0.20, lambda:frameTelaPedido.destroy())
    criaBotao(frameTelaPedido, "Gerar pedido", 0.87, 0.95, 0.20, lambda:montarValoresDosItens(frameTelaPedido))

    aplicar_maiusculo_em_todos_entries(self)

    
