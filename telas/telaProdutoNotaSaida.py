import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from tkinter import messagebox
import requests
from PIL import Image
import datetime
from telas.telaTransporteNotaSaida import telaTransporteNotaSaida
from componentes import criaFrameJanela, criaBotao, criaBotaoPequeno, criaLabel, criaEntry, criaSimouNaoLateral, criaTextAreaModal, criarLabelEntry, criarLabelComboBox, criarLabelLateralComboBox, criarLabelLateralEntry
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries


def telaProdutosNotaSaida(self, cnpj, cfop):

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

    variavelCfop = ctk.StringVar()
    variavelCfop.set(cfop)



    frameTelaNotaProduto = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    frameParaItens = ctk.CTkScrollableFrame(frameTelaNotaProduto, height=800, orientation="vertical", fg_color=self.corFundo)
    frameParaItens.place(relx=0.5, rely=0.6, relwidth=0.94, anchor="center")
    container = ctk.CTkFrame(frameParaItens, fg_color="red", height=1500)
    container.pack(fill="x", padx=0, pady=0)
    frameParaItensNoFrame = ctk.CTkFrame(frameParaItens, height=1500, fg_color=self.corFundo)
    frameParaItensNoFrame.place(x=-25, y=-280, relwidth=1.06)
 

    def passe(self):
        pass

    def buscaProduto(nomeDoProduto, entradaProduto, yNovo):
        if hasattr(self, "resultadoLabelsProduto"):
            for label in self.resultadoLabelsProduto:
                label.destroy()

        self.resultadoLabelsProduto = []

        for i, row in enumerate(Buscas.buscaEstoqueProdutosFiscal(nomeDoProduto, cnpj)):
            if i >= 5:
                break     
            label = criaBotao(frameParaItensNoFrame,row[0],0.195,yNovo+0.02 + i * 0.02,0.26,lambda nome=row[0], valor=row[6].replace(',', '.'), quantidade=row[8].replace(',', '.'), ent=entradaProduto:selecionaProduto(nome, valor, quantidade, ent))
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
                # linha["preco"].configure(state="disabled")


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
        self.mod_bc_icms = ctk.StringVar()
        self.bc_icms = ctk.StringVar()
        self.red_bc_icms = ctk.StringVar()
        self.aliq_icms = ctk.StringVar()
        self.vr_icms = ctk.StringVar()
        self.mva_icms_st = ctk.StringVar()
        self.bc_icms_st = ctk.StringVar()
        self.red_bc_icms_st = ctk.StringVar()
        self.aliq_icms_st = ctk.StringVar()
        self.vr_icms_st = ctk.StringVar()
        self.vr_bc_icms_st_ret = ctk.StringVar()
        self.vr_icms_st_ret  = ctk.StringVar()
        self.vr_icms_subst = ctk.StringVar()
        self.vr_bc_ICMS = ctk.StringVar()
        self.vr_icms_st_dest = ctk.StringVar()
        self.bc_icms_st_dest = ctk.StringVar()
        self.aliq_icms_cfop = ctk.StringVar()
        self.bc_FCP = ctk.StringVar()
        self.aliq_fcp_porc = ctk.StringVar()
        self.vr_FCP = ctk.StringVar()
        self.aliq_fcp_dif = ctk.StringVar()
        self.bc_fcp_st = ctk.StringVar()
        self.aliq_fcp_st = ctk.StringVar()
        self.vr_fcp_st = ctk.StringVar()
        self.vr_fcp_dif = ctk.StringVar()
        self.bc_fcp_st_ret = ctk.StringVar()
        self.aliq_fcp_st_ret = ctk.StringVar()
        self.vr_fcp_st_ret = ctk.StringVar()
        self.vr_fcp_efet = ctk.StringVar()
        self.codigoEntry = ctk.StringVar()
        self.NCMEntry = ctk.StringVar()
        self.CSETEntry = ctk.StringVar()
        self.quantidadeEntry = ctk.StringVar()
        self.beneficioEntry = ctk.StringVar()
        self.aliqIOFEntry = ctk.StringVar()
        self.aliqIIEntry = ctk.StringVar()
        self.BCIIEntry = ctk.StringVar()
        self.VrIOFEntry = ctk.StringVar()
        self.VrIIEntry = ctk.StringVar()
        self.VRDespAduaneira = ctk.StringVar()
        self.aliquEntry =ctk.StringVar()
        self.credICMSEntry =ctk.StringVar()
        self.aliq_pis = ctk.StringVar()
        self.bc_pis = ctk.StringVar()
        self.vr_pis = ctk.StringVar()
        self.aliq_pis_st = ctk.StringVar()
        self.bc_pis_st = ctk.StringVar()
        self.vr_pis_st = ctk.StringVar()
        self.aliq_cofins = ctk.StringVar()
        self.bc_cofins = ctk.StringVar()
        self.vr_cofins = ctk.StringVar()
        self.aliq_cofins_st = ctk.StringVar()
        self.bc_cofins_st = ctk.StringVar()
        self.vr_cofins_st = ctk.StringVar()

        def PisCofins(frame):
            if hasattr(self, "framePisCofins") and self.framePisCofins.winfo_exists():
                self.framePisCofins.lift()  
            else:
                self.framePisCofins = criaFrameJanela(frameTelaNotaProduto, 0.5, 0.5, 0.8, 0.9, self.corModal)
                criaBotaoPequeno(self.framePisCofins, "Calcular", 0.4, 0.95, 0.1, lambda:calculaValores())


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

                criarLabelEntry(self.framePisCofins, "Alíq. PIS (%)", 0.3, 0.18, 0.15, self.aliq_pis)
                criarLabelEntry(self.framePisCofins, "BC PIS", 0.5, 0.18, 0.15, self.bc_pis)
                criarLabelEntry(self.framePisCofins, "Vr. PIS", 0.7, 0.18, 0.15, self.vr_pis)
                criaSimouNaoLateral(self.framePisCofins, "Modalidade PIS", "Percentual", "Valor/Qtd", 0.05, 0.15, passe)

                criarLabelEntry(self.framePisCofins, "Alíq. PIS ST (%)", 0.3, 0.35, 0.15, self.aliq_pis_st)
                criarLabelEntry(self.framePisCofins, "BC PIS ST", 0.5, 0.35, 0.15, self.bc_pis_st)
                criarLabelEntry(self.framePisCofins, "Vr. PIS ST", 0.7, 0.35, 0.15, self.vr_pis_st)
                criaSimouNaoLateral(self.framePisCofins, "Modalidade PIS ST", "Percentual", "Valor/Qtd", 0.05, 0.33, passe)
                

                COFINS = ctk.CTkLabel(self.framePisCofins,  text="COFINS-----------------------------------------------------------------------------", font=("TkDefaultFont", 11))
                COFINS.place(relx=0.02, rely=0.54, relheight=0.015)

                criarLabelEntry(self.framePisCofins, "Alíq. COFINS (%)", 0.3, 0.60, 0.15, self.aliq_cofins)
                criarLabelEntry(self.framePisCofins, "BC COFINS", 0.5, 0.60, 0.15, self.bc_cofins)
                criarLabelEntry(self.framePisCofins, "Vr. COFINS", 0.7, 0.60, 0.15, self.vr_cofins)
                criaSimouNaoLateral(self.framePisCofins, "Modalidade COFINS", "Percentual", "Valor/Qtd", 0.05, 0.58, passe)

                aliqCOF = criarLabelEntry(self.framePisCofins, "Alíq. COFINS ST (%)", 0.3, 0.77, 0.15, self.aliq_cofins_st)
                bcCOF = criarLabelEntry(self.framePisCofins, "BC COFINS ST", 0.5, 0.77, 0.15, self.bc_cofins_st)
                pisCOF = criarLabelEntry(self.framePisCofins, "Vr. COFINS ST", 0.7, 0.77, 0.15, self.vr_cofins_st)
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
        criarLabelEntry(frame, "Código:",                    0.31, 0.05+posGera, 0.15, self.codigoEntry)
        criarLabelEntry(frame, "NCM:",                       0.47, 0.05+posGera, 0.10, self.NCMEntry)
        criarLabelEntry(frame, "CSET:",                      0.58, 0.05+posGera, 0.10, self.CSETEntry)
        criarLabelEntry(frame, "QTD:",                       0.69, 0.05+posGera, 0.05, self.quantidadeEntry)
        criarLabelEntry(frame, "Beneficio Fisc:",            0.75, 0.05+posGera, 0.15, self.beneficioEntry)
        self.cst_a = criarLabelComboBox(frame, "CST A",      0.05, 0.12+posGera, 0.85, opcoes_CST_A)

        self.csosn = criarLabelComboBox(frame, "CSOSN",      0.05, 0.195+posGera, 0.5, opcoes_csosn)
        criarLabelEntry(frame, "Alíq. Cálc. Créd. (%)",      0.59, 0.19+posGera, 0.13, self.aliquEntry)
        criarLabelEntry(frame, "Vr. Cred. ICMS",             0.77, 0.19+posGera, 0.13, self.credICMSEntry)
        self.cst_b = criarLabelComboBox(frame, "CST B",      0.05, 0.27+posGera, 0.85, opcoes_CST_B)



        self.mod_bc_icms = criarLabelLateralComboBox(frame, "Mod. BC ICMS",     0.11, 0.37+posGera, 0.09, opcoes_MOD_ICMS)
        criarLabelLateralEntry(frame, "BC ICMS",             0.11, 0.41+posGera, 0.09, self.bc_icms)
        criarLabelLateralEntry(frame, "Red. BC ICMS (%)",    0.11, 0.45+posGera, 0.09, self.red_bc_icms)
        criarLabelLateralEntry(frame, "Aliq. ICMS (%)",      0.11, 0.49+posGera, 0.09, self.aliq_icms)
        criarLabelLateralEntry(frame, "Vr. ICMS",            0.11, 0.53+posGera, 0.09, self.vr_icms)

        self.mod_bc_icms_st = criarLabelLateralComboBox(frame, "Mod. BC ICMS ST",  0.34, 0.37+posGera, 0.09, opcoes_MOD_ICMS)
        self.vr_bc_icms = criarLabelLateralEntry(frame, "Valor BC ICMS",       0.34, 0.41+posGera, 0.09, self.vr_bc_ICMS)

        self.valor_csosn    = self.csosn.get()
        self.valor_cst_a    = self.cst_a.get()
        self.valor_cst_b    = self.cst_b.get()
        self.valor_mod_bc_icms    = self.mod_bc_icms.get()
        self.valor_mod_bc_icms_st = self.mod_bc_icms_st.get()
        self.valor_vr_bc_icms     = self.vr_bc_icms.get()
        criarLabelLateralEntry(frame, "MVA ICMS ST (%)",     0.34, 0.45+posGera, 0.09, self.mva_icms_st)
        criarLabelLateralEntry(frame, "BC ICMS ST",          0.34, 0.49+posGera, 0.09, self.bc_icms_st)
        criarLabelLateralEntry(frame, "Red. BC ICMS ST (%)", 0.34, 0.53+posGera, 0.09, self.red_bc_icms_st)

        criarLabelLateralEntry(frame, "Vr. ICMS ST",         0.57, 0.37+posGera, 0.09, self.vr_icms_st)
        criarLabelLateralEntry(frame, "Vr. BC ICMS ST Ret.", 0.57, 0.41+posGera, 0.09, self.vr_bc_icms_st_ret)
        criarLabelLateralEntry(frame, "Vr. ICMS ST Ret.",    0.57, 0.45+posGera, 0.09, self.vr_icms_st_ret)
        criarLabelLateralEntry(frame, "Alíq. ICMS ST c/ FCP",0.57, 0.49+posGera, 0.09, self.aliq_icms_cfop)
        criarLabelLateralEntry(frame, "BC ICMS ST Dest.",    0.57, 0.53+posGera, 0.09, self.bc_icms_st_dest)

        criarLabelLateralEntry(frame, "Vr. ICMS Subst.",     0.80, 0.37+posGera, 0.09, self.vr_icms_subst)
        criarLabelLateralEntry(frame, "Aliq. ICMS ST (%)",   0.80, 0.41+posGera, 0.09, self.aliq_icms_st)
        criarLabelLateralEntry(frame, "Vr. ICMS ST Dest.",   0.80, 0.45+posGera, 0.09, self.vr_icms_st_dest)

        destinatario = ctk.CTkLabel(frame,  text="FCP-----------------------------------------------------------------------------", font=("TkDefaultFont", 11))
        destinatario.place(relx=0.02, rely=0.52, relheight=0.01)

        criarLabelLateralEntry(frame, "BC FCP",               0.11, 0.585+posGera, 0.09, self.bc_FCP)
        criarLabelLateralEntry(frame, "Alíq. FCP (%)",        0.11, 0.625+posGera, 0.09, self.aliq_fcp_porc)
        criarLabelLateralEntry(frame, "Vr. FCP",              0.11, 0.665+posGera, 0.09, self.vr_FCP)
        criarLabelLateralEntry(frame, "Aliq. FCP Dif.(%)",    0.34, 0.585+posGera, 0.09, self.aliq_fcp_dif)
        criarLabelLateralEntry(frame, "BC FCP ST",            0.34, 0.625+posGera, 0.09, self.bc_fcp_st)
        criarLabelLateralEntry(frame, "Alíq. FCP ST (%)",     0.34, 0.665+posGera, 0.09, self.aliq_fcp_st)
        criarLabelLateralEntry(frame, "Vr. FCP ST",           0.57, 0.585+posGera, 0.09, self.vr_fcp_st)
        criarLabelLateralEntry(frame, "Vr. FCP Dif.",         0.57, 0.625+posGera, 0.09, self.vr_fcp_dif)
        criarLabelLateralEntry(frame, "BC FCP ST Ret.",       0.57, 0.665+posGera, 0.09, self.bc_fcp_st_ret)
        criarLabelLateralEntry(frame, "Alíq. FCP ST Ret.(%)", 0.80, 0.585+posGera, 0.09, self.aliq_fcp_st_ret)
        criarLabelLateralEntry(frame, "Vr. FCP ST Ret.",      0.80, 0.625+posGera, 0.09, self.vr_fcp_st_ret)
        criarLabelLateralEntry(frame, "Vr. FCP Efetivo",      0.80, 0.665+posGera, 0.09, self.vr_fcp_efet)



        criarLabelEntry(frame, "Alíq. IOF (%)",              0.05, 0.70+posGera, 0.25, self.aliqIOFEntry)
        criarLabelEntry(frame, "Alíq. II (%)",               0.31, 0.70+posGera, 0.15, self.aliqIIEntry)
        criarLabelEntry(frame, "BC II ",                     0.47, 0.70+posGera, 0.10, self.BCIIEntry)
        criarLabelEntry(frame, "Vr. IOF",                    0.58, 0.70+posGera, 0.10, self.VrIOFEntry)
        criarLabelEntry(frame, "Vr. II",                     0.69, 0.70+posGera, 0.05, self.VrIIEntry)
        criarLabelEntry(frame, "Vr. Desp. Aduaneiras",       0.75, 0.70+posGera, 0.15, self.VRDespAduaneira)
        criaTextAreaModal(frame, 0.05, 0.75, 0.85, 'Observações do item', "")


        criaBotaoPequeno(frame, "PIS/COFINS", 0.7, 0.95, 0.1, lambda:PisCofins(frame))
        criaBotaoPequeno(frame, "Salvar e Sair", 0.1, 0.95, 0.1, lambda:salvar_dados_e_sair())
        criaBotaoPequeno(frame, "Calcular", 0.4, 0.95, 0.1, lambda:calculaValores())
        ctk.CTkButton(frame, text="X", width=10, height=10, corner_radius=0,command=destroyModal).place(relx=0.989, rely=0.018, anchor="center")


        if hasattr(self, "dadosProdutos") and produto.get() in self.dadosProdutos:
            print(self.dadosProdutos)

            dados_salvos = self.dadosProdutos[produto.get()]

            # Já existentes
            self.codigoEntry.set(dados_salvos.get("codigo", ""))
            self.NCMEntry.set(dados_salvos.get("ncm", ""))
            self.CSETEntry.set(dados_salvos.get("cset", ""))
            self.quantidadeEntry.set(dados_salvos.get("quantidade", ""))
            self.beneficioEntry.set(dados_salvos.get("beneficio", ""))
            self.aliquEntry.set(dados_salvos.get("aliqICMS", ""))
            self.credICMSEntry.set(dados_salvos.get("credICMS", ""))
            self.bc_icms.set(dados_salvos.get("bc_icms", ""))
            self.aliq_icms.set(dados_salvos.get("aliq_icms", ""))
            self.vr_icms.set(dados_salvos.get("vr_icms", ""))
            self.csosn.set(dados_salvos.get("csosn", ""))
            self.cst_a.set(dados_salvos.get("cst_a", ""))
            self.cst_b.set(dados_salvos.get("cst_b", ""))
            self.mod_bc_icms.set(dados_salvos.get("mod_bc_icms", ""))
            self.red_bc_icms.set(dados_salvos.get("red_bc_icms", ""))
            self.mod_bc_icms_st.set(dados_salvos.get("mod_bc_icms_st", ""))
            self.vr_bc_icms.insert(0, dados_salvos.get("vr_bc_icms", ""))
            self.mva_icms_st.set(dados_salvos.get("mva_icms_st", ""))
            self.bc_icms_st.set(dados_salvos.get("bc_icms_st", ""))
            self.red_bc_icms_st.set(dados_salvos.get("red_bc_icms_st", ""))
            self.vr_icms_st.set(dados_salvos.get("vr_icms_st", ""))
            self.vr_bc_icms_st_ret.set(dados_salvos.get("vr_bc_icms_st_ret", ""))
            self.vr_icms_st_ret.set(dados_salvos.get("vr_icms_st_ret", ""))
            self.aliq_icms_cfop.set(dados_salvos.get("aliq_icms_cfop", ""))
            self.bc_icms_st_dest.set(dados_salvos.get("bc_icms_st_dest", ""))
            self.vr_icms_subst.set(dados_salvos.get("vr_icms_subst", ""))
            self.aliq_icms_st.set(dados_salvos.get("aliq_icms_st", ""))
            self.vr_icms_st_dest.set(dados_salvos.get("vr_icms_st_dest", ""))
            self.bc_FCP.set(dados_salvos.get("bc_FCP", ""))
            self.aliq_fcp_porc.set(dados_salvos.get("aliq_fcp_porc", ""))
            self.vr_FCP.set(dados_salvos.get("vr_FCP", ""))
            self.aliq_fcp_dif.set(dados_salvos.get("aliq_fcp_dif", ""))
            self.bc_fcp_st.set(dados_salvos.get("bc_fcp_st", ""))
            self.aliq_fcp_st.set(dados_salvos.get("aliq_fcp_st", ""))
            self.vr_fcp_st.set(dados_salvos.get("vr_fcp_st", ""))
            self.vr_fcp_dif.set(dados_salvos.get("vr_fcp_dif", ""))
            self.bc_fcp_st_ret.set(dados_salvos.get("bc_fcp_st_ret", ""))
            self.aliq_fcp_st_ret.set(dados_salvos.get("aliq_fcp_st_ret", ""))
            self.vr_fcp_st_ret.set(dados_salvos.get("vr_fcp_st_ret", ""))
            self.vr_fcp_efet.set(dados_salvos.get("vr_fcp_efet", ""))
            self.aliqIOFEntry.set(dados_salvos.get("aliq_iof", ""))
            self.aliqIIEntry.set(dados_salvos.get("aliq_ii", ""))
            self.BCIIEntry.set(dados_salvos.get("bc_ii", ""))
            self.VrIOFEntry.set(dados_salvos.get("vr_iof", ""))
            self.VrIIEntry.set(dados_salvos.get("vr_ii", ""))
            self.VRDespAduaneira.set(dados_salvos.get("vr_desp_aduaneiras", ""))
            self.aliq_pis.set(dados_salvos.get("aliq_pis",""))
            self.bc_pis.set(dados_salvos.get("bc_pis",""))
            self.vr_pis.set(dados_salvos.get("vr_pis",""))
            self.aliq_pis_st.set(dados_salvos.get("aliq_pis_st",""))
            self.bc_pis_st.set(dados_salvos.get("bc_pis_st",""))
            self.vr_pis_st.set(dados_salvos.get("vr_pis_st",""))
            self.aliq_cofins.set(dados_salvos.get("aliq_cofins",""))
            self.bc_cofins.set(dados_salvos.get("bc_cofins",""))
            self.vr_cofins.set(dados_salvos.get("vr_cofins",""))
            self.aliq_cofins_st.set(dados_salvos.get("aliq_cofins_st",""))
            self.bc_cofins_st.set(dados_salvos.get("bc_cofins_st",""))
            self.vr_cofins_st.set(dados_salvos.get("vr_cofins_st",""))




        def calculaValores():
            # VO (valor da operação) pegando do subtotal da linha; se vazio, calcula do básico
            try:
                vo = float(linha["subtotal"].get().replace(",", "."))
            except:
                try:
                    preco = float((linha["preco"].get() or "0").replace(",", "."))
                except:
                    preco = 0.0
                try:
                    qtd = float(linha["quantidade"].get() or "0")
                except:
                    qtd = 0.0
                try:
                    acresc = float((linha["acrescimo"].get() or "0").replace(",", "."))
                except:
                    acresc = 0.0
                try:
                    desc_real = float((linha["desc_real"].get() or "0").replace(",", "."))
                except:
                    desc_real = 0.0
                try:
                    desc_perc = float((linha["desc_porcentagem"].get() or "0").replace(",", "."))
                except:
                    desc_perc = 0.0
                vo = preco * qtd - desc_real - (preco * qtd * (desc_perc / 100.0)) + acresc
                if vo < 0:
                    vo = 0.0

            # -----------------------
            # ICMS PRÓPRIO (CST 00)
            # -----------------------
            mod_icms = self.mod_bc_icms.get()
            try:
                red_icms = float((self.red_bc_icms.get() or "0").replace(",", "."))
            except:
                red_icms = 0.0
            try:
                aliq_icms = float((self.aliq_icms.get() or "0").replace(",", "."))
            except:
                aliq_icms = 0.0

            # Valor da Operação (simples): vBC = VO * (1 - Red/100)
            if mod_icms == "Valor da Operação" or mod_icms == "":
                vbc_icms = vo * (1.0 - (red_icms / 100.0))
            else:
                # Mantém simples: usa mesma forma como aproximação
                vbc_icms = vo * (1.0 - (red_icms / 100.0))

            vicms = vbc_icms * (aliq_icms / 100.0)

            self.bc_icms.set(f"{vbc_icms:.2f}")
            print(vbc_icms)
            self.vr_icms.set(f"{vicms:.2f}")

            # -----------------------
            # ICMS ST (se houver)
            # -----------------------
            mod_st = self.mod_bc_icms_st.get()
            try:
                red_st = float((self.red_bc_icms_st.get() or "0").replace(",", "."))
            except:
                red_st = 0.0
            try:
                mva = float((self.mva_icms_st.get() or "0").replace(",", "."))
            except:
                mva = 0.0
            try:
                aliq_st = float((self.aliq_icms_st.get() or "0").replace(",", "."))
            except:
                aliq_st = 0.0

            # Base ST conforme modalidade
            vbc_st = 0.0
            if mod_st == "Margem Valor Agregado (%)":
                vbc_pre = vo * (1.0 - (red_st / 100.0))
                vbc_st = vbc_pre * (1.0 + (mva / 100.0))
            elif mod_st in ("Pauta (Valor)", "Preço Tabelado Máx. (Valor)"):
                # Campo "Valor BC ICMS" (override/pauta)
                try:
                    vbc_st = float((self.vr_bc_ICMS.get() or "0").replace(",", "."))
                except:
                    vbc_st = 0.0
            elif mod_st == "Valor da Operação":
                vbc_st = vo * (1.0 - (red_st / 100.0))
            else:
                vbc_st = 0.0

            self.bc_icms_st.set(f"{vbc_st:.2f}" if vbc_st > 0 else "")

            # vICMSST = (vBCST * AlqST) - vICMS
            vicmsst_bruto = vbc_st * (aliq_st / 100.0)
            vicmsst = max(vicmsst_bruto - vicms, 0.0)

            if vbc_st > 0:
                self.vr_icms_st.set(f"{vicmsst:.2f}")
                self.vr_bc_icms_st_ret.set(f"{vbc_st:.2f}")
                self.vr_icms_st_ret.set(f"{vicmsst:.2f}")
                self.vr_icms_subst.set(f"{vicmsst:.2f}")
            else:
                self.vr_icms_st.set("")
                self.vr_bc_icms_st_ret.set("")
                self.vr_icms_st_ret.set("")
                self.vr_icms_subst.set("")

            # -----------------------
            # FCP / FCP-ST (se aplicável)
            # -----------------------
            # FCP: vFCP = BC_FCP * pFCP; se BC_FCP vazio, usa vBCST
            try:
                p_fcp = float((self.aliq_fcp_porc.get() or "0").replace(",", "."))
            except:
                p_fcp = 0.0
            try:
                bc_fcp = float((self.bc_FCP.get() or "0").replace(",", "."))
            except:
                bc_fcp = 0.0
            if bc_fcp == 0.0:
                bc_fcp = vbc_st
            vfcp = bc_fcp * (p_fcp / 100.0)

            self.bc_FCP.set(f"{bc_fcp:.2f}" if bc_fcp > 0 else "")
            self.vr_FCP.set(f"{vfcp:.2f}" if vfcp > 0 else "")

            # FCP-ST: vFCPST = BC_FCP_ST * pFCP_ST; se base vazia, usa vBCST
            try:
                p_fcp_st = float((self.aliq_fcp_st.get() or "0").replace(",", "."))
            except:
                p_fcp_st = 0.0
            try:
                bc_fcp_st = float((self.bc_fcp_st.get() or "0").replace(",", "."))
            except:
                bc_fcp_st = 0.0
            if bc_fcp_st == 0.0:
                bc_fcp_st = vbc_st
            vfcp_st = bc_fcp_st * (p_fcp_st / 100.0)

            self.bc_fcp_st.set(f"{bc_fcp_st:.2f}" if bc_fcp_st > 0 else "")
            self.vr_fcp_st.set(f"{vfcp_st:.2f}" if vfcp_st > 0 else "")

            # --- PIS (base = VO, igual à lógica "Valor da Operação") ---
            try:
                aliq_pis = float((self.aliq_pis.get() or "0").replace(",", "."))
            except:
                aliq_pis = 0.0
            try:
                vbc_pis = float((self.bc_pis.get() or "0").replace(",", "."))
            except:
                vbc_pis = 0.0
            if vbc_pis == 0.0:
                vbc_pis = vo  # mesma base do BC ICMS quando "Valor da Operação"
            self.bc_pis.set(f"{vbc_pis:.2f}")
            self.vr_pis.set(f"{(vbc_pis * aliq_pis / 100.0):.2f}")

            # --- COFINS (base = VO, igual à lógica "Valor da Operação") ---
            try:
                aliq_cofins = float((self.aliq_cofins.get() or "0").replace(",", "."))
            except:
                aliq_cofins = 0.0
            try:
                vbc_cofins = float((self.bc_cofins.get() or "0").replace(",", "."))
            except:
                vbc_cofins = 0.0
            if vbc_cofins == 0.0:
                vbc_cofins = vo  # mesma base do BC ICMS quando "Valor da Operação"
            self.bc_cofins.set(f"{vbc_cofins:.2f}")
            self.vr_cofins.set(f"{(vbc_cofins * aliq_cofins / 100.0):.2f}")


        calculaValores()
        



        def salvar_dados_e_sair():
            if not hasattr(self, "dadosProdutos"):
                self.dadosProdutos = {}




