import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
import datetime
from telas.telaProdutoNotaSaida import telaProdutosNotaSaida
from funcoesTerceiras import filtrar, verificaSeQuerFiltrarPorPeriodo
from componentes import criaFrameJanela, criaBotao, criarLabelComboBox, criarLabelEntry, criarLabelLateralComboBox, criarLabelLateralEntry
from consultas.select import Buscas 



def telaNotaFiscalSaida(self, valor):
    self.frameTelaNotaSaida = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    usuarioLogado =" self.logado"
    usuarioLogado = usuarioLogado.capitalize()


    def buscaCliente(event=None): 
        nomeDoCliente = self.Rs.get()
        dadosCliente = Buscas.buscaClientesFiscal(nomeDoCliente)


        if hasattr(self, 'resultadoLabels'):
            for label in self.resultadoLabels: 
                label.destroy()
        self.resultadoLabels = []
            
        yNovo = 0.16
        for i, row in enumerate(dadosCliente):
            if i >= 5:
                break
            label = ctk.CTkButton(self.frameTelaNotaSaida,  text=row[0], corner_radius=0,fg_color=self.cor, font=("Century Gothic bold", 15), command=lambda  nome=row[0], documento=row[1], ie=row[2], rua=row[3], num=row[4], cep=row[5], bairro=row[6], cidade=row[7], estado=row[8]: selecionaCliente(nome, documento, ie, rua, num, cep, bairro, cidade, estado))
            label.place(relx=0.1, rely=yNovo, relwidth=0.3)
            self.resultadoLabels.append(label)  
            yNovo += 0.0399


    def selecionaCliente(nome, documento, ie, rua, num, cep, bairro, cidade, estado):
        print("Cliente selecionado:", nome, documento, ie, rua, num, cep, bairro, cidade, estado)

        # --- normaliza 'estado' (nome completo) para UF ---
        import unicodedata
        est_str = (estado or "").strip()
        if len(est_str) == 2 and est_str.isalpha():
            uf = est_str.upper()
        else:
            est_norm = ''.join(
                c for c in unicodedata.normalize('NFD', est_str)
                if unicodedata.category(c) != 'Mn'
            ).lower()
            mapa_ufs = {
                'acre': 'AC',
                'alagoas': 'AL',
                'amapa': 'AP',
                'amazonas': 'AM',
                'bahia': 'BA',
                'ceara': 'CE',
                'distrito federal': 'DF',
                'espirito santo': 'ES',
                'goias': 'GO',
                'maranhao': 'MA',
                'mato grosso': 'MT',
                'mato grosso do sul': 'MS',
                'minas gerais': 'MG',
                'para': 'PA',
                'paraiba': 'PB',
                'parana': 'PR',
                'pernambuco': 'PE',
                'piaui': 'PI',
                'rio de janeiro': 'RJ',
                'rio grande do norte': 'RN',
                'rio grande do sul': 'RS',
                'rondonia': 'RO',
                'roraima': 'RR',
                'santa catarina': 'SC',
                'sao paulo': 'SP',
                'sergipe': 'SE',
                'tocantins': 'TO',
            }
            uf = mapa_ufs.get(est_norm, est_str[:2].upper() if len(est_str) >= 2 else "")
        # --------------------------------------------------

        self.nomeDestinatario = nome
        self.documentoDestinatario = documento
        self.bairroDestinatario = bairro
        self.cidadeDestinatario = cidade
        self.estadoDestinatario = uf  # <- agora usa a sigla
        self.ruaDestinatario = rua
        self.numeroDestinatario = num
        self.cidadeDestinatario = cidade
        self.cepDestinatario = cep

        self.variavelRazaoSocialRemetente.set(nome)
        self.inscricaoEstadualDestinatario.set(ie)
        self.variavelCNPJRazaoSocialRemetente.set(documento)

        for label in self.resultadoLabels: 
            label.destroy()

        # pass



    def on_stop_typing(event=None):
        print("Parou de digitar")
        buscaCliente()






    def acessar(dados, *caminho, default=""):
        for chave in caminho:
            if isinstance(dados, dict) and chave in dados:
                dados = dados[chave]
            else:
                return default
        if isinstance(dados, dict) and "#text" in dados:
            return dados["#text"]
        return dados if isinstance(dados, str) else default



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
            case "5402": variavelCFOPNota.set("Venda de mercadoria recebida de terceiros sujeita ao reg")
            case _: variavelCFOPNota.set("")
        return variavelCFOPNota.get()


    def decideEmitente(self, valor):
        if valor == "Nutrigel":
            self.variavelRazaoSocialEmitente.set("NUTRIGEL DISTRIBUIDORA EIRELI")
            self.variavelInscEstadualEmitente.set("6259569630086")
            self.variavelCNPJRazaoSocialEmitente.set("00995044000107")  # 14 dígitos, sem máscara

            # Endereço do emitente
            self.variavelNumeroEnd          = "126"
            self.variavelLogradouroEnd      = "R DOUTOR OSCAR DA CUNHA"
            self.variavelBairroEnd          = "FABRICAS"
            self.variavelComplementoEnd     = "LETRA B"
            self.variavelMunicipioEnd       = "SAO JOAO DEL REI"
            self.variavelUFEnd              = "MG"
            self.variavelCEPEnd             = "36301194"    
            self.variavelCodigoMunicipioEnd = "3162500"      
            self.variavelTelefoneEnd        = "3233716171"


        if valor == "Multimáquinas":
            self.variavelRazaoSocialEmitente.set("POLIMAQUINAS")
            self.variavelCNPJRazaoSocialEmitente.set("23889618000150")
            self.variavelInscEstadualEmitente.set(0)


        if valor == "Polimáquinas":
            self.variavelRazaoSocialEmitente.set("NUTRIGEL DISTRIBUIDORA EIRELI")
            self.variavelCNPJRazaoSocialEmitente.set("009950440001-07")
            self.variavelInscEstadualEmitente.set(0)


    opcoesPagamento = ["À vista", "À prazo", "Outros"]
    opcoesTransporte = [
        "Contratação do Frete por conta do Remetente (CIF)",
        "Contratação do Frete por conta do Destinatário (FOB)",
        "Contratação do Frete por conta de Terceiros",
        "Transporte Próprio por conta do Remetente",
        "Transporte Próprio por conta do Destinatário",
        "Sem Ocorrência de Transporte"
    ]

    self.inscricaoEstadualDestinatario = ctk.StringVar()
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


    ctk.CTkLabel(self.frameTelaNotaSaida, text="Destinatário----------").place(relx=0.1, rely=0.05)
    self.Rs = criarLabelEntry(self.frameTelaNotaSaida, "Razão social", 0.1, 0.10, 0.3, self.variavelRazaoSocialRemetente)
    cnpj = criarLabelEntry(self.frameTelaNotaSaida, "CNPJ", 0.45, 0.10, 0.15, self.variavelCNPJRazaoSocialRemetente)
    self.Rs.bind("<KeyRelease>", buscaCliente)
    self.Rs.bind("<Button-1>", buscaCliente)


    criarLabelEntry(self.frameTelaNotaSaida, "Inscrição Estadual", 0.1, 0.20, 0.15, self.inscricaoEstadualDestinatario)

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
