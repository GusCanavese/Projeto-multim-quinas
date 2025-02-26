import customtkinter as ctk
import db
from tkinter import messagebox
import datetime
import gc
from PIL import Image
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
        self.telaGerarPedido()


    #? ===================== TELAS ===================== #

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
            self.botaogGerarPedido = ctk.CTkButton(self.frameTelaAcoes, text="Gerar pedido", width=300, corner_radius=5, font=("Arial", 18), command=self.telaDefineCnpjDoProduto)
            self.botaogGerarPedido.place(relx=0.33, y=250, anchor="center")

            # botão de consultar estoque # ! ainda não está ativo nem possui uma tela criada para ele 
            self.botaoConsultarEstoque = ctk.CTkButton(self.frameTelaAcoes, text="Consultar estoque", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaoConsultarEstoque.place(relx=0.66, y=250, anchor="center")

            # botão de gerar orçamento # ! ainda não está ativo nem possui uma tela criada para ele 
            self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaAcoes, text="Gerar orçamento", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaoGerarOrcamento.place(relx=0.33, y=200, anchor="center") 
        else:
            # botão do cada
            self.botaoCadastro = ctk.CTkButton(self.frameTelaAcoes, text="Cadastros", width=300, corner_radius=5, font=("Arial", 18), command=self.telaCadastros)
            self.botaoCadastro.place(relx=0.33, y=200, anchor="center")

            # botão de relatório de vendas # ! ainda não está ativo nem possui uma tela criada para ele 
            self.botaoRelatorioDeVendas = ctk.CTkButton(self.frameTelaAcoes, text="Relatório de vendas", width=300, corner_radius=5, font=("Arial", 18), command=self)
            self.botaoRelatorioDeVendas.place(relx=0.66, y=200, anchor="center")

            # botão de gerar pedidos # ! ainda não está ativo nem possui uma tela criada para ele
            self.botaogGerarPedido = ctk.CTkButton(self.frameTelaAcoes, text="Gerar pedido", width=300, corner_radius=5, font=("Arial", 18), command=self.telaDefineCnpjDoProduto)
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

        # botão cadastrar transportadoras  
        self.botaoGerarFaturamento = ctk.CTkButton(self.frameTelaCadastros, text="Transportadoras", width=300, corner_radius=5, font=("Arial", 18), command=self.telaCadastroTransportadoras)
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
        self.labelFuncionaria = ctk.CTkLabel(self.frameTelaCadastroProduto, text="Descrição", font=("Century Gothic bold", 15))
        self.labelFuncionaria.place(x=435, y=300)
        opcoesDescricao = ["Nenhum","Uso consumo", "Mercadoria para revenda", "Peças para reposição"]
        self.Descricao = ctk.CTkComboBox(self.frameTelaCadastroProduto, width=310, corner_radius=5, font=("Century Gothic bold", 20), values=opcoesDescricao)
        self.Descricao.place(x=435, y=330)
        
        # código interno
        self.labelCNPJ = ctk.CTkLabel(self.frameTelaCadastroProduto, text="CNPJ", font=("Century Gothic bold", 15))
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

    # tela para cadastrar fornecedores    
    def telaCadastroFornecedores(self):
        # função criada somente para verificar qual checkbox ta marcado e qual
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
                        self.labelCPFfornecedor = ctk.CTkLabel(self.frameTelaCadastroFornecedores, width=100, text="Insira o CPF", font=("Century Gothic bold", 15), anchor="w")
                        self.labelCPFfornecedor.place(x=800, y=200)
                        self.CPFfornecedor = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="CPF", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                        self.CPFfornecedor.place(x=800, y=230)
                        if hasattr(self, "CNPJFornecedor"):
                            self.CNPJFornecedor.destroy()
                            del self.CNPJFornecedor
                            gc.collect
                        return 3
                    case 4:
                        self.checkboxCPF.deselect()
                        self.labelCNPJFornecedor = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="Insira o CNPJ", font=("Century Gothic bold", 15))
                        self.labelCNPJFornecedor.place(x=800, y=200)
                        self.CNPJFornecedor = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="CNPJ", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                        self.CNPJFornecedor.place(x=800, y=230)
                        if hasattr(self, "CPFfornecedor"):
                            self.CPFfornecedor.destroy()
                            del self.CPFfornecedor
                            gc.collect
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
                            del self.emailFornecedor
                            gc.collect()

                        if hasattr(self, "labelEmailFornecedor"):
                            self.labelEmailFornecedor.destroy()
                            del self.labelEmailFornecedor
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
        self.checkboxEstrangeira.place(x=9, y=120, anchor="center")
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

    # tela para cadastrar transportadoras
    def telaCadastroTransportadoras(self):
        self.frameTelaCadastroTransportadoras = ctk.CTkFrame(self, height=700, width=1200, corner_radius=5)
        self.frameTelaCadastroTransportadoras.place(x=40, y=100)      
        self.frameTelaCadastroTransportadoras.grid_propagate(False)

        def meDesmarqueTransportadora(checkboxSelecionada):
            match checkboxSelecionada:
                case 1:
                    self.checkboxInativoTransportadora.deselect()
                    return 1
                case 2:
                    self.checkboxAtivoTransportadora.deselect()
                    return 2
                case 3:
                    self.checkboxPJTransportadora.deselect()
                    self.labelCPFTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, width=100, text="Insira o CPF", font=("Century Gothic bold", 15), anchor="w")
                    self.labelCPFTransportadora.place(x=800, y=200)
                    self.CPFTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="CPF", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                    self.CPFTransportadora.place(x=800, y=230)
                    if hasattr(self, "CNPJTransportadora"):
                        self.CNPJTransportadora.destroy()
                        del self.CNPJTransportadora
                        gc.collect()
                    return 3
                case 4:
                    self.checkboxCPFTransportadora.deselect()
                    self.labelCNPJTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, text="Insira o CNPJ", font=("Century Gothic bold", 15))
                    self.labelCNPJTransportadora.place(x=800, y=200)
                    self.CNPJTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="CNPJ", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                    self.CNPJTransportadora.place(x=800, y=230)
                    if hasattr(self, "CPFTransportadora"):
                        self.CPFTransportadora.destroy()
                        del self.CPFTransportadora
                        gc.collect()
                    return 4
                case 5:
                    self.checkboxNaoRecebeEmailTransportadora.deselect()
                    self.labelEmailTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, text="Email", font=("Century Gothic bold", 15))
                    self.labelEmailTransportadora.place(x=800, y=300)
                    self.emailTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Email", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                    self.emailTransportadora.place(x=800, y=330)
                    return 5
                case 6:
                    if hasattr(self, "emailTransportadora"):
                        self.emailTransportadora.destroy()
                        del self.emailTransportadora
                        gc.collect()

                    if hasattr(self, "labelEmailTransportadora"):
                        self.labelEmailTransportadora.destroy()
                        del self.labelEmailTransportadora
                        gc.collect()

                    self.checkboxRecebeEmailTransportadora.deselect()
                    return 6

        # titulo
        self.tituloCadastroTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, height=0, text="Cadastrar Transportadoras", font=("Century Gothic bold", 30))
        self.tituloCadastroTransportadora.place(relx=0.5, y=40, anchor="center")

        # checkbox ATIVO
        self.checkboxAtivoTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="Sim", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(1)))
        self.checkboxAtivoTransportadora.place(x=150, y=120, anchor="center")
        self.checkboxInativoTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="Não", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(2)))
        self.checkboxInativoTransportadora.place(x=210, y=120, anchor="center")
        self.checkboxAtivoTransportadoraLabel = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, height=0, text="ATIVO?", font=("Century Gothic bold", 14))
        self.checkboxAtivoTransportadoraLabel.place(x=125, y=90, anchor="center")
        
        # checkbox TIPO
        self.checkboxCPFTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="CPF", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(3)))
        self.checkboxCPFTransportadora.place(x=330, y=120, anchor="center")
        self.checkboxPJTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="CNPJ", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(4)))
        self.checkboxPJTransportadora.place(x=390, y=120, anchor="center")
        self.checkboxCPFouPJTransportadoraLabel = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, height=0, text="TIPO", font=("Century Gothic bold", 14))
        self.checkboxCPFouPJTransportadoraLabel.place(x=295, y=90, anchor="center")

        # checkbox EMAIL
        self.checkboxRecebeEmailTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="Sim", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(5)))
        self.checkboxRecebeEmailTransportadora.place(x=510, y=120, anchor="center")
        self.checkboxNaoRecebeEmailTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="Não", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(6)))
        self.checkboxNaoRecebeEmailTransportadora.place(x=570, y=120, anchor="center")
        self.checkboxEmailTransportadoraLabel = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, height=0, text="RECEBE EMAIL?", font=("Century Gothic bold", 14))
        self.checkboxEmailTransportadoraLabel.place(x=515, y=90, anchor="center")

        # nome real
        self.labelNomeTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, text="Razão social", font=("Century Gothic bold", 15))
        self.labelNomeTransportadora.place(x=100, y=200)
        self.nomeTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Nome", width=300, corner_radius=5, font=("Century Gothic bold", 20))
        self.nomeTransportadora.place(x=100, y=230)

        # nome fantasia
        self.labelNomeTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, text="Nome fantasia", font=("Century Gothic bold", 15))
        self.labelNomeTransportadora.place(x=450, y=200)
        self.nomeFantasiaTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Nome", width=300, corner_radius=5, font=("Century Gothic bold", 20))
        self.nomeFantasiaTransportadora.place(x=450, y=230)

        # inscrição estadual
        self.labelinscriçãoEstadualTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, text="Inscrição estadual", font=("Century Gothic bold", 15))
        self.labelinscriçãoEstadualTransportadora.place(x=100, y=300)
        self.inscriçãoEstadualTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Nº inscrição", width=300, corner_radius=5, font=("Century Gothic bold", 20))
        self.inscriçãoEstadualTransportadora.place(x=100, y=330)

        # Telefone
        self.labelTelefoneTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, width=100, text="Telefone", font=("Century Gothic bold", 15), anchor="w")
        self.labelTelefoneTransportadora.place(x=450, y=300)
        self.telefoneTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Telefone", width=300, corner_radius=5, font=("Century Gothic bold", 20))
        self.telefoneTransportadora.place(x=450, y=330)

        # Descrição
        self.labelDescricaoTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, width=100, text="Descrição", font=("Century Gothic bold", 15), anchor="w")
        self.labelDescricaoTransportadora.place(x=100, y=400)
        self.descricaoTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Descrição", width=1000, corner_radius=5, font=("Century Gothic bold", 20))
        self.descricaoTransportadora.place(x=100, y=430)


        # voltar
        self.botaoVoltar = ctk.CTkButton(self.frameTelaCadastroTransportadoras, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaCadastroTransportadoras.destroy)
        self.botaoVoltar.place(x=200, y=600)
        
        # registra no bd
        self.botaoCadastrarUsuario = ctk.CTkButton(self.frameTelaCadastroTransportadoras, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=self.registraTransportadoraNoBanco)
        self.botaoCadastrarUsuario.place(x=800, y=600)

    #tela para cadastrar clientes
    def telaCadastroClientes(self):
        self.frameTelaCadastroClientes = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameTelaCadastroClientes.place(x=140, y=100)     
        self.frameTelaCadastroClientes.grid_propagate(False)

        # ================ widgets da tela cadastro =====================#
        # titulo
        self.textoCadastro = ctk.CTkLabel(self.frameTelaCadastroClientes, width=950, height=0, text="Cadastrar cliente", font=("Century Gothic bold", 30))
        self.textoCadastro.grid(row=0, column=0, padx=10, pady=20)

        # nome
        self.labelNomeCliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="Nome", font=("Century Gothic bold", 15))
        self.labelNomeCliente.place(x=100, y=100)
        self.nomeCliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="nomeCliente", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.nomeCliente.place(x=100, y=130)

        #CPF/CNPJ
        self.labelCPF_PJcliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="CPF/CNPJ", font=("Century Gothic bold", 15))
        self.labelCPF_PJcliente.place(x=100, y=170)
        self.CPF_PJcliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="Documento", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.CPF_PJcliente.place(x=100, y=200)

        #RG
        self.labelRGcliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="Insira o RG", font=("Century Gothic bold", 15))
        self.labelRGcliente.place(x=100, y=240)
        self.RGcliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="RG", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.RGcliente.place(x=100, y=270)


    #? ===================== FUNÇÕES DA TELA DE GERAR PEDIDO ===================== #

    def telaDefineCnpjDoProduto(self):
        self.frameDefineCnpjDoProduto = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameDefineCnpjDoProduto.place(x=140, y=100)     
        self.frameDefineCnpjDoProduto.grid_propagate(False)
        
        def confereCNPJpreenchido():
            if self.consultaCNPJ.get() != "Nenhum":
                self.telaGerarPedido()
            else:
                if hasattr(self, "labelCNPJNaoPreenchido"):
                    del self.labelCNPJNaoPreenchido
                    gc.collect
                self.labelCNPJNaoPreenchido = ctk.CTkLabel(self.frameDefineCnpjDoProduto, text="Nenhum CNPJ selecionado", text_color="red", font=("Century Gothic bold", 15))
                self.labelCNPJNaoPreenchido.place(relx=0.5, y=400, anchor="center")

        # título
        self.tituloDefineCnpj = ctk.CTkLabel(self.frameDefineCnpjDoProduto, height=0, text="Escolha o cnpj para a venda", font=("Century Gothic bold", 30))
        self.tituloDefineCnpj.place(relx=0.5, y=40, anchor="center")

        # cnpj que será a consulta no banco de dados
        self.labelConsultaCNPJ = ctk.CTkLabel(self.frameDefineCnpjDoProduto, text="Digite o cnpj que a venda será efetuada", font=("Century Gothic bold", 15))
        self.labelConsultaCNPJ.place(relx=0.5, y=300, anchor="center")
        opcoesCNPJ = ["Nenhum","Multimáquinas", "Polimáquinas", "Refrimaquinas"]
        self.consultaCNPJ = ctk.CTkComboBox(self.frameDefineCnpjDoProduto, width=310, corner_radius=5, font=("Century Gothic bold", 20), values=opcoesCNPJ)
        self.consultaCNPJ.place(relx=0.5, y=330, anchor="center")

        # voltar
        self.botaoVoltar = ctk.CTkButton(self.frameDefineCnpjDoProduto, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameDefineCnpjDoProduto.destroy)
        self.botaoVoltar.place(x=200, y=600)
        
        # ir para gerar pedido
        self.botaoCadastrarUsuario = ctk.CTkButton(self.frameDefineCnpjDoProduto, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=confereCNPJpreenchido)
        self.botaoCadastrarUsuario.place(x=600, y=600)

    def telaGerarPedido(self):


        self.frameTelaGerarPedido = ctk.CTkFrame(self, height=700, width=1200, corner_radius=5)
        self.frameTelaGerarPedido.place(x=40, y=100)      
        self.frameTelaGerarPedido.grid_propagate(False)

        # título
        self.textoGerarPedido = ctk.CTkLabel(self.frameTelaGerarPedido,  text="Gerar pedido", font=("Century Gothic bold", 30))
        self.textoGerarPedido.place(relx=0.5, y=40, anchor="center")

        # entrada da do número da venda #!seria bom ser auto increment
        self.labelNumeroDataVenda = ctk.CTkLabel(self.frameTelaGerarPedido,  text="Número da venda", font=("Century Gothic bold", 14))
        self.labelNumeroDataVenda.place(x=30, y=75)
        self.numeroDeVenda = ctk.CTkEntry(self.frameTelaGerarPedido, placeholder_text="Número", width=180, corner_radius=5, font=("Arial", 15))
        self.numeroDeVenda.place(x=30, y=100)

        # entrada da data da criação do pedido
        self.labelDataDeCriacao = ctk.CTkLabel(self.frameTelaGerarPedido,  text="Data de criação", font=("Century Gothic bold", 14))
        self.labelDataDeCriacao.place(x=250, y=75)
        self.dataDeCriacao = ctk.CTkEntry(self.frameTelaGerarPedido, textvariable=ctk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%y")), width=180, corner_radius=5, font=("Arial", 15))
        self.dataDeCriacao.place(x=250, y=100)

        # entrada da data da venda
        self.labelDataDaVenda = ctk.CTkLabel(self.frameTelaGerarPedido,  text="Data da venda", font=("Century Gothic bold", 14))
        self.labelDataDaVenda.place(x=470, y=75)
        self.dataDaVenda = ctk.CTkEntry(self.frameTelaGerarPedido, placeholder_text="DD/MM/AAAA",  width=180, corner_radius=5, font=("Arial", 15))
        self.dataDaVenda.place(x=470, y=100)

        # Status da venda
        self.variavelEmAbertoFechado = "Em aberto"
        self.labelStatusDoPedido = ctk.CTkLabel(self.frameTelaGerarPedido, text="Status", font=("Century Gothic bold", 14))
        self.labelStatusDoPedido.place(x=690, y=75)
        self.statusDoPedido = ctk.CTkEntry(self.frameTelaGerarPedido, textvariable=ctk.StringVar(value=self.variavelEmAbertoFechado), placeholder_text="DD/MM/AAAA", width=180, corner_radius=5, font=("Arial", 15))
        self.statusDoPedido.place(x=690, y=100)

        # qual funcionaria ta fazendo a venda? #! PEGAR O USUÁRIO QUE ESTÁ LOGADO
        self.labelFuncionaria = ctk.CTkLabel(self.frameTelaGerarPedido, text="Vendedor(a)", font=("Century Gothic bold", 15))
        self.labelFuncionaria.place(x=910, y=75)
        opcoesFuncionaria = ["Nenhum","Bruna", "Camila", "Vânia", "Yara", "Mauricio", "Ana Flávia"]
        self.funcionariaPedido = ctk.CTkComboBox(self.frameTelaGerarPedido, width=180, corner_radius=5, font=("Century Gothic bold", 15), values=opcoesFuncionaria)
        self.funcionariaPedido.place(x=910, y=100)


        # pesquisa que fica aparecendo e sumindo os valores que estou pesquisando


        def buscaCliente(event=None):
            nomeDoCliente = self.nomeDoClienteBuscado.get()
            queryBuscaCliente = "SELECT nome FROM clientes WHERE nome LIKE %s"
            db.cursor.execute(queryBuscaCliente, (f"%{nomeDoCliente}%",))
            resultado = db.cursor.fetchall()

            if hasattr(self, 'resultadoLabels'):
                for label in self.resultadoLabels: 
                    label.destroy()

            self.resultadoLabels = []

            yNovo = 230  
            for i, row in enumerate(resultado):
                if i>=5:
                    break
                label = ctk.CTkButton(self.frameTelaGerarPedido, width=280, text=row[0], fg_color="#38343c", font=("Century Gothic bold", 15), command=lambda value=row[0]: selecionaCliente(value))
                label.place(x=30, y=yNovo)
                self.resultadoLabels.append(label)  
                yNovo += 30


            def selecionaCliente(valor):
                self.nomeDoClienteBuscado.delete(0, "end")
                self.nomeDoClienteBuscado.insert(0, valor)
                for label in self.resultadoLabels: 
                    label.destroy()



        iconeLupa = ctk.CTkImage(light_image=Image.open("search.png"), size=(20, 20))
        labelIcone = ctk.CTkButton(self.frameTelaGerarPedido, image=iconeLupa, fg_color="#38343c", width=30, corner_radius=5, command=buscaCliente)
        labelIcone.place(x=30, y=200)
        self.labelNomeDoCliente = ctk.CTkLabel(self.frameTelaGerarPedido, text="Nome do cliente", font=("Century Gothic", 14))
        self.labelNomeDoCliente.place(x=30, y=170)
        self.nomeDoClienteBuscado = ctk.CTkEntry(self.frameTelaGerarPedido, placeholder_text="Nome do Cliente", width=250, corner_radius=5, font=("Arial", 15))
        self.nomeDoClienteBuscado.place(x=60, y=200)
        self.nomeDoClienteBuscado.bind("<KeyRelease>", buscaCliente)  # Chama a busca ao digitar





        #* vai para testes
        # CNPJ, deixar o cnpj que será feita a venda
        self.variavelEmAbertoFechado = "Em aberto"
        self.labelStatusDoPedido = ctk.CTkLabel(self.frameTelaGerarPedido, text="Status", font=("Century Gothic bold", 14))
        self.labelStatusDoPedido.place(x=600, y=175)
        self.statusDoPedido = ctk.CTkEntry(self.frameTelaGerarPedido, textvariable=ctk.StringVar(value=self.variavelEmAbertoFechado), placeholder_text="DD/MM/AAAA", width=180, corner_radius=5, font=("Arial", 15))
        self.statusDoPedido.place(x=600, y=200)

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

        nomeReal = self.nomeFornecedor.get()
        nomeFantasia = self.nomeFantasia.get()
        inscricaoestadual = self.inscriçãoEstadual.get()
        CRT = self.codigoCRT.get()
        telefone = self.telefone.get()
        
        #! coloca a checkbox esteja em branco


        if hasattr(self, "CNPJFornecedor"):
            print("tem cnpj")
            cnpjfornecedor = self.CNPJFornecedor.get()
            print(cnpjfornecedor)
            if hasattr(self, "emailFornecedor"):
                emailFornecedor = self.emailFornecedor.get()
                if emailFornecedor:
                    condicaoEmailFornecedor = (ativo or inativo) and (CPFfornecedor or PJfornecedor) and (nacional or estrangeira) and (fabricante or naoFabricante) and (naoRecebeEmail or recebeEmail) and cnpjfornecedor and emailFornecedor and nomeReal and nomeFantasia and inscricaoestadual and CRT and telefone
                else:
                    messagebox.showerror("erro", "valores estão em branco")
            else:
                condicaoEmailFornecedor = (ativo or inativo) and (CPFfornecedor or PJfornecedor) and (nacional or estrangeira) and (fabricante or naoFabricante) and (naoRecebeEmail or recebeEmail) and nomeReal and nomeFantasia and inscricaoestadual and CRT and telefone
        
        elif hasattr(self, "CPFfornecedor") and self.CPFfornecedor:
            print("tem cpf")
            cpffornecedor = self.CPFfornecedor.get()
            print(cpffornecedor)
            if hasattr(self, "emailFornecedor"):
                emailFornecedor = self.emailFornecedor.get()
                if emailFornecedor:
                    condicaoEmailFornecedor = (ativo or inativo) and (CPFfornecedor or PJfornecedor) and (nacional or estrangeira) and (fabricante or naoFabricante) and (naoRecebeEmail or recebeEmail) and cpffornecedor and emailFornecedor and nomeReal and nomeFantasia and inscricaoestadual and CRT and telefone
                else:
                    messagebox.showerror("erro", "valores estão em branco")
            else:
                condicaoEmailFornecedor = (ativo or inativo) and (CPFfornecedor or PJfornecedor) and (nacional or estrangeira) and (fabricante or naoFabricante) and (naoRecebeEmail or recebeEmail) and nomeReal and nomeFantasia and inscricaoestadual and CRT and telefone
        else:
            messagebox.showerror("erro", "valores estão em branco")


        if condicaoEmailFornecedor:
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
                if self.CPFfornecedor.get():
                    colunas.append("CPF")
                    valores.append(f"'{self.CPFfornecedor.get()}'")
            if self.checkboxPJ.get():
                colunas.append("tipo")
                valores.append("'CNPJ'")
                if self.CNPJFornecedor.get():
                    colunas.append("CNPJ")
                    valores.append(f"'{self.CNPJFornecedor.get()}'")
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
                if hasattr(self, "emailFornecedor"):
                    if self.emailFornecedor.get():
                        colunas.append("email")
                        valores.append(f"'{self.emailFornecedor.get()}'")
            if self.checkboxNaoRecebeEmail.get():
                colunas.append("recebe_email")
                valores.append("'Não'")
                print("email nao existe")
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

            messagebox.showinfo("Sucesso", "O fornecedor foi cadastrado com sucesso!")
            self.frameTelaCadastroFornecedores.destroy()
            gc.collect()


        
        else:
            messagebox.showerror("erro", "valores estão em branco")

    # é chamado quando se cadastra um novo produto
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
            self.frameProdutoNaoCadastrado.place(relx=0.5, y=600, )
            self.ProdutoNaoCadastrado = ctk.CTkLabel(self.frameProdutoNaoCadastrado,  text="Prencha os campos obrigatórios", font=("Arial", 18))
            self.ProdutoNaoCadastrado.place(relx=0.5, y=30, anchor="center")
        else:
            db.cursor.execute(queryInserirProdutos, (nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ,))
            db.conn.commit()
            messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")
            self.frameTelaCadastroProduto.destroy()

    # é chamado ao cadastrar uma transportadora 
    def registraTransportadoraNoBanco(self):
        # pegando checkbox
        ativoTransportadora   = self.checkboxAtivoTransportadora.get()
        inativoTransportadora = self.checkboxInativoTransportadora.get()
        varCPFTransportadora = self.checkboxCPFTransportadora.get()
        PJTransportadora = self.checkboxPJTransportadora.get()
        recebeEmailTransportadora = self.checkboxRecebeEmailTransportadora.get()
        naoRecebeEmailTransportadora = self.checkboxNaoRecebeEmailTransportadora.get()

        # pegando entradas
        nomeTransportadora = self.nomeTransportadora.get()
        nomeFantasiaTranportadora = self.nomeFantasiaTransportadora.get()
        inscricaoEstadualtransportadora = self.inscriçãoEstadualTransportadora.get()
        telefoneTransportadora = self.telefoneTransportadora.get()
        descricaoTransportadora = self.descricaoTransportadora.get()

        if hasattr(self, "CNPJTransportadora") and self.CNPJTransportadora:
            print("tem cnpj")
            cnpjTransportadora = self.CNPJTransportadora.get()
            if hasattr(self, "emailTransportadora"):
                print("tem email")
                varEmailTransportadora = self.emailTransportadora.get()
                if varEmailTransportadora:
                    condicaoQueryTransportadora = (ativoTransportadora or inativoTransportadora) and (varCPFTransportadora or PJTransportadora) and (recebeEmailTransportadora or naoRecebeEmailTransportadora) and nomeTransportadora and nomeFantasiaTranportadora and inscricaoEstadualtransportadora and telefoneTransportadora and descricaoTransportadora and cnpjTransportadora and varEmailTransportadora
                else:
                    messagebox.showerror("erro", "campos estão em branco")
            else:
                condicaoQueryTransportadora = (ativoTransportadora or inativoTransportadora) and (varCPFTransportadora or PJTransportadora) and (recebeEmailTransportadora or naoRecebeEmailTransportadora) and nomeTransportadora and nomeFantasiaTranportadora and inscricaoEstadualtransportadora and telefoneTransportadora and descricaoTransportadora and cnpjTransportadora

        elif hasattr(self, "CPFTransportadora") and self.CPFTransportadora:
            print("tem cpf")
            cpfTransportadora = self.CPFTransportadora.get()
            if hasattr(self, "emailTransportadora"):
                print("tem email")
                varEmailTransportadora = self.emailTransportadra.get()
                if varEmailTransportadora:
                    condicaoQueryTransportadora = (ativoTransportadora or inativoTransportadora) and (varCPFTransportadora or PJTransportadora) and (recebeEmailTransportadora or naoRecebeEmailTransportadora) and nomeTransportadora and nomeFantasiaTranportadora and inscricaoEstadualtransportadora and telefoneTransportadora and descricaoTransportadora and cpfTransportadora and varEmailTransportadora
                else:
                    messagebox.showerror("erro", "campos estão em branco")
            else:
                condicaoQueryTransportadora = (ativoTransportadora or inativoTransportadora) and (varCPFTransportadora or PJTransportadora) and (recebeEmailTransportadora or naoRecebeEmailTransportadora) and nomeTransportadora and nomeFantasiaTranportadora and inscricaoEstadualtransportadora and telefoneTransportadora and descricaoTransportadora and cpfTransportadora
        else:
            messagebox.showerror("Erro", "campos estão em branco")
                    

        if condicaoQueryTransportadora:
            colunas = []
            valores = []
            if self.checkboxAtivoTransportadora.get():
                colunas.append("ativo")
                valores.append("'Sim'")
            if self.checkboxInativoTransportadora.get():
                colunas.append("ativo")
                valores.append("'Não'")
            if self.checkboxCPFTransportadora.get():
                colunas.append("tipo")
                valores.append("'CPF'")
                if self.CPFTransportadora.get():
                    colunas.append("CPF")
                    valores.append(f"'{self.CPFTransportadora.get()}'")
            if self.checkboxPJTransportadora.get():
                colunas.append("tipo")
                valores.append("'CNPJ'")
                if self.CNPJTransportadora.get():
                    colunas.append("CNPJ")
                    valores.append(f"'{self.CNPJTransportadora.get()}'")
            if self.checkboxRecebeEmailTransportadora.get():
                colunas.append("recebe_email")
                valores.append("'Sim'")
                if hasattr(self, "emailTransportadora"):
                    if self.emailTransportadora.get():
                        colunas.append("email")
                        valores.append(f"'{self.emailTransportadora.get()}'")
            if self.checkboxNaoRecebeEmailTransportadora.get():
                colunas.append("recebe_email")
                valores.append("'Não'")
                print("email nao existe")
            if self.nomeTransportadora.get():
                colunas.append("nome_real")
                valores.append(f"'{self.nomeTransportadora.get()}'")
            if self.nomeFantasiaTransportadora.get():
                colunas.append("nome_fantasia")
                valores.append(f"'{self.nomeFantasiaTransportadora.get()}'")
            if self.inscriçãoEstadualTransportadora.get():
                colunas.append("inscricao_estadual")
                valores.append(f"'{self.inscriçãoEstadualTransportadora.get()}'")
            if self.telefoneTransportadora.get():
                colunas.append("telefone")
                valores.append(f"'{self.telefoneTransportadora.get()}'")

            query = f"INSERT INTO transportadoras ({', '.join(colunas)}) VALUES ({', '.join(valores)})"
            print(query)

            db.cursor.execute(query)
            db.conn.commit()

            messagebox.showinfo("Sucesso", "A transportadora foi cadastrado com sucesso!")
            self.frameTelaCadastroTransportadoras.destroy()
            gc.collect()
        
        
        else:
            messagebox.showerror("erro", "valores estão em branco")

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
