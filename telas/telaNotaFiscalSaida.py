import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
import datetime
from telas.telaProdutoNotaSaida import telaProdutosNotaSaida
from funcoesTerceiras import filtrar, verificaSeQuerFiltrarPorPeriodo
from componentes import criaFrameJanela, criaBotao, criarLabelComboBox, criarLabelEntry, criarLabelLateralComboBox, criarLabelLateralEntry


def telaNotaFiscalSaida(self, valor):

    def acessar(dados, *caminho, default=""):
        for chave in caminho:
            if isinstance(dados, dict) and chave in dados:
                dados = dados[chave]
            else:
                return default
        if isinstance(dados, dict) and "#text" in dados:
            return dados["#text"]
        return dados if isinstance(dados, str) else default

    self.frameTelaNotaSaida = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    usuarioLogado =" self.logado"
    usuarioLogado = usuarioLogado.capitalize()

    def buscaNatureza(cfop):
        variavelCFOPNota = ctk.StringVar()
        match cfop:
            case "1101": variavelCFOPNota.set("Compra para industrialização (MG)")
            case "1102": variavelCFOPNota.set("Compra para comercialização (MG)")
            case "1202": variavelCFOPNota.set("Devolução de venda (MG)")
            case "1401": variavelCFOPNota.set("ST - Industrialização (MG)")
            case "1403": variavelCFOPNota.set("ST - Revenda (MG)")
            case "1406": variavelCFOPNota.set("ST - Imobilizado (MG)")
            case "1407": variavelCFOPNota.set("ST - Consumo (MG)")
            case "1411": variavelCFOPNota.set("ST - Devolução (MG)")
            case "1551": variavelCFOPNota.set("Tributado - Imobilizado (MG)")
            case "1556": variavelCFOPNota.set("Tributado - Consumo (MG)")
            case "1653": variavelCFOPNota.set("Compra de combustível para comercialização")
            case "1922": variavelCFOPNota.set("Retorno de remessa para industrialização")
            case "2101": variavelCFOPNota.set("Compra para industrialização (outro estado)")
            case "2102": variavelCFOPNota.set("Compra para comercialização (outro estado)")
            case "2202": variavelCFOPNota.set("Devolução de venda (outro estado)")
            case "2401": variavelCFOPNota.set("ST - Industrialização (outro estado)")
            case "2403": variavelCFOPNota.set("ST - Revenda (outro estado)")
            case "2406": variavelCFOPNota.set("ST - Imobilizado (outro estado)")
            case "2407": variavelCFOPNota.set("ST - Consumo (outro estado)")
            case "2411": variavelCFOPNota.set("ST - Devolução (outro estado)")
            case "2551": variavelCFOPNota.set("Tributado - Imobilizado (outro estado)")
            case "2556": variavelCFOPNota.set("Tributado - Consumo (outro estado)")
            case "1949": variavelCFOPNota.set("Compra de mercadoria importada para comercialização/indústria (MG)")
            case "1915": variavelCFOPNota.set("Aquisição de bem para imobilizado importado (MG)")
            case "1916": variavelCFOPNota.set("Aquisição de material para uso/consumo importado (MG)")
            case "2949": variavelCFOPNota.set("Compra de mercadoria importada para comercialização/indústria (outro estado)")
            case "2915": variavelCFOPNota.set("Aquisição de bem para imobilizado importado (outro estado)")
            case "2916": variavelCFOPNota.set("Aquisição de material para uso/consumo importado (outro estado)")
            case _: variavelCFOPNota.set("")
        return variavelCFOPNota.get()


    def decideEmitente(self, valor):
        if valor == "Nutrigel":
            print("entrou aqui")
            self.variavelNumeroDaNota.set("000001")
            self.variavelSerieDaNota.set("1")
            self.variavelRazaoSocialEmitente.set("NUTRIGEL DISTRIBUIDORA EIRELI")
            self.variavelCNPJRazaoSocialEmitente.set("00.995.044/0001-07")
            self.variavelInscEstadualEmitente.set(0)

    opcoesSituacao = ["Normal", "Extemporâneo"]
    opcoesFinalidade = ["Normal", "complementar", "Ajuste"]
    opcoesPagamento = ["À vista", "À prazo", "Outros"]
    opcoesTransporte = [
        "Contratação do Frete por conta do Remetente (CIF)",
        "Contratação do Frete por conta do Destinatário (FOB)",
        "Contratação do Frete por conta de Terceiros",
        "Transporte Próprio por conta do Remetente",
        "Transporte Próprio por conta do Destinatário",
        "Sem Ocorrência de Transporte"
    ]

    self.variavelNumeroDaNota = ctk.StringVar()
    self.variavelSerieDaNota = ctk.StringVar()
    self.variavelChaveDaNota = ctk.StringVar()
    self.variavelRazaoSocialRemetente = ctk.StringVar()
    self.variavelCNPJRazaoSocialRemetente = ctk.StringVar()
    self.variavelRazaoSocialEmitente = ctk.StringVar()
    self.variavelCNPJRazaoSocialEmitente = ctk.StringVar()
    self.variavelInscEstadualEmitente = ctk.StringVar()
    self.variavelInscEstadualRemetente = ctk.StringVar()
    self.variavelCFOP = ctk.StringVar()
    self.variavelNatureza = ctk.StringVar()
    self.variavelStatus = ctk.StringVar()
    self.variavelDataDocumento = ctk.StringVar()
    self.data = ctk.StringVar()
    self.variavelHoraEntradaSaida = ctk.StringVar()
    self.variavelDataCriacao = ctk.StringVar()
    self.variavelDataConfirmacao = ctk.StringVar()
    self.variavelVendedor = ctk.StringVar()
    self.variavelEntradaOuSaida = ctk.StringVar()
    self.formaDePagamento = ctk.StringVar()
    self.variavelModalidadeFrete = ctk.StringVar()
    self.variavelValorTotal = ctk.StringVar()
    self.opcoesFinalidade = ["Normal", "Complementar", "Ajuste"]
    self.opcoesSituacao = ["Ativa", "Cancelada", "Inutilizada"]
    
    self.variavelVendedor.set(usuarioLogado)
    self.variavelDataCriacao.set(value=datetime.datetime.now().strftime("%d/%m/%y"))
    self.variavelStatus.set("Em Digitação")

    #ATRIBUIR VALOR CORRETO PARA ESSAS VARIAVEIS
    self.variavelInscEstadualRemetente.set(0)
    self.variavelModalidadeFrete.set(0)
    self.variavelValorTotal.set(0)
    self.variavelEntradaOuSaida.set("Saída") if valor else self.variavelEntradaOuSaida.set("Entrada")


    criarLabelEntry(self.frameTelaNotaSaida, "Número da NF", 0.1, 0.05, 0.07, self.variavelNumeroDaNota)
    criarLabelEntry(self.frameTelaNotaSaida, "Série", 0.2, 0.05, 0.07, self.variavelSerieDaNota)
    criarLabelEntry(self.frameTelaNotaSaida, "Chave da NF", 0.3, 0.05, 0.3, self.variavelChaveDaNota)

    ctk.CTkLabel(self.frameTelaNotaSaida, text="Destinatário----------").place(relx=0.1, rely=0.15)
    criarLabelEntry(self.frameTelaNotaSaida, "Razão social", 0.1, 0.20, 0.3, self.variavelRazaoSocialRemetente)
    criarLabelEntry(self.frameTelaNotaSaida, "CNPJ", 0.45, 0.20, 0.15, self.variavelCNPJRazaoSocialRemetente)

    ctk.CTkLabel(self.frameTelaNotaSaida, text="Emitente----------").place(relx=0.1, rely=0.3)
    opcoes=["nenhum", "Multimaquinas", "Nutrigel", "Polimáquinas"]
    emt = criarLabelComboBox(self.frameTelaNotaSaida, "Razão social", 0.1, 0.35, 0.3, opcoes)
    emt.configure(command= lambda valor: decideEmitente(self, emt.get()))
    criarLabelEntry(self.frameTelaNotaSaida, "CNPJ", 0.45, 0.35, 0.15, self.variavelCNPJRazaoSocialEmitente)

    self.variavelHoraEntradaSaida.set('')
    criarLabelLateralEntry(self.frameTelaNotaSaida, "Status", 0.75, 0.09, 0.1, self.variavelStatus)
    criarLabelLateralEntry(self.frameTelaNotaSaida, "Data documento", 0.75, 0.14, 0.1, self.variavelDataDocumento)
    criarLabelLateralEntry(self.frameTelaNotaSaida, "Data entrada", 0.75, 0.19, 0.1, self.data)
    criarLabelLateralEntry(self.frameTelaNotaSaida, "Hora entrada/saída", 0.75, 0.24, 0.1, self.variavelHoraEntradaSaida)
    criarLabelLateralEntry(self.frameTelaNotaSaida, "Data criação", 0.75, 0.29, 0.1, self.variavelDataCriacao)
    criarLabelLateralEntry(self.frameTelaNotaSaida, "Data confirmação", 0.75, 0.34, 0.1, self.variavelDataConfirmacao)
    criarLabelLateralEntry(self.frameTelaNotaSaida, "Vendedor", 0.75, 0.39, 0.1, self.variavelVendedor)
    criarLabelLateralEntry(self.frameTelaNotaSaida, "Tipo da nota", 0.75, 0.44, 0.1, self.variavelEntradaOuSaida)
    criarLabelLateralComboBox(self.frameTelaNotaSaida, "Data finalidade", 0.75, 0.49, 0.1, self.opcoesFinalidade)
    criarLabelLateralComboBox(self.frameTelaNotaSaida, "Data situação", 0.75, 0.54, 0.1, self.opcoesSituacao)


    cfop = criarLabelEntry(self.frameTelaNotaSaida, "CFOP", 0.1, 0.49, 0.07, self.variavelCFOP)
    cfop.configure(validate="key", validatecommand=(self.register(lambda text: len(text) <= 4), '%P'))
    cfop.bind("<KeyRelease>", lambda event: self.variavelNatureza.set(buscaNatureza(self.variavelCFOP.get())))
    criarLabelEntry(self.frameTelaNotaSaida, "Natureza da Operação", 0.2, 0.49, 0.4, self.variavelNatureza)

    ctk.CTkLabel(self.frameTelaNotaSaida, text="Transporte----------").place(relx=0.1, rely=0.59)
    self.modalidadeDoFrete = criarLabelComboBox(self.frameTelaNotaSaida, "Modalidade do frete", 0.1, 0.64, 0.27, opcoesTransporte)
    formasPag = criarLabelComboBox(self.frameTelaNotaSaida, "Forma de pagamento", 0.4, 0.64, 0.2, opcoesPagamento)
    formasPag.set(self.formaDePagamento.get())

    criaBotao(self.frameTelaNotaSaida, "Próximo - Tela de Produtos", 0.25, 0.94, 0.15, lambda: telaProdutosNotaSaida(self, cfop.get())).place(anchor="nw")
    criaBotao(self.frameTelaNotaSaida, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaNotaSaida.destroy()).place(anchor="nw")
