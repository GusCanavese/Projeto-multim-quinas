import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import confirmarExclusaoDoProduto, confirmarAlteracoesNoProduto


def telaVerProduto(self, p):
    print(p)
    # campos linha de cima
    self.frameTelaVerProdutos = ctk.CTkFrame(self)
    self.frameTelaVerProdutos.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)
    
    self.labelQuantidade = ctk.CTkLabel(self.frameTelaVerProdutos, text="Quantidade", font=("Century Gothic bold", 14))
    self.labelQuantidade.place(relx=0.09, rely=0.05)
    self.quantidade = ctk.CTkEntry(self.frameTelaVerProdutos, textvariable=ctk.StringVar(value=p[0]), width=150, corner_radius=5, font=("Arial", 15))
    self.quantidade.place(relx=0.09, rely=0.1)

    self.labelDataDeCriacao = ctk.CTkLabel(self.frameTelaVerProdutos, text="CNPJ", font=("Century Gothic bold", 14))
    self.labelDataDeCriacao.place(relx=0.24, rely=0.05)
    self.dataDeCriacao = ctk.CTkLabel(self.frameTelaVerProdutos, width=150, fg_color="#38343c", corner_radius=5, textvariable=ctk.StringVar(value=p[4]), font=("Arial", 15))
    self.dataDeCriacao.place(relx=0.24, rely=0.1)

    self.labelNome = ctk.CTkLabel(self.frameTelaVerProdutos, text="Nome do produto", font=("Century Gothic bold", 14))
    self.labelNome.place(relx=0.39, rely=0.05)
    self.Nome = ctk.CTkLabel(self.frameTelaVerProdutos, width=150, fg_color="#38343c", corner_radius=5, textvariable=ctk.StringVar(value=p[1]), font=("Arial", 15))
    self.Nome.place(relx=0.39, rely=0.1,)

    self.labelPrecoVenda = ctk.CTkLabel(self.frameTelaVerProdutos, text="preço de venda", font=("Century Gothic bold", 14))
    self.labelPrecoVenda.place(relx=0.69, rely=0.05)
    self.precoVenda = ctk.CTkEntry(self.frameTelaVerProdutos, width=150, corner_radius=5, textvariable=ctk.StringVar(value=p[8]), font=("Arial", 15))
    self.precoVenda.place(relx=0.69, rely=0.1)


    
    
    # campos linha de baixo

    self.labelProdutoNCM = ctk.CTkLabel(self.frameTelaVerProdutos, text="NCM", font=("Century Gothic bold", 14))
    self.labelProdutoNCM.place(relx=0.09, rely=0.2)
    self.ProdutoNCM = ctk.CTkLabel(self.frameTelaVerProdutos, width=150, fg_color="#38343c", corner_radius=5, textvariable=ctk.StringVar(value=p[5]), font=("Arial", 15))
    self.ProdutoNCM.place(relx=0.09, rely=0.25)

    self.labelDataDeCriacao = ctk.CTkLabel(self.frameTelaVerProdutos, text="CFOP", font=("Century Gothic bold", 14))
    self.labelDataDeCriacao.place(relx=0.24, rely=0.2)
    self.dataDeCriacao = ctk.CTkLabel(self.frameTelaVerProdutos, width=150, fg_color="#38343c", corner_radius=5, textvariable=ctk.StringVar(value=p[6]), font=("Arial", 15))
    self.dataDeCriacao.place(relx=0.24, rely=0.25)

    self.labelDataDeCriacao = ctk.CTkLabel(self.frameTelaVerProdutos, text="CEST", font=("Century Gothic bold", 14))
    self.labelDataDeCriacao.place(relx=0.39, rely=0.2)
    self.dataDeCriacao = ctk.CTkLabel(self.frameTelaVerProdutos, width=150, fg_color="#38343c", corner_radius=5, textvariable=ctk.StringVar(value=p[7]), font=("Arial", 15))
    self.dataDeCriacao.place(relx=0.39, rely=0.25)

    self.labelDataDeCriacao = ctk.CTkLabel(self.frameTelaVerProdutos, text="Origem CST", font=("Century Gothic bold", 14))
    self.labelDataDeCriacao.place(relx=0.54, rely=0.2)
    self.dataDeCriacao = ctk.CTkLabel(self.frameTelaVerProdutos, width=150, fg_color="#38343c", corner_radius=5, textvariable=ctk.StringVar(value=p[8]), font=("Arial", 15))
    self.dataDeCriacao.place(relx=0.54, rely=0.25)

    self.labelCodigoInterno = ctk.CTkLabel(self.frameTelaVerProdutos, text="Código interno", font=("Century Gothic bold", 14))
    self.labelCodigoInterno.place(relx=0.69, rely=0.2)
    self.CodigoInterno = ctk.CTkLabel(self.frameTelaVerProdutos, width=150, fg_color="#38343c", corner_radius=5, textvariable=ctk.StringVar(value=p[2]), font=("Arial", 15))
    self.CodigoInterno.place(relx=0.69, rely=0.25)



    self.botaoVoltar = ctk.CTkButton(self.frameTelaVerProdutos, text="Voltar", command=self.frameTelaVerProdutos.destroy)
    self.botaoVoltar.place(relx=0.1, rely=0.94, relwidth=0.15, anchor="nw")

    self.botaoSalvarAlteracoes = ctk.CTkButton(self.frameTelaVerProdutos, text="Salvar alterações", command=lambda:confirmarAlteracoesNoProduto.confirmarAlteracoesNoProduto(self, p[1], self.quantidade.get(), self.precoVenda.get()))
    self.botaoSalvarAlteracoes.place(relx=0.3, rely=0.94, relwidth=0.15, anchor="nw")

    self.botaoExcluir = ctk.CTkButton(self.frameTelaVerProdutos, text="Excluir produto", fg_color="#8B0000", width=200, corner_radius=5, font=("Arial", 15), command=lambda:confirmarExclusaoDoProduto.confirmarExclusaoDoProduto(self, p[1]))
    self.botaoExcluir.place(relx=0.5, rely=0.94) 


    # self.labelStatusDoPedidoTelaVerPedido = ctk.CTkLabel(self.frameTelaVerProdutos, text="Status: ", font=("Century Gothic bold", 14))
    # self.labelStatusDoPedidoTelaVerPedido.place(relx=0.62, rely=0.05)

    # self.labelFuncionaria = ctk.CTkLabel(self.frameTelaVerProdutos, text="Vendedor(a)", font=("Century Gothic bold", 15))
    # self.labelFuncionaria.place(relx=0.79, rely=0.05)
    # self.funcionariaPedido = ctk.CTkLabel(self.frameTelaVerProdutos, width=100, corner_radius=5, textvariable=ctk.StringVar(value=p[1]), fg_color="#38343c", font=("Century Gothic bold", 15))
    # self.funcionariaPedido.place(relx=0.787, rely=0.1)

    # # Segunda linha (rely 0.2 e 0.25)
    # self.labelNomeDoCliente = ctk.CTkLabel(self.frameTelaVerProdutos, text="Nome do cliente *", font=("Century Gothic", 14))
    # self.labelNomeDoCliente.place(relx=0.02, rely=0.2)
    # self.nomeDoClienteBuscado = ctk.CTkLabel(self.frameTelaVerProdutos, textvariable=ctk.StringVar(value=p[0]), fg_color="#38343c", width=140, corner_radius=5, font=("Arial", 15))
    # self.nomeDoClienteBuscado.place(relx=0.0, rely=0.25)

    # self.labelCPFCliente = ctk.CTkLabel(self.frameTelaVerProdutos, text="CPF/CNPJ *", font=("Century Gothic bold", 14))
    # self.labelCPFCliente.place(relx=0.42, rely=0.2)
    # self.CPFCliente = ctk.CTkLabel(self.frameTelaVerProdutos, width=180, textvariable=ctk.StringVar(value=p[1]), fg_color="#38343c", corner_radius=5, font=("Arial", 15))
    # self.CPFCliente.place(relx=0.42, rely=0.25)

    # # Terceira linha (rely 0.35 e 0.4)
    # self.labelEnderecoNoPedido = ctk.CTkLabel(self.frameTelaVerProdutos, text="Endereço *",  font=("Century Gothic bold", 14))
    # self.labelEnderecoNoPedido.place(relx=0.61, rely=0.2)
    # self.entradaEnderecoNoPedido = ctk.CTkLabel(self.frameTelaVerProdutos, textvariable=ctk.StringVar(value=p[2]), fg_color="#38343c", width=400, corner_radius=5, font=("Arial", 13)) 
    # self.entradaEnderecoNoPedido.place(relx=0.61, rely=0.25)

    # self.labelProdutoTelaVerPedido = ctk.CTkLabel(self.frameTelaVerProdutos, width=50, text="Produto", font=("Century Gothic bold", 14))
    # self.labelProdutoTelaVerPedido.place(relx=0.02, rely=0.35)
    # self.entradaProdutoTelaVerPedido = ctk.CTkEntry(self.frameTelaVerProdutos, textvariable=ctk.StringVar(value=p[0]),  width=300, corner_radius=5, font=("Arial", 13))
    # self.entradaProdutoTelaVerPedido.place(relx=0, rely=0.4)