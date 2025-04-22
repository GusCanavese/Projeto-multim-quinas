import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import confirmarAlteracoesNoPedido

def telaVerPedidos(self, p, d, desc):
    for i in desc:
        print(i.rsplit(' ', 1))
        print(i.rsplit(' ', 1))

    self.frameTelaVerPedidos = ctk.CTkFrame(self)
    self.frameTelaVerPedidos.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    if p[4] == "Não confirmado":
        self.status = "Venda em aberto"
        dataDaVendaTelaVerPedidos = ''
        self.statusDoPedidoTelaVerPedido = ctk.CTkButton(self.frameTelaVerPedidos, text='Confirmar venda', width=180, corner_radius=5, font=("Arial", 15), command=lambda:confirmarAlteracoesNoPedido.confirmarHoje(self, p[0]))
        self.statusDoPedidoTelaVerPedido.place(relx=0.61, rely=0.1)
    else: 
        self.statusDoPedidoTelaVerPedido = ctk.CTkButton(self.frameTelaVerPedidos, text='Venda confirmada', fg_color='green', width=180, corner_radius=5, font=("Arial", 15))
        self.statusDoPedidoTelaVerPedido.place(relx=0.61, rely=0.1)
        self.status = "Confirmado"
        dataDaVendaTelaVerPedidos = p[4]


    # Primeira linha (relx espaçado em 0.2, rely em 0.05 e 0.1)
    self.labelNumeroDataVenda = ctk.CTkLabel(self.frameTelaVerPedidos, text="Número da venda", font=("Century Gothic bold", 14))
    self.labelNumeroDataVenda.place(relx=0.02, rely=0.05)
    self.numeroDeVenda = ctk.CTkLabel(self.frameTelaVerPedidos, textvariable=ctk.StringVar(value=p[0]), fg_color="#38343c", width=180, corner_radius=5, font=("Arial", 15))
    self.numeroDeVenda.place(relx=0, rely=0.1)

    self.labelDataDeCriacao = ctk.CTkLabel(self.frameTelaVerPedidos, text="Data de criação", font=("Century Gothic bold", 14))
    self.labelDataDeCriacao.place(relx=0.22, rely=0.05)
    self.dataDeCriacao = ctk.CTkLabel(self.frameTelaVerPedidos, width=180, fg_color="#38343c", corner_radius=5, textvariable=ctk.StringVar(value=p[2]), font=("Arial", 15))
    self.dataDeCriacao.place(relx=0.20, rely=0.1,)

    self.labelDataDaVendaTelaVerPedidos = ctk.CTkLabel(self.frameTelaVerPedidos, text="Data da venda", font=("Century Gothic bold", 14))
    self.labelDataDaVendaTelaVerPedidos.place(relx=0.42, rely=0.05)
    self.dataDaVendaTelaVerPedidos = ctk.CTkEntry(self.frameTelaVerPedidos, textvariable=ctk.StringVar(value=dataDaVendaTelaVerPedidos), placeholder_text="DD/MM/AAAA", width=180, corner_radius=5, font=("Arial", 15))
    self.dataDaVendaTelaVerPedidos.place(relx=0.42, rely=0.1)

    self.labelStatusDoPedidoTelaVerPedido = ctk.CTkLabel(self.frameTelaVerPedidos, text="Status: ", font=("Century Gothic bold", 14))
    self.labelStatusDoPedidoTelaVerPedido.place(relx=0.62, rely=0.05)
    # self.statusDoPedidoTelaVerPedido = ctk.CTkLabel(self.frameTelaVerPedidos, text=self.status, width=80, corner_radius=5, font=("Arial", 14))
    # self.statusDoPedidoTelaVerPedido.place(relx=0.66, rely=0.05)


    self.labelFuncionaria = ctk.CTkLabel(self.frameTelaVerPedidos, text="Vendedor(a)", font=("Century Gothic bold", 15))
    self.labelFuncionaria.place(relx=0.79, rely=0.05)
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
    self.CPFCliente.place(relx=0.42, rely=0.25)

    # Terceira linha (rely 0.35 e 0.4)
    self.labelEnderecoNoPedido = ctk.CTkLabel(self.frameTelaVerPedidos, text="Endereço *",  font=("Century Gothic bold", 14))
    self.labelEnderecoNoPedido.place(relx=0.61, rely=0.2)
    self.entradaEnderecoNoPedido = ctk.CTkLabel(self.frameTelaVerPedidos, textvariable=ctk.StringVar(value=d[2]), fg_color="#38343c", width=400, corner_radius=5, font=("Arial", 13)) 
    self.entradaEnderecoNoPedido.place(relx=0.61, rely=0.25)

    self.labelProdutoTelaVerPedido = ctk.CTkLabel(self.frameTelaVerPedidos, width=50, text="Produto", font=("Century Gothic bold", 14))
    self.labelProdutoTelaVerPedido.place(relx=0.02, rely=0.35)
    self.entradaProdutoTelaVerPedido = ctk.CTkEntry(self.frameTelaVerPedidos, textvariable=ctk.StringVar(value=desc[0]),  width=300, corner_radius=5, font=("Arial", 13))
    self.entradaProdutoTelaVerPedido.place(relx=0, rely=0.4)





    # Botão centralizado na parte inferior
    self.botaoVoltar = ctk.CTkButton(self.frameTelaVerPedidos, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaVerPedidos.destroy) 
    self.botaoVoltar.place(relx=0.08, rely=0.9) 

    # Botão centralizado na parte inferior
    self.botaoVoltar = ctk.CTkButton(self.frameTelaVerPedidos, text="Confirmar alterações", width=200, corner_radius=5, font=("Arial", 15), command=lambda:confirmarAlteracoesNoPedido.confirmarAlteracoesNoPedido(self, self.dataDaVendaTelaVerPedidos.get(), p[0]))
    self.botaoVoltar.place(relx=0.25, rely=0.9) 