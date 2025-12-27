import customtkinter as ctk
from tkinter import messagebox
from componentes import criaFrameJanela, criaBotao, criaTextArea, criarLabelEntry
from funcoesTerceiras import criarNFe, criarNFCe
from consultas.insert import Insere
from telas.telaObservacoes import montar_parametros_nota_saida


def acessar(dados, *caminho, default=""):
    atual = dados
    for chave in caminho:
        if isinstance(atual, dict) and chave in atual:
            atual = atual[chave]
        else:
            return default
    if isinstance(atual, dict) and "#text" in atual:
        atual = atual["#text"]
    if atual in (None, ""):
        return default
    return str(atual)


def telaObservacoesNotaSaida(self, EhNotaDoConsumidor):
    self.frameTelaObservacoes = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    numeroPedidoVinculado = ctk.StringVar()
    self.numeroPedidoVinculadoVar = numeroPedidoVinculado

    dados_nfe = getattr(self, "dadosNota", None)
    nota_entrada_importada = bool(getattr(self, "importouNotaEntrada", False) and dados_nfe)
    essa_eh_nota_de_entrada = bool(getattr(self, "essaEhNotaDeEntrada", False))
    texto_contribuinte = acessar(dados_nfe, "NFe", "infNFe", "infAdic", "infCpl", default=" ")
    texto_fisco = acessar(dados_nfe, "NFe", "infNFe", "infAdic", "infAdFisco", default=" ")

    area1 = criaTextArea(
        self.frameTelaObservacoes,
        0.5,
        0.15,
        0.4,
        "INFORMAÇÕES DO INTERESSE DO CONTRIBUINTE",
        texto_contribuinte,
    )
    area1.place(relheight=0.3)
    area2 = criaTextArea(
        self.frameTelaObservacoes,
        0.05,
        0.15,
        0.4,
        "INFORMAÇÕES DO INTERESSE DO FISCO",
        texto_fisco,
    )
    area2.place(relheight=0.3)

    self.variavelObservacoes = ctk.StringVar()
    self.variavelObservacoes.set(0)

    self.observacaoContribuinteTexto = texto_contribuinte.strip()
    self.observacaoFiscoTexto = texto_fisco.strip()
    self.observacoesNotaImportada = {
        "contribuinte": self.observacaoContribuinteTexto,
        "fisco": self.observacaoFiscoTexto,
    }

    def atualizar_observacoes():
        self.observacaoContribuinteTexto = area1.get("1.0", "end").strip()
        self.observacaoFiscoTexto = area2.get("1.0", "end").strip()
        self.numeroPedidoVinculadoValor = numeroPedidoVinculado.get().strip()
        self.observacoesNotaImportada = {
            "contribuinte": self.observacaoContribuinteTexto,
            "fisco": self.observacaoFiscoTexto,
        }

    def salvar_e_gerar(modulo):
        atualizar_observacoes()
        modulo.gerarNFe(self)
        if getattr(self, "frameTelaObservacoes", None):
            self.frameTelaObservacoes.destroy()
        if getattr(self, "frameTelaTotais", None):
            self.frameTelaTotais.destroy()
        if getattr(self, "frametelaTransporte", None):
            self.frametelaTransporte.destroy()
        if getattr(self, "frameTelaNotaSaida", None):
            self.frameTelaNotaSaida.destroy()
        if getattr(self, "frameTelaNotaFiscalEntrada", None):
            self.frameTelaNotaFiscalEntrada.destroy()
        if getattr(self, "frameTelaGerarFaturamento", None):
            self.frameTelaGerarFaturamento.destroy()
        if getattr(self, "frameValorTotais", None):
            self.frameValorTotais.destroy()
        if getattr(self, "frameTelaNotaProduto", None):
            self.frameTelaNotaProduto.destroy()
        if getattr(self, "frameTelaFiscal", None):
            self.frameTelaFiscal.destroy()
        if getattr(self, "frameEscolherNotaFiscal", None):
            self.frameEscolherNotaFiscal.destroy()

        from telas.telaFiscal import telaFiscal

        telaFiscal(self)

    def salvar_nota_importada():
        atualizar_observacoes()
        if not dados_nfe:
            messagebox.showerror("Erro", "Não há dados da nota importada para salvar.")
            return
        try:
            cfop_override = getattr(self, "cfop_produtos_var", None) or getattr(self, "variavelCFOP", None)
            parametros = montar_parametros_nota_saida(dados_nfe, cfop_override)
            tpNF = parametros[9] if len(parametros) > 9 else None
            eh_entrada = essa_eh_nota_de_entrada or str(tpNF) == "0"
            data_saida = parametros[13] or parametros[12]

            if eh_entrada:
                print("ta chamando a da entrada nas observações saida")
                Insere.inserir_nota_fiscal(
                    parametros[4],  # chave_nfe
                    parametros[3],  # numero_nfe
                    parametros[2],  # serie_nfe
                    parametros[12],  # data_emissao
                    data_saida,  # data_saida
                    parametros[14],  # emitente_cnpj
                    parametros[15],  # emitente_nome
                    parametros[17],  # destinatario_cnpj
                    parametros[18],  # destinatario_nome
                    parametros[20],  # valor_total
                    parametros[21],  # valor_produtos
                    parametros[26],  # valor_bc_icms
                    parametros[27],  # valor_icms
                    parametros[28],  # valor_icms_desonerado
                    parametros[30],  # valor_bc_icms_st
                    parametros[31],  # valor_icms_st
                    parametros[32],  # valor_ipi
                    parametros[33],  # valor_pis
                    parametros[34],  # valor_cofins
                    parametros[35],  # valor_bc_irrf
                    parametros[36],  # transportadora_cnpj
                    parametros[37],  # transportadora_nome
                    parametros[56],  # itens_json
                    parametros[55],  # data_vencimento
                )
            else:
                print("ta chamando a da saída")
                Insere.inserir_nota_fiscal_saida(
                    *parametros,
                    "Entrada",
                )
            if getattr(self, "frameTelaObservacoes", None):
                self.frameTelaObservacoes.destroy()
            if getattr(self, "frameTelaTotais", None):
                self.frameTelaTotais.destroy()
            if getattr(self, "frametelaTransporte", None):
                self.frametelaTransporte.destroy()
            if getattr(self, "frameTelaNotaSaida", None):
                self.frameTelaNotaSaida.destroy()
            if getattr(self, "frameTelaNotaFiscalEntrada", None):
                self.frameTelaNotaFiscalEntrada.destroy()
            if getattr(self, "frameTelaGerarFaturamento", None):
                self.frameTelaGerarFaturamento.destroy()
            if getattr(self, "frameValorTotais", None):
                self.frameValorTotais.destroy()
            if getattr(self, "frameTelaNotaProduto", None):
                self.frameTelaNotaProduto.destroy()
            if getattr(self, "frameTelaFiscal", None):
                self.frameTelaFiscal.destroy()
            if getattr(self, "frameEscolherNotaFiscal", None):
                self.frameEscolherNotaFiscal.destroy()

            from telas.telaFiscal import telaFiscal

            telaFiscal(self)
        except Exception as exc:
            messagebox.showerror("Erro", f"Falha ao salvar nota importada: {exc}")

    if nota_entrada_importada:
        criaBotao(
            self.frameTelaObservacoes,
            "Salvar nota",
            0.25,
            0.94,
            0.15,
            salvar_nota_importada,
        ).place(anchor="nw")
    else:
        if EhNotaDoConsumidor:
            criaBotao(
                self.frameTelaObservacoes,
                "Salvar e gerar nfc-e",
                0.40,
                0.94,
                0.15,
                lambda: salvar_e_gerar(criarNFCe),
            ).place(anchor="nw")
        else:
            criaBotao(
                self.frameTelaObservacoes,
                "Salvar e gerar nf-e",
                0.25,
                0.94,
                0.15,
                lambda: salvar_e_gerar(criarNFe),
            ).place(anchor="nw")
            criarLabelEntry(self.frameTelaObservacoes, "Número pedido vinculado", 0.05, 0.58, 0.15, numeroPedidoVinculado)


    # criaBotao(self.frameTelaObservacoes, "consultar", 0.55, 0.94, 0.15, lambda: criarNFe.consultar_ultimo_recibo(self)).place(anchor="nw")
    criaBotao(self.frameTelaObservacoes, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaObservacoes.destroy()).place(anchor="nw")


# COLOCAR O CAMINHO CORRETO DOS CERTIFICADOS