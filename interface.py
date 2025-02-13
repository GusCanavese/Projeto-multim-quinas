import customtkinter as ctk
import db
import messagebox


# ctk.set_appearance_mode("system")  


ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.janela()
        
    def criaFrames(self):
        self.frameTelaCadastro = None
        self.frameTelaProduto = None
        self.frameTelaLogin = None


    # define as propriedades da janela
    def janela(self):
        self.criaFrames()
        self.resizable(False, False)
        alturaTela = 900
        larguraTela = 1280
        self.geometry(f"{larguraTela}x{alturaTela}+-1500+0")
        self.telaLogin()

    # tela de login inicial
    def telaLogin(self):
        self.title("login")
        
        if(self.frameTelaProduto == None):
            pass
        else:
            self.frameTelaProduto.destroy()

    
        # ================ widgets da tela login =====================#
        self.frameTelaLogin = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameTelaLogin.place(x=140, y=100)     # colocando no lugar
        self.frameTelaLogin.grid_propagate(False)   # evita ela de se configurar automaticamente

        self.texto = ctk.CTkLabel(self.frameTelaLogin, width=1000, height=100, text="Fazer login", font=("Century Gothic bold", 30))
        self.texto.grid(row=0, column=0, padx=10, pady=20)

        self.login = ctk.CTkEntry(self.frameTelaLogin, placeholder_text="login", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.login.grid(row=1, column=0, padx=10, pady=10)

        self.senha = ctk.CTkEntry(self.frameTelaLogin, placeholder_text="Senha", width=350, corner_radius=5, font=("Century Gothic bold", 20), show="*")
        self.senha.grid(row=2, column=0, padx=10, pady=10)

        # self.botao = ctk.CTkButton(self.frame, text="Entrar", width=200, corner_radius=5, font=("Arial", 15), command=self.telaProduto)
        # self.botao.grid(row=3, column=0, padx=20, pady=20)

        self.botao = ctk.CTkButton(self.frameTelaLogin, text="Entrar", width=200, corner_radius=5, font=("Arial", 15), command=self.consultarUsuarioCadastrado)
        self.botao.grid(row=3, column=0, padx=20, pady=20)


        # texto antes do cadastro de produtos
        self.textoCadastro = ctk.CTkLabel(self.frameTelaLogin, text="Caso não tenha cadastro", font=("Arial", 15))
        self.textoCadastro.grid(row=4, column=0, padx=10, pady=10)

        # botão do cadastro de funcionarios
        self.botaoCadastro = ctk.CTkButton(self.frameTelaLogin, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=self.telaDeCadastroFuncionario)
        self.botaoCadastro.grid(row=5, column=0, padx=20, pady=20)
        # ================ widgets da tela login =====================#

    # tela de cadastro de produtos
    def telaProduto(self):
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
        self.frameTelaLogin.destroy()
        self.title("TelaCadastro")
        self.frameTelaCadastro = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameTelaCadastro.place(x=140, y=100)     
        self.frameTelaCadastro.grid_propagate(False)

        # ================ widgets da tela cadastro =====================#
        # titulo
        self.textoCadastro = ctk.CTkLabel(self.frameTelaCadastro, width=950, height=0, text="Cadastrar Usuário", font=("Century Gothic bold", 30))
        self.textoCadastro.grid(row=0, column=0, padx=10, pady=20)

        # nome
        self.labelNome = ctk.CTkLabel(self.frameTelaCadastro, text="Nome a ser registrado*", font=("Century Gothic bold", 15))
        self.labelNome.place(x=100, y=100)
        self.nome = ctk.CTkEntry(self.frameTelaCadastro, placeholder_text="Nome", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.nome.place(x=100, y=130)

        # login
        self.labelLogin = ctk.CTkLabel(self.frameTelaCadastro, text="Login para ser usado na tela principal*", font=("Century Gothic bold", 15))   
        self.labelLogin.place(x=100, y=200)
        self.login = ctk.CTkEntry(self.frameTelaCadastro, placeholder_text="Login", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.login.place(x=100, y=230)

        # senha
        self.labelSenha = ctk.CTkLabel(self.frameTelaCadastro, text="Senha para utilizar na tela principal*", font=("Century Gothic bold", 15))
        self.labelSenha.place(x=100, y=300)
        self.senha = ctk.CTkEntry(self.frameTelaCadastro, placeholder_text="Senha", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.senha.place(x=100, y=330)

        # cargo
        self.labelCargo = ctk.CTkLabel(self.frameTelaCadastro, text="Cargo do funcionário", font=("Century Gothic bold", 15))   
        self.labelCargo.place(x=550, y=100)
        opcoes = ["Gerente", "Vendedor(a) interno", "Vendedor(a) externo", "Financeiro"]
        self.cargo = ctk.CTkComboBox(self.frameTelaCadastro, width=350, corner_radius=5, font=("Century Gothic bold", 20), values=opcoes)
        self.cargo.place(x=550, y=130)

        # cpf
        self.labelCpf = ctk.CTkLabel(self.frameTelaCadastro, text="Documento do funcionário*", font=("Century Gothic bold", 15))
        self.labelCpf.place(x=550, y=200)
        self.cpf = ctk.CTkEntry(self.frameTelaCadastro, placeholder_text="CPF", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.cpf.place(x=550, y=230)

        # email/contato
        self.labelContato = ctk.CTkLabel(self.frameTelaCadastro, text="Contato do funcionário", font=("Century Gothic bold", 15))
        self.labelContato.place(x=550, y=300)
        self.contato = ctk.CTkEntry(self.frameTelaCadastro, placeholder_text="Contato", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.contato.place(x=550, y=330)


        # ============== Botões =============== #
        # voltar
        self.botaoVoltar = ctk.CTkButton(self.frameTelaCadastro, text="Voltar", width=200, fg_color="#088b1b", corner_radius=5, font=("Arial", 15), command=self.telaLogin)
        self.botaoVoltar.place(x=200, y=600)
        
        # registra no bd
        self.botaoCadastrarUsuario = ctk.CTkButton(self.frameTelaCadastro, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=self.registraUsuarioNoBanco)
        self.botaoCadastrarUsuario.place(x=600, y=600)



    def registraUsuarioNoBanco(self):
        nome = self.nome.get()
        cargo = self.cargo.get()
        login = self.login.get()
        cpf = self.cpf.get()
        senha = self.senha.get()
        contato = self.contato.get()

        queryInserirFuncionario = "INSERT INTO funcionarios(nome, cargo, login, cpf, senha, contato) VALUES(%s, %s, %s, %s, %s, %s);"

        if not nome or not login or not cpf or not senha : 
            messagebox.showinfo(title="Registro falhou", message="campos obrigatórios não podem estar em branco") 
        else:
            db.cursor.execute(queryInserirFuncionario, (nome, cargo, login, cpf, senha, contato,))
            db.conn.commit()
            messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")
            self.telaLogin()

    def consultarUsuarioCadastrado(self):
        login = self.login.get()
        queryConsultarLogin = "SELECT id FROM funcionarios WHERE login = %s;"
        db.cursor.execute(queryConsultarLogin, (login,))
        resultados = db.cursor.fetchall()

        if resultados == ((0,),):
            self.telaProduto()
        else:
            messagebox.showerror(title="Erro", message="Usuário não cadastrado")
        # print(resultados)
        

        


if __name__ == "__main__":
    app = App()
    app.mainloop()
