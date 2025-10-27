import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
from datetime import datetime
from telas.telaProdutos import telaProdutos
from componentes import criaFrameJanela, criarLabelEntry, criarLabelComboBox, criarLabelLateralEntry, criarLabelLateralComboBox, criaBotao
from telas.telaTransporte import telaTransporte





def acessar(dados, *caminho, default=""):
    for chave in caminho:
        if isinstance(dados, dict) and chave in dados:
            dados = dados[chave]
        else:
            return default
    if isinstance(dados, dict) and "#text" in dados:
        return dados["#text"]
    return dados if isinstance(dados, str) else default


def telaNotaFiscalEntrada(self, dadosNota):
    self.dadosNotaPegar = []
    self.frameTelaNotaFiscalEntrada = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)


    def buscaNatureza(cfop):
        variavelCFOPNota=ctk.StringVar()

        match cfop:
            case "1101":
                variavelCFOPNota.set("Compra para industrialização (MG)")
            case "1102":
                variavelCFOPNota.set("Compra para comercialização (MG)")
            case "1202":
                variavelCFOPNota.set("Devolução de venda (MG)")
            case "1401":
                variavelCFOPNota.set("ST - Industrialização (MG)")
            case "1403":
                variavelCFOPNota.set("ST - Revenda (MG)")
            case "1406":
                variavelCFOPNota.set("ST - Imobilizado (MG)")
            case "1407":
                variavelCFOPNota.set("ST - Consumo (MG)")
            case "1411":
                variavelCFOPNota.set("ST - Devolução (MG)")
            case "1551":
                variavelCFOPNota.set("Tributado - Imobilizado (MG)")
            case "1556":
                variavelCFOPNota.set("Tributado - Consumo (MG)")
            case "1653":
                variavelCFOPNota.set("Compra de combustível para comercialização")
            case "1922":
                variavelCFOPNota.set("Retorno de remessa para industrialização")
            case "2101":
                variavelCFOPNota.set("Compra para industrialização (outro estado)")
            case "2102":
                variavelCFOPNota.set("Compra para comercialização (outro estado)")
            case "2202":
                variavelCFOPNota.set("Devolução de venda (outro estado)")
            case "2401":
                variavelCFOPNota.set("ST - Industrialização (outro estado)")
            case "2403":
                variavelCFOPNota.set("ST - Revenda (outro estado)")
            case "2406":
                variavelCFOPNota.set("ST - Imobilizado (outro estado)")
            case "2407":
                variavelCFOPNota.set("ST - Consumo (outro estado)")
            case "2411":
                variavelCFOPNota.set("ST - Devolução (outro estado)")
            case "2551":
                variavelCFOPNota.set("Tributado - Imobilizado (outro estado)")
            case "2556":
                variavelCFOPNota.set("Tributado - Consumo (outro estado)")
            case "1949":
                variavelCFOPNota.set("Compra de mercadoria importada para comercialização/indústria (MG)")
            case "1915":
                variavelCFOPNota.set("Aquisição de bem para imobilizado importado (MG)")
            case "1916":
                variavelCFOPNota.set("Aquisição de material para uso/consumo importado (MG)")
            case "2949":
                variavelCFOPNota.set("Compra de mercadoria importada para comercialização/indústria (outro estado)")
            case "2915":
                variavelCFOPNota.set("Aquisição de bem para imobilizado importado (outro estado)")
            case "2916":
                variavelCFOPNota.set("Aquisição de material para uso/consumo importado (outro estado)")
            case _:
                variavelCFOPNota.set("")

        return variavelCFOPNota.get()




    # Variáveis de entrada
    variavelNumeroDaNota             = ctk.StringVar()
    variavelChaveDaNota              = ctk.StringVar()
    variavelSerieDaNota              = ctk.StringVar()
    variavelRazaoSocialEmitente      = ctk.StringVar()
    variavelCNPJRazaoSocialEmitente  = ctk.StringVar()
    variavelRazaoSocialRemetente     = ctk.StringVar()
    variavelCNPJRazaoSocialRemetente = ctk.StringVar()
    variavelDataDocumento            = ctk.StringVar()
    variavelDataEntrada              = ctk.StringVar()
    variavelDataCriacao              = ctk.StringVar()
    variavelHoraEntradaSaida         = ctk.StringVar()
    variavelStatus                   = ctk.StringVar()
    variavelDataConfirmacao          = ctk.StringVar()
    variavelCFOP                     = ctk.StringVar()
    variavelNatureza                 = ctk.StringVar()
    formaDePagamento                 = ctk.StringVar()
    variavelEntradaOuSaida           = ctk.StringVar()
    data                             = ctk.StringVar()

    data.set(value=datetime.now().strftime("%d/%m/%Y"))

    # Formatação de datas
    id_nfe = acessar(dadosNota, "NFe", "infNFe", "Id")
    tirarPrefixoDaNota = id_nfe[3:] if id_nfe.startswith("NFe") else id_nfe

    def formatar_data(data_str):
        if "T" in data_str:
            data_str = data_str.split("T")[0]
        try:
            return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            return ""
    dataCriacao      = formatar_data(acessar(dadosNota, "NFe", "infNFe", "ide", "dhEmi"))
    dataEntrada      = formatar_data(acessar(dadosNota, "NFe", "infNFe", "ide", "dhSaiEnt"))
    dataDocumento    = formatar_data(acessar(dadosNota, "NFe", "infNFe", "ide", "dhEmi"))
    horaEntradaSaida = acessar(dadosNota, "NFe", "infNFe", "ide", "dhSaiEnt").split("T")[-1][:5] if "T" in acessar(dadosNota, "NFe", "infNFe", "ide", "dhSaiEnt") else ""
    codigoPagamento  = acessar(dadosNota, "NFe", "infNFe", "pag", "detPag", "tPag")
    variavelNumeroDaNota.set(acessar(dadosNota, "NFe", "infNFe", "ide", "nNF"))
    variavelSerieDaNota.set(acessar(dadosNota, "NFe", "infNFe", "ide", "serie"))
    variavelChaveDaNota.set(tirarPrefixoDaNota)
    variavelRazaoSocialEmitente.set(acessar(dadosNota, "NFe", "infNFe", "emit", "xNome"))
    variavelCNPJRazaoSocialEmitente.set(acessar(dadosNota, "NFe", "infNFe", "emit", "CNPJ"))
    variavelRazaoSocialRemetente.set(acessar(dadosNota, "NFe", "infNFe", "dest", "xNome"))
    variavelCNPJRazaoSocialRemetente.set(acessar(dadosNota, "NFe", "infNFe", "dest", "CNPJ"))
    var = "Saída" if acessar(dadosNota, "NFe", "infNFe", "ide", "tpNF") == 0 else "Entrada"

    # COLOCAR PARA IDENTIFICAR SOMENTE QUANDO TIVER IMPORTANDO A NOTA FISCAL


    variavelEntradaOuSaida.set(var)
    variavelDataDocumento.set(dataDocumento)
    variavelDataEntrada.set(dataEntrada)
    variavelDataCriacao.set(dataCriacao)
    variavelHoraEntradaSaida.set(horaEntradaSaida)
    variavelStatus.set("Em Digitação")
    variavelDataConfirmacao.set(dataEntrada)
    

    # Combos
    match codigoPagamento:
        case "01" | "02" | "03" | "04" | "17":
            formaDePagamento.set("À Vista")
        case "14" | "15":
            formaDePagamento.set("À Prazo")
        case "90":
            formaDePagamento.set("Sem Pagamento")
        case _:
            formaDePagamento.set("Outros")

    opcoesSituacao   = ["Normal", "Extemporâneo"]
    opcoesFinalidade = ["Normal", "complementar", "Ajuste"]
    opcoesPagamento  = ["À vista", "À prazo", "Outros"]
    opcoesTransporte = [
        "Contratação do Frete por conta do Remetente (CIF)",
        "Contratação do Frete por conta do Destinatário (FOB)",
        "Contratação do Frete por conta de Terceiros",
        "Transporte Próprio por conta do Remetente",
        "Transporte Próprio por conta do Destinatário",
        "Sem Ocorrência de Transporte"
    ]

    # Layout do formulário
    criarLabelEntry(self.frameTelaNotaFiscalEntrada, "Número da NF", 0.1, 0.05, 0.07, variavelNumeroDaNota)
    criarLabelEntry(self.frameTelaNotaFiscalEntrada, "Série", 0.2, 0.05, 0.07, variavelSerieDaNota)
    criarLabelEntry(self.frameTelaNotaFiscalEntrada, "Chave da NF", 0.3, 0.05, 0.3, variavelChaveDaNota)

    ctk.CTkLabel(self.frameTelaNotaFiscalEntrada, text="Destinatário----------").place(relx=0.1, rely=0.15)
    criarLabelEntry(self.frameTelaNotaFiscalEntrada, "Razão social", 0.1, 0.20, 0.3, variavelRazaoSocialRemetente)
    criarLabelEntry(self.frameTelaNotaFiscalEntrada, "CNPJ", 0.45, 0.20, 0.15, variavelCNPJRazaoSocialRemetente)

    ctk.CTkLabel(self.frameTelaNotaFiscalEntrada, text="Emitente----------").place(relx=0.1, rely=0.3)
    criarLabelEntry(self.frameTelaNotaFiscalEntrada, "Razão social", 0.1, 0.35, 0.3, variavelRazaoSocialEmitente)
    criarLabelEntry(self.frameTelaNotaFiscalEntrada, "CNPJ", 0.45, 0.35, 0.15, variavelCNPJRazaoSocialEmitente)



    variavelHoraEntradaSaida.set('')
    criarLabelLateralEntry(self.frameTelaNotaFiscalEntrada, "Status",             0.75, 0.09, 0.1, variavelStatus)
    criarLabelLateralEntry(self.frameTelaNotaFiscalEntrada, "Data documento",     0.75, 0.14, 0.1, variavelDataDocumento)
    criarLabelLateralEntry(self.frameTelaNotaFiscalEntrada, "Data entrada",       0.75, 0.19, 0.1, data)
    criarLabelLateralEntry(self.frameTelaNotaFiscalEntrada, "Hora entrada/saída", 0.75, 0.24, 0.1, variavelHoraEntradaSaida)
    criarLabelLateralEntry(self.frameTelaNotaFiscalEntrada, "Data criação",       0.75, 0.29, 0.1, data)
    criarLabelLateralEntry(self.frameTelaNotaFiscalEntrada, "Data confirmação",   0.75, 0.34, 0.1, variavelDataConfirmacao)
    criarLabelLateralEntry(self.frameTelaNotaFiscalEntrada, "Tipo da nota",       0.75, 0.39, 0.1, variavelEntradaOuSaida)
    criarLabelLateralComboBox(self.frameTelaNotaFiscalEntrada, "Data finalidade", 0.75, 0.44, 0.1, opcoesFinalidade)
    criarLabelLateralComboBox(self.frameTelaNotaFiscalEntrada, "Data situação",   0.75, 0.49, 0.1, opcoesSituacao)

    cfop = criarLabelEntry(self.frameTelaNotaFiscalEntrada, "CFOP", 0.1, 0.49, 0.07, variavelCFOP)
    cfop.configure(validate="key",validatecommand=(self.register(lambda text: len(text) <= 4), '%P'))
    cfop.bind("<KeyRelease>", lambda event: variavelNatureza.set(buscaNatureza(variavelCFOP.get())))
    criarLabelEntry(self.frameTelaNotaFiscalEntrada, "Natureza da Operação", 0.2, 0.49, 0.4, variavelNatureza)

    ctk.CTkLabel(self.frameTelaNotaFiscalEntrada, text="Transporte----------").place(relx=0.1, rely=0.59)
    self.modalidadeDoFrete = criarLabelComboBox(self.frameTelaNotaFiscalEntrada, "Modalidade do frete", 0.1, 0.64, 0.27, opcoesTransporte)
    formasPag = criarLabelComboBox(self.frameTelaNotaFiscalEntrada, "Forma de pagamento", 0.4, 0.64, 0.2, opcoesPagamento)
    formasPag.set(formaDePagamento.get())

    criaBotao(self.frameTelaNotaFiscalEntrada, "Próximo - Tela de Produtos", 0.25, 0.94, 0.15, lambda: telaProdutos(self, dadosNota, 0, cfop)).place(anchor="nw")
    criaBotao(self.frameTelaNotaFiscalEntrada, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaNotaFiscalEntrada.destroy()).place(anchor="nw")
