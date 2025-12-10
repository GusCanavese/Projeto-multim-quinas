import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from telas import telaNotaFiscalEntrada, telaVerDebito
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criarLabelEntry, criaBotao

def telaVercontasApagar(self, d):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    varConfirmado          = ctk.StringVar()
    varVencimento          = ctk.StringVar()
    varDescricao           = ctk.StringVar()
    varTotal               = ctk.StringVar()
    varFormapag            = ctk.StringVar()
    varQtdParcelas         = ctk.StringVar()
    varNumeroNfe           = ctk.StringVar()
    varEmitenteNome        = ctk.StringVar()
    varChaveNfe            = ctk.StringVar()
    varSerieNfe            = ctk.StringVar()
    varDataEmissao         = ctk.StringVar()
    varDataSaida           = ctk.StringVar()
    varEmitenteCnpj        = ctk.StringVar()
    varDestinatarioCnpj    = ctk.StringVar()
    varDestinatarioNome    = ctk.StringVar()
    varValorProdutos       = ctk.StringVar()
    varValorBcIcms         = ctk.StringVar()
    varValorIcms           = ctk.StringVar()
    varValorIcmsDesonerado = ctk.StringVar()
    varValorBcIcmsSt       = ctk.StringVar()
    varValorIcmsSt         = ctk.StringVar()
    varValorIpi            = ctk.StringVar()
    varValorPis            = ctk.StringVar()
    varValorCofins         = ctk.StringVar()
    varValorBcIrrf         = ctk.StringVar()
    varTransportadoraCnpj  = ctk.StringVar()
    varTransportadoraNome  = ctk.StringVar()
    varItens               = ctk.StringVar()
    varDataRegistro        = ctk.StringVar()

    if " pedido" in d[2]:
        varConfirmado.set(d[0])
        varVencimento.set(d[1])
        varDescricao.set(d[2])
        varTotal.set(d[3])
        varFormapag.set(d[4])
        varQtdParcelas.set(d[5])

        
        criarLabelEntry(frame, "Foi confirmado?", 0.05, 0.05, 0.1, varConfirmado)
        criarLabelEntry(frame, "Data vencimento", 0.2, 0.05, 0.1, varVencimento)
        criarLabelEntry(frame, "Descrição", 0.35, 0.05, 0.6, varDescricao)

        
        criarLabelEntry(frame, "Valor total", 0.05, 0.2, 0.267, varTotal)
        criarLabelEntry(frame, "Forma Pagamento", 0.367, 0.2, 0.267, varFormapag)
        criarLabelEntry(frame, "QTD parcelas", 0.684, 0.2, 0.266, varQtdParcelas)

        criaBotao(frame, "Voltar", 0.05, 0.94, 0.15, lambda: frame.destroy()).place(anchor="nw")



    if " nota" in d[2]:
        varConfirmado.set(d[0]),
        varVencimento.set(d[1]),
        varDescricao.set(d[2]),
        varTotal.set(d[3]),
        varNumeroNfe.set(d[4]),
        varEmitenteNome.set(d[5]),
        varChaveNfe.set(d[6]),
        varSerieNfe.set(d[7]),
        varDataEmissao.set(d[8]),
        varDataSaida.set(d[9]),
        varEmitenteCnpj.set(d[10]),
        varDestinatarioCnpj.set(d[11]),
        varDestinatarioNome.set(d[12]),
        varValorProdutos.set(d[13]),
        varValorBcIcms.set(d[14]),
        varValorIcms.set(d[15]),
        varValorIcmsDesonerado.set(d[16]),
        varValorBcIcmsSt.set(d[17]),
        varValorIcmsSt.set(d[18]),
        varValorIpi.set(d[19]),
        varValorPis.set(d[20]),
        varValorCofins.set(d[21]),
        varValorBcIrrf.set(d[22]),
        varTransportadoraCnpj.set(d[23]),
        varTransportadoraNome.set(d[24]),
        varItens.set(d[25]),
        varDataRegistro.set(d[26])


        tabs = ctk.CTkTabview(frame, fg_color="transparent")
        tabs.place(relx=0.5, rely=0.5, relwidth=0.94, relheight=0.84, anchor="center")

        tab_dados = tabs.add("Dados")
        tab_itens = tabs.add("Itens")
        tabs.set("Dados")

        criarLabelEntry(tab_dados, "Confirmado", 0.05, 0.05, 0.2, varConfirmado)
        criarLabelEntry(tab_dados, "Vencimento", 0.27, 0.05, 0.2, varVencimento)
        criarLabelEntry(tab_dados, "Valor total", 0.49, 0.05, 0.2, varTotal)
        criarLabelEntry(tab_dados, "Número NFE", 0.71, 0.05, 0.24, varNumeroNfe)

        criarLabelEntry(tab_dados, "Descrição", 0.05, 0.15, 0.9, varDescricao)

        criarLabelEntry(tab_dados, "Emitente", 0.05, 0.25, 0.42, varEmitenteNome)
        criarLabelEntry(tab_dados, "Emitente CNPJ", 0.52, 0.25, 0.43, varEmitenteCnpj)

        criarLabelEntry(tab_dados, "Destinatário", 0.05, 0.35, 0.42, varDestinatarioNome)
        criarLabelEntry(tab_dados, "Destinatário CNPJ", 0.52, 0.35, 0.43, varDestinatarioCnpj)

        criarLabelEntry(tab_dados, "Chave NFE", 0.05, 0.45, 0.42, varChaveNfe)
        criarLabelEntry(tab_dados, "Série NFE", 0.52, 0.45, 0.43, varSerieNfe)

        criarLabelEntry(tab_dados, "Data emissão", 0.05, 0.55, 0.2, varDataEmissao)
        criarLabelEntry(tab_dados, "Data saída", 0.27, 0.55, 0.2, varDataSaida)
        criarLabelEntry(tab_dados, "Data registro", 0.49, 0.55, 0.2, varDataRegistro)

        criarLabelEntry(tab_dados, "Valor produtos", 0.05, 0.65, 0.2, varValorProdutos)
        criarLabelEntry(tab_dados, "Valor BC ICMS", 0.27, 0.65, 0.2, varValorBcIcms)
        criarLabelEntry(tab_dados, "Valor ICMS", 0.49, 0.65, 0.2, varValorIcms)
        criarLabelEntry(tab_dados, "ICMS desonerado", 0.71, 0.65, 0.24, varValorIcmsDesonerado)

        criarLabelEntry(tab_dados, "Valor BC ICMS ST", 0.05, 0.75, 0.2, varValorBcIcmsSt)
        criarLabelEntry(tab_dados, "Valor ICMS ST", 0.27, 0.75, 0.2, varValorIcmsSt)
        criarLabelEntry(tab_dados, "Valor IPI", 0.49, 0.75, 0.2, varValorIpi)
        criarLabelEntry(tab_dados, "Valor PIS", 0.71, 0.75, 0.24, varValorPis)

        criarLabelEntry(tab_dados, "Valor COFINS", 0.05, 0.85, 0.2, varValorCofins)
        criarLabelEntry(tab_dados, "Valor BC IRRF", 0.27, 0.85, 0.2, varValorBcIrrf)
        criarLabelEntry(tab_dados, "Transportadora CNPJ", 0.49, 0.85, 0.2, varTransportadoraCnpj)
        criarLabelEntry(tab_dados, "Transportadora", 0.71, 0.85, 0.24, varTransportadoraNome)

        ctk.CTkLabel(tab_itens, text="Itens", width=50, font=("TkDefaultFont", 15)).place(relx=0.05, rely=0.05, anchor="w")

        itens_frame = ctk.CTkScrollableFrame(tab_itens, fg_color="transparent")
        itens_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8, anchor="nw")

        def separar_itens_por_descricao(texto_itens):
            linhas = [linha.strip() for linha in texto_itens.splitlines() if linha.strip()]
            itens_separados = []
            item_atual = []

            for linha in linhas:
                if linha.lower().startswith("descricao") or linha.lower().startswith("descrição"):
                    if item_atual:
                        itens_separados.append("\n".join(item_atual))
                        item_atual = []
                item_atual.append(linha)

            if item_atual:
                itens_separados.append("\n".join(item_atual))

            if not itens_separados:
                itens_separados.append("\n".join(linhas))

            return itens_separados

        for indice, item in enumerate(separar_itens_por_descricao(varItens.get()), start=1):
            bloco_item = ctk.CTkFrame(itens_frame, corner_radius=8)
            bloco_item.pack(fill="x", pady=5, padx=0)

            ctk.CTkLabel(bloco_item, text=f"Item {indice}", font=("TkDefaultFont", 14, "bold"), anchor="w", justify="left").pack(anchor="w", padx=10, pady=(8, 0))
            ctk.CTkLabel(bloco_item, text=item, anchor="w", justify="left", wraplength=750).pack(anchor="w", padx=10, pady=(0, 8))

        criaBotao(frame, "Voltar", 0.05, 0.94, 0.15, lambda: frame.destroy()).place(anchor="nw")

