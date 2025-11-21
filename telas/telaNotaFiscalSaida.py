import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
import datetime
from telas.telaProdutoNotaSaida import telaProdutosNotaSaida
from funcoesTerceiras import filtrar, verificaSeQuerFiltrarPorPeriodo
from componentes import checkbox, criaFrameJanela, criaBotao, criarLabelComboBox, criarLabelEntry, criarLabelLateralComboBox, criarLabelLateralEntry
from consultas.select import Buscas 
from telas.telaNotaReferenciada import telaNotaReferenciada
from telas.telaCadastroClientes import telaCadastroClientes



def telaNotaFiscalSaida(self, valor, EhNotaDoConsumidor):
    self.frameTelaNotaSaida = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    usuarioLogado =" self.logado"
    usuarioLogado = usuarioLogado.capitalize()



    def decideATela(valor):
        if valor == "Devolução" or valor == "Complementar":
            self.botaoTela = criaBotao(self.frameTelaNotaSaida, "Próximo - Tela notas Ref.", 0.25, 0.94, 0.15, lambda: telaNotaReferenciada(self, emt.get(), cfop.get())).place(anchor="nw")
        else:
            self.botaoTela = criaBotao(self.frameTelaNotaSaida, "Próximo - Tela de Produtos", 0.25, 0.94, 0.15, lambda: telaProdutosNotaSaida(self, emt.get(), cfop.get())).place(anchor="nw")


    def buscaCliente(event=None): 
        nomeDoCliente = self.Rs.get()
        cnpjCliente = self.cnpjClienteNotaSaida.get()
        dadosCliente = Buscas.buscaClientesFiscal(nomeDoCliente, cnpjCliente)


        if hasattr(self, 'resultadoLabels'):
            for label in self.resultadoLabels: 
                label.destroy()
        self.resultadoLabels = []
            
        yNovo = 0.16
        if len(dadosCliente) > 0:
            for i, row in enumerate(dadosCliente):
                if i >= 5:
                    break
                label = ctk.CTkButton(self.frameTelaNotaSaida,  text=row[0], corner_radius=0,fg_color=self.cor, font=("Century Gothic bold", 15), command = lambda  nome=row[0], documento=row[1], ie=row[2], rua=row[3], num=row[4], cep=row[5], bairro=row[6], cidade=row[7], estado=row[8]: selecionaCliente(nome, documento, ie, rua, num, cep, bairro, cidade, estado))
                label.place(relx=0.1, rely=yNovo, relwidth=0.3)
                self.resultadoLabels.append(label)  
                yNovo += 0.0399
        else:
            print("entrou")
            label = ctk.CTkButton(self.frameTelaNotaSaida,  text="+ Cadastrar cliente", corner_radius=0, fg_color=self.cor, font=("Century Gothic bold", 15), command = lambda: telaCadastroClientes(self, 1))
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
        documento = (documento or '').replace('.', '').replace('/', '').replace('-', '')
        self.variavelCNPJRazaoSocialRemetente.set(documento)

        for label in self.resultadoLabels: 
            label.destroy()

        # pass





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
            case "5405": variavelCFOPNota.set("Venda de mercadoria recebida de terceiros sujeita ao reg")
            case "5102": variavelCFOPNota.set("Venda de mercadoria adquirida ou recebida de terceiros")
            case "1411": variavelCFOPNota.set("Devolução de venda de mercadoria recebida de terceiros em operação com mercadoria sujeita a substituição tributária")
            case "1202": variavelCFOPNota.set("Devolução de venda de mercadoria adquirida ou recebida de terceiros")
            case "1926": variavelCFOPNota.set("Lançamento efetuado a título de reclassificação de mercadoria decorrente de formação de kit ou de sua desagregação")
        return variavelCFOPNota.get()


    def decideEmitente(self, valor):
        if valor == "Nutrigel":
            self.variavelRazaoSocialEmitente.set("NUTRIGEL DISTRIBUIDORA EIRELI")
            self.variavelInscEstadualEmitente.set("6259569630086")
            self.variavelCNPJRazaoSocialEmitente.set("00995044000107")

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
            self.variavelCSCToken           = "fc61ad002385a054543bbf619d0247b5"
            
            self.caminhoCertificado = r"C:\Users\GABRIEL\Desktop\dist\certificados\certificadoNutrigel.pfx"
            self.senhaCertificado   = "nutri@00995"

        if valor == "Multimáquinas":
            self.variavelRazaoSocialEmitente.set("MULTIMAQUINAS REFRIGERACAO E MAQUINAS DEL REI LTDA")
            self.variavelCNPJRazaoSocialEmitente.set("05704180000106")  # 14 dígitos, sem máscara
            self.variavelInscEstadualEmitente.set("6252430230046")

            # Endereço
            self.variavelNumeroEnd          = "97"
            self.variavelLogradouroEnd      = "R DOUTOR OSCAR DA CUNHA"
            self.variavelBairroEnd          = "FABRICAS"
            self.variavelComplementoEnd     = ""
            self.variavelMunicipioEnd       = "SAO JOAO DEL REI"
            self.variavelUFEnd              = "MG"
            self.variavelCEPEnd             = "36301194"
            self.variavelCodigoMunicipioEnd = "3162500"
            self.variavelTelefoneEnd        = "3233713382"
            self.variavelCSCToken           = "7ea94a1685c35cc42d21a839c1dc840f"

            self.caminhoCertificado = r"C:\Users\GABRIEL\Desktop\dist\certificados\certificadoMultimaquinas.pfx"
            self.senhaCertificado   = "multi2025"

        if valor == "Polimáquinas":
            self.variavelRazaoSocialEmitente.set("ANA F COELHO RESENDE")
            self.variavelCNPJRazaoSocialEmitente.set("23889618000150")
            self.variavelInscEstadualEmitente.set("84549874")  # cartão CNPJ não traz IE

            # Endereço (Vila Velha/ES)
            self.variavelNumeroEnd          = "30"
            self.variavelLogradouroEnd      = "R ANA MEROTTO STEFANON"
            self.variavelBairroEnd          = "COBILANDIA"
            self.variavelComplementoEnd     = "SALA 03"
            self.variavelMunicipioEnd       = "VILA VELHA"
            self.variavelUFEnd              = "ES"
            self.variavelCEPEnd             = "29111630"
            self.variavelCodigoMunicipioEnd = "3205200"
            self.variavelTelefoneEnd        = "3233713382"
            self.variavelCSCToken           = "a985151a07100b97c8af2c1e179908cd"


            self.caminhoCertificado = r"C:\Users\GABRIEL\Desktop\dist\certificados\certificadoPolimaquinas.pfx"
            self.senhaCertificado   = "23889"

    
    self.movimentacaoProdutos = ctk.BooleanVar()
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
    self.opcoesFinalidade = ["Normal", "Complementar", "Ajuste", "Devolução", "Normal - consumidor final"]
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
    self.cnpjClienteNotaSaida = criarLabelEntry(self.frameTelaNotaSaida, "CNPJ", 0.45, 0.10, 0.15, self.variavelCNPJRazaoSocialRemetente)
    
    self.Rs.bind("<KeyRelease>", buscaCliente)
    self.Rs.bind("<Button-1>", buscaCliente)

    self.cnpjClienteNotaSaida.bind("<KeyRelease>", buscaCliente)
    self.cnpjClienteNotaSaida.bind("<Button-1>", buscaCliente)


    criarLabelEntry(self.frameTelaNotaSaida, "Inscrição Estadual", 0.1, 0.20, 0.15, self.inscricaoEstadualDestinatario)

    ctk.CTkLabel(self.frameTelaNotaSaida, text="Emitente----------").place(relx=0.1, rely=0.3)
    opcoes=["nenhum", "Multimáquinas", "Nutrigel", "Polimáquinas"]
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
    finalidade = criarLabelLateralComboBox(self.frameTelaNotaSaida, "Data finalidade", 0.75, 0.49, 0.1, self.opcoesFinalidade)
    finalidade.configure(command=lambda valor: decideATela(valor))
    criarLabelLateralComboBox(self.frameTelaNotaSaida, "Data situação", 0.75, 0.54, 0.1, self.opcoesSituacao)


    cfop = criarLabelEntry(self.frameTelaNotaSaida, "CFOP", 0.1, 0.49, 0.07, self.variavelCFOP)
    cfop.configure(validate="key", validatecommand=(self.register(lambda text: len(text) <= 4), '%P'))
    cfop.bind("<KeyRelease>", lambda event: self.variavelNatureza.set(buscaNatureza(self.variavelCFOP.get())))
    criarLabelEntry(self.frameTelaNotaSaida, "Natureza da Operação", 0.2, 0.49, 0.4, self.variavelNatureza)



    criaBotao(self.frameTelaNotaSaida, "Próximo - Tela de Produtos", 0.25, 0.94, 0.15, lambda: telaProdutosNotaSaida(self, emt.get(), cfop.get(), EhNotaDoConsumidor)).place(anchor="nw")
    criaBotao(self.frameTelaNotaSaida, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaNotaSaida.destroy()).place(anchor="nw")
    checkBox = checkbox(self.frameTelaNotaSaida, "Movimentação dos produtos", 0.7, 0.60, None, lambda: self.movimentacaoProdutos.set(checkBox.get()))