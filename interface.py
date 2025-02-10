import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.frameProduto = None  # Inicializa o atributo como None
        self.configuracoesJanela()
        self.telaLogin()
        
    def configuracoesJanela(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.geometry("700x500")
        
    def telaLogin(self):
        self.title("login")
        self.resizable(False, False)
        if self.frameProduto is not None:
            self.frameProduto.place_forget()

        # Conteúdo da primeira janela
        self.frame = ctk.CTkFrame(self, height=250, corner_radius=10)
        self.frame.place(x=150, y=100)

        self.texto = ctk.CTkLabel(self.frame, width=400, text="Fazer login", font=("Century Gothic bold", 20))
        self.texto.grid(padx=10, pady=20)

        self.email = ctk.CTkEntry(self.frame, placeholder_text="Email", width=300, corner_radius=15, font=("Century Gothic bold", 15))
        self.email.grid(padx=10, pady=10)

        self.senha = ctk.CTkEntry(self.frame, placeholder_text="Senha", width=300, corner_radius=15, font=("Century Gothic bold", 15), show="*")
        self.senha.grid(padx=10, pady=10)

        self.botao = ctk.CTkButton(self.frame, text="Entrar", width=200, corner_radius=15, font=("Arial", 15), command=self.telaProduto)
        self.botao.grid(padx=20, pady=20)

        self.textoCadastro = ctk.CTkLabel(self.frame, text="Caso não tenha cadastro", font=("Arial", 10))
        self.textoCadastro.grid(padx=10, pady=10)
        self.botaoCadastro = ctk.CTkButton(self.frame, text="Cadastrar", width=200, corner_radius=15, font=("Arial", 15), command=self.telaDeCadastro)
        self.botaoCadastro.grid(padx=20, pady=20)

    def telaProduto(self):
        self.frame.place_forget()
        self.title("Produto")

        self.frameProduto = ctk.CTkFrame(self, height=400, width=680)
        self.frameProduto.place(x=10, y=10)

        self.labelCadastro = ctk.CTkLabel(self.frameProduto, text="Cadastro do produto", font=("Century Gothic bold", 20))
        self.labelCadastro.grid(padx=30, pady=10)

        self.nomeLabel = ctk.CTkLabel(self.frameProduto, text="Nome do produto", font=("Century Gothic bold", 10))
        self.nomeLabel.place(x=35, y=60)
        self.nome = ctk.CTkEntry(self.frameProduto, placeholder_text="Nome", width=300, corner_radius=15, font=("Century Gothic bold", 15))
        self.nome.grid(row=1, column=0, padx=30, pady=40)

        self.quantidadeLabel = ctk.CTkLabel(self.frameProduto, text="Quantidade do produto", font=("Century Gothic bold", 10))
        self.quantidadeLabel.place(x=35, y=140)
        self.quantidade = ctk.CTkEntry(self.frameProduto, placeholder_text="Quantidade", width=300, corner_radius=15, font=("Century Gothic bold", 15))
        self.quantidade.grid(row=2, column=0, padx=30, pady=10)

        self.valor = ctk.CTkEntry(self.frameProduto, placeholder_text="Valor", width=300, corner_radius=15, font=("Century Gothic bold", 15))
        self.valor.grid(row=3, column=0, padx=30, pady=10)

        self.codigo = ctk.CTkEntry(self.frameProduto, placeholder_text="Código", width=300, corner_radius=15, font=("Century Gothic bold", 15))
        self.codigo.grid(row=4, column=0, padx=30, pady=10)

        self.botaoVoltar = ctk.CTkButton(self.frameProduto, text="Voltar", width=200, corner_radius=15, font=("Arial", 15), command=self.telaLogin)
        self.botaoVoltar.grid(row=5, column=0, padx=20, pady=20)



    def telaDeCadastro(self):
        self.frame.place_forget()

if __name__ == "__main__":
    app = App()
    app.mainloop()
