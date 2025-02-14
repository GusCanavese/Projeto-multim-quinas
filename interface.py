import customtkinter as ctk
import db
import messagebox


# ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.janela()
    
    # inicializa frames de todoas as janelas pra evitar erros de "destruição de vazio"
    def criaFrames(self):
        self.frameTelaCadastro = None
        self.frameTelaProduto = None
        self.frameTelaLogin = None
        self.frameTelaAcoes = None
        self.frameUsuarioNaoCadastrado = None

    # define as propriedades da janela
    def janela(self):
        self.criaFrames()
        self.resizable(False, False)
        alturaTela = 900
        larguraTela = 1280
        self.geometry(f"{larguraTela}x{alturaTela}+-1500+0")
        self.telaDeCadastroFuncionario()

    # tela de login inicial
    def telaLogin(self):
        self.title("login")
        if(self.frameTelaProduto == None):
            pass
        else:
            self.frameTelaProduto.destroy()

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
        self.frameTelaAcoes.place(x=140, y=100)     # colocando no lugar
        self.frameTelaAcoes.grid_propagate(False)
        
        # título
        self.Acoes = ctk.CTkLabel(self.frameTelaAcoes, width=950, height=0, text="Ações", font=("Century Gothic bold", 30))
        self.Acoes.place(relx=0.5, y=50, anchor="center")

        # botão do cadastro de funcionarios
        self.botaoCadastro = ctk.CTkButton(self.frameTelaAcoes, text="Cadastros", width=300, corner_radius=5, font=("Arial", 18), command=self.telaDeCadastroFuncionario)
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
        self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaAcoes, text="Trocar usuário", width=200, corner_radius=5, font=("Arial", 18), command=self.telaLogin)
        self.botaoGerarOrcamento.place(relx=0.33, y=650, anchor="center")

    # tela de cadastro de produtos
    def telaProduto(self):
        if(self.frameTelaLogin == None):
            pass
        else:
            self.frameTelaLogin.destroy()

        self.title("TelaProduto")
        self.frameTelaProduto = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameTelaProduto.place(x=140, y=100)     
        self.frameTelaProduto.grid_propagate(False)

        self.frameTelaProduto = ctk.CTkFrame(self, height=400, width=680)
        self.frameTelaProduto.place(x=10, y=10)

        self.labelCadastro = ctk.CTkLabel(self.frameTelaProduto, text="Cadastro do produto", font=("Century Gothic bold", 20))
        self.labelCadastro.grid(padx=30, pady=10)

        self.nomeLabel = ctk.CTkLabel(self.frameTelaProduto, text="Nome do produto", font=("Century Gothic bold", 10))
        self.nomeLabel.place(x=100, y=130)
        self.nome = ctk.CTkEntry(self.frameTelaProduto, placeholder_text="Nome", width=300, corner_radius=5, font=("Century Gothic bold", 15))
        self.nome.grid(row=1, column=0, padx=30, pady=40)

        self.quantidadeLabel = ctk.CTkLabel(self.frameTelaProduto, text="Quantidade do produto", font=("Century Gothic bold", 10))
        self.quantidadeLabel.place(x=35, y=140)
        self.quantidade = ctk.CTkEntry(self.frameTelaProduto, placeholder_text="Quantidade", width=300, corner_radius=5, font=("Century Gothic bold", 15))
        self.quantidade.grid(row=2, column=0, padx=30, pady=10)

        self.valor = ctk.CTkEntry(self.frameTelaProduto, placeholder_text="Valor", width=300, corner_radius=5, font=("Century Gothic bold", 15))
        self.valor.grid(row=3, column=0, padx=30, pady=10)

        self.codigo = ctk.CTkEntry(self.frameTelaProduto, placeholder_text="Código", width=300, corner_radius=5, font=("Century Gothic bold", 15))
        self.codigo.grid(row=4, column=0, padx=30, pady=10)

        self.botaoVoltar = ctk.CTkButton(self.frameTelaProduto, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.telaLogin)
        self.botaoVoltar.grid(row=5, column=0, padx=20, pady=20)

    # cadastro de funcionários/usuários
    def telaDeCadastroFuncionario(self):
        if(self.frameTelaLogin == None):
            pass
        else:
            self.frameTelaLogin.destroy()
        # self.frameTelaLogin.destroy()
        self.title("TelaCadastro")
        self.frameTelaCadastro = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameTelaCadastro.place(x=140, y=100)     
        self.frameTelaCadastro.grid_propagate(False)

        # ================ widgets da tela cadastro =====================#
        # titulo
        self.textoCadastro = ctk.CTkLabel(self.frameTelaCadastro, width=950, height=0, text="Cadastrar Usuário", font=("Century Gothic bold", 30))
        self.textoCadastro.grid(row=0, column=0, padx=10, pady=20)

        # nome
        self.labelNome = ctk.CTkLabel(self.frameTelaCadastro, text="Nome", font=("Century Gothic bold", 15))
        self.labelNome.place(x=100, y=100)
        self.nome = ctk.CTkEntry(self.frameTelaCadastro, placeholder_text="Nome", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.nome.place(x=100, y=130)

        # login
        self.labelLogin = ctk.CTkLabel(self.frameTelaCadastro, text="Login para acesso*", font=("Century Gothic bold", 15))   
        self.labelLogin.place(x=100, y=200)
        self.login = ctk.CTkEntry(self.frameTelaCadastro, placeholder_text="Login", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.login.place(x=100, y=230)

        # senha
        self.labelSenha = ctk.CTkLabel(self.frameTelaCadastro, text="Senha para acesso*", font=("Century Gothic bold", 15))
        self.labelSenha.place(x=550, y=200)
        self.senha = ctk.CTkEntry(self.frameTelaCadastro, placeholder_text="Senha", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.senha.place(x=550, y=230)

        # cargo
        self.labelCargo = ctk.CTkLabel(self.frameTelaCadastro, text="Cargo", font=("Century Gothic bold", 15))   
        self.labelCargo.place(x=550, y=100)
        opcoes = ["Gerente", "Vendedor(a) interno", "Vendedor(a) externo", "Financeiro"]
        self.cargo = ctk.CTkComboBox(self.frameTelaCadastro, width=350, corner_radius=5, font=("Century Gothic bold", 20), values=opcoes)
        self.cargo.place(x=550, y=130)

        # ============== Botões =============== #
        # voltar
        self.botaoVoltar = ctk.CTkButton(self.frameTelaCadastro, text="Voltar", width=200, fg_color="#088b1b", corner_radius=5, font=("Arial", 15), command=self.telaAcoes)
        self.botaoVoltar.place(x=200, y=600)
        
        # registra no bd
        self.botaoCadastrarUsuario = ctk.CTkButton(self.frameTelaCadastro, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=self.registraUsuarioNoBanco)
        self.botaoCadastrarUsuario.place(x=600, y=600)



    def registraUsuarioNoBanco(self):
        nome = self.nome.get()
        cargo = self.cargo.get()
        login = self.login.get()
        senha = self.senha.get()

        queryInserirFuncionario = "INSERT INTO funcionarios(nome, cargo, login, senha) VALUES(%s, %s, %s, %s);"

        if not nome or not login or not senha : 
            messagebox.showinfo(title="Registro falhou", message="campos obrigatórios não podem estar em branco") 
        else:
            db.cursor.execute(queryInserirFuncionario, (nome, cargo, login, senha,))
            db.conn.commit()
            messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")
            self.telaLogin()

    def consultarUsuarioCadastrado(self):
        login = self.login.get()
        queryConsultarLogin = "SELECT id FROM funcionarios WHERE login = %s;"
        db.cursor.execute(queryConsultarLogin, (login,))
        resultados = db.cursor.fetchall()

        if resultados == ((23,),):
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
