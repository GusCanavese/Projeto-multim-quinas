import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas

def telaVerPedidos(self, p, d, dl):
    print(p)
    print(d)
    def buscaProduto(event=None):
        nomeDoProduto = self.entradaProdutoTelaVerPedido.get()
        Buscas.buscaProduto(nomeDoProduto)

        if hasattr(self, "resultadoLabelsProduto"):
            for label in self.resultadoLabelsProduto:
                label.destroy()

        self.resultadoLabelsProduto = []
        yNovo = 362
        
        for i, row in enumerate(Buscas.buscaProduto(nomeDoProduto)):
            if i >=3: break
            label = ctk.CTkButton(self.frameTelaVerPedidos, width=300, text=row[0], fg_color="#38343c", font=("Century Gothic bold", 15), command=lambda nome = row[0], valor = row[1], quantidade=row[2]: selecionaProduto(nome, valor, quantidade))
            label.place(relx=82, y=yNovo)
            self.resultadoLabelsProduto.append(label)
            yNovo += 29

        # ações realizadas quando digitamos em cada campo
    
    self.frameTelaVerPedidos = ctk.CTkFrame(self)
    self.frameTelaVerPedidos.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    # Primeira linha (relx espaçado em 0.2, rely em 0.05 e 0.1)
    self.labelNumeroDataVenda = ctk.CTkLabel(self.frameTelaVerPedidos, text="Número da venda", font=("Century Gothic bold", 14))
    self.labelNumeroDataVenda.place(relx=0.02, rely=0.05)
    self.numeroDeVenda = ctk.CTkLabel(self.frameTelaVerPedidos, textvariable=ctk.StringVar(value=p[0]), fg_color="#38343c", width=180, corner_radius=5, font=("Arial", 15))
    self.numeroDeVenda.place(relx=0, rely=0.1)

    self.labelDataDeCriacao = ctk.CTkLabel(self.frameTelaVerPedidos, text="Data de criação", font=("Century Gothic bold", 14))
    self.labelDataDeCriacao.place(relx=0.22, rely=0.05)
    self.dataDeCriacao = ctk.CTkLabel(self.frameTelaVerPedidos, width=180, fg_color="#38343c", corner_radius=5, textvariable=ctk.StringVar(value=p[2]), font=("Arial", 15))
    self.dataDeCriacao.place(relx=0.20, rely=0.1,)

    self.labelDataDaVenda = ctk.CTkLabel(self.frameTelaVerPedidos, text="Data da venda", font=("Century Gothic bold", 14))
    self.labelDataDaVenda.place(relx=0.42, rely=0.05)
    self.dataDaVenda = ctk.CTkEntry(self.frameTelaVerPedidos, placeholder_text="DD/MM/AAAA", width=180, corner_radius=5, font=("Arial", 15))
    self.dataDaVenda.place(relx=0.42, rely=0.1)

    self.labelStatusDoPedido = ctk.CTkLabel(self.frameTelaVerPedidos, text="Status", font=("Century Gothic bold", 14))
    self.labelStatusDoPedido.place(relx=0.62, rely=0.05)
    self.statusDoPedido = ctk.CTkEntry(self.frameTelaVerPedidos,  width=180, corner_radius=5, font=("Arial", 15))
    self.statusDoPedido.place(relx=0.62, rely=0.1)

    self.labelFuncionaria = ctk.CTkLabel(self.frameTelaVerPedidos, text="Vendedor(a)", font=("Century Gothic bold", 15))
    self.labelFuncionaria.place(relx=0.805, rely=0.05)
    self.funcionariaPedido = ctk.CTkLabel(self.frameTelaVerPedidos, width=100, corner_radius=5, textvariable=ctk.StringVar(value=p[1]), fg_color="#38343c", font=("Century Gothic bold", 15))
    self.funcionariaPedido.place(relx=0.787, rely=0.1)

    # Segunda linha (rely 0.2 e 0.25)
    self.labelNomeDoCliente = ctk.CTkLabel(self.frameTelaVerPedidos, text="Nome do cliente *", font=("Century Gothic", 14))
    self.labelNomeDoCliente.place(relx=0.02, rely=0.2)
    self.nomeDoClienteBuscado = ctk.CTkLabel(self.frameTelaVerPedidos, textvariable=ctk.StringVar(value=d[0]), fg_color="#38343c", width=140, corner_radius=5, font=("Arial", 15))
    self.nomeDoClienteBuscado.place(relx=0.0, rely=0.25)

    self.labelCPFCliente = ctk.CTkLabel(self.frameTelaVerPedidos, text="CPF/CNPJ *", font=("Century Gothic bold", 14))
    self.labelCPFCliente.place(relx=0.42, rely=0.2)
    self.CPFCliente = ctk.CTkLabel(self.frameTelaVerPedidos, width=180, textvariable=ctk.StringVar(value=d[1]), fg_color="#38343c", corner_radius=5, font=("Arial", 15))
    self.CPFCliente.place(relx=0.389, rely=0.25)

    # Terceira linha (rely 0.35 e 0.4)
    self.labelEnderecoNoPedido = ctk.CTkLabel(self.frameTelaVerPedidos, text="Endereço *",  font=("Century Gothic bold", 14))
    self.labelEnderecoNoPedido.place(relx=0.62, rely=0.2)
    self.entradaEnderecoNoPedido = ctk.CTkLabel(self.frameTelaVerPedidos, textvariable=ctk.StringVar(value=d[2]), fg_color="#38343c", width=400, corner_radius=5, font=("Arial", 13))
    self.entradaEnderecoNoPedido.place(relx=0.61, rely=0.25)

    # Terceira linha (rely 0.35 e 0.4)
    self.labelProdutoTelaVerPedido = ctk.CTkLabel(self.frameTelaVerPedidos, width=50, text="Produto", font=("Century Gothic bold", 14))
    self.labelProdutoTelaVerPedido.place(relx=0.02, rely=0.35)
    self.entradaProdutoTelaVerPedido = ctk.CTkEntry(self.frameTelaVerPedidos, textvariable=ctk.StringVar(value=dl[0]),  width=300, corner_radius=5, font=("Arial", 13))
    self.entradaProdutoTelaVerPedido.place(relx=0, rely=0.4)
    self.entradaProdutoTelaVerPedido.bind("<KeyRelease>", buscaProduto)






    # Botão centralizado na parte inferior
    self.botaoVoltar = ctk.CTkButton(self.frameTelaVerPedidos, text="Gerar pedido", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaVerPedidos.destroy)
    self.botaoVoltar.place(relx=0.4, rely=0.8) 