######## ==================== DADOS TA AQUIIIII ======================== ########
            self.dadosProdutos[produto.get()] = {
                "codigo": self.codigoEntry.get(),
                "ncm": self.NCMEntry.get(),
                "cset": self.CSETEntry.get(),
                "quantidade": self.quantidadeEntry.get(),
                "beneficio": self.beneficioEntry.get(),
                "cestA": self.cst_a.get(),
                "aliqICMS": self.aliquEntry.get(),
                "credICMS": self.credICMSEntry.get(),
                "bc_icms": self.bc_icms.get(),
                "aliq_icms": self.aliq_icms.get(),
                "vr_icms": self.vr_icms.get(),
                "csosn": self.csosn.get(),
                "cst_a": self.cst_a.get(),
                "cst_b": self.cst_b.get(),
                "mod_bc_icms": self.mod_bc_icms.get(),
                "red_bc_icms": self.red_bc_icms.get(),
                "mod_bc_icms_st": self.mod_bc_icms_st.get(),
                "vr_bc_icms": self.vr_bc_icms.get(),
                "mva_icms_st": self.mva_icms_st.get(),
                "bc_icms_st": self.bc_icms_st.get(),
                "red_bc_icms_st": self.red_bc_icms_st.get(),
                "vr_icms_st": self.vr_icms_st.get(),
                "vr_bc_icms_st_ret": self.vr_bc_icms_st_ret.get(),
                "vr_icms_st_ret": self.vr_icms_st_ret.get(),
                "aliq_icms_cfop": self.aliq_icms_cfop.get(),
                "bc_icms_st_dest": self.bc_icms_st_dest.get(),
                "vr_icms_subst": self.vr_icms_subst.get(),
                "aliq_icms_st": self.aliq_icms_st.get(),
                "vr_icms_st_dest": self.vr_icms_st_dest.get(),
                "bc_FCP": self.bc_FCP.get(),
                "aliq_fcp_porc": self.aliq_fcp_porc.get(),
                "vr_FCP": self.vr_FCP.get(),
                "aliq_fcp_dif": self.aliq_fcp_dif.get(),
                "bc_fcp_st": self.bc_fcp_st.get(),
                "aliq_fcp_st": self.aliq_fcp_st.get(),
                "vr_fcp_st": self.vr_fcp_st.get(),
                "vr_fcp_dif": self.vr_fcp_dif.get(),
                "bc_fcp_st_ret": self.bc_fcp_st_ret.get(),
                "aliq_fcp_st_ret": self.aliq_fcp_st_ret.get(),
                "vr_fcp_st_ret": self.vr_fcp_st_ret.get(),
                "vr_fcp_efet": self.vr_fcp_efet.get(),
                "aliq_iof": self.aliqIOFEntry.get(),
                "aliq_ii": self.aliqIIEntry.get(),
                "bc_ii": self.BCIIEntry.get(),
                "vr_iof": self.VrIOFEntry.get(),
                "vr_ii": self.VrIIEntry.get(),
                "vr_desp_aduaneiras": self.VRDespAduaneira.get(),
                "aliq_pis": self.aliq_pis.get(),
                "bc_pis": self.bc_pis.get(),
                "vr_pis": self.vr_pis.get(),
                "aliq_pis_st": self.aliq_pis_st.get(),
                "bc_pis_st": self.bc_pis_st.get(),
                "vr_pis_st": self.vr_pis_st.get(),
                "aliq_cofins": self.aliq_cofins.get(),
                "bc_cofins": self.bc_cofins.get(),
                "vr_cofins": self.vr_cofins.get(),
                "aliq_cofins_st": self.aliq_cofins_st.get(),
                "bc_cofins_st": self.bc_cofins_st.get(),
                "vr_cofins_st": self.vr_cofins_st.get()

            }
            print(self.dadosProdutos)

            destroyModal()


    def atualizarTotalGeral():
        total = 0.0

        for linha in self.linhas:
            entry_preco       = linha["preco"]
            entry_descPorc    = linha["desc_porcentagem"]
            entry_descReal    = linha["desc_real"]
            entry_subtotal    = linha["subtotal"]
            entry_quantida    = linha["quantidade"]
            entry_acrescim    = linha["acrescimo"]

            descReal = float((entry_descReal.get() or "0").replace(",", "."))
            descPorc = float((entry_descPorc.get() or "0").replace(",", ".")) / 100.0
            quantida = float(entry_quantida.get() or 0)
            acrescim = float((entry_acrescim.get() or "0").replace(",", "."))

            # Base unitária
            precoAtual = float((entry_preco.get() or "0").replace(",", "."))
            valorUnit = (
                precoAtual if precoAtual > 0
                else linha.get("subtotal_original", float((entry_subtotal.get() or "0").replace(",", ".")))
            )

            # 1) Calcula total bruto da linha (preço x quantidade) + acréscimo
            baseSemDesc = (valorUnit * quantida if quantida > 0 else valorUnit) + acrescim
            novo_subtotal = baseSemDesc

            # 2) Se houver DESCONTO EM R$, aplica UMA VEZ no total da linha
            if descReal > 0:
                entry_descPorc.delete(0, "end"); entry_descPorc.insert(0, "0")
                novo_subtotal = max(baseSemDesc - descReal, 0.0)

            # 3) Se houver DESCONTO EM %, aplica sobre o total da linha
            elif descPorc > 0:
                entry_descReal.delete(0, "end"); entry_descReal.insert(0, "0")
                novo_subtotal = max(baseSemDesc * (1.0 - descPorc), 0.0)

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
                    entrada.configure(textvariable=variavelCfop)

                if campo == 'subtotal':
                    entrada.bind("<KeyRelease>", lambda event: atualizarTotalGeral())

                if campo == "preco":
                    entrada.bind("<KeyRelease>", lambda event, e=entrada: atualizarTotalGeral())


                
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
        self.entradaProduto = ""

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


    criaBotao(frameTelaNotaProduto, "Próximo - Tela Transporte", 0.25, 0.94, 0.15, lambda: (montarValoresDosItens(frameTelaNotaProduto), telaTransporteNotaSaida(self))).place(anchor="nw")
    criaBotao(frameTelaNotaProduto, "Voltar", 0.05, 0.94, 0.15, lambda: frameTelaNotaProduto.destroy()).place(anchor="nw")

    aplicar_maiusculo_em_todos_entries(self)

    