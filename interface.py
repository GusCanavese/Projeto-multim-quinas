import customtkinter as ctk
import db
import messagebox


# ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")




class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.frameTelaProduto = None  #Inicializa o atributo como None
        self.janela()
    
    # define as propriedades da janela
    def janela(self):
        self.resizable(False, False)
        if self.frameTelaProduto is not None:
            self.frameTelaProduto.place_forget()

        alturaTela = 900
        larguraTela = 1280
        self.geometry(f"{larguraTela}x{alturaTela}+-1500+0")
        self.telaLogin()

    # tela de login inicial
    def telaLogin(self):
        self.title("login")
    
        # ================ widgets da tela login =====================#
        self.frame = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frame.place(x=140, y=100)     # colocando no lugar
        self.frame.grid_propagate(False)   # evita ela de se configurar automaticamente

        self.texto = ctk.CTkLabel(self.frame, width=1000, height=100, text="Fazer login", font=("Century Gothic bold", 30))
        self.texto.grid(row=0, column=0, padx=10, pady=20)

        self.email = ctk.CTkEntry(self.frame, placeholder_text="Email", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.email.grid(row=1, column=0, padx=10, pady=10)

        self.senha = ctk.CTkEntry(self.frame, placeholder_text="Senha", width=350, corner_radius=5, font=("Century Gothic bold", 20), show="*")
        self.senha.grid(row=2, column=0, padx=10, pady=10)

        self.botao = ctk.CTkButton(self.frame, text="Entrar", width=200, corner_radius=5, font=("Arial", 15), command=self.telaProduto)
        self.botao.grid(row=3, column=0, padx=20, pady=20)

        # texto antes do cadastro de produtos
        self.textoCadastro = ctk.CTkLabel(self.frame, text="Caso não tenha cadastro", font=("Arial", 15))
        self.textoCadastro.grid(row=4, column=0, padx=10, pady=10)
        # botão do cadastro de produtos que leva para a tela de cadastro
        self.botaoCadastro = ctk.CTkButton(self.frame, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=self.telaDeCadastro)
        self.botaoCadastro.grid(row=5, column=0, padx=20, pady=20)
        # ================ widgets da tela login =====================#

    # tela de cadastro de produtos
    def telaProduto(self):
        self.frame.place_forget()
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

    def telaDeCadastro(self):
        self.frame.place_forget()
        self.title("TelaCadastro")
        self.frameTelaCadastro = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
        self.frameTelaCadastro.place(x=140, y=100)     
        self.frameTelaCadastro.grid_propagate(False)

        # ================ widgets da tela cadastro =====================#
        # titulo
        self.textoCadastro = ctk.CTkLabel(self.frameTelaCadastro, width=1000, height=0, text="Cadastrar Usuário", font=("Century Gothic bold", 30))
        self.textoCadastro.grid(row=0, column=0, padx=10, pady=20)



        self.labelNome = ctk.CTkLabel(self.frameTelaCadastro, text="Digite o nome a ser registrado", font=("Century Gothic bold", 15))
        self.labelNome.place(x=100, y=150)
        self.nome = ctk.CTkEntry(self.frameTelaCadastro, placeholder_text="Login", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.nome.place(x=100, y=100)
        # login
        self.login = ctk.CTkEntry(self.frameTelaCadastro, placeholder_text="Nome", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.login.place(x=100, y=200)
        # cpf
        # senha
        # email/contato
        self.cargo = ctk.CTkEntry(self.frameTelaCadastro, placeholder_text="Cargo", width=350, corner_radius=5, font=("Century Gothic bold", 20))
        self.cargo.place(x=550, y=100)

        self.botaoVoltar = ctk.CTkButton(self.frameTelaCadastro, text="Voltar", width=200, fg_color="#088b1b", corner_radius=5, font=("Arial", 15), command=self.telaLogin)
        self.botaoVoltar.place(x=200, y=400)
        
        # botão que cria um novo usuário no banco de dados
        self.botaoCadastrarUsuario = ctk.CTkButton(self.frameTelaCadastro, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=self.registraUsuarioNoBanco)
        self.botaoCadastrarUsuario.place(x=600, y=400)

    def registraUsuarioNoBanco(self):
        nome = self.nome.get()
        cargo = self.cargo.get()

        print(type(nome))
        print(type(cargo))

        db.cursor.lastrowid

        db.cursor.execute("""
            INSERT INTO funcionarios(nome, cargo) VALUES(%s, %s)
        """, (nome, cargo))
        db.conn.commit()

        messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")

        self.telaLogin()



if __name__ == "__main__":
    app = App()
    app.mainloop()
