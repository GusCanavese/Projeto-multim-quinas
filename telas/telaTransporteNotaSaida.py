import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from componentes import criaBotaoPequeno, criaEntry, criaFrameJanela, criaLabel, criarLabelEntry, criarLabelComboBox, criarLabelLateralEntry, criaBotao
from telas.telaCadastroTransportadoras import telaCadastroTransportadoras
from telas.telaTotaisNotaSaida import telaTotaisNotaSaida

def telaTransporteNotaSaida(self, EhNotaDoConsumidor, ehNotaEntrada):
    self.frametelaTransporte = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    self.dadosTransporteImportado = {
        "transportador": {},
        "volumes": [],
        "modalidadeFrete": "",
    }

    def buscaTransportador(event=None): 
        nomeDoTransportador = self.nomeTransportador.get()
        cnpjTransportador   = self.documentoTransportador.get()
        dadosTransportador  = Buscas.buscaTransportador(nomeDoTransportador, cnpjTransportador)

        if hasattr(self, 'resultadoLabels'):
            for label in self.resultadoLabels: 
                label.destroy()
        self.resultadoLabels = []
            
        yNovo = 0.16
        if len(dadosTransportador) > 0:
            for i, row in enumerate(dadosTransportador):
                if i >= 5:
                    break
                label = ctk.CTkButton(self.frametelaTransporte,  text=row[0], corner_radius=0, fg_color=self.cor, font=("Century Gothic bold", 15), command = lambda  nome=row[0], documento=row[1]: selecionaCliente(nome, documento))
                label.place(relx=0.35, rely=yNovo, relwidth=0.3)
                self.resultadoLabels.append(label)  
                yNovo += 0.0399
        else:
            print("entrou")
            label = ctk.CTkButton(self.frametelaTransporte,  text="+ Cadastrar Transportador", corner_radius=0, fg_color=self.cor, font=("Century Gothic bold", 15), command = lambda: telaCadastroTransportadoras(self))
            label.place(relx=0.35, rely=yNovo, relwidth=0.3)
            self.resultadoLabels.append(label)  
            yNovo += 0.0399
    
    def selecionaCliente(nome, documento):

        # --------------------------------------------------

        self.nomeDestinatario = nome
        self.documentoDestinatario = documento

        self.variavelRazaoSocialRemetente.set(nome)
        self.variavelCNPJRazaoSocialRemetente.set(documento)

        for label in self.resultadoLabels: 
            label.destroy()





    listaLabels = ["Quantidade", "Espécie",	"Marca", "Numeração", "Peso Bruto",	"Peso Líquido"]
    opcoesTransporte = [
        "Contratação do Frete por conta do Remetente (CIF)",
        "Contratação do Frete por conta do Destinatário (FOB)",
        "Contratação do Frete por conta de Terceiros",
        "Transporte Próprio por conta do Remetente",
        "Transporte Próprio por conta do Destinatário",
        "Sem Ocorrência de Transporte"
    ]


    
    
    # variáveis
    variavelTransportador = ctk.StringVar()
    variavelCNPJTransportador = ctk.StringVar()
    self.variavelCFOPTransporte = ctk.StringVar()
    self.variavelBCRetencaoICMS = ctk.StringVar()
    self.variavelValorICMSRetido = ctk.StringVar()
    self.variavelValorServicoTransp = ctk.StringVar()
    self.variavelAliquotaRetICMS = ctk.StringVar()
    self.variavelMunicipioGerador = ctk.StringVar()


    criarLabelComboBox(self.frametelaTransporte, "Modalidade do frete", 0.05, 0.1, 0.25, opcoesTransporte)
    self.nomeTransportador = criarLabelEntry(self.frametelaTransporte, "Transportador", 0.35, 0.1, 0.3, variavelTransportador)
    self.documentoTransportador = criarLabelEntry(self.frametelaTransporte, "CPF/CNPJ", 0.7, 0.1, 0.2, variavelCNPJTransportador)
    self.nomeTransportador.bind("<KeyRelease>",buscaTransportador)
    self.nomeTransportador.bind("<Button-1>",buscaTransportador)
    self.documentoTransportador.bind("<Button-1>",buscaTransportador)
    self.documentoTransportador.bind("<KeyRelease>",buscaTransportador)

    # Bloco de tributação organizado em colunas para evitar sobreposição com os volumes
    frame_tributacao = ctk.CTkFrame(self.frametelaTransporte, fg_color="transparent")
    frame_tributacao.place(relx=0.08, rely=0.52, relwidth=0.88, relheight=0.2)

    colunas = [0.09, 0.41, 0.73]
    largura_coluna = 0.18

    criarLabelLateralEntry(frame_tributacao, "CFOP", colunas[0], 0.20, largura_coluna, self.variavelCFOPTransporte)
    criarLabelLateralEntry(frame_tributacao, "BC Retenção ICMS", colunas[1], 0.20, largura_coluna, self.variavelBCRetencaoICMS)
    criarLabelLateralEntry(frame_tributacao, "Valor ICMS Retido", colunas[2], 0.20, largura_coluna, self.variavelValorICMSRetido)

    criarLabelLateralEntry(frame_tributacao, "Valor do Serviço", colunas[0], 0.68, largura_coluna, self.variavelValorServicoTransp)
    criarLabelLateralEntry(frame_tributacao, "Aliquota Ret. ICMS", colunas[1], 0.68, largura_coluna, self.variavelAliquotaRetICMS)
    criarLabelLateralEntry(frame_tributacao, "Município Gerador", colunas[2], 0.68, largura_coluna, self.variavelMunicipioGerador)

    self.posicaoy = 0.3
    self.posicaox = 0.05
    self.posicaoyBotaoTransp = 0.35
    self.posicaoyBotaoRemoverTransp = 0.284
    self.valorSubtotal = 0
    self.linhasTransporte = []

    self.botaoRemoverItem = ctk.CTkButton(self.frametelaTransporte, text="X", width=20, corner_radius=0, fg_color="red", command=lambda: removerItem(self))
    self.botaoRemoverItem.place(relx=0.80, rely=self.posicaoyBotao-0.04)

    for i, coluna in enumerate(listaLabels):
        criaLabel(self.frametelaTransporte, coluna, self.posicaox, self.posicaoy, 0.145, self.cor)
        self.posicaox +=0.1453
    self.posicaox = 0.05
    self.botaoAdicionarItemTransp = criaBotaoPequeno(self.frametelaTransporte, "Adicionar item", 0.7, self.posicaoyBotaoTransp, 0.07, lambda: (adicionarItem(self)))

    def adicionarItem(self):
        print(f"removi, tamanho: {self.posicaoyBotaoTransp}")
        self.posicaoy += 0.04
        self.posicaoyBotaoTransp += 0.04
        self.posicaoyBotaoRemoverTransp += 0.04

        self.botaoRemoverItem.place(relx=0.93, rely=self.posicaoyBotaoRemoverTransp)
        self.botaoAdicionarItemTransp.place(relx=0.883, rely=self.posicaoyBotaoTransp)
        
        linha_widgets = {}
        
        for i, coluna in enumerate(listaLabels):
            entrada = criaEntry(self.frametelaTransporte, self.posicaox, self.posicaoy, 0.145, None)
            campo = ["Quantidade", "Espécie", "Marca", "Numeração", "Peso Bruto", "Peso Líquido"][i - 2]
            linha_widgets[campo] = entrada
            self.posicaox += 0.1453

        self.posicaox = 0.05
        self.linhasTransporte.append(linha_widgets)

    def removerItem(self):
        print(f"removi, tamanho: {self.posicaoyBotaoTransp}")
        if len(self.linhasTransporte) > 1:
            ultima_linha = self.linhasTransporte.pop()

            for widget in ultima_linha.values():
                if hasattr(widget, "destroy"):
                    widget.destroy()

            self.posicaoy -= 0.04
            self.posicaoyBotaoTransp -= 0.04
            self.posicaoyBotaoRemoverTransp -= 0.04
            
            self.botaoAdicionarItemTransp.place(relx=0.883, rely=self.posicaoyBotaoTransp)
            self.botaoRemoverItem.place(relx=0.93, rely=self.posicaoyBotaoRemoverTransp)

        if len(self.linhasTransporte) == 1:
            self.botaoRemoverItem.place_forget()


    
    adicionarItem(self)





