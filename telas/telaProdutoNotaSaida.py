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
from componentes import criaFrameJanela, criaFrameJanela, criaBotao, criaBotaoPequeno, criaLabel, criaEntry, criaSimouNaoLateral, criaTextAreaModal, criarLabelEntry, criarLabelComboBox, criarLabelLateralComboBox, criarLabelLateralEntry, criaSimouNao
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
 

    def passe(self):
        pass

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
        vr_icms_subst = ctk.StringVar()
        vr_bc_ICMS = ctk.StringVar()
        vr_icms_st_dest = ctk.StringVar()
        bc_icms_st_dest = ctk.StringVar()
        aliq_icms_cfop = ctk.StringVar()
        bc_FCP = ctk.StringVar()
        aliq_fcp_porc = ctk.StringVar()
        vr_FCP = ctk.StringVar()
        aliq_fcp_dif = ctk.StringVar()
        bc_fcp_st = ctk.StringVar()
        aliq_fcp_st = ctk.StringVar()
        vr_fcp_st = ctk.StringVar()
        vr_fcp_dif = ctk.StringVar()
        bc_fcp_st_ret = ctk.StringVar()
        aliq_fcp_st_ret = ctk.StringVar()
        vr_fcp_st_ret = ctk.StringVar()
        vr_fcp_efet = ctk.StringVar()
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
        aliquEntry =ctk.StringVar()
        credICMSEntry =ctk.StringVar()
        
        aliq_pis = ctk.StringVar()
        bc_pis = ctk.StringVar()
        vr_pis = ctk.StringVar()
        aliq_pis_st = ctk.StringVar()
        bc_pis_st = ctk.StringVar()
        vr_pis_st = ctk.StringVar()

        aliq_cofins = ctk.StringVar()
        bc_cofins = ctk.StringVar()
        vr_cofins = ctk.StringVar()
        aliq_cofins_st = ctk.StringVar()
        bc_cofins_st = ctk.StringVar()
        vr_cofins_st = ctk.StringVar()

        def PisCofins(frame):
            if hasattr(self, "framePisCofins") and self.framePisCofins.winfo_exists():
                self.framePisCofins.lift()  
            else:
                self.framePisCofins = criaFrameJanela(frameTelaNotaProduto, 0.5, 0.5, 0.8, 0.9, self.corModal)

                opcoes=[    "01 - Operação Tributável (base de cálculo = valor da operação alíquota normal (cumulativo/não cumulativo))",
                            "02 - Operação Tributável (base de cálculo = valor da operação (alíquota diferenciada))",
                            "03 - Operação Tributável (base de cálculo = quantidade vendida x alíquota por unidade de produto)",
                            "04 - Operação Tributável (tributação monofásica (alíquota zero))",
                            "05 - Operação Tributável por Substituição Tributária",
                            "06 - Operação Tributável (alíquota zero)",
                            "07 - Operação Isenta da Contribuição",
                            "08 - Operação Sem Incidência da Contribuição",
                            "09 - Operação com Suspensão da Contribuição",
                            "49 - Outras Operações de Saída",
                            "50 - Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno",
                            "51 - Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno",
                            "52 - Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação",
                            "53 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno",
                            "54 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação",
                            "55 - Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação",
                            "56 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação",
                            "60 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno",
                            "61 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno",
                            "62 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação",
                            "63 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno",
                            "64 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação",
                            "65 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação",
                            "66 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação",
                            "67 - Crédito Presumido - Outras Operações",
                            "70 - Operação de Aquisição sem Direito a Crédito",
                            "71 - Operação de Aquisição com Isenção",
                            "72 - Operação de Aquisição com Suspensão",
                            "73 - Operação de Aquisição a Alíquota Zero",
                            "74 - Operação de Aquisição sem Incidência da Contribuição",
                            "75 - Operação de Aquisição por Substituição Tributária",
                            "98 - Outras Operações de Entrada",
                            "99 - Outras Operações"
                        ]

                PIS = ctk.CTkLabel(self.framePisCofins,  text="PIS-----------------------------------------------------------------------------", font=("TkDefaultFont", 11))
                PIS.place(relx=0.02, rely=0.03, relheight=0.015)
                criarLabelComboBox(self.framePisCofins, "CST", 0.05, 0.07, 0.9, opcoes)

                criarLabelEntry(self.framePisCofins, "Alíq. PIS (%)", 0.3, 0.18, 0.15, aliq_pis)
                criarLabelEntry(self.framePisCofins, "BC PIS", 0.5, 0.18, 0.15, bc_pis)
                criarLabelEntry(self.framePisCofins, "Vr. PIS", 0.7, 0.18, 0.15, vr_pis)
                criaSimouNaoLateral(self.framePisCofins, "Modalidade PIS", "Percentual", "Valor/Qtd", 0.05, 0.15, passe)

                criarLabelEntry(self.framePisCofins, "Alíq. PIS ST (%)", 0.3, 0.35, 0.15, aliq_pis_st)
                criarLabelEntry(self.framePisCofins, "BC PIS ST", 0.5, 0.35, 0.15, bc_pis_st)
                criarLabelEntry(self.framePisCofins, "Vr. PIS ST", 0.7, 0.35, 0.15, vr_pis_st)
                criaSimouNaoLateral(self.framePisCofins, "Modalidade PIS ST", "Percentual", "Valor/Qtd", 0.05, 0.33, passe)
                

                COFINS = ctk.CTkLabel(self.framePisCofins,  text="COFINS-----------------------------------------------------------------------------", font=("TkDefaultFont", 11))
                COFINS.place(relx=0.02, rely=0.54, relheight=0.015)

                criarLabelEntry(self.framePisCofins, "Alíq. COFINS (%)", 0.3, 0.60, 0.15, aliq_cofins)
                criarLabelEntry(self.framePisCofins, "BC COFINS", 0.5, 0.60, 0.15, bc_cofins)
                criarLabelEntry(self.framePisCofins, "Vr. COFINS", 0.7, 0.60, 0.15, vr_cofins)
                criaSimouNaoLateral(self.framePisCofins, "Modalidade COFINS", "Percentual", "Valor/Qtd", 0.05, 0.58, passe)

                aliqCOF = criarLabelEntry(self.framePisCofins, "Alíq. COFINS ST (%)", 0.3, 0.77, 0.15, aliq_cofins_st)
                bcCOF = criarLabelEntry(self.framePisCofins, "BC COFINS ST", 0.5, 0.77, 0.15, bc_cofins_st)
                pisCOF = criarLabelEntry(self.framePisCofins, "Vr. COFINS ST", 0.7, 0.77, 0.15, vr_cofins_st)
                criaSimouNaoLateral(self.framePisCofins, "Modalidade COFINS ST", "Percentual", "Valor/Qtd", 0.05, 0.76, passe)





                criaBotaoPequeno(self.framePisCofins, "Tributação", 0.7, 0.95, 0.1, lambda:frame.lift())
                criaBotaoPequeno(self.framePisCofins, "Salvar e Sair", 0.1, 0.95, 0.1, lambda:salvar_dados_e_sair())
                ctk.CTkButton(self.framePisCofins, text="X", width=10, height=10, corner_radius=0,command=destroyModal).place(relx=0.989, rely=0.018, anchor="center")


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


        frame = criaFrameJanela(frameTelaNotaProduto, 0.5, 0.5, 0.8, 0.9, self.corModal)

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
            if hasattr(self, "framePisCofins"):
                self.framePisCofins.destroy()






        posGera=-0.03

        criarLabelEntry(frame, "Produto:",                   0.05, 0.05+posGera, 0.25, produto)
        criarLabelEntry(frame, "Código:",                    0.31, 0.05+posGera, 0.15, codigoEntry)
        criarLabelEntry(frame, "NCM:",                       0.47, 0.05+posGera, 0.10, NCMEntry)
        criarLabelEntry(frame, "CSET:",                      0.58, 0.05+posGera, 0.10, CSETEntry)
        criarLabelEntry(frame, "QTD:",                       0.69, 0.05+posGera, 0.05, quantidadeEntry)
        criarLabelEntry(frame, "Beneficio Fisc:",            0.75, 0.05+posGera, 0.15, beneficioEntry)
        cst_a = criarLabelComboBox(frame, "CST A",            0.05, 0.12+posGera, 0.85, opcoes_CST_A)

        csosn = criarLabelComboBox(frame, "CSOSN",                   0.05, 0.195+posGera, 0.5, opcoes_csosn)
        criarLabelEntry(frame, "Alíq. Cálc. Créd. (%)",      0.59, 0.19+posGera, 0.13, aliquEntry)
        criarLabelEntry(frame, "Vr. Cred. ICMS",             0.77, 0.19+posGera, 0.13, credICMSEntry)
        cst_b = criarLabelComboBox(frame, "CST B",                   0.05, 0.27+posGera, 0.85, opcoes_CST_B)

        criarLabelLateralComboBox(frame, "Mod. BC ICMS",     0.11, 0.37+posGera, 0.09, opcoes_MOD_ICMS)
        criarLabelLateralEntry(frame, "BC ICMS",             0.11, 0.41+posGera, 0.09, bc_icms)
        criarLabelLateralEntry(frame, "Red. BC ICMS (%)",    0.11, 0.45+posGera, 0.09, red_bc_icms)
        criarLabelLateralEntry(frame, "Aliq. ICMS (%)",      0.11, 0.49+posGera, 0.09, aliq_icms)
        criarLabelLateralEntry(frame, "Vr. ICMS",            0.11, 0.53+posGera, 0.09, vr_icms)

        mod_bc_icms_st = criarLabelLateralComboBox(frame, "Mod. BC ICMS ST",  0.34, 0.37+posGera, 0.09, opcoes_MOD_ICMS)
        vr_bc_icms = criarLabelLateralEntry(frame, "Valor BC ICMS",       0.34, 0.41+posGera, 0.09, vr_bc_ICMS)
        criarLabelLateralEntry(frame, "MVA ICMS ST (%)",     0.34, 0.45+posGera, 0.09, mva_icms_st)
        criarLabelLateralEntry(frame, "BC ICMS ST",          0.34, 0.49+posGera, 0.09, bc_icms_st)
        criarLabelLateralEntry(frame, "Red. BC ICMS ST (%)", 0.34, 0.53+posGera, 0.09, red_bc_icms_st)

        criarLabelLateralEntry(frame, "Vr. ICMS ST",         0.57, 0.37+posGera, 0.09, vr_icms_st)
        criarLabelLateralEntry(frame, "Vr. BC ICMS ST Ret.", 0.57, 0.41+posGera, 0.09, vr_bc_icms_st_ret)
        criarLabelLateralEntry(frame, "Vr. ICMS ST Ret.",    0.57, 0.45+posGera, 0.09, vr_icms_st_ret)
        criarLabelLateralEntry(frame, "Alíq. ICMS ST c/ FCP",0.57, 0.49+posGera, 0.09, aliq_icms_cfop)
        criarLabelLateralEntry(frame, "BC ICMS ST Dest.",    0.57, 0.53+posGera, 0.09, bc_icms_st_dest)

        criarLabelLateralEntry(frame, "Vr. ICMS Subst.",     0.80, 0.37+posGera, 0.09, vr_icms_subst)
        criarLabelLateralEntry(frame, "Aliq. ICMS ST (%)",   0.80, 0.41+posGera, 0.09, aliq_icms_st)
        criarLabelLateralEntry(frame, "Vr. ICMS ST Dest.",   0.80, 0.45+posGera, 0.09, vr_icms_st_dest)

        destinatario = ctk.CTkLabel(frame,  text="FCP-----------------------------------------------------------------------------", font=("TkDefaultFont", 11))
        destinatario.place(relx=0.02, rely=0.52, relheight=0.01)

        criarLabelLateralEntry(frame, "BC FCP",               0.11, 0.585+posGera, 0.09, bc_FCP)
        criarLabelLateralEntry(frame, "Alíq. FCP (%)",        0.11, 0.625+posGera, 0.09, aliq_fcp_porc)
        criarLabelLateralEntry(frame, "Vr. FCP",              0.11, 0.665+posGera, 0.09, vr_FCP)
        criarLabelLateralEntry(frame, "Aliq. FCP Dif.(%)",    0.34, 0.585+posGera, 0.09, aliq_fcp_dif)
        criarLabelLateralEntry(frame, "BC FCP ST",            0.34, 0.625+posGera, 0.09, bc_fcp_st)
        criarLabelLateralEntry(frame, "Alíq. FCP ST (%)",     0.34, 0.665+posGera, 0.09, aliq_fcp_st)
        criarLabelLateralEntry(frame, "Vr. FCP ST",           0.57, 0.585+posGera, 0.09, vr_fcp_st)
        criarLabelLateralEntry(frame, "Vr. FCP Dif.",         0.57, 0.625+posGera, 0.09, vr_fcp_dif)
        criarLabelLateralEntry(frame, "BC FCP ST Ret.",       0.57, 0.665+posGera, 0.09, bc_fcp_st_ret)
        criarLabelLateralEntry(frame, "Alíq. FCP ST Ret.(%)", 0.80, 0.585+posGera, 0.09, aliq_fcp_st_ret)
        criarLabelLateralEntry(frame, "Vr. FCP ST Ret.",      0.80, 0.625+posGera, 0.09, vr_fcp_st_ret)
        criarLabelLateralEntry(frame, "Vr. FCP Efetivo",      0.80, 0.665+posGera, 0.09, vr_fcp_efet)



        criarLabelEntry(frame, "Alíq. IOF (%)",              0.05, 0.70+posGera, 0.25, aliqIOFEntry)
        criarLabelEntry(frame, "Alíq. II (%)",               0.31, 0.70+posGera, 0.15, aliqIIEntry)
        criarLabelEntry(frame, "BC II ",                     0.47, 0.70+posGera, 0.10, BCIIEntry)
        criarLabelEntry(frame, "Vr. IOF",                    0.58, 0.70+posGera, 0.10, VrIOFEntry)
        criarLabelEntry(frame, "Vr. II",                     0.69, 0.70+posGera, 0.05, VrIIEntry)
        criarLabelEntry(frame, "Vr. Desp. Aduaneiras",       0.75, 0.70+posGera, 0.15, VRDespAduaneira)
        criaTextAreaModal(frame, 0.05, 0.75, 0.85, 'Observações do item', "")


        criaBotaoPequeno(frame, "PIS/COFINS", 0.7, 0.95, 0.1, lambda:PisCofins(frame))
        criaBotaoPequeno(frame, "Salvar e Sair", 0.1, 0.95, 0.1, lambda:salvar_dados_e_sair())
        ctk.CTkButton(frame, text="X", width=10, height=10, corner_radius=0,command=destroyModal).place(relx=0.989, rely=0.018, anchor="center")


        if hasattr(self, "dadosProdutos") and produto.get() in self.dadosProdutos:

            dados_salvos = self.dadosProdutos[produto.get()]

            # Já existentes
            codigoEntry.set(dados_salvos.get("codigo", ""))
            NCMEntry.set(dados_salvos.get("ncm", ""))
            CSETEntry.set(dados_salvos.get("cset", ""))
            quantidadeEntry.set(dados_salvos.get("quantidade", ""))
            beneficioEntry.set(dados_salvos.get("beneficio", ""))
            aliquEntry.set(dados_salvos.get("aliqICMS", ""))
            credICMSEntry.set(dados_salvos.get("credICMS", ""))
            bc_icms.set(dados_salvos.get("bc_icms", ""))
            aliq_icms.set(dados_salvos.get("aliq_icms", ""))
            vr_icms.set(dados_salvos.get("vr_icms", ""))
            csosn.set(dados_salvos.get("csosn", ""))
            cst_a.set(dados_salvos.get("cst_a", ""))
            cst_b.set(dados_salvos.get("cst_b", ""))
            mod_bc_icms.set(dados_salvos.get("mod_bc_icms", ""))
            red_bc_icms.set(dados_salvos.get("red_bc_icms", ""))
            mod_bc_icms_st.set(dados_salvos.get("mod_bc_icms_st", ""))
            vr_bc_icms.insert(0, dados_salvos.get("vr_bc_icms", ""))
            mva_icms_st.set(dados_salvos.get("mva_icms_st", ""))
            bc_icms_st.set(dados_salvos.get("bc_icms_st", ""))
            red_bc_icms_st.set(dados_salvos.get("red_bc_icms_st", ""))
            vr_icms_st.set(dados_salvos.get("vr_icms_st", ""))
            vr_bc_icms_st_ret.set(dados_salvos.get("vr_bc_icms_st_ret", ""))
            vr_icms_st_ret.set(dados_salvos.get("vr_icms_st_ret", ""))
            aliq_icms_cfop.set(dados_salvos.get("aliq_icms_cfop", ""))
            bc_icms_st_dest.set(dados_salvos.get("bc_icms_st_dest", ""))
            vr_icms_subst.set(dados_salvos.get("vr_icms_subst", ""))
            aliq_icms_st.set(dados_salvos.get("aliq_icms_st", ""))
            vr_icms_st_dest.set(dados_salvos.get("vr_icms_st_dest", ""))
            bc_FCP.set(dados_salvos.get("bc_FCP", ""))
            aliq_fcp_porc.set(dados_salvos.get("aliq_fcp_porc", ""))
            vr_FCP.set(dados_salvos.get("vr_FCP", ""))
            aliq_fcp_dif.set(dados_salvos.get("aliq_fcp_dif", ""))
            bc_fcp_st.set(dados_salvos.get("bc_fcp_st", ""))
            aliq_fcp_st.set(dados_salvos.get("aliq_fcp_st", ""))
            vr_fcp_st.set(dados_salvos.get("vr_fcp_st", ""))
            vr_fcp_dif.set(dados_salvos.get("vr_fcp_dif", ""))
            bc_fcp_st_ret.set(dados_salvos.get("bc_fcp_st_ret", ""))
            aliq_fcp_st_ret.set(dados_salvos.get("aliq_fcp_st_ret", ""))
            vr_fcp_st_ret.set(dados_salvos.get("vr_fcp_st_ret", ""))
            vr_fcp_efet.set(dados_salvos.get("vr_fcp_efet", ""))
            aliqIOFEntry.set(dados_salvos.get("aliq_iof", ""))
            aliqIIEntry.set(dados_salvos.get("aliq_ii", ""))
            BCIIEntry.set(dados_salvos.get("bc_ii", ""))
            VrIOFEntry.set(dados_salvos.get("vr_iof", ""))
            VrIIEntry.set(dados_salvos.get("vr_ii", ""))
            VRDespAduaneira.set(dados_salvos.get("vr_desp_aduaneiras", ""))
            aliq_pis.set(dados_salvos.get("aliq_pis",""))
            bc_pis.set(dados_salvos.get("bc_pis",""))
            vr_pis.set(dados_salvos.get("vr_pis",""))
            aliq_pis_st.set(dados_salvos.get("aliq_pis_st",""))
            bc_pis_st.set(dados_salvos.get("bc_pis_st",""))
            vr_pis_st.set(dados_salvos.get("vr_pis_st",""))
            aliq_cofins.set(dados_salvos.get("aliq_cofins",""))
            bc_cofins.set(dados_salvos.get("bc_cofins",""))
            vr_cofins.set(dados_salvos.get("vr_cofins",""))
            aliq_cofins_st.set(dados_salvos.get("aliq_cofins_st",""))
            bc_cofins_st.set(dados_salvos.get("bc_cofins_st",""))
            vr_cofins_st.set(dados_salvos.get("vr_cofins_st",""))





        def salvar_dados_e_sair():
            if not hasattr(self, "dadosProdutos"):
                self.dadosProdutos = {}

            self.dadosProdutos[produto.get()] = {
                "codigo": codigoEntry.get(),
                "ncm": NCMEntry.get(),
                "cset": CSETEntry.get(),
                "quantidade": quantidadeEntry.get(),
                "beneficio": beneficioEntry.get(),
                "cestA": cst_a.get(),
                "aliqICMS": aliquEntry.get(),
                "credICMS": credICMSEntry.get(),
                "bc_icms": bc_icms.get(),
                "aliq_icms": aliq_icms.get(),
                "vr_icms": vr_icms.get(),
                "csosn": csosn.get(),
                "cst_a": cst_a.get(),
                "cst_b": cst_b.get(),
                "mod_bc_icms": mod_bc_icms.get(),
                "red_bc_icms": red_bc_icms.get(),
                "mod_bc_icms_st": mod_bc_icms_st.get(),
                "vr_bc_icms": vr_bc_icms.get(),
                "mva_icms_st": mva_icms_st.get(),
                "bc_icms_st": bc_icms_st.get(),
                "red_bc_icms_st": red_bc_icms_st.get(),
                "vr_icms_st": vr_icms_st.get(),
                "vr_bc_icms_st_ret": vr_bc_icms_st_ret.get(),
                "vr_icms_st_ret": vr_icms_st_ret.get(),
                "aliq_icms_cfop": aliq_icms_cfop.get(),
                "bc_icms_st_dest": bc_icms_st_dest.get(),
                "vr_icms_subst": vr_icms_subst.get(),
                "aliq_icms_st": aliq_icms_st.get(),
                "vr_icms_st_dest": vr_icms_st_dest.get(),
                "bc_FCP": bc_FCP.get(),
                "aliq_fcp_porc": aliq_fcp_porc.get(),
                "vr_FCP": vr_FCP.get(),
                "aliq_fcp_dif": aliq_fcp_dif.get(),
                "bc_fcp_st": bc_fcp_st.get(),
                "aliq_fcp_st": aliq_fcp_st.get(),
                "vr_fcp_st": vr_fcp_st.get(),
                "vr_fcp_dif": vr_fcp_dif.get(),
                "bc_fcp_st_ret": bc_fcp_st_ret.get(),
                "aliq_fcp_st_ret": aliq_fcp_st_ret.get(),
                "vr_fcp_st_ret": vr_fcp_st_ret.get(),
                "vr_fcp_efet": vr_fcp_efet.get(),
                "aliq_iof": aliqIOFEntry.get(),
                "aliq_ii": aliqIIEntry.get(),
                "bc_ii": BCIIEntry.get(),
                "vr_iof": VrIOFEntry.get(),
                "vr_ii": VrIIEntry.get(),
                "vr_desp_aduaneiras": VRDespAduaneira.get(),

                "aliq_pis": aliq_pis.get(),
                "bc_pis": bc_pis.get(),
                "vr_pis": vr_pis.get(),
                "aliq_pis_st": aliq_pis_st.get(),
                "bc_pis_st": bc_pis_st.get(),
                "vr_pis_st": vr_pis_st.get(),
                "aliq_cofins": aliq_cofins.get(),
                "bc_cofins": bc_cofins.get(),
                "vr_cofins": vr_cofins.get(),
                "aliq_cofins_st": aliq_cofins_st.get(),
                "bc_cofins_st": bc_cofins_st.get(),
                "vr_cofins_st": vr_cofins_st.get()

            }

            destroyModal()



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

    