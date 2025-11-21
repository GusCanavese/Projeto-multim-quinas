
import sys
import os

from telas.telaTotais import telaTotais
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from tkinter import messagebox, TclError
import requests
from PIL import Image
import datetime
from telas.telaTransporteNotaSaida import telaTransporteNotaSaida
from componentes import criaFrameJanela, criaBotao, criaBotaoPequeno, criaLabel, criaEntry, criaSimouNaoLateral, criaTextAreaModal, criarLabelEntry, criarLabelComboBox, criarLabelLateralComboBox, criarLabelLateralEntry
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries


def telaProdutos(self, dadosNota, EhNotaDoConsumidor, cfop):
    print(EhNotaDoConsumidor)
    """
    Tela de Produtos da Nota de Saída.
    Se `dadosNota` (NF-e de entrada) for fornecido, os itens serão
    pré-carregados automaticamente nas linhas (produto, preço, quantidade, subtotal).
    """

    nota_importada = bool(dadosNota)
    if nota_importada:
        self.dadosNota = dadosNota
        # compatibilidade com telas que já utilizavam esse atributo
        self.dadosNFeEntrada = dadosNota

    self.importouNotaEntrada = nota_importada

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

        for i, row in enumerate(Buscas.buscaEstoqueProdutosFiscal(nomeDoProduto)):
            if i >= 5:
                break
            label = criaBotao(frameParaItensNoFrame,row[0],0.195,yNovo + 0.02 + i * 0.02,0.26,lambda nome=row[0], valor=row[6].replace(',', '.'), quantidade=row[8].replace(',', '.'), ent=entradaProduto, ncm=row[4]: selecionaProduto(nome, valor, quantidade, ent, ncm))
            label.configure(fg_color=self.cor, corner_radius=0, font=("TkDefaultFont", 14))
            self.resultadoLabelsProduto.append(label)

    def selecionaProduto(nome, valor, quantidade, entradaProduto, ncm):
        entradaProduto.delete(0, "end")
        entradaProduto.insert(0, nome)

        # Procura a linha correta
        for linha in self.linhas:
            if linha["produto"] == entradaProduto:
                linha["preco"].delete(0, "end")
                linha["preco"].insert(0, valor)

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
                linha["ncm"] = ncm

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
        self.aliq_pis = ctk.StringVar()
        self.aliq_icms_cfop = ctk.StringVar()
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
        self.bc_pis = ctk.StringVar()
        self.vr_pis = ctk.StringVar()
        self.aliq_pis_st = ctk.StringVar()
        self.bc_pis_st = ctk.StringVar()
        self.aliq_cofins = ctk.StringVar()
        self.bc_cofins = ctk.StringVar()
        self.vr_cofins = ctk.StringVar()
        self.aliq_cofins_st = ctk.StringVar()
        self.bc_cofins_st = ctk.StringVar()
        self.vr_cofins_st = ctk.StringVar()

        def _pis_cofins_frame_aberto():
            try:
                return hasattr(self, "framePisCofins") and self.framePisCofins.winfo_exists()
            except TclError:
                return False

        def PisCofins(frame):
            if _pis_cofins_frame_aberto():
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

                self.aliq_pis.set("0.65%")
                aliqpis = criarLabelEntry(self.framePisCofins, "Alíq. PIS (%)", 0.3, 0.18, 0.15, self.aliq_pis)
                aliqpis.configure(state="disabled")

                criarLabelEntry(self.framePisCofins, "BC PIS", 0.5, 0.18, 0.15, self.bc_pis)
                criarLabelEntry(self.framePisCofins, "Vr. PIS", 0.7, 0.18, 0.15, self.vr_pis)
                criaSimouNaoLateral(self.framePisCofins, "Modalidade PIS", "Percentual", "Valor/Qtd", 0.05, 0.15, passe)

                
                
                COFINS = ctk.CTkLabel(self.framePisCofins,  text="COFINS-----------------------------------------------------------------------------", font=("TkDefaultFont", 11))
                COFINS.place(relx=0.02, rely=0.54, relheight=0.015)

                self.aliq_cofins.set("3%")
                aliqcofi = criarLabelEntry(self.framePisCofins, "Alíq. COFINS (%)", 0.3, 0.60, 0.15, self.aliq_cofins)
                aliqcofi.configure(state="disabled")

                criarLabelEntry(self.framePisCofins, "BC COFINS", 0.5, 0.60, 0.15, self.bc_cofins)
                criarLabelEntry(self.framePisCofins, "Vr. COFINS", 0.7, 0.60, 0.15, self.vr_cofins)
                criaSimouNaoLateral(self.framePisCofins, "Modalidade COFINS", "Percentual", "Valor/Qtd", 0.05, 0.58, passe)

                

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
                self.framePisCofins = None

        posGera=-0.03

        criarLabelEntry(frame, "Produto:",                   0.05, 0.05+posGera, 0.25, produto)
        criarLabelEntry(frame, "Código:",                    0.31, 0.05+posGera, 0.15, self.codigoEntry)
        criarLabelEntry(frame, "NCM:",                       0.47, 0.05+posGera, 0.10, self.NCMEntry)
        if "ncm" in linha and linha["ncm"]:
            self.NCMEntry.set(linha["ncm"])
        criarLabelEntry(frame, "CSET:",                      0.58, 0.05+posGera, 0.10, self.CSETEntry)
        criarLabelEntry(frame, "QTD:",                       0.69, 0.05+posGera, 0.05, self.quantidadeEntry)
        criarLabelEntry(frame, "Beneficio Fisc:",            0.75, 0.05+posGera, 0.15, self.beneficioEntry)
        self.cst_a = criarLabelComboBox(frame, "CST A",      0.05, 0.12+posGera, 0.85, opcoes_CST_A)

        self.csosn = criarLabelComboBox(frame, "CSOSN",      0.05, 0.195+posGera, 0.5, opcoes_csosn)
        criarLabelEntry(frame, "Alíq. Cálc. Créd. (%)",      0.59, 0.19+posGera, 0.13, self.aliquEntry)
        criarLabelEntry(frame, "Vr. Cred. ICMS",             0.77, 0.19+posGera, 0.13, self.credICMSEntry)
        self.cst_b = criarLabelComboBox(frame, "CST B",      0.05, 0.27+posGera, 0.85, opcoes_CST_B)
        if "cst_b_produto" in linha and linha["cst_b_produto"]:
            self.cst_b.set(linha["cst_b_produto"])

        self.mod_bc_icms = criarLabelLateralComboBox(frame, "Mod. BC ICMS",     0.11, 0.37+posGera, 0.09, opcoes_MOD_ICMS)
        self.bc_icms.set(linha["subtotal"].get())
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
            dados_salvos = self.dadosProdutos[produto.get()]

            # Já existentes
            self.codigoEntry.set(dados_salvos.get("codigo", ""))
            self.NCMEntry.set(dados_salvos.get("ncm", ""))
            self.CSETEntry.set(dados_salvos.get("cset", ""))
            self.quantidadeEntry.set(dados_salvos.get("quantidade", ""))
            self.beneficioEntry.set(dados_salvos.get("beneficio", ""))
            self.aliquEntry.set(dados_salvos.get("aliqICMS", ""))
            self.credICMSEntry.set(dados_salvos.get("credICMS", ""))
            self.aliq_icms.set(dados_salvos.get("aliq_icms", ""))
            self.vr_icms.set(dados_salvos.get("vr_icms", ""))
            self.csosn.set(dados_salvos.get("csosn", ""))
            self.cst_a.set(dados_salvos.get("cst_a", ""))
            self.cst_b.set(dados_salvos.get("cst_b", ""))
            self.red_bc_icms.set(dados_salvos.get("red_bc_icms", ""))
            self.mod_bc_icms_st.set(dados_salvos.get("mod_bc_icms_st", ""))
            self.mod_bc_icms.set(dados_salvos.get("mod_bc_icms", ""))
            self.mva_icms_st.set(dados_salvos.get("mva_icms_st", ""))
            self.red_bc_icms_st.set(dados_salvos.get("red_bc_icms_st", ""))
            self.vr_bc_icms.insert(0, dados_salvos.get("vr_bc_icms", ""))
            self.vr_bc_icms_st_ret.set(dados_salvos.get("vr_bc_icms_st_ret", ""))
            self.vr_icms_st.set(dados_salvos.get("vr_icms_st", ""))
            self.vr_icms_st_ret.set(dados_salvos.get("vr_icms_st_ret", ""))
            self.vr_icms_st_dest.set(dados_salvos.get("vr_icms_st_dest", ""))
            self.aliq_icms_cfop.set(dados_salvos.get("aliq_icms_cfop", ""))
            self.bc_icms.set(dados_salvos.get("bc_icms", 0.00))
            self.bc_icms_st.set(dados_salvos.get("bc_icms_st", ""))
            self.bc_icms_st_dest.set(dados_salvos.get("bc_icms_st_dest", ""))
            self.vr_icms_subst.set(dados_salvos.get("vr_icms_subst", ""))
            self.aliq_icms_st.set(dados_salvos.get("aliq_icms_st", ""))
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
            self.aliq_cofins.set(dados_salvos.get("aliq_cofins",""))
            self.bc_cofins.set(dados_salvos.get("bc_cofins",""))
            self.vr_cofins.set(dados_salvos.get("vr_cofins",""))
            


        base_calculo_original = None
        base_reduzida_anterior = None

        def calculaValores():

            # calcula a base de calculo
            # redução base de calculo
            # aliquota
            # e valor
            # tudo do icms

            try:
                base_informada = float(self.bc_icms.get())
                reducao_percentual = float(self.red_bc_icms.get())
            except:
                raise ValueError("Os valores não devem estar em branco")

            nonlocal base_calculo_original, base_reduzida_anterior

            # Garante que a base usada no cálculo sempre seja a original informada,
            # evitando reduções cumulativas a cada clique em "Calcular".
            if base_calculo_original is None:
                base_calculo_original = base_informada
            elif base_informada not in (base_calculo_original, base_reduzida_anterior):
                base_calculo_original = base_informada

            base_calculo = base_calculo_original
            auxiliar = base_calculo * reducao_percentual / 100
            base_reduzida = base_calculo - auxiliar
            base_reduzida_anterior = base_reduzida
            self.bc_icms.set(f"{base_reduzida:.2f}")

            valorICMS = base_reduzida * (float(self.aliq_icms.get()) / 100.0)
            self.vr_icms.set(f"{valorICMS:.2f}")

            
            # --- PIS 
            aliq_pis = 0.00065
            valorBCPis = base_calculo - valorICMS
            self.bc_pis.set(f"{valorBCPis:.2f}")
            vr_pis = (valorBCPis * aliq_pis * 10)
            self.vr_pis.set(f"{vr_pis:.2f}")

            # --- COFINS (mesma lógica do PIS) ---
            aliq_cofins = 0.03
            valorBCCofins = base_calculo - valorICMS
            self.bc_cofins.set(f"{valorBCCofins:.2f}")
            vr_cofins = (valorBCCofins * aliq_cofins)
            self.vr_cofins.set(f"{vr_cofins:.2f}")



        def salvar_dados_e_sair():
            if not hasattr(self, "dadosProdutos"):
                self.dadosProdutos = {}

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
                "aliq_cofins": self.aliq_cofins.get(),
                "bc_cofins": self.bc_cofins.get(),
                "vr_cofins": self.vr_cofins.get(),
                "aliq_cofins_st": self.aliq_cofins_st.get(),
            }
            linha["ncm"] = self.NCMEntry.get()
            linha["cst_b_produto"] = self.cst_b.get()
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

            # 1) Total bruto da linha
            baseSemDesc = (valorUnit * quantida if quantida > 0 else valorUnit) + acrescim
            novo_subtotal = baseSemDesc

            # 2) Desconto em R$
            if descReal > 0:
                entry_descPorc.delete(0, "end"); entry_descPorc.insert(0, "0")
                novo_subtotal = max(baseSemDesc - descReal, 0.0)

            # 3) Desconto em %
            elif descPorc > 0:
                entry_descReal.delete(0, "end"); entry_descReal.insert(0, "0")
                novo_subtotal = max(baseSemDesc * (1.0 - descPorc), 0.0)

            entry_subtotal.delete(0, "end")
            entry_subtotal.insert(0, f"{novo_subtotal:.2f}")
            total += novo_subtotal

        self.valorSubtotalFaturamento = total

    # Cabeçalhos
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
    campos_obrigatorios = ("produto", "preco", "quantidade")

    def ultima_linha_preenchida():
        if not self.linhas:
            return True

        linha = self.linhas[-1]
        for campo in campos_obrigatorios:
            widget = linha.get(campo)
            if hasattr(widget, "get") and widget.get().strip() == "":
                return False
        return True

    self.botaoAdicionarItem = criaBotaoPequeno(
        frameParaItensNoFrame,
        "Adicionar item",
        0.7,
        self.posicaoyBotao,
        0.07,
        lambda: (
            messagebox.showerror(
                "Campos vazios",
                "Preencha todos os campos da última linha antes de adicionar um novo item",
            )
            if not ultima_linha_preenchida()
            else adicionarItem(self)
        )
    )
    
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
        self.yNovo = self.posicaoy + 0.02

    # cria primeira linha em branco
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

    
    # ======= NOVO: Pré-carregar itens da NF-e (com CFOP e dados para tributação) =======
    if dadosNota:
        # Garante que existe um dicionário para dados fiscais por produto
        if not hasattr(self, "dadosProdutos") or not isinstance(getattr(self, "dadosProdutos"), dict):
            self.dadosProdutos = {}

        # Extrai a lista de itens da NF-e lida
        try:
            itens = dadosNota["NFe"]["infNFe"]["det"]
            if not isinstance(itens, list):
                itens = [itens]
        except Exception:
            itens = []

        def _get_text(d, *keys, default=""):
            try:
                cur = d
                for k in keys:
                    cur = cur[k]
                if isinstance(cur, dict) and "#text" in cur:  # alguns nós vêm como {'#text': 'valor'}
                    return str(cur.get("#text", default))
                return str(cur)
            except Exception:
                return default

        # Primeira linha já existe; demais itens criam novas linhas
        for idx, item in enumerate(itens):
            if idx == 0 and self.linhas:
                linha_widgets = self.linhas[-1]
            else:
                adicionarItem(self)
                linha_widgets = self.linhas[-1]

            prod = item.get("prod", {}) if isinstance(item, dict) else {}
            xProd = _get_text(item, "prod", "xProd", default="")
            cProd = _get_text(item, "prod", "cProd", default="")
            qCom  = _get_text(item, "prod", "qCom",  default="0")
            uCom  = _get_text(item, "prod", "uCom",  default="")
            vUn   = _get_text(item, "prod", "vUnCom", default="0.00")
            vProd = _get_text(item, "prod", "vProd", default="0.00")
            ncm   = _get_text(item, "prod", "NCM",   default="")
            cfop_item = _get_text(item, "prod", "CFOP", default="")

            # Normaliza valores numéricos
            try:
                vUn_fmt = f"{float(str(vUn).replace(',', '.')):.2f}"
            except Exception:
                vUn_fmt = "0.00"
            try:
                vProd_fmt = f"{float(str(vProd).replace(',', '.')):.2f}"
            except Exception:
                vProd_fmt = vUn_fmt

            # Preenche os campos visíveis da linha
            linha_widgets["produto"].delete(0, "end")
            linha_widgets["produto"].insert(0, xProd)

            linha_widgets["preco"].delete(0, "end")
            linha_widgets["preco"].insert(0, vUn_fmt)

            linha_widgets["quantidade"].delete(0, "end")
            linha_widgets["quantidade"].insert(0, str(qCom))

            linha_widgets["estoque"].delete(0, "end")
            linha_widgets["estoque"].insert(0, "0")
            linha_widgets["estoque"].configure(state="disabled")

            linha_widgets["desc_real"].delete(0, "end")
            linha_widgets["desc_real"].insert(0, "0")

            linha_widgets["desc_porcentagem"].delete(0, "end")
            linha_widgets["desc_porcentagem"].insert(0, "0")

            linha_widgets["acrescimo"].delete(0, "end")
            linha_widgets["acrescimo"].insert(0, "0")

            linha_widgets["subtotal"].delete(0, "end")
            linha_widgets["subtotal"].insert(0, vProd_fmt or vUn_fmt)
            linha_widgets["subtotal_original"] = float(vProd_fmt or vUn_fmt)

            # Atualiza CFOP (campo compartilha a mesma StringVar em todas as linhas)
            try:
                if cfop_item:
                    variavelCfop.set(cfop_item)
            except Exception:
                pass

            # Salva dados essenciais para a tela de tributação (modal)
            chave = xProd or cProd or f"ITEM_{idx+1}"
            self.dadosProdutos[chave] = {
                "codigo": cProd,
                "ncm": ncm,
                "quantidade": str(qCom),
                "uCom": uCom,
                "cfop": cfop_item,
            }
    
    criaBotao(
        frameTelaNotaProduto,
        "Próximo - Tela Transporte",
        0.25,
        0.94,
        0.15,
        lambda: (
            montarValoresDosItens(frameTelaNotaProduto),
            telaTransporteNotaSaida(self, EhNotaDoConsumidor, nota_importada),
        ),
    ).place(anchor="nw")
    criaBotao(frameTelaNotaProduto, "Voltar", 0.05, 0.94, 0.15, lambda: frameTelaNotaProduto.destroy()).place(anchor="nw")

    # aplicar_maiusculo_em_todos_entries(self)
    # Recalcula o total geral após o pré-carregamento
    try:
        atualizarTotalGeral()
    except Exception:
        pass
# ======= FIM Pré-carregar itens da NF-e =======
