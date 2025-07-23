import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from telas import telaRegistraCredito, telaVerDebito
from componentes import criaFrame, criaFrameJanela, criarLabelEntry, criaBotao

def telaVercontasApagar(self, d):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)

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
        

        criarLabelEntry(frame, "Cód. Identificador", 0.05, 0.05, 0.187, varNumeroNfe)
        criarLabelEntry(frame, "Parcela", 0.287, 0.05, 0.187, None)
        criarLabelEntry(frame, "Nota Fiscal/Pedido/O.S.", 0.524, 0.05, 0.187, None)
        criarLabelEntry(frame, "Funcionário responsável", 0.761, 0.05, 0.187, None)


        criarLabelEntry(frame, "Cód. Identificador", 0.05, 0.15, 0.267, varNumeroNfe)
        criarLabelEntry(frame, "Parcela", 0.367, 0.15, 0.267, None)
        criarLabelEntry(frame, "Nota Fiscal/Pedido/O.S.", 0.684, 0.15, 0.266, None)

        criarLabelEntry(frame, "Descricao", 0.05, 0.25, 0.6, None)
        criarLabelEntry(frame, "Número do documento", 0.7, 0.25, 0.25, None)

        criarLabelEntry(frame, "Forma de pagamento", 0.05, 0.35, 0.187, None)
        criarLabelEntry(frame, "Conta bancária", 0.287, 0.35, 0.187, None)
        criarLabelEntry(frame, "Plano orçamentário", 0.524, 0.35, 0.187, None)
        criarLabelEntry(frame, "Departamento", 0.761, 0.35, 0.187, None)
        
        criarLabelEntry(frame, "Fornecedor", 0.05, 0.45, 0.9, None)

        criarLabelEntry(frame, "Original", 0.05, 0.55, 0.187, varNumeroNfe)
        criarLabelEntry(frame, "Bruto", 0.287, 0.55, 0.187, None)
        criarLabelEntry(frame, "Pago", 0.524, 0.55, 0.187, None)
        criarLabelEntry(frame, "Desconto", 0.761, 0.55, 0.187, None)

        criarLabelEntry(frame, "Acréscimo", 0.05, 0.65, 0.187, None)
        criarLabelEntry(frame, "Júros por atraso", 0.287, 0.65, 0.187, None)
        criarLabelEntry(frame, "Júros dia", 0.524, 0.65, 0.187, None)

        criaBotao(frame, "Voltar", 0.05, 0.94, 0.15, lambda: frame.destroy()).place(anchor="nw")
        
        