# ===== Pré-preencher TRANSPORTE a partir da NF-e (somente se ehNotaEntrada) =====
    if ehNotaEntrada:
        print("entrou")
        dados = None
        if hasattr(self, "dadosNota") and self.dadosNota:
            dados = self.dadosNota
        elif hasattr(self, "dadosNFeEntrada") and self.dadosNFeEntrada:
            dados = self.dadosNFeEntrada

        if isinstance(dados, dict):
            # ----------------- transporta: nome / documento -----------------
            try:
                transp = dados["NFe"]["infNFe"]["transp"]

                ret_transp = transp.get("retTransp", {}) if isinstance(transp, dict) else {}

                def _valor_ret(chave):
                    if not isinstance(ret_transp, dict):
                        return ""
                    val = ret_transp.get(chave, "")
                    if isinstance(val, dict) and "#text" in val:
                        val = val.get("#text", "")
                    return str(val).strip()

                # Nome do transportador
                nomeTransp = ""
                try:
                    nomeTransp = transp["transporta"]["xNome"]
                    if isinstance(nomeTransp, dict) and "#text" in nomeTransp:
                        nomeTransp = nomeTransp["#text"]
                except Exception:
                    nomeTransp = ""
                try:
                    atual = (self.nomeTransportador.get() or "").strip()
                    if atual == "" and (str(nomeTransp).strip() != ""):
                        self.nomeTransportador.delete(0, "end")
                        self.nomeTransportador.insert(0, str(nomeTransp))
                except Exception:
                    pass

                # Documento (CNPJ/CPF)
                docTransp = ""
                try:
                    docTransp = transp["transporta"].get("CNPJ", "")
                    if not docTransp:
                        docTransp = transp["transporta"].get("CPF", "")
                    if isinstance(docTransp, dict) and "#text" in docTransp:
                        docTransp = docTransp["#text"]
                except Exception:
                    docTransp = ""
                try:
                    atual = (self.documentoTransportador.get() or "").strip()
                    if atual == "" and (str(docTransp).strip() != ""):
                        self.documentoTransportador.delete(0, "end")
                        self.documentoTransportador.insert(0, str(docTransp))
                except Exception:
                    pass

                self.dadosTransporteImportado["transportador"] = {
                    "nome": str(nomeTransp).strip(),
                    "documento": str(docTransp).strip(),
                }

                v_serv = _valor_ret("vServ")
                v_bc_ret = _valor_ret("vBCRet")
                p_icms_ret = _valor_ret("pICMSRet")
                v_icms_ret = _valor_ret("vICMSRet")
                cfop_ret = _valor_ret("CFOP")
                cmunfg_ret = _valor_ret("cMunFG")

                self.variavelValorServicoTransp.set(v_serv)
                self.variavelBCRetencaoICMS.set(v_bc_ret)
                self.variavelAliquotaRetICMS.set(p_icms_ret)
                self.variavelValorICMSRetido.set(v_icms_ret)
                self.variavelCFOPTransporte.set(cfop_ret)
                self.variavelMunicipioGerador.set(cmunfg_ret)

                self.dadosTransporteImportado["retencaoICMS"] = {
                    "vServ": v_serv,
                    "vBCRet": v_bc_ret,
                    "pICMSRet": p_icms_ret,
                    "vICMSRet": v_icms_ret,
                    "CFOP": cfop_ret,
                    "cMunFG": cmunfg_ret,
                }

                # ----------------- volumes: qVol, esp, marca, nVol, pesoB, pesoL -----------------
                vols = None
                try:
                    vols = transp["vol"]
                except Exception:
                    vols = None

                if vols:
                    if isinstance(vols, dict):
                        vols = [vols]

                    for i, vol in enumerate(vols):
                        # garante linha disponível
                        if i == 0:
                            linha = self.linhasTransporte[0] if len(self.linhasTransporte) > 0 else None
                        else:
                            adicionarItem(self)
                            linha = self.linhasTransporte[-1] if len(self.linhasTransporte) > 0 else None
                        if not isinstance(linha, dict):
                            continue

                        volume_info = {}

                        # Quantidade -> qVol
                        val = ""
                        try:
                            val = vol.get("qVol", "")
                            if isinstance(val, dict) and "#text" in val:
                                val = val["#text"]
                        except Exception:
                            val = ""
                        volume_info["quantidade"] = str(val).strip()
                        if "Quantidade" in linha and str(val).strip() != "":
                            try:
                                cur = (linha["Quantidade"].get() or "").strip() if hasattr(linha["Quantidade"], "get") else ""
                            except Exception:
                                cur = ""
                            if cur in ("", "0", "0.0", "0.00"):
                                try:
                                    linha["Quantidade"].delete(0, "end")
                                    linha["Quantidade"].insert(0, str(val))
                                except Exception:
                                    pass

                        # Espécie -> esp
                        val = ""
                        try:
                            val = vol.get("esp", "")
                            if isinstance(val, dict) and "#text" in val:
                                val = val["#text"]
                        except Exception:
                            val = ""
                        volume_info["especie"] = str(val).strip()
                        if "Espécie" in linha and str(val).strip() != "":
                            try:
                                cur = (linha["Espécie"].get() or "").strip() if hasattr(linha["Espécie"], "get") else ""
                            except Exception:
                                cur = ""
                            if cur == "":
                                try:
                                    linha["Espécie"].delete(0, "end")
                                    linha["Espécie"].insert(0, str(val))
                                except Exception:
                                    pass

                        # Marca -> marca
                        val = ""
                        try:
                            val = vol.get("marca", "")
                            if isinstance(val, dict) and "#text" in val:
                                val = val["#text"]
                        except Exception:
                            val = ""
                        volume_info["marca"] = str(val).strip()
                        if "Marca" in linha and str(val).strip() != "":
                            try:
                                cur = (linha["Marca"].get() or "").strip() if hasattr(linha["Marca"], "get") else ""
                            except Exception:
                                cur = ""
                            if cur == "":
                                try:
                                    linha["Marca"].delete(0, "end")
                                    linha["Marca"].insert(0, str(val))
                                except Exception:
                                    pass

                        # Numeração -> nVol
                        val = ""
                        try:
                            val = vol.get("nVol", "")
                            if isinstance(val, dict) and "#text" in val:
                                val = val["#text"]
                        except Exception:
                            val = ""
                        volume_info["numeracao"] = str(val).strip()
                        if "Numeração" in linha and str(val).strip() != "":
                            try:
                                cur = (linha["Numeração"].get() or "").strip() if hasattr(linha["Numeração"], "get") else ""
                            except Exception:
                                cur = ""
                            if cur == "":
                                try:
                                    linha["Numeração"].delete(0, "end")
                                    linha["Numeração"].insert(0, str(val))
                                except Exception:
                                    pass

                        # Peso Bruto -> pesoB
                        val = ""
                        try:
                            val = vol.get("pesoB", "")
                            if isinstance(val, dict) and "#text" in val:
                                val = val["#text"]
                        except Exception:
                            val = ""
                        volume_info["peso_bruto"] = str(val).strip()
                        if "Peso Bruto" in linha and str(val).strip() != "":
                            try:
                                cur = (linha["Peso Bruto"].get() or "").strip() if hasattr(linha["Peso Bruto"], "get") else ""
                            except Exception:
                                cur = ""
                            if cur in ("", "0", "0.0", "0.00"):
                                try:
                                    linha["Peso Bruto"].delete(0, "end")
                                    linha["Peso Bruto"].insert(0, str(val))
                                except Exception:
                                    pass

                        # Peso Líquido -> pesoL
                        val = ""
                        try:
                            val = vol.get("pesoL", "")
                            if isinstance(val, dict) and "#text" in val:
                                val = val["#text"]
                        except Exception:
                            val = ""
                        volume_info["peso_liquido"] = str(val).strip()
                        if "Peso Líquido" in linha and str(val).strip() != "":
                            try:
                                cur = (linha["Peso Líquido"].get() or "").strip() if hasattr(linha["Peso Líquido"], "get") else ""
                            except Exception:
                                cur = ""
                            if cur in ("", "0", "0.0", "0.00"):
                                try:
                                    linha["Peso Líquido"].delete(0, "end")
                                    linha["Peso Líquido"].insert(0, str(val))
                                except Exception:
                                    pass

                        if volume_info:
                            self.dadosTransporteImportado["volumes"].append(volume_info)

                # opcional: salvar modFrete para uso em outra tela
                try:
                    mf = transp.get("modFrete", "")
                    if isinstance(mf, dict) and "#text" in mf:
                        mf = mf["#text"]
                    self.modFrete = str(mf)
                    self.dadosTransporteImportado["modalidadeFrete"] = self.modFrete
                except Exception:
                    pass

            except Exception:
                pass
    # ===== Fim do pré-preenchimento de transporte =====

    criaBotao(self.frametelaTransporte, "Próximo - Tela Totais", 0.25, 0.94, 0.15, lambda: telaTotaisNotaSaida(self, EhNotaDoConsumidor)).place(anchor="nw")
    criaBotao(self.frametelaTransporte, "Voltar", 0.05, 0.94, 0.15, lambda: self.frametelaTransporte.destroy()).place(anchor="nw")