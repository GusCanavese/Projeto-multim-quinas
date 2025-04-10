import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk

def telaVerPedidos(self, p):
    print(p[1])
    self.frameTelaVerPedidos = ctk.CTkFrame(self)
    self.frameTelaVerPedidos.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    # Primeira linha (relx espaçado em 0.2, rely em 0.05 e 0.1)
    self.labelNumeroDataVenda = ctk.CTkLabel(self.frameTelaVerPedidos, text="Número da venda", font=("Century Gothic bold", 14))
    self.labelNumeroDataVenda.place(relx=0.02, rely=0.05)
    self.numeroDeVenda = ctk.CTkEntry(self.frameTelaVerPedidos, placeholder_text="Número", width=180, corner_radius=5, font=("Arial", 15))
    self.numeroDeVenda.place(relx=0.02, rely=0.1)

    self.labelDataDeCriacao = ctk.CTkLabel(self.frameTelaVerPedidos, text="Data de criação", font=("Century Gothic bold", 14))
    self.labelDataDeCriacao.place(relx=0.22, rely=0.05)
    self.dataDeCriacao = ctk.CTkEntry(self.frameTelaVerPedidos, width=180, corner_radius=5, font=("Arial", 15))
    self.dataDeCriacao.place(relx=0.22, rely=0.1,)

    self.labelDataDaVenda = ctk.CTkLabel(self.frameTelaVerPedidos, text="Data da venda", font=("Century Gothic bold", 14))
    self.labelDataDaVenda.place(relx=0.42, rely=0.05)
    self.dataDaVenda = ctk.CTkEntry(self.frameTelaVerPedidos, placeholder_text="DD/MM/AAAA", width=180, corner_radius=5, font=("Arial", 15))
    self.dataDaVenda.place(relx=0.42, rely=0.1)

    self.labelStatusDoPedido = ctk.CTkLabel(self.frameTelaVerPedidos, text="Status", font=("Century Gothic bold", 14))
    self.labelStatusDoPedido.place(relx=0.62, rely=0.05)
    self.statusDoPedido = ctk.CTkEntry(self.frameTelaVerPedidos, textvariable=ctk.StringVar(value="Em aberto"), width=180, corner_radius=5, font=("Arial", 15))
    self.statusDoPedido.place(relx=0.62, rely=0.1)

    self.labelFuncionaria = ctk.CTkLabel(self.frameTelaVerPedidos, text="Vendedor(a)", font=("Century Gothic bold", 15))
    self.labelFuncionaria.place(relx=0.805, rely=0.05)
    self.funcionariaPedido = ctk.CTkEntry(self.frameTelaVerPedidos, width=180, corner_radius=5, textvariable=ctk.StringVar(value=p[1]), font=("Century Gothic bold", 15))
    self.funcionariaPedido.place(relx=0.805, rely=0.1)

    # Segunda linha (rely 0.2 e 0.25)
    self.labelNomeDoCliente = ctk.CTkLabel(self.frameTelaVerPedidos, text="Nome do cliente *", font=("Century Gothic", 14))
    self.labelNomeDoCliente.place(relx=0.02, rely=0.2)
    self.nomeDoClienteBuscado = ctk.CTkEntry(self.frameTelaVerPedidos, placeholder_text="Nome do Cliente", width=420, corner_radius=5, font=("Arial", 15))
    self.nomeDoClienteBuscado.place(relx=0.02, rely=0.25)

    self.labelCPFCliente = ctk.CTkLabel(self.frameTelaVerPedidos, text="CPF/CNPJ *", font=("Century Gothic bold", 14))
    self.labelCPFCliente.place(relx=0.42, rely=0.2)
    self.CPFCliente = ctk.CTkEntry(self.frameTelaVerPedidos, width=180, corner_radius=5, font=("Arial", 15))
    self.CPFCliente.place(relx=0.42, rely=0.25)

    # Terceira linha (rely 0.35 e 0.4)
    self.labelEnderecoNoPedido = ctk.CTkLabel(self.frameTelaVerPedidos, text="Endereço *", font=("Century Gothic bold", 14))
    self.labelEnderecoNoPedido.place(relx=0.62, rely=0.2)
    self.entradaEnderecoNoPedido = ctk.CTkEntry(self.frameTelaVerPedidos, width=400, corner_radius=5, font=("Arial", 13))
    self.entradaEnderecoNoPedido.place(relx=0.62, rely=0.25)



    # Botão centralizado na parte inferior
    self.botaoVoltar = ctk.CTkButton(self.frameTelaVerPedidos, text="Gerar pedido", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaVerPedidos.destroy)
    self.botaoVoltar.place(relx=0.4, rely=0.8)