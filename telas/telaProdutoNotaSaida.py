import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from tkinter import messagebox
import requests
from PIL import Image
import datetime
from telas.telaTotaisNota import telaTotaisNotaSaida
from componentes import criaFrameJanela, criaFrameJanela, criaBotao, criaBotaoPequeno, criaLabel, criaEntry, criaTextArea, criaTextAreaModal, criarLabelEntry, criarLabelComboBox, criarLabelLateralComboBox, criarLabelLateralEntry
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries


def telaProdutosNotaSaida(self, cfop):

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




    listaLabels = ["Item", "Produto", "Preço", "Quantidade", "Estoque", "Desconto $", "Desconto %", "Acréscimo", "Subtotal", "cfop"]

    dataCriacao = ctk.StringVar()
    variavelEmAbertoFechado = ctk.StringVar()
    variavelCfop = ctk.StringVar()
    mod_bc_icms = ctk.StringVar()
    bc_icms = ctk.StringVar()
    red_bc_icms = ctk.StringVar()
    aliq_icms = ctk.StringVar()
    vr_icms = ctk.StringVar()

    mva_icms_st = ctk.StringVar()
    bc_icms_st = ctk.StringVar()
    red_bc_icms_st = ctk.StringVar()
    aliq_icms_st = ctk.StringVar()

    vr_icms_st = ctk.StringVar()
    vr_bc_icms_st_ret = ctk.StringVar()
    vr_icms_st_ret  = ctk.StringVar()

    codigoEntry = ctk.StringVar()
    NCMEntry = ctk.StringVar()
    CSETEntry = ctk.StringVar()
    quantidadeEntry = ctk.StringVar()
    beneficioEntry = ctk.StringVar()

    aliqIOFEntry = ctk.StringVar()
    aliqIIEntry = ctk.StringVar()
    BCIIEntry = ctk.StringVar()
    VrIOFEntry = ctk.StringVar()
    VrIIEntry = ctk.StringVar()
    VRDespAduaneira = ctk.StringVar()

    self.pis_cofins_vars = {"campo_teste": ctk.StringVar(value="")}

    aliquEntry =ctk.StringVar()
    credICMSEntry =ctk.StringVar()
    variavelCfop.set(cfop)


    variavelEmAbertoFechado.set("Em aberto")
    dataCriacao.set(value=datetime.datetime.now().strftime("%d/%m/%y"))

    frameTelaNotaProduto = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    frameParaItens = ctk.CTkScrollableFrame(frameTelaNotaProduto, height=800, orientation="vertical", fg_color=self.corFundo)
    frameParaItens.place(relx=0.5, rely=0.6, relwidth=0.94, anchor="center")
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

    def fechar_resultados(event):
        if hasattr(self, 'resultadoLabels'):
            for label in self.resultadoLabels:
                label.destroy()
        if hasattr(self, 'resultadoLabelsProduto'):
            for label in self.resultadoLabelsProduto:
                label.destroy()

    frameParaItens.bind("<Button-1>", fechar_resultados)
    frameParaItensNoFrame.bind("<Button-1>", fechar_resultados)
    frameTelaNotaProduto.bind("<Button-1>", fechar_resultados)


    












    def botaoTribut(self, linha):
        opcoes_CST_A = [
            "0 - Nacional, exceto as indicadas nos códigos 3, 4, 5 e 8",
            "1 - Estrangeira - Importação direta, exceto a indicada no código 6",
            "2 - Estrangeira - Adquirida no mercado interno, exceto a indicada no código 7",
            "3 - Nacional, mercadoria ou bem com Conteúdo de Importação superior a 40% e inferior ou igual a 70%",
            "4 - Nacional, cuja produção tenha sido feita em conformidade com os processos produtivos básicos de que tratam as legislações citadas nos Ajustes",
            "5 - Nacional, mercadoria ou bem com Conteúdo de Importação inferior ou igual a 40%",
            "6 - Estrangeira - Importação direta, sem similar nacional, constante em lista da CAMEX e gás natural",
            "7 - Estrangeira - Adquirida no mercado interno, sem similar nacional, constante em lista da CAMEX e gás natural",
            "8 - Nacional, mercadoria ou bem com Conteúdo de Importação superior a 70%"
        ]

        opcoes_csosn = [
            "101 - Tributada pelo Simples Nacional com permissão de crédito",
            "102 - Tributada pelo Simples Nacional sem permissão de crédito",
            "103 - Isenção do ICMS no Simples Nacional para faixa de receita bruta",
            "201 - Tributada pelo Simples Nacional com permissão de crédito e com cobrança do ICMS por substituição tributária",
            "202 - Tributada pelo Simples Nacional sem permissão de crédito e com cobrança do ICMS por substituição tributária",
            "203 - Isenção do ICMS no Simples Nacional para faixa de receita bruta e com cobrança do ICMS por substituição tributária",
            "300 - Imune",
            "400 - Não tributada pelo Simples Nacional",
            "500 - ICMS cobrado anteriormente por substituição tributária (substituído) ou por antecipação",
            "900 - Outros"
        ]

        opcoes_CST_B = [
            "00 - Tributada integralmente",
            "02 - Tributação monofásica própria sobre combustíveis",
            "10 - Tributada e com cobrança do ICMS por substituição tributária",
            "15 - Tributação monofásica própria e com responsabilidade pela retenção sobre combustíveis",
            "20 - Com redução de base de cálculo",
            "30 - Isenta ou não tributada e com cobrança do ICMS por substituição tributária",
            "40 - Isenta",
            "41 - Não tributada",
            "50 - Suspensão",
            "51 - Diferimento",
            "53 - Tributação monofásica sobre combustíveis com recolhimento diferido",
            "60 - ICMS cobrado anteriormente por substituição tributária",
            "61 - Tributação monofásica sobre combustíveis cobrada anteriormente",
            "70 - Com redução de base de cálculo e cobrança do ICMS por substituição tributária",
            "90 - Outros"
        ]
        
        opcoes_MOD_ICMS = [ 
            "Margem Valor Agregado (%)",
            "Pauta (Valor)",
            "Preço Tabelado Máx. (Valor)",
            "Valor da Operação"
        ]
        
        preco = linha["preco"].get()
        quantidade = linha["quantidade"].get()
        subtotal = linha["subtotal"].get()
        cfop = linha["cfop"].get()

        produto = ctk.StringVar()
        produto.set(linha["produto"].get())

        frame = criaFrameJanela(frameTelaNotaProduto, 0.5, 0.5, 0.6, 0.9, self.corModal)

        for widget in frameTelaNotaProduto.winfo_children():
            try:
                widget.configure(state="disabled")
            except:
                pass

        def destroyModal():
            for widget in frameTelaNotaProduto.winfo_children():
                try:
                    widget.configure(state="normal")
                except:
                    pass
            frame.destroy()

        ctk.CTkButton(frame, text="X", width=10, height=10, corner_radius=0,command=destroyModal).place(relx=0.989, rely=0.018, anchor="center")

        criarLabelEntry(frame, "Produto:", 0.05, 0.05, 0.25, produto)


        criarLabelEntry(frame, "Código:", 0.31, 0.05, 0.15, codigoEntry)
        criarLabelEntry(frame, "NCM:", 0.47, 0.05, 0.10, NCMEntry)
        criarLabelEntry(frame, "CSET:", 0.58, 0.05, 0.10, CSETEntry)
        criarLabelEntry(frame, "QTD:", 0.69, 0.05, 0.05, quantidadeEntry)
        criarLabelEntry(frame, "Beneficio Fisc:", 0.75, 0.05, 0.15, beneficioEntry)
        criarLabelComboBox(frame, "CST A", 0.05, 0.13, 0.85, opcoes_CST_A)
        criarLabelComboBox(frame, "CSOSN", 0.05, 0.21, 0.5, opcoes_csosn)
        criarLabelEntry(frame, "Alíq. Cálc. Créd. (%)", 0.59, 0.21, 0.13, aliquEntry)
        criarLabelEntry(frame, "Vr. Cred. ICMS", 0.77, 0.21, 0.13, credICMSEntry)
        criarLabelComboBox(frame, "CST A", 0.05, 0.29, 0.85, opcoes_CST_B)


        criarLabelLateralComboBox(frame, "Mod. BC ICMS",     0.15, 0.39, 0.12, opcoes_MOD_ICMS)
        criarLabelLateralEntry(frame, "BC ICMS",             0.15, 0.43, 0.12, bc_icms)
        criarLabelLateralEntry(frame, "Red. BC ICMS (%)",    0.15, 0.47, 0.12, red_bc_icms)
        criarLabelLateralEntry(frame, "Aliq. ICMS (%)",      0.15, 0.51, 0.12, aliq_icms)
        criarLabelLateralEntry(frame, "Vr. ICMS",            0.15, 0.55, 0.12, vr_icms)
        criarLabelLateralComboBox(frame, "Mod. BC ICMS ST",  0.45, 0.39, 0.12, opcoes_MOD_ICMS)
        criarLabelLateralEntry(frame, "MVA ICMS ST (%)",     0.45, 0.43, 0.12, mva_icms_st)
        criarLabelLateralEntry(frame, "BC ICMS ST",          0.45, 0.47, 0.12, bc_icms_st)
        criarLabelLateralEntry(frame, "Red. BC ICMS ST (%)", 0.45, 0.51, 0.12, red_bc_icms_st)
        criarLabelLateralEntry(frame, "Aliq. ICMS ST (%)",   0.45, 0.55, 0.12, aliq_icms_st)
        criarLabelLateralEntry(frame, "Vr. ICMS ST",         0.75, 0.39, 0.12, vr_icms_st)
        criarLabelLateralEntry(frame, "Vr. BC ICMS ST Ret.", 0.75, 0.43, 0.12, vr_bc_icms_st_ret)
        criarLabelLateralEntry(frame, "Vr. ICMS ST Ret.",    0.75, 0.47, 0.12, vr_icms_st_ret)


        criarLabelEntry(frame, "Alíq. IOF (%)",        0.05, 0.60, 0.25, aliqIOFEntry)
        criarLabelEntry(frame, "Alíq. II (%)",         0.31, 0.60, 0.15, aliqIIEntry)
        criarLabelEntry(frame, "BC II ",               0.47, 0.60, 0.10, BCIIEntry)
        criarLabelEntry(frame, "Vr. IOF",              0.58, 0.60, 0.10, VrIOFEntry)
        criarLabelEntry(frame, "Vr. II",               0.69, 0.60, 0.05, VrIIEntry)
        criarLabelEntry(frame, "Vr. Desp. Aduaneiras", 0.75, 0.60, 0.15, VRDespAduaneira)

        self.textArea1 = criaTextAreaModal(frame, 0.05, 0.68, 0.85, 'Observações do item', "")

        criaBotaoPequeno(frame, "PIS/COFINS", 0.6, 0.9, 0.1, lambda:PisCofins())

    def PisCofins():
        if framePisCofins.winfo_exists():
            framePisCofins.lift()  
            return
        
        framePisCofins = criaFrameJanela(frameTelaNotaProduto, 0.5, 0.5, 0.6, 0.9, self.corModal)

        criarLabelEntry(
            framePisCofins, 
            "TESTE", 
            0.1, 0.5, 0.5, 
            self.pis_cofins_vars["campo_teste"]
        )

        criaBotaoPequeno(
            framePisCofins, 
            "Voltar Tributação", 
            0.1, 0.6, 0.2, 
            lambda: framePisCofins.place_forget()
        )




















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

    for i, coluna in enumerate(listaLabels):
        if i == 0:
            criaLabel(frameParaItensNoFrame, coluna, self.posicaox, self.posicaoy, 0.040, self.cor)
            self.posicaox +=0.042
        if i == 1:
            criaLabel(frameParaItensNoFrame, coluna, self.posicaox, self.posicaoy, 0.16, self.cor)
            self.posicaox +=0.161
        if i!=0 and i!=1:
            criaLabel(frameParaItensNoFrame, coluna, self.posicaox, self.posicaoy, 0.08, self.cor)
            self.posicaox +=0.081
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

    def adicionarItem(self):
        self.posicaoy += 0.02
        self.posicaoyBotao += 0.02
        self.posicaoyBotaoRemover += 0.02

        self.botaoAdicionarItem.place(relx=0.875, rely=self.posicaoyBotao)
        self.botaoRemoverItem.place(relx=0.91, rely=self.posicaoyBotaoRemover)
        linha_widgets = {}

        self.btnTribut = criaBotao(frameParaItensNoFrame, "Tribut", 0.89, self.posicaoyBotaoRemover + 0.0095, 0.03, lambda lw=linha_widgets: botaoTribut(self, lw))
        self.btnTribut.configure(corner_radius=0)
        linha_widgets["botao"] = self.btnTribut
        

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
                entrada = criaEntry(frameParaItensNoFrame, self.posicaox, self.posicaoy, 0.08, None)
                campo = ["preco", "quantidade", "estoque", "desc_real", "desc_porcentagem", "acrescimo", "subtotal", "cfop"][i - 2]
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

                if campo == 'cfop':
                    print(campo)
                    entrada.configure(textvariable=variavelCfop)
                    print(entrada)

                if campo == 'subtotal':
                    entrada.bind("<KeyRelease>", lambda event: atualizarTotalGeral())


                
                self.posicaox += 0.081

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


    criaBotao(frameTelaNotaProduto, "Próximo - Tela totais", 0.25, 0.94, 0.15, lambda: (montarValoresDosItens(frameTelaNotaProduto),telaTotaisNotaSaida(self))).place(anchor="nw")
    criaBotao(frameTelaNotaProduto, "Voltar", 0.05, 0.94, 0.15, lambda: frameTelaNotaProduto.destroy()).place(anchor="nw")

    aplicar_maiusculo_em_todos_entries(self)

    