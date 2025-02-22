import customtkinter as ctk
import db
from tkinter import messagebox
import gc
# import messagebox


# ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.janela()
    
    # inicializa frames de todoas as janelas pra evitar erros de "destruição de vazio"
    def criaFrames(self):
        self.frameTelaCadastroFuncionario = None
        self.frameTelaProduto = None
        self.frameTelaLogin = None
        self.frameTelaAcoes = None
        self.frameUsuarioNaoCadastrado = None
        self.frameTelaCadastros = None
        self.frameTelaCadastroProduto = None

    # define as propriedades da janela
    def janela(self):
        self.criaFrames()
        self.resizable(False, False)
        alturaTela = 900
        larguraTela = 1280
        self.geometry(f"{larguraTela}x{alturaTela}+-1500+0")
        self.telaCadastroFornecedores()




# ! fazer a tela do cadastro de fornecedores

    # tela de login inicial
    def telaLogin(self):
        self.title("login")
        self.frameTelaLogin = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameTelaLogin.place(x=140, y=100)     # colocando no lugar
        self.frameTelaLogin.grid_propagate(False)   # evita ela de se configurar automaticamente

        # titulo
        self.texto = ctk.CTkLabel(self.frameTelaLogin, width=1000, height=100, text="Fazer Login", font=("Century Gothic bold", 35))
        self.texto.place(relx=0.5, y=200, anchor="center")

        # input de login
        self.login = ctk.CTkEntry(self.frameTelaLogin, placeholder_text="Login", width=400, corner_radius=5, font=("Century Gothic bold", 25))
        self.login.place(relx=0.5, y=300, anchor="center")

        # input de senha
        self.senha = ctk.CTkEntry(self.frameTelaLogin, placeholder_text="Senha", width=400, corner_radius=5, font=("Century Gothic bold", 25), show="*")
        self.senha.place(relx=0.5, y=350, anchor="center")

        # botão para entrar
        self.botaoEntrar = ctk.CTkButton(self.frameTelaLogin, text="Entrar", width=200, corner_radius=5, font=("Arial", 20), command=self.consultarUsuarioCadastrado)
        self.botaoEntrar.place(relx=0.5, y=420, anchor="center")

    # tela que define os botões que vão levar para as outras funcionalidades
    def telaAcoes(self):
        self.criaFrames()# reseta o endereço de memória de todos os frames para None novamente, e em seguida cria o atual
        usuarioBloqueado = self.login.get()
        queryConsultaUsuarioBloqueado = "SELECT cargo FROM funcionarios WHERE login = %s;"
        db.cursor.execute(queryConsultaUsuarioBloqueado, (usuarioBloqueado,))
        cargoUsuarioBloqueado = db.cursor.fetchall()

        
        self.frameTelaAcoes = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameTelaAcoes.place(x=140, y=100)     # colocando no lugar
        self.frameTelaAcoes.grid_propagate(False)
        
        # título
        self.Acoes = ctk.CTkLabel(self.frameTelaAcoes, width=950, height=0, text="Ações", font=("Century Gothic bold", 30))
        self.Acoes.place(relx=0.5, y=50, anchor="center")

        # condição que bloqueia o acesso dos vendedores externos
        if cargoUsuarioBloqueado == (('Vendedor(a) externo',),):
            # botão de relatório de vendas # ! ainda não está ativo nem possui uma tela criada para ele 
            self.botaoRelatorioDeVendas = ctk.CTkButton(self.frameTelaAcoes, text="Relatório de vendas", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaoRelatorioDeVendas.place(relx=0.66, y=200, anchor="center")

            # botão de gerar pedidos # ! ainda não está ativo nem possui uma tela criada para ele
            self.botaogGerarPedido = ctk.CTkButton(self.frameTelaAcoes, text="Gerar pedido", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaogGerarPedido.place(relx=0.33, y=250, anchor="center")

            # botão de consultar estoque # ! ainda não está ativo nem possui uma tela criada para ele 
            self.botaoConsultarEstoque = ctk.CTkButton(self.frameTelaAcoes, text="Consultar estoque", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaoConsultarEstoque.place(relx=0.66, y=250, anchor="center")

            # botão de gerar orçamento # ! ainda não está ativo nem possui uma tela criada para ele 
            self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaAcoes, text="Gerar orçamento", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaoGerarOrcamento.place(relx=0.33, y=200, anchor="center") 
        else:
            # botão do cadastro de funcionarios
            self.botaoCadastro = ctk.CTkButton(self.frameTelaAcoes, text="Cadastros", width=300, corner_radius=5, font=("Arial", 18), command=self.telaCadastros)
            self.botaoCadastro.place(relx=0.33, y=200, anchor="center")

            # botão de relatório de vendas # ! ainda não está ativo nem possui uma tela criada para ele 
            self.botaoRelatorioDeVendas = ctk.CTkButton(self.frameTelaAcoes, text="Relatório de vendas", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaoRelatorioDeVendas.place(relx=0.66, y=200, anchor="center")

            # botão de gerar pedidos # ! ainda não está ativo nem possui uma tela criada para ele
            self.botaogGerarPedido = ctk.CTkButton(self.frameTelaAcoes, text="Gerar pedido", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaogGerarPedido.place(relx=0.33, y=250, anchor="center")

            # botão de contas a pagar e a receber da loja # ! ainda não está ativo nem possui uma tela criada para ele 
            self.botaoContasPagarReceber = ctk.CTkButton(self.frameTelaAcoes, text="Contas a pagar/receber", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaoContasPagarReceber.place(relx=0.66, y=250, anchor="center")

            # botão de gerar faturamento # ! ainda não está ativo nem possui uma tela criada para ele 
            self.botaoGerarFaturamento = ctk.CTkButton(self.frameTelaAcoes, text="Gerar faturamento", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaoGerarFaturamento.place(relx=0.33, y=300, anchor="center")

            # botão de consultar estoque # ! ainda não está ativo nem possui uma tela criada para ele 
            self.botaoConsultarEstoque = ctk.CTkButton(self.frameTelaAcoes, text="Consultar estoque", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaoConsultarEstoque.place(relx=0.66, y=300, anchor="center")

            # botão de gerar orçamento # ! ainda não está ativo nem possui uma tela criada para ele 
            self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaAcoes, text="Gerar orçamento", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaoGerarOrcamento.place(relx=0.33, y=350, anchor="center")

        # botão de trocar usuário 
        self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaAcoes, text="Trocar usuário", width=200, corner_radius=5, font=("Arial", 18), command=self.frameTelaAcoes.destroy)
        self.botaoGerarOrcamento.place(relx=0.33, y=650, anchor="center")


    #? ===================== FUNÇÕES DAS TELAS DE CADASTRO ===================== #

    # tela para acessar todos os outros cadastros possíveis
    def telaCadastros(self):
        self.frameTelaCadastros = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameTelaCadastros.place(x=140, y=100)     # colocando no lugar
        self.frameTelaCadastros.grid_propagate(False)
        
        # título
        self.Acoes = ctk.CTkLabel(self.frameTelaCadastros, width=950, height=0, text="Cadastros", font=("Century Gothic bold", 30))
        self.Acoes.place(relx=0.5, y=50, anchor="center")
        
        # botão do cadastro de funcionarios # ! ainda não está ativo nem possui uma tela criada para ele
        self.botaoCadastro = ctk.CTkButton(self.frameTelaCadastros, text="Produtos", width=300, corner_radius=5, font=("Arial", 18), command=self.telaCadastroProdutos)
        self.botaoCadastro.place(relx=0.33, y=200, anchor="center")

        # botão de cadastrar clientes # ! ainda não está ativo nem possui uma tela criada para ele 
        self.botaoRelatorioDeVendas = ctk.CTkButton(self.frameTelaCadastros, text="Clientes", width=300, corner_radius=5, font=("Arial", 18), command=self)
        self.botaoRelatorioDeVendas.place(relx=0.66, y=200, anchor="center")

        # botão de cadastrar fornecedores
        self.botaogGerarPedido = ctk.CTkButton(self.frameTelaCadastros, text="Fornecedores", width=300, corner_radius=5, font=("Arial", 18), command=self.telaCadastroFornecedores)
        self.botaogGerarPedido.place(relx=0.33, y=250, anchor="center")

        # botão de cadastrar funcionários
        self.botaoContasPagarReceber = ctk.CTkButton(self.frameTelaCadastros, text="Funcionários", width=300, corner_radius=5, font=("Arial", 18), command=self.telaCadastroFuncionario)
        self.botaoContasPagarReceber.place(relx=0.66, y=250, anchor="center")

        # botão cadastrar transportadoras # ! ainda não está ativo nem possui uma tela criada para ele 
        self.botaoGerarFaturamento = ctk.CTkButton(self.frameTelaCadastros, text="Transportadoras", width=300, corner_radius=5, font=("Arial", 18), command=self)
        self.botaoGerarFaturamento.place(relx=0.33, y=300, anchor="center")

        # botão para voltar para a tela
        self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaCadastros, text="Voltar", width=200, corner_radius=5, font=("Arial", 18), command=self.frameTelaCadastros.destroy)
        self.botaoGerarOrcamento.place(relx=0.33, y=650, anchor="center")

    # tela para cadastro de produtos e suas especificações
    def telaCadastroProdutos(self):
        self.frameTelaCadastroProduto = ctk.CTkFrame(self, height=700, width=1200, corner_radius=5)
        self.frameTelaCadastroProduto.place(x=40, y=100)     
        self.frameTelaCadastroProduto.grid_propagate(False)

        # titulo
        self.textoCadastro = ctk.CTkLabel(self.frameTelaCadastroProduto, width=950, height=0, text="Cadastrar Produto", font=("Century Gothic bold", 30))
        self.textoCadastro.place(relx=0.5, y=50, anchor="center")

        # Nome
        self.labelNomeProduto = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Nome do produto", font=("Century Gothic bold", 15))
        self.labelNomeProduto.place(x=100, y=100)
        self.nomeProduto = ctk.CTkEntry(self.frameTelaCadastroProduto, placeholder_text="Nome", width=280, corner_radius=5, font=("Century Gothic bold", 20))
        self.nomeProduto.place(x=100, y=130)

        # valor custo
        self.labelValorCusto = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Valor de custo", font=("Century Gothic bold", 15))
        self.labelValorCusto.place(x=400, y=100)
        self.ValorCusto = ctk.CTkEntry(self.frameTelaCadastroProduto, placeholder_text="Custo", width=280, corner_radius=5, font=("Century Gothic bold", 20))
        self.ValorCusto.place(x=400, y=130)

        # valor venda
        self.labelValorVenda = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Valor de venda", font=("Century Gothic bold", 15))
        self.labelValorVenda.place(x=700, y=100)
        self.ValorVenda = ctk.CTkEntry(self.frameTelaCadastroProduto, placeholder_text="Venda", width=280, corner_radius=5, font=("Century Gothic bold", 20))
        self.ValorVenda.place(x=700, y=130)

        # quantidade
        self.labelQuantidade = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Quantidade", font=("Century Gothic bold", 15))
        self.labelQuantidade.place(x=1000, y=100)
        self.Quantidade = ctk.CTkEntry(self.frameTelaCadastroProduto, placeholder_text="0", width=80, corner_radius=5, font=("Century Gothic bold", 20))
        self.Quantidade.place(x=1000, y=130)

        # código interno
        self.labelCodigoInterno = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Código interno", font=("Century Gothic bold", 15))
        self.labelCodigoInterno.place(x=100, y=200)
        self.CodigoInterno = ctk.CTkEntry(self.frameTelaCadastroProduto, placeholder_text="Código", width=280, corner_radius=5, font=("Century Gothic bold", 20))
        self.CodigoInterno.place(x=100, y=230)

        # código NCM
        self.labelNCM = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Código NCM", font=("Century Gothic bold", 15))
        self.labelNCM.place(x=400, y=200)
        self.NCM = ctk.CTkEntry(self.frameTelaCadastroProduto, placeholder_text="NCM", width=200, corner_radius=5, font=("Century Gothic bold", 20))
        self.NCM.place(x=400, y=230)

        # código CFOP
        self.labelCFOP = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Código CFOP", font=("Century Gothic bold", 15))
        self.labelCFOP.place(x=620, y=200)
        self.CFOP = ctk.CTkEntry(self.frameTelaCadastroProduto, placeholder_text="CFOP", width=220, corner_radius=5, font=("Century Gothic bold", 20))
        self.CFOP.place(x=620, y=230)

        # código CEST
        self.labelCEST = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Código CEST", font=("Century Gothic bold", 15))
        self.labelCEST.place(x=860, y=200)
        self.CEST = ctk.CTkEntry(self.frameTelaCadastroProduto, placeholder_text="CEST", width=220, corner_radius=5, font=("Century Gothic bold", 20))
        self.CEST.place(x=860, y=230)

        # código interno
        self.labelOrigemCST = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Origem (CST A)", font=("Century Gothic bold", 15))
        self.labelOrigemCST.place(x=100, y=300)
        self.OrigemCST = ctk.CTkEntry(self.frameTelaCadastroProduto, placeholder_text="Origem", width=310, corner_radius=5, font=("Century Gothic bold", 20))
        self.OrigemCST.place(x=100, y=330)
        
        # descrição
        self.labelDescricao = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Descrição", font=("Century Gothic bold", 15))
        self.labelDescricao.place(x=435, y=300)
        opcoesDescricao = ["Nenhum","Uso consumo", "Mercadoria para revenda", "Peças para reposição"]
        self.Descricao = ctk.CTkComboBox(self.frameTelaCadastroProduto, width=310, corner_radius=5, font=("Century Gothic bold", 20), values=opcoesDescricao)
        self.Descricao.place(x=435, y=330)
        
        # código interno
        self.labelCNPJ = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Origem (CST A)", font=("Century Gothic bold", 15))
        self.labelCNPJ.place(x=770, y=300)
        opcoesCNPJ = ["Nenhum","Multimáquinas", "Polimáquinas", "Refrimaquinas"]
        self.CNPJ = ctk.CTkComboBox(self.frameTelaCadastroProduto, width=310, corner_radius=5, font=("Century Gothic bold", 20), values=opcoesCNPJ)
        self.CNPJ.place(x=770, y=330)

        # voltar
        self.botaoVoltar = ctk.CTkButton(self.frameTelaCadastroProduto, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaCadastroProduto.destroy)
        self.botaoVoltar.place(x=200, y=600)

        # botão de cadastrar
        self.botaoCadastrarUsuario = ctk.CTkButton(self.frameTelaCadastroProduto, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=self.registraProdutoNoBanco)
        self.botaoCadastrarUsuario.place(x=800, y=600)
    

        # cadastro de funcionários/usuários
    
    # tela para cadastros de funcionários
    def telaCadastroFuncionario(self):
        self.frameTelaCadastroFuncionario = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameTelaCadastroFuncionario.place(x=140, y=100)     
        self.frameTelaCadastroFuncionario.grid_propagate(False)


        # ================ widgets da tela cadastro =====================#
        # titulo
        self.textoCadastro = ctk.CTkLabel(self.frameTelaCadastroFuncionario, width=950, height=0, text="Cadastrar funcionário", font=("Century Gothic bold", 30))
        self.textoCadastro.grid(row=0, column=0, padx=10, pady=20)

        # nome
        self.labelNomeFuncionario = ctk.CTkLabel(self.frameTelaCadastroFuncionario, text="Nome", font=("Century Gothic bold", 15))
        self.labelNomeFuncionario.place(x=100, y=100)
        self.nomeFuncionario = ctk.CTkEntry(self.frameTelaCadastroFuncionario, placeholder_text="nomeFuncionario", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.nomeFuncionario.place(x=100, y=130)

        # login
        self.labelLogin = ctk.CTkLabel(self.frameTelaCadastroFuncionario, text="Login para acesso*", font=("Century Gothic bold", 15))   
        self.labelLogin.place(x=100, y=200)
        self.loginFuncionario = ctk.CTkEntry(self.frameTelaCadastroFuncionario, placeholder_text="Login", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.loginFuncionario.place(x=100, y=230)

        # senha
        self.labelSenha = ctk.CTkLabel(self.frameTelaCadastroFuncionario, text="Senha para acesso*", font=("Century Gothic bold", 15))
        self.labelSenha.place(x=550, y=200)
        self.senhaFuncionario = ctk.CTkEntry(self.frameTelaCadastroFuncionario, placeholder_text="Senha", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.senhaFuncionario.place(x=550, y=230)

        # cargo
        self.labelCargo = ctk.CTkLabel(self.frameTelaCadastroFuncionario, text="Cargo", font=("Century Gothic bold", 15))   
        self.labelCargo.place(x=550, y=100)
        opcoes = ["Gerente", "Vendedor(a) interno", "Vendedor(a) externo", "Financeiro"]
        self.cargo = ctk.CTkComboBox(self.frameTelaCadastroFuncionario, width=350, corner_radius=5, font=("Century Gothic bold", 20), values=opcoes)
        self.cargo.place(x=550, y=130)

        # ============== Botões =============== #
        # voltar
        self.botaoVoltar = ctk.CTkButton(self.frameTelaCadastroFuncionario, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaCadastroFuncionario.destroy)
        self.botaoVoltar.place(x=200, y=600)
        
        # registra no bd
        self.botaoCadastrarUsuario = ctk.CTkButton(self.frameTelaCadastroFuncionario, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=self.registraUsuarioNoBanco)
        self.botaoCadastrarUsuario.place(x=600, y=600)

    # tela para cadastrar fornecedores de produtos    
    def telaCadastroFornecedores(self):
        def meDesmarque(checkboxSelecionada):
            match checkboxSelecionada:
                    case 1:
                        self.checkboxInativo.deselect()
                        return 1
                    case 2:
                        self.checkboxAtivo.deselect()
                        return 2
                    case 3:
                        self.checkboxPJ.deselect()
                        self.labelCNPJFornecedor = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="Insira o CNPJ", font=("Century Gothic bold", 15))
                        self.labelCNPJFornecedor.place(x=800, y=200)
                        self.CNPJFornecedor = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="CNPJ", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                        self.CNPJFornecedor.place(x=800, y=230)
                        if hasattr(self, "CPFFornecedor"):
                            self.CNPJFornecedor.destroy()
                        return 3
                    case 4:
                        self.checkboxCPF.deselect()
                        self.labelCPFfornecedor = ctk.CTkLabel(self.frameTelaCadastroFornecedores, width=100, text="Insira o CPF", font=("Century Gothic bold", 15), anchor="w")
                        self.labelCPFfornecedor.place(x=800, y=200)
                        self.CPFfornecedor = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="CPF", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                        self.CPFfornecedor.place(x=800, y=230)
                        if hasattr(self, "CNPJFornecedor"):
                            self.CNPJFornecedor.destroy()
                        return 4
                    case 5:
                        self.checkboxEstrangeira.deselect()
                        return 5
                    case 6:
                        self.checkboxNacional.deselect()
                        return 6
                    case 7:
                        self.checkboxNaoFabricante.deselect()
                        return 7
                    case 8:
                        self.checkboxFabricante.deselect()
                        return 8
                    case 9:
                        self.checkboxNaoRecebeEmail.deselect()
                        self.labelEmailFornecedor = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="Email", font=("Century Gothic bold", 15))
                        self.labelEmailFornecedor.place(x=100, y=400)
                        self.emailFornecedor = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Email", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                        self.emailFornecedor.place(x=100, y=430)
                        return 9
                    case 10:
                        if hasattr(self, "emailFornecedor"):
                            self.emailFornecedor.destroy()
                            gc.collect()

                        if hasattr(self, "labelEmailFornecedor"):
                            self.labelEmailFornecedor.destroy()
                            gc.collect()

                        self.checkboxRecebeEmail.deselect()
                        return 10

        self.frameTelaCadastroFornecedores = ctk.CTkFrame(self, height=700, width=1200, corner_radius=5)
        self.frameTelaCadastroFornecedores.place(x=40, y=100)      
        self.frameTelaCadastroFornecedores.grid_propagate(False)
        
        # titulo
        self.textoCadastroFornecedores = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="Cadastrar fornecedores", font=("Century Gothic bold", 30))
        self.textoCadastroFornecedores.place(relx=0.5, y=40, anchor="center")

        # checkbox ATIVO
        self.checkboxAtivo = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Sim", command=lambda: self.after(10, lambda: meDesmarque(1)))
        self.checkboxAtivo.place(x=150, y=120, anchor="center")
        self.checkboxInativo = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Não", command=lambda: self.after(10, lambda: meDesmarque(2)))
        self.checkboxInativo.place(x=210, y=120, anchor="center")
        self.checkboxAtivoLabel = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="ATIVO?", font=("Century Gothic bold", 14))
        self.checkboxAtivoLabel.place(x=125, y=90, anchor="center")
        
        # checkbox TIPO
        self.checkboxCPF = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="CPF", command=lambda: self.after(10, lambda: meDesmarque(3)))
        self.checkboxCPF.place(x=330, y=120, anchor="center")
        self.checkboxPJ = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="CNPJ", command=lambda: self.after(10, lambda: meDesmarque(4)))
        self.checkboxPJ.place(x=390, y=120, anchor="center")
        self.checkboxCPFouPJLabel = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="TIPO", font=("Century Gothic bold", 14))
        self.checkboxCPFouPJLabel.place(x=295, y=90, anchor="center")

        # checkbox ORIGEM
        self.checkboxNacional = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Nacional", command=lambda: self.after(10, lambda: meDesmarque(5)))
        self.checkboxNacional.place(x=540, y=120, anchor="center")
        self.checkboxEstrangeira = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Estrangeira", command=lambda: self.after(10, lambda: meDesmarque(6)))
        self.checkboxEstrangeira.place(x=630, y=120, anchor="center")
        self.checkboxOrigemLabel = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="ORIGEM", font=("Century Gothic bold", 14))
        self.checkboxOrigemLabel.place(x=520, y=90, anchor="center")

        # checkbox FABRICANTE
        self.checkboxFabricante = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Sim", command=lambda: self.after(10, lambda: meDesmarque(7)))
        self.checkboxFabricante.place(x=800, y=120, anchor="center")
        self.checkboxNaoFabricante = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Não", command=lambda: self.after(10, lambda: meDesmarque(8)))
        self.checkboxNaoFabricante.place(x=860, y=120, anchor="center")
        self.checkboxFabricanteLabel = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="FABRICANTE", font=("Century Gothic bold", 14))
        self.checkboxFabricanteLabel.place(x=795, y=90, anchor="center")

        # checkbox EMAIL
        self.checkboxRecebeEmail = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Sim", command=lambda: self.after(10, lambda: meDesmarque(9)))
        self.checkboxRecebeEmail.place(x=1010, y=120, anchor="center")
        self.checkboxNaoRecebeEmail = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Não", command=lambda: self.after(10, lambda: meDesmarque(10)))
        self.checkboxNaoRecebeEmail.place(x=1090, y=120, anchor="center")
        self.checkboxEmailLabel = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="RECEBE EMAIL?", font=("Century Gothic bold", 14))
        self.checkboxEmailLabel.place(x=1015, y=90, anchor="center")

        # nome real
        self.labelNome = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="Razão social", font=("Century Gothic bold", 15))
        self.labelNome.place(x=100, y=200)
        self.nomeFornecedor = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Nome", width=300, corner_radius=5, font=("Century Gothic bold", 20))
        self.nomeFornecedor.place(x=100, y=230)

        # nome fantasia
        self.labelNome = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="Nome fantasia", font=("Century Gothic bold", 15))
        self.labelNome.place(x=450, y=200)
        self.nomeFantasia = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Nome", width=300, corner_radius=5, font=("Century Gothic bold", 20))
        self.nomeFantasia.place(x=450, y=230)

        # inscrição estadual
        self.labelinscriçãoEstadual = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="Inscrição estadual", font=("Century Gothic bold", 15))
        self.labelinscriçãoEstadual.place(x=100, y=300)
        self.inscriçãoEstadual = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Nº inscrição", width=300, corner_radius=5, font=("Century Gothic bold", 20))
        self.inscriçãoEstadual.place(x=100, y=330)

        # código crt
        self.labelcodigoCRT = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="CRT", font=("Century Gothic bold", 15))
        self.labelcodigoCRT.place(x=450, y=300)
        self.codigoCRT = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Código", width=300, corner_radius=5, font=("Century Gothic bold", 20))
        self.codigoCRT.place(x=450, y=330)

        # Telefone
        self.labelTelefone = ctk.CTkLabel(self.frameTelaCadastroFornecedores, width=100, text="Telefone", font=("Century Gothic bold", 15), anchor="w")
        self.labelTelefone.place(x=800, y=300)
        self.telefone = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Telefone", width=300, corner_radius=5, font=("Century Gothic bold", 20))
        self.telefone.place(x=800, y=330)

        
        # voltar
        self.botaoVoltar = ctk.CTkButton(self.frameTelaCadastroFornecedores, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaCadastroFornecedores.destroy)
        self.botaoVoltar.place(x=200, y=600)
        
        # registra no bd
        self.botaoCadastrarUsuario = ctk.CTkButton(self.frameTelaCadastroFornecedores, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=self.registraFornecedorNoBanco)
        self.botaoCadastrarUsuario.place(x=800, y=600)



    #? ===================== FUNÇÕES DO BANCO DE DADOS ===================== #

    # é chamado quando é cadastrado um novo usuário
    def registraUsuarioNoBanco(self):
        nome = self.nomeFuncionario.get()
        cargo = self.cargo.get()
        login = self.loginFuncionario.get()
        senha = self.senhaFuncionario.get()

        queryInserirFuncionario = "INSERT INTO funcionarios(nome, cargo, login, senha) VALUES(%s, %s, %s, %s);"

        if not nome or not login or not senha : 
            messagebox.showinfo(title="Registro falhou", message="Campos obrigatórios não podem estar em branco")
        else:
            db.cursor.execute(queryInserirFuncionario, (nome, cargo, login, senha,))
            db.conn.commit()
            messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")
            self.frameTelaCadastroFuncionario.destroy()
   
    # é chamado quando se cadastra um novo fornecedor
    def registraFornecedorNoBanco(self):
        # primeiro tem que pegar os checkbox
        ativo = self.checkboxAtivo.get()
        inativo = self.checkboxInativo.get()
        CPFfornecedor = self.checkboxCPF.get()
        PJfornecedor = self.checkboxPJ.get()
        nacional = self.checkboxNacional.get()
        estrangeira = self.checkboxEstrangeira.get()
        fabricante = self.checkboxFabricante.get()
        naoFabricante = self.checkboxNaoFabricante.get()
        recebeEmail = self.checkboxRecebeEmail.get()
        naoRecebeEmail = self.checkboxNaoRecebeEmail.get()

        if hasattr(self, "emailFornecedor"):
            emailFornecedor = self.emailFornecedor.get()
        nomeReal = self.nomeFornecedor.get()
        nomeFantasia = self.nomeFantasia.get()
        inscricaoestadual = self.inscriçãoEstadual.get()
        CRT = self.codigoCRT.get()
        telefone = self.telefone.get()

        if(ativo or inativo) and (CPFfornecedor or PJfornecedor) and (nacional or estrangeira) and (fabricante or naoFabricante) and (naoRecebeEmail or recebeEmail) and emailFornecedor and nomeReal and nomeFantasia and inscricaoestadual and CRT and telefone:
            colunas = []
            valores = []
            if self.checkboxAtivo.get():
                colunas.append("ativo")
                valores.append("'Sim'")
            if self.checkboxInativo.get():
                colunas.append("ativo")
                valores.append("'Não'")
            if self.checkboxCPF.get():
                colunas.append("tipo")
                valores.append("'CPF'")
            if self.checkboxPJ.get():
                colunas.append("tipo")
                valores.append("'CNPJ'")
            if self.checkboxNacional.get():
                colunas.append("origem")
                valores.append("'Nacional'")
            if self.checkboxEstrangeira.get():
                colunas.append("origem")
                valores.append("'Estrangeira'")
            if self.checkboxFabricante.get():
                colunas.append("fabricante")
                valores.append("'Sim'")
            if self.checkboxNaoFabricante.get():
                colunas.append("fabricante")
                valores.append("'Não'")
            if self.checkboxRecebeEmail.get():
                colunas.append("recebe_email")
                valores.append("'Sim'")
            if self.checkboxNaoRecebeEmail.get():
                colunas.append("recebe_email")
                valores.append("'Não'")
                if hasattr(self, "emailFornecedor"):
                    if self.emailFornecedor.get():
                        colunas.append("email")
                        valores.append(f"{self.self.emailFornecedor.get()}")
            if self.nomeFornecedor.get():
                colunas.append("nome_real")
                valores.append(f"'{self.nomeFornecedor.get()}'")
            if self.nomeFantasia.get():
                colunas.append("nome_fantasia")
                valores.append(f"'{self.nomeFantasia.get()}'")
            if self.inscriçãoEstadual.get():
                colunas.append("inscricao_estadual")
                valores.append(f"'{self.inscriçãoEstadual.get()}'")
            if self.codigoCRT.get():
                colunas.append("CRT")
                valores.append(f"'{self.codigoCRT.get()}'")
            if self.telefone.get():
                colunas.append("telefone")
                valores.append(f"'{self.telefone.get()}'")

            query = f"INSERT INTO fornecedores ({', '.join(colunas)}) VALUES ({', '.join(valores)})"
            print("Query gerada:", query)
        
            db.cursor.execute(query)
            db.conn.commit()
        
        else:
            messagebox.showerror("erro", "valores estão em branco")

    # é chamado quando se cadastra um novo usuário
    def registraProdutoNoBanco(self):
        nome = self.nomeProduto.get()
        valorCusto = self.ValorCusto.get()
        valorVenda = self.ValorVenda.get()
        quantidade = self.Quantidade.get()
        codigoInterno = self.CodigoInterno.get()
        NCM = self.NCM.get()
        CFOP = self.CFOP.get()
        CEST = self.CEST.get()
        origemCST = self.OrigemCST.get()
        descricao = self.Descricao.get()
        CNPJ = self.CNPJ.get()
        queryInserirProdutos = "INSERT INTO produtos(nome_do_produto, valor_de_custo, valor_de_venda, quantidade, codigo_interno, codigo_ncm, codigo_cfop, codigo_cest, origem_cst, descricao, CNPJ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        if not(nome and valorCusto and valorVenda and quantidade and codigoInterno and NCM and CFOP and CEST and origemCST and descricao and CNPJ):
            self.frameProdutoNaoCadastrado = ctk.CTkFrame(self, height=60, width=300, corner_radius=5, border_width=2, border_color="red",fg_color="transparent")
            self.frameProdutoNaoCadastrado.place(relx=0.5, y=600, anchor="center")
            self.ProdutoNaoCadastrado = ctk.CTkLabel(self.frameProdutoNaoCadastrado,  text="Prencha os campos obrigatórios", font=("Arial", 18))
            self.ProdutoNaoCadastrado.place(relx=0.5, y=30, anchor="center")
        else:
            db.cursor.execute(queryInserirProdutos, (nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ,))
            db.conn.commit()
            messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")
            self.frameTelaCadastroProduto.destroy()

    # é chamado quando estamos entrando no sistema
    def consultarUsuarioCadastrado(self):
        login = self.login.get()
        senha = self.senha.get()
        queryConsultarLogin = "SELECT cargo FROM funcionarios WHERE login = %s AND senha= %s;"
        db.cursor.execute(queryConsultarLogin, (login, senha,))
        resultados = db.cursor.fetchall()
        print(resultados)

        if senha and login:
            if resultados:
                self.telaAcoes()
            if(self.frameUsuarioNaoCadastrado == None):
                pass
            else:
                self.frameUsuarioNaoCadastrado.destroy()

        
                
        else:
            self.frameUsuarioNaoCadastrado = ctk.CTkFrame(self, height=100, width=300, corner_radius=5, border_width=2, border_color="red",fg_color="transparent")
            self.frameUsuarioNaoCadastrado.place(relx=0.5, y=600, anchor="center")
            self.usuarioNaoCadastrado = ctk.CTkLabel(self.frameUsuarioNaoCadastrado,  text="Esse usuário não foi encontrado.", font=("Arial", 18))
            self.usuarioNaoCadastrado.place(x=20, y=35)


if __name__ == "__main__":
    app = App()
    app.mainloop()
