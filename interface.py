import customtkinter as ctk

import requests
import db
from tkinter import messagebox
import datetime
import gc
from PIL import Image
from geradorDePedido import gerar_recibo
from consultas.select import Buscas
from consultas.insert import Insere
# import random


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
        # self.criaFrames()
        self.resizable(False, False)
        alturaTela = 900
        larguraTela = 1280
        self.geometry(f"{larguraTela}x{alturaTela}+-1500+0")
        self.telaLogin()


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

        self.frameTelaAcoes = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameTelaAcoes.place(x=140, y=100)     
        self.frameTelaAcoes.grid_propagate(False)
        usuarioBloqueado = self.login.get()
        cargo = Buscas.buscaCargoUsuarioBloqueado(usuarioBloqueado)


        
        # título
        self.Acoes = ctk.CTkLabel(self.frameTelaAcoes, width=950, height=0, text="Ações", font=("Century Gothic bold", 30))
        self.Acoes.place(relx=0.5, y=50, anchor="center")

        # condição que bloqueia o acesso dos vendedores externos
        if cargo == (('Vendedor(a) externo',),):
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

            # botão de gerar pedidos
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
    # define em qual loja será chamado o produto
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

    # insere os dados do pedido
    def telaGerarPedido(self):
        self.variavelCnpjBuscado = None
        self.variavelCtkEntry = ctk.StringVar() #esses 2 só inicializam para conseguir usar fora da função
        self.variavelIndiceDoProduto = ctk.StringVar()
        self.quantidadeMaximaPermitida = ctk.StringVar()
        self.variavelDefinidaDePorcentagem = ctk.StringVar()
        self.variavelDefinidaDeReal = ctk.StringVar()
        self.variavelDefinidaDeAcrescimo = ctk.StringVar()
        self.variavelDefinidaDeSubtotal = ctk.StringVar()
        self.variavelDefinidaDeUnidadeDeMedida = ctk.StringVar()
        self.variavelFuncionarioAtual = ctk.StringVar()
        
        self.variavelTotalDescontoReal = ctk.StringVar()
        self.variavelTotalDescontoPorcentagem = ctk.StringVar()
        self.variavelTotalAcrescimo = ctk.StringVar()
        self.variavelTotalSubtotal = ctk.StringVar()
        self.variavelnumeroDoPedido = ctk.StringVar()

        # usuarioLogado = self.login.get()
        self.numeroDoPedido = 0
        self.totalPreco = 0.0
        self.totalQuantidade = 0
        self.totalDescontoReal = 0.0
        self.totalDescontoPorcentagem = 0.0
        self.totalAcrescimo = 0.0
        self.totalSubtotal = 0.0

        # self.variavelFuncionarioAtual.set(usuarioLogado)

        self.variavelSubtotal = 0.00
        self.variavelSubtotalAux = 0.00
        
        def geraNumeroPedido():
            self.numeroDoPedido += 1
            maiorNumero = Buscas.selecionaNumeroPedido()[0]
            if maiorNumero == None:
                maiorNumero = 0 
            numeroDoPedidoSendoCriado = maiorNumero+1
            self.variavelnumeroDoPedido.set(numeroDoPedidoSendoCriado)

        # criação do frame
        self.frameTelaGerarPedido = ctk.CTkFrame(self, height=800, width=1200, corner_radius=5)
       
        self.frameTelaGerarPedido.place(x=40, y=50)      

        # criar canva para itens adicionados
        self.frameParaItens = ctk.CTkScrollableFrame(self.frameTelaGerarPedido, width=1150, height=200, orientation="vertical")
        self.frameParaItens.place(relx=0.5, y=450, anchor="center")

        self.container = ctk.CTkFrame(self.frameParaItens, height=1500)
        self.container.pack(fill="x", padx=1, pady=1)

        self.frameParaItensNoFrame = ctk.CTkFrame(self.frameParaItens, width=1250, height=1500)
        self.frameParaItensNoFrame.place(x=-25, y=-280)

        # frame para calcular os totais no final da pagina
        self.frameTotais = ctk.CTkFrame(self.frameTelaGerarPedido, width=250, height=150)
        self.frameTotais.place(x=650, y=600)

        # frame valor final para finalizar o preço de tudo
        self.frameValorFinal = ctk.CTkFrame(self.frameTelaGerarPedido, width=200, height=150)
        self.frameValorFinal.place(x=950, y=600)
        self.quantidades = []

        self.valoresDosItens = []
        self.totaisDosItens = []

        def salvarValoresDosItens():
            self.valoresDosItens = []

            # Adiciona os valores originais (campos que dão origem aos itens)
              # Verifica se os campos originais existem
            valoresItem = {
                "codigo": 1,
                "descricao": self.entradaProdutoPesquisado.get(),
                "valor_unitario": self.entradaPreco.get() or 0,
                "quantidade": self.entradaQuantdadeItem.get() or 0,
                "unidade": self.entradaUnidadeMedida.get(),
                "desconto_real": self.descontoTotalReal.get() or 0,
                "desconto_porcentagem": self.descontoTotalPorcento.get() or 0,
                "acrescimo": self.entradaAcrescimo.get() or 0,
                "subtotal": self.entradaSubtotal.get() or 0
            }
            self.valoresDosItens.append(valoresItem)

            # Adiciona os valores dos itens já criados
            i=1
            for item in self.itensCriados:
                i+=1
                valoresItem = {
                    "codigo": 1,
                    "descricao": item[1].get(),
                    "valor_unitario": float(item[2].get() or 0),
                    "unidade": item[4].get(),
                    "quantidade": int(item[3].get() or 0),
                    "desconto_real": float(item[5].get() or 0),
                    "desconto_porcentagem": float(item[6].get() or 0),
                    "acrescimo": float(item[7].get() or 0),
                    "subtotal": float(item[8].get() or 0)
                }
                self.valoresDosItens.append(valoresItem)

            self.totaisDosItens = {
                "total_preco": self.totalPreco,
                "total_quantidade": self.totalQuantidade,
                "total_desconto_real": self.totalDescontoReal,
                "total_desconto_porcentagem": self.totalDescontoPorcentagem,
                "total_acrescimo": self.totalAcrescimo,
                "total_subtotal": self.totalSubtotal
            }

            # print(self.valoresDosItens)


        def calcularTotais():
            self.totalPreco = 0.0
            self.totalQuantidade = 0
            self.totalDescontoReal = 0.0
            self.totalDescontoPorcentagem = 0.0
            self.totalAcrescimo = 0.0
            self.totalSubtotal = 0.0

            primeiroCampoDescontoReal = float(self.entradaDescontosReal.get() or 0)  
            self.totalDescontoReal += primeiroCampoDescontoReal  

            primeiroCampoDescontoPorcentagem = float(self.entradaDescontosPorcentagem.get() or 0)  
            self.totalDescontoPorcentagem += primeiroCampoDescontoPorcentagem  

            primeiroCampoAcrescimo = float(self.entradaAcrescimo.get() or 0)  
            self.totalAcrescimo += primeiroCampoAcrescimo  

            primeiroCampoSubtotal = float(self.entradaSubtotal.get() or 0)  
            self.totalSubtotal += primeiroCampoSubtotal  

            for item in self.itensCriados:
                preco = float(item[2].get() or 0)  # entradaPreco
                quantidade = int(item[3].get() or 0)  # entradaQuantidade
                descontoReal = float(item[5].get() or 0)  # entradaDescontosReal
                descontoPorcentagem = float(item[6].get() or 0)  # entradaDescontosPorcentagem
                acrescimo = float(item[7].get() or 0)  # entradaAcrescimo
                subtotal = float(item[8].get() or 0)  # entradaSubtotal

                subtotalCalculado = (preco * quantidade) + acrescimo - descontoReal

                item[8].delete(0, "end")
                item[8].insert(0, f"{subtotalCalculado:.2f}")

                self.totalPreco += preco
                self.totalQuantidade += quantidade
                self.totalDescontoReal += descontoReal
                self.totalDescontoPorcentagem += descontoPorcentagem
                self.totalAcrescimo += acrescimo
                self.totalSubtotal += subtotalCalculado

            self.variavelTotalDescontoReal.set(round(self.totalDescontoReal, 2))
            self.variavelTotalAcrescimo.set(round(self.totalAcrescimo, 2))
            self.variavelTotalDescontoPorcentagem.set(round(self.totalDescontoPorcentagem, 2))
            self.variavelTotalSubtotal.set(round(self.totalSubtotal, 2))
            salvarValoresDosItens()
        
            print(self.quantidades)

        # pesquisa que fica aparecendo e sumindo os valores que estou pesquisando
        def buscaCliente(event=None): 
            calcularTotais()
            nomeDoCliente = self.nomeDoClienteBuscado.get()
            dadosCliente = Buscas.buscaDadosCliente(nomeDoCliente)

            if hasattr(self, 'resultadoLabels'):
                for label in self.resultadoLabels: 
                    label.destroy()

            self.resultadoLabels = []
            
            yNovo = 230  
            for i, row in enumerate(dadosCliente):
                if i >= 3:
                    break
                label = ctk.CTkButton(self.frameTelaGerarPedido, width=280, text=row[0], fg_color="#38343c", font=("Century Gothic bold", 15), command=lambda  nome=row[0], cnpj=row[1]: selecionaCliente(nome, cnpj))
                label.place(x=30, y=yNovo)
                self.resultadoLabels.append(label)  
                yNovo += 30

        # seleciona o nome e o cpf/cnpj 
        def selecionaCliente(nome, cnpj):
            self.nomeDoClienteBuscado.delete(0, "end")
            self.nomeDoClienteBuscado.insert(0, nome)
            self.variavelCnpjBuscado = cnpj
            if cnpj:
                self.variavelCtkEntry.set(self.variavelCnpjBuscado)
            else:
                self.variavelCtkEntry.set("sem valores")
            for label in self.resultadoLabels: 
                label.destroy()

        # pesquisa que fica aparecendo quando digitamos algo no campo do produto
        def buscaProduto(event=None):
            calcularTotais()
            nomeDoProduto = self.entradaProdutoPesquisado.get()
            Buscas.buscaProduto(nomeDoProduto)
            # print(Buscas.buscaProduto(nomeDoProduto))

            if hasattr(self, "resultadoLabelsProduto"):
                for label in self.resultadoLabelsProduto:
                    label.destroy()

            self.resultadoLabelsProduto = []
            yNovo = 362
            
            for i, row in enumerate(Buscas.buscaProduto(nomeDoProduto)):
                if i >=3: break
                label = ctk.CTkButton(self.frameParaItensNoFrame, width=300, text=row[0], fg_color="#38343c", font=("Century Gothic bold", 15), command=lambda nome = row[0], valor = row[1], quantidade=row[2]: selecionaProduto(nome, valor, quantidade))
                label.place(x=82, y=yNovo)
                self.resultadoLabelsProduto.append(label)
                yNovo += 29

            # ações realizadas quando digitamos em cada campo
            self.entradaQuantdadeItem.bind("<KeyRelease>", lambda event: verificaQuantidadeMaxima(self.quantidadeMaximaAtualOriginal))
            self.entradaAcrescimo.bind("<KeyRelease>", lambda event: calcularAlteracoes())
            self.entradaPreco.bind("<KeyRelease>", lambda event: calcularAlteracoes())
            self.entradaDescontosReal.bind("<FocusIn>", lambda event: limparCampo(event, self.entradaDescontosPorcentagem))
            self.entradaDescontosReal.bind("<KeyRelease>", lambda event: calcularAlteracoes())
            self.entradaDescontosPorcentagem.bind("<FocusIn>", lambda event: limparCampo(event, self.entradaDescontosReal))
            self.entradaDescontosPorcentagem.bind("<KeyRelease>", lambda event: calcularAlteracoes())
            self.entradaAcrescimo.bind("<KeyRelease>", lambda event: calcularTotais())
            self.entradaDescontosPorcentagem.bind("<KeyRelease>", lambda event: calcularTotais())
            self.entradaDescontosReal.bind("<KeyRelease>", lambda event: calcularTotais())
            self.entradaSubtotal.bind("<KeyRelease>", lambda event: calcularTotais())
            
        # chamado somente para deixar o campo "desconto" em branco
        def limparCampo(event, campo):
            campo.delete(0, "end")

        # ao selecionar o produto é chamada
        def selecionaProduto(nome, valor, quantidade):
            
            self.entradaProdutoPesquisado.delete(0, "end")
            self.entradaProdutoPesquisado.insert(0, nome)
            
            self.entradaQuantdadeItem.delete(0, "end")
            self.entradaQuantdadeItem.insert(0, 1)

            self.entradaPreco.delete(0,"end")
            self.entradaPreco.insert(0, valor)

            self.entradaUnidadeMedida.delete(0, "end")
            self.entradaUnidadeMedida.insert(0, "UN")

            self.variavelDefinidaDeAcrescimo.set(0.00)
            self.quantidadeMaximaAtualOriginal = quantidade 

            calcularAlteracoes()
            for label in self.resultadoLabelsProduto: 
                label.destroy()
                
            calcularTotais()
            
        # toda alteração realizada o subtotal precisa ser atualizado
        def calcularAlteracoes():
            preco = float(self.entradaPreco.get() or 0)
            acrescimo = float(self.entradaAcrescimo.get() or 0)
            descontoReal = float(self.entradaDescontosReal.get() or 0)      
            descontoPorcentagem = float(self.entradaDescontosPorcentagem.get() or 0)
            if descontoReal:
                self.variavelSubtotal = ((preco * int(self.entradaQuantdadeItem.get())) + acrescimo) - descontoReal
                self.variavelDefinidaDeSubtotal.set(self.variavelSubtotal)
            else:
                descontoPorcentagem = descontoPorcentagem/100
                self.variavelSubtotal = ((preco * int(self.entradaQuantdadeItem.get())) + acrescimo)
                self.variavelSubtotalAux = self.variavelSubtotal
                self.variavelSubtotal = ((preco * int(self.entradaQuantdadeItem.get())) + acrescimo) * descontoPorcentagem
                self.variavelSubtotalAux = self.variavelSubtotalAux - self.variavelSubtotal
                self.variavelDefinidaDeSubtotal.set(self.variavelSubtotalAux)

        # verifica se a quantidade sendo vendida é menor do que a quantidade existente no depósito
        def verificaQuantidadeMaxima(quantidade):
            if quantidade is not None and int(self.entradaQuantdadeItem.get()) > quantidade:
                self.quantidadeMaximaPermitida.set(quantidade)
                labelValorQuanrtidadeMax = ctk.CTkLabel(self, text="poode nao man", fg_color="red", text_color="white", corner_radius=5)
                labelValorQuanrtidadeMax.pack(pady=10)
                self.after(3000, labelValorQuanrtidadeMax.destroy)
                calcularAlteracoes()

            else:
                calcularAlteracoes()
                print(self.variavelSubtotal)
                print("Menor, tá de boa")

        # remove cada item, e o coloca novamente no seu lugar e no seu index na lista
        def removerItem(index):
            if 0 <= index < len(self.itensCriados):  
                for widget in self.itensCriados[index]:
                    if widget:  
                        widget.destroy()  
                self.itensCriados.pop(index)  

                
                for i in range(index, len(self.itensCriados)):
                    y_pos = self.yInicial + (i * self.yFuturoBotao)
                    self.itensCriados[i][0].place(y=y_pos)
                    for widget in self.itensCriados[i][1:]:  
                        if widget:
                            widget.place(y=y_pos)

                
                if self.itensCriados:
                    ultimoItem = self.itensCriados[-1]
                    if ultimoItem[-1] is None:  
                        botaoRemover = ctk.CTkButton(
                            self.frameParaItensNoFrame, text="X", width=30, height=30, fg_color="red", 
                            corner_radius=5, command=lambda idx=len(self.itensCriados) - 1: removerItem(idx)
                        )
                        botaoRemover.place(x=1140, y=self.yInicial + ((len(self.itensCriados) - 1) * self.yFuturoBotao))
                        ultimoItem[-1] = botaoRemover  
                self.yAtualBotao -= self.yFuturoBotao
                self.botaoAdicionarItem.place(x=1011, y=self.yAtualBotao + 40)
       
        def adicionarItem():
            if self.itensCriados:
                ultimoItem = self.itensCriados[-1]
                camposObrigatorios = [
                    ultimoItem[1].get(),  
                    ultimoItem[2].get(),  
                    ultimoItem[3].get(),  
                    ultimoItem[4].get()   
                ]

                if any(campo == "" for campo in camposObrigatorios):
                    labelValorPreenchaCampos = ctk.CTkLabel(self, text="Preencha todos os campos", fg_color="red", text_color="white", corner_radius=5)
                    labelValorPreenchaCampos.pack(pady=10)
                    self.after(3000, labelValorPreenchaCampos.destroy)
                    return  

            numeroItem = len(self.itensCriados) + 1

            labelNumeroItem = ctk.CTkLabel(self.frameParaItensNoFrame, text=f"{numeroItem+1}", fg_color="#38343c", height=30, width=50, corner_radius=0)
            labelNumeroItem.place(x=30, y=self.yAtualBotao)

            entradaProdutoPesquisado = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=200, corner_radius=0)
            entradaProdutoPesquisado.place(x=82, y=self.yAtualBotao)

            entradaPreco = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
            entradaPreco.place(x=284, y=self.yAtualBotao)

            entradaQuantidade = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
            entradaQuantidade.place(x=406, y=self.yAtualBotao)

            entradaUnidadeMedida = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
            entradaUnidadeMedida.place(x=528, y=self.yAtualBotao)

            entradaDescontosReal = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
            entradaDescontosReal.place(x=650, y=self.yAtualBotao)

            entradaDescontosPorcentagem = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
            entradaDescontosPorcentagem.place(x=772, y=self.yAtualBotao)

            entradaAcrescimo = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
            entradaAcrescimo.place(x=894, y=self.yAtualBotao)

            entradaSubtotal = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
            entradaSubtotal.place(x=1016, y=self.yAtualBotao)

            botaoRemover = ctk.CTkButton(self.frameParaItensNoFrame, text="X", width=30, height=30, fg_color="red", corner_radius=5, command=lambda idx=len(self.itensCriados): removerItem(idx))
            botaoRemover.place(x=1140, y=self.yAtualBotao)

            if self.itensCriados:
                ultimoItem = self.itensCriados[-1]
                if ultimoItem[-1]: 
                    ultimoItem[-1].destroy() 
                    ultimoItem[-1] = None 

            self.itensCriados.append([
                labelNumeroItem, entradaProdutoPesquisado, entradaPreco, entradaQuantidade, entradaUnidadeMedida,
                entradaDescontosReal, entradaDescontosPorcentagem, entradaAcrescimo, entradaSubtotal, botaoRemover
            ])

            calcularAlteracoesParaItem(numeroItem - 1)

            self.yAtualBotao += self.yFuturoBotao
            self.botaoAdicionarItem.place(x=1011, y=self.yAtualBotao + 20)

            entradaProdutoPesquisado.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: buscaProdutoParaItem(idx))
            entradaPreco.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: calcularAlteracoesParaItem(idx))
            entradaQuantidade.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: verificaQuantidadeMaximaParaItem(self.quantidadeMaximaAtualItem, idx))
            entradaDescontosReal.bind("<FocusIn>", lambda event, idx=len(self.itensCriados) - 1: limparCampo(event, self.itensCriados[idx][6]))
            entradaDescontosReal.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: calcularAlteracoesParaItem(idx))
            entradaDescontosPorcentagem.bind("<FocusIn>", lambda event, idx=len(self.itensCriados) - 1: limparCampo(event, self.itensCriados[idx][5]))
            entradaDescontosPorcentagem.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: calcularAlteracoesParaItem(idx))
            entradaAcrescimo.bind("<KeyRelease>", lambda event, idx=len(self.itensCriados) - 1: calcularAlteracoesParaItem(idx))
            calcularTotais()

        # busca o produto no banco de dados
        def buscaProdutoParaItem(index):
            nomeDoProduto = self.itensCriados[index][1].get()
            Buscas.buscaProduto(nomeDoProduto)
            print(Buscas.buscaProduto(nomeDoProduto))


            if hasattr(self, "resultadoLabelsProduto"):
                for label in self.resultadoLabelsProduto:
                    label.destroy()

            self.resultadoLabelsProduto = []

            yNovo = 394 + (index*32)
            
            for i, row in enumerate(Buscas.buscaProduto(nomeDoProduto)):
                if i >= 3: break
                label = ctk.CTkButton(self.frameParaItensNoFrame, width=300, text=row[0], fg_color="#38343c", font=("Century Gothic bold", 15), command=lambda nome=row[0], valor=row[1], quantidade=row[2]: selecionaProdutoParaItem(nome, valor, quantidade, index))
                label.place(x=82, y=yNovo)
                self.quantidades.append(row[2])

                self.resultadoLabelsProduto.append(label)
                yNovo += 29
            calcularTotais()

        # ao clicar no produto ele é selecionado 
        def selecionaProdutoParaItem(nome, valor, quantidade, index):

            self.itensCriados[index][1].delete(0, "end")
            self.itensCriados[index][1].insert(0, nome)

            self.itensCriados[index][3].delete(0, "end")
            self.itensCriados[index][3].insert(0, 1)

            self.itensCriados[index][2].delete(0, "end")
            self.itensCriados[index][2].insert(0, valor)

            self.itensCriados[index][4].delete(0, "end")
            self.itensCriados[index][4].insert(0, "UN")

            self.itensCriados[index][7].delete(0, "end")
            self.itensCriados[index][7].insert(0, 0.00)

            self.quantidadeMaximaAtualItem = quantidade

            print(quantidade)

            calcularAlteracoesParaItem(index)

            for label in self.resultadoLabelsProduto:
                label.destroy()

            calcularTotais()

        # sempre que o campo for alterado, serão realizadas operações para modificar seu subtotal
        def calcularAlteracoesParaItem(index):
            preco = float(self.itensCriados[index][2].get() or 0)
            quantidade = int(self.itensCriados[index][3].get() or 0)
            acrescimo = float(self.itensCriados[index][7].get() or 0)
            descontoReal = float(self.itensCriados[index][5].get() or 0)
            descontoPorcentagem = float(self.itensCriados[index][6].get() or 0)

            if descontoReal:
                subtotal = ((preco * quantidade) + acrescimo) - descontoReal
            else:
                descontoPorcentagem = descontoPorcentagem / 100
                subtotal = ((preco * quantidade) + acrescimo)
                subtotalAux = subtotal
                subtotal = ((preco * quantidade) + acrescimo) * descontoPorcentagem
                subtotalAux = subtotalAux - subtotal
                subtotal = subtotalAux

            self.itensCriados[index][8].delete(0, "end")
            self.itensCriados[index][8].insert(0, f"{subtotal:.2f}")
            calcularTotais()

        # verifica se a quantidade da venda é maior que a presente do estoque
        def verificaQuantidadeMaximaParaItem(quantidade, index):
            quantidadeDigitada = int(self.itensCriados[index][3].get() or 0)

            if quantidade is not None and quantidadeDigitada > quantidade:
                self.itensCriados[index][3].delete(0, "end")  
                self.itensCriados[index][3].insert(0, str(quantidade))  

                labelValorQuantidadeMax = ctk.CTkLabel(self, text="Quantidade excede o estoque", fg_color="red", text_color="white", corner_radius=5)
                labelValorQuantidadeMax.pack(pady=10)
                self.after(3000, labelValorQuantidadeMax.destroy)  

                calcularAlteracoesParaItem(index)
            else:
                self.quantidades.clear()
                calcularAlteracoesParaItem(index)
                print("Quantidade válida")
    
        def buscaCep(cepPassado, numero):
            url = f"https://cep.awesomeapi.com.br/json/{cepPassado}"
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                endereco_completo = f"{dados.get('address', '')} - {numero} - {dados.get('district', '')} - {dados.get('city', '')} - {dados.get('state', '')}"
                if numero == '':
                    messagebox.showerror(title="Não encontrado", message="Campo 'Número não deve ficar em branco'")
                else:
                    self.entradaEnderecoNoPedido.delete(0, ctk.END)
                    self.entradaEnderecoNoPedido.insert(0, endereco_completo)
            else:
                messagebox.showerror(title="Não encontrado", message="CEP não foi encontrado")
        

        self.yAtualBotao = 364
        self.yFuturoBotao = 32
        self.yInicial = 364
        self.itensCriados = []

        self.botaoAdicionarItem = ctk.CTkButton(self.frameParaItensNoFrame, text="Adicionar Item", width=130, height=20, corner_radius=5, font=("Arial", 15), command=adicionarItem)
        self.botaoAdicionarItem.place(x=1011, y=380)

        # título
        geraNumeroPedido()
        self.textoGerarPedido = ctk.CTkLabel(self.frameTelaGerarPedido,  text="Gerar pedido", font=("Century Gothic bold", 30))
        self.textoGerarPedido.place(relx=0.5, y=40, anchor="center")

        # entrada da do número da venda #!seria bom ser auto increment
        self.labelNumeroDataVenda = ctk.CTkLabel(self.frameTelaGerarPedido,  text="Número da venda", font=("Century Gothic bold", 14))
        self.labelNumeroDataVenda.place(x=30, y=75)
        self.numeroDeVenda = ctk.CTkEntry(self.frameTelaGerarPedido, textvariable = self.variavelnumeroDoPedido, placeholder_text="Número", width=180, corner_radius=5, font=("Arial", 15))
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
        self.funcionariaPedido = ctk.CTkEntry(self.frameTelaGerarPedido, textvariable=self.variavelFuncionarioAtual, width=180, corner_radius=5, font=("Century Gothic bold", 15))
        self.funcionariaPedido.place(x=910, y=100)

        iconeLupa = ctk.CTkImage(light_image=Image.open("arquivos/search.png"), size=(20, 20))
        labelIcone = ctk.CTkButton(self.frameTelaGerarPedido, image=iconeLupa, fg_color="#38343c", width=30, corner_radius=5, command=buscaCliente)
        labelIcone.place(x=30, y=180)

        # nome do cliente
        self.labelNomeDoCliente = ctk.CTkLabel(self.frameTelaGerarPedido, text="Nome do cliente", font=("Century Gothic", 14))
        self.labelNomeDoCliente.place(x=30, y=150)
        self.nomeDoClienteBuscado = ctk.CTkEntry(self.frameTelaGerarPedido,  placeholder_text="Nome do Cliente", width=370, corner_radius=5, font=("Arial", 15))
        self.nomeDoClienteBuscado.place(x=60, y=180)
        self.nomeDoClienteBuscado.bind("<KeyRelease>", buscaCliente)  # Chama a busca ao digitar
        self.frameTelaGerarPedido.bind("<Button-1>", lambda event: [label.destroy() for label in getattr(self, 'resultadoLabels', [])]) # exclui os valores da pesquisa de nome de usuário quando clicar em outro lgar no frame

        # cpf ou cnpj do cliente
        self.labelCPFCliente = ctk.CTkLabel(self.frameTelaGerarPedido,  text="CPF/CNPJ", font=("Century Gothic bold", 14))
        self.labelCPFCliente.place(x=470, y=150)
        self.CPFCliente = ctk.CTkEntry(self.frameTelaGerarPedido, textvariable=self.variavelCtkEntry, width=180, corner_radius=5, font=("Arial", 15))
        self.CPFCliente.place(x=470, y=180)

        # cep paraa buscar endereço
        self.labelCEP = ctk.CTkLabel(self.frameTelaGerarPedido, text="CEP", font=("Century Gothic bold", 14))
        self.labelCEP.place(x=690, y=150)
        self.entradaCEP = ctk.CTkEntry(self.frameTelaGerarPedido, width=180, corner_radius=5, font=("Arial", 15))
        self.entradaCEP.place(x=690, y=180)

        self.labelNumero = ctk.CTkLabel(self.frameTelaGerarPedido, text="Nº", font=("Century Gothic bold", 14))
        self.labelNumero.place(x=910, y=150)
        self.entradaNumero = ctk.CTkEntry(self.frameTelaGerarPedido, width=60, corner_radius=5, font=("Arial", 15))
        self.entradaNumero.place(x=910, y=180)

        # cep paraa buscar endereço
        self.labelEnderecoNoPedido = ctk.CTkLabel(self.frameTelaGerarPedido, text="Endereço", font=("Century Gothic bold", 14))
        self.labelEnderecoNoPedido.place(x=470, y=235)
        self.entradaEnderecoNoPedido = ctk.CTkEntry(self.frameTelaGerarPedido, width=400, corner_radius=5, font=("Arial", 13))
        self.entradaEnderecoNoPedido.place(x=470, y=260)


        # REFERENCIA    
        self.labelReferenciaEnderecoEntrega = ctk.CTkLabel(self.frameTelaGerarPedido, text="Referencia", font=("Century Gothic bold", 14))
        self.labelReferenciaEnderecoEntrega.place(x=910, y=235)
        self.entradaReferenciaEnderecoEntrega = ctk.CTkEntry(self.frameTelaGerarPedido, width=180, corner_radius=5, font=("Arial", 13))
        self.entradaReferenciaEnderecoEntrega.place(x=910, y=260)



            

        # botão buscacep
        self.botaoBuscaCEP = ctk.CTkButton(self.frameTelaGerarPedido, text="Buscar CEP", width=30, corner_radius=5, command=lambda:buscaCep(self.entradaCEP.get(), self.entradaNumero.get()))
        self.botaoBuscaCEP.place(x=1015, y=180)




        # item
        self.labelNumeroItem = ctk.CTkLabel(self.frameParaItensNoFrame, text="Item", fg_color="#38343c",  height=30, width=50, corner_radius=0)
        self.labelNumeroItem.place(x=30, y=300)
        self.NumeroItem = ctk.CTkLabel(self.frameParaItensNoFrame, text="1", fg_color="#38343c",  height=30, width=50, corner_radius=0)
        self.NumeroItem.place(x=30, y=332)

        # produto
        self.LabelProdutoPesquisado = ctk.CTkLabel(self.frameParaItensNoFrame, text="Produto", fg_color="#38343c",  height=30, width=200, corner_radius=0)
        self.LabelProdutoPesquisado.place(x=82, y=300)
        self.entradaProdutoPesquisado = ctk.CTkEntry(self.frameParaItensNoFrame,  height=30, width=200, corner_radius=0)
        self.entradaProdutoPesquisado.place(x=82, y=332)
        self.entradaProdutoPesquisado.bind("<KeyRelease>", buscaProduto)
        self.frameTelaGerarPedido.bind("<Button-1>", lambda event: [label.destroy() for label in getattr(self, 'resultadoLabelsProduto', [])]) # exclui os valores da pesquisa de nome de usuário quando clicar em outro lgar no frame


        # detalhes
        self.labelPreco = ctk.CTkLabel(self.frameParaItensNoFrame, text="Preço", fg_color="#38343c",  height=30, width=120, corner_radius=0)
        self.labelPreco.place(x=284, y=300)
        self.entradaPreco = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
        self.entradaPreco.place(x=284, y=332)

        # Quantidade
        self.labelQuantdadeItem = ctk.CTkLabel(self.frameParaItensNoFrame, text="Quantidade", fg_color="#38343c",  height=30, width=120, corner_radius=0)
        self.labelQuantdadeItem.place(x=406, y=300)
        self.entradaQuantdadeItem = ctk.CTkEntry(self.frameParaItensNoFrame, textvariable=self.quantidadeMaximaPermitida, height=30, width=120, corner_radius=0)
        self.entradaQuantdadeItem.place(x=406, y=332)


        # Unidade de Medida
        self.labelUnidadeMedida = ctk.CTkLabel(self.frameParaItensNoFrame,  text="Unidade de medida", fg_color="#38343c",  height=30, width=120, corner_radius=0)
        self.labelUnidadeMedida.place(x=528, y=300)
        self.entradaUnidadeMedida = ctk.CTkEntry(self.frameParaItensNoFrame, height=30, width=120, corner_radius=0)
        self.entradaUnidadeMedida.place(x=528, y=332)

        # Desconto Real
        self.labelDescontosReal = ctk.CTkLabel(self.frameParaItensNoFrame, text="Desconto($)", fg_color="#38343c",  height=30, width=120, corner_radius=0)
        self.labelDescontosReal.place(x=650, y=300)
        self.entradaDescontosReal = ctk.CTkEntry(self.frameParaItensNoFrame, textvariable=self.variavelDefinidaDeReal, height=30, width=120, corner_radius=0)
        self.entradaDescontosReal.place(x=650, y=332)

        # Desconto porcentagem
        self.labelDescontosPorcentagem = ctk.CTkLabel(self.frameParaItensNoFrame, text="Desconto(%)", fg_color="#38343c",  height=30, width=120, corner_radius=0)
        self.labelDescontosPorcentagem.place(x=772, y=300)
        self.entradaDescontosPorcentagem = ctk.CTkEntry(self.frameParaItensNoFrame, textvariable=self.variavelDefinidaDePorcentagem, height=30, width=120, corner_radius=0)
        self.entradaDescontosPorcentagem.place(x=772, y=332)

        # Acrescimo
        self.labelAcrescimo = ctk.CTkLabel(self.frameParaItensNoFrame, text="Acrescimo", fg_color="#38343c",  height=30, width=120, corner_radius=0)
        self.labelAcrescimo.place(x=894, y=300)
        self.entradaAcrescimo = ctk.CTkEntry(self.frameParaItensNoFrame, textvariable=self.variavelDefinidaDeAcrescimo, height=30, width=120, corner_radius=0)
        self.entradaAcrescimo.place(x=894, y=332)

        # Subtotal
        self.labelSubtotal = ctk.CTkLabel(self.frameParaItensNoFrame, text="Subtotal", fg_color="#38343c",  height=30, width=120, corner_radius=0)
        self.labelSubtotal.place(x=1016, y=300)
        self.entradaSubtotal = ctk.CTkEntry(self.frameParaItensNoFrame, textvariable=self.variavelDefinidaDeSubtotal, height=30, width=120, corner_radius=0)
        self.entradaSubtotal.place(x=1016, y=332)


        # área de texto observações
        self.labelAreaTexto = ctk.CTkLabel(self.frameTelaGerarPedido, text="Observações", height=30, font=("Century Gothic", 15))
        self.labelAreaTexto.place(x=30, y=570)
        self.textArea = ctk.CTkTextbox(self.frameTelaGerarPedido, width=300, height=150, corner_radius=8, wrap="word")
        self.textArea.insert("0.0","É necessário a apresentação do recibo de venda para que a vendedora abra a assistência técnica, se necessário. Não devolvemos dinheiro. \n\nCONDIÇÃO DE PAGAMENTO:\nTROCA: \nENTREGA:")
        self.textArea.place(x=30, y=600)

        # área de texto enrtrega
        self.labelAreaTexto = ctk.CTkLabel(self.frameTelaGerarPedido, text="Observações da entrega", height=30, font=("Century Gothic", 15))
        self.labelAreaTexto.place(x=360, y=570)
        self.textArea = ctk.CTkTextbox(self.frameTelaGerarPedido, width=250, height=150, corner_radius=8, wrap="word")
        self.textArea.insert("0.0","Referências de endereço, localização, etc")
        self.textArea.place(x=360, y=600)

        # área de totais
        self.labelAreaTotais = ctk.CTkLabel(self.frameTelaGerarPedido, text="Totais", font=("Century Gothic", 15))
        self.labelAreaTotais.place(x=650, y=570)

        self.labelDescontoTotalPorcento = ctk.CTkLabel(self.frameTotais, text="Desconto total(%)", font=("Century Gothic", 11))
        self.labelDescontoTotalPorcento.place(x=10, y=-3)
        self.descontoTotalPorcento = ctk.CTkEntry(self.frameTotais, state="readonly", textvariable=self.variavelTotalDescontoPorcentagem, height=20, width=100, corner_radius=0)
        self.descontoTotalPorcento.place(x=10, y=20)

        self.labelDescontoTotalReal = ctk.CTkLabel(self.frameTotais, text="Desconto total($)", font=("Century Gothic", 11))
        self.labelDescontoTotalReal.place(x=140, y=-3)
        self.descontoTotalReal = ctk.CTkEntry(self.frameTotais, state="readonly", textvariable=self.variavelTotalDescontoReal, height=20, width=100, corner_radius=0)
        self.descontoTotalReal.place(x=140, y=20)

        self.labelDescontoTotalPorcento = ctk.CTkLabel(self.frameTotais, text="Acréscimo total",  font=("Century Gothic", 11))
        self.labelDescontoTotalPorcento.place(x=10, y=43)
        self.descontoTotalPorcento = ctk.CTkEntry(self.frameTotais, state="readonly", textvariable=self.variavelTotalAcrescimo, height=20, width=100, corner_radius=0)
        self.descontoTotalPorcento.place(x=10, y=65)

        self.labelValorFrete = ctk.CTkLabel(self.frameTotais, text="Valor frete",  font=("Century Gothic", 11))
        self.labelValorFrete.place(x=140, y=43)
        self.valorFrete = ctk.CTkEntry(self.frameTotais, height=20, width=100, corner_radius=0)
        self.valorFrete.place(x=140, y=65)

        self.labelValorFinal = ctk.CTkLabel(self.frameValorFinal, text="TOTAL:", font=("Century Gothic", 20))
        self.labelValorFinal.place(x=0, y=0)
        self.valorFinal = ctk.CTkEntry(self.frameValorFinal, textvariable=self.variavelTotalSubtotal, corner_radius=0, height=40, width=180)
        self.valorFinal.place(x=10, y=50)

        # voltar
        self.botaoVoltarTelaGerarPedido = ctk.CTkButton(self.frameTelaGerarPedido, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaGerarPedido.destroy)
        self.botaoVoltarTelaGerarPedido.place(x=30, y=760)

        # gerar pedido
        self.botaoGerarPedido = ctk.CTkButton(self.frameTelaGerarPedido, text="Gerar pedido", width=200, corner_radius=5, font=("Arial", 15), command=self.telaImprimirPedido)
        self.botaoGerarPedido.place(x=950, y=760)

    # gera o pedido
    def telaImprimirPedido(self):
        dataAgora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        resultados = Buscas.buscaDadosCliente(self.nomeDoClienteBuscado.get())
        for i, row in enumerate(resultados):
            telefone = row[2]
        print(self.valoresDosItens)
        self.dados = {
            "frete":self.valorFrete,
            "valor_total": self.valorFinal,
            "total_subtotal":self.totalSubtotal,
            "total_acrescimo":self.totalAcrescimo,
            "total_desc_real":self.variavelTotalDescontoReal,
            "total_desc_porc":self.variavelTotalDescontoPorcentagem,
            "total_quantidade": self.totalQuantidade,
            "itens": self.valoresDosItens,
            "referencia": self.entradaReferenciaEnderecoEntrega.get(),
            "endereco": self.entradaEnderecoNoPedido.get(),
            "cep": self.entradaCEP.get(),
            "telefone": telefone,
            "cnpj": self.CPFCliente.get(),
            "cpf": self.CPFCliente.get(),
            "destinatario": self.entradaEnderecoNoPedido.get(),
            "data_confirmacao":self.dataDaVenda.get() ,
            "numero_recibo":self.numeroDeVenda.get(),
            "data_emissao":dataAgora,
            "subtotal": self.totalSubtotal,
        }

        gerar_recibo("Pedido.pdf", self.dados)
        

    #? ===================== FUNÇÕES DO BANCO DE DADOS ===================== #

    # é chamado quando é cadastrado um novo usuário
    def registraUsuarioNoBanco(self):
        nome = self.nomeFuncionario.get()
        cargo = self.cargo.get()
        login = self.loginFuncionario.get()
        senha = self.senhaFuncionario.get()

        if not nome or not login or not senha : 
            messagebox.showinfo(title="Registro falhou", message="Campos obrigatórios não podem estar em branco")
        else:
            # cata da classe insere, a query que ta sendo feitra la
            Insere.insereUsuarioNoBanco(nome, cargo, login, senha)
            self.frameTelaCadastroFuncionario.destroy()
        
    # é chamado quando se cadastra um novo fornecedor
    def registraFornecedorNoBanco(self):
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

            Insere.registraFornecedorNoBanco(colunas, valores)
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


        if not(nome and valorCusto and valorVenda and quantidade and codigoInterno and NCM and CFOP and CEST and origemCST and descricao and CNPJ):
            self.frameProdutoNaoCadastrado = ctk.CTkFrame(self, height=60, width=300, corner_radius=5, border_width=2, border_color="red",fg_color="transparent")
            self.frameProdutoNaoCadastrado.place(relx=0.5, y=600, )
            self.ProdutoNaoCadastrado = ctk.CTkLabel(self.frameProdutoNaoCadastrado,  text="Prencha os campos obrigatórios", font=("Arial", 18))
            self.ProdutoNaoCadastrado.place(relx=0.5, y=30, anchor="center")
        else:
            Insere.insereProdutosNoBanco(nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ)
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
                varEmailTransportadora = self.emailTransportadora.get()
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

            Insere.insereTransportadoraNoBanco(colunas, valores)
            self.frameTelaCadastroTransportadoras.destroy()
            gc.collect()

        
        else:
            messagebox.showerror("erro", "valores estão em branco")

    # é chamado quando estamos entrando no sistema
    def consultarUsuarioCadastrado(self):
        login = self.login.get()
        senha = self.senha.get()
        usuarioLogando = Buscas.consultaUsuario(login, senha)
        print(usuarioLogando)

        if not usuarioLogando:
            self.frameUsuarioNaoCadastrado = ctk.CTkFrame(self, height=100, width=300, corner_radius=5, border_width=2, border_color="red",fg_color="transparent")
            self.frameUsuarioNaoCadastrado.place(relx=0.5, y=600, anchor="center")
            self.usuarioNaoCadastrado = ctk.CTkLabel(self.frameUsuarioNaoCadastrado,  text="Esse usuário não foi encontrado.", font=("Arial", 18))
            self.usuarioNaoCadastrado.place(x=20, y=35)
            self.after(3000, self.frameUsuarioNaoCadastrado.destroy)
            gc.collect

        else:
            self.telaAcoes()
                


if __name__ == "__main__":
    app = App()
    app.mainloop()
