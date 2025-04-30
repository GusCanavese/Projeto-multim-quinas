import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.buscarProdutos import buscarProdutos


def telaEstoque(self):

    self.frameTelaEstoque = ctk.CTkFrame(self, corner_radius=5)
    self.frameTelaEstoque.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    # Frame rolável (conteúdo principal)
    self.frameProdutosNoEstoque = ctk.CTkScrollableFrame(self.frameTelaEstoque)
    self.frameProdutosNoEstoque.place(relx=0.3, rely=0.01, relwidth=0.68, relheight=0.93)

    # Filtros - lado esquerdo
    self.labelBuscarPorNome = ctk.CTkLabel(self.frameTelaEstoque, text="Filtrar pelo Código", font=("Century Gothic bold", 15))
    self.labelBuscarPorNome.place(relx=0.03, rely=0.01, anchor="nw")
    self.buscarPorCodigo = ctk.CTkEntry(self.frameTelaEstoque, corner_radius=5, font=("Century Gothic bold", 20))
    self.buscarPorCodigo.place(relx=0.03, rely=0.06, relwidth=0.22, anchor="nw")

    self.labelBuscarPorNome = ctk.CTkLabel(self.frameTelaEstoque, text="Filtrar pelo Nome", font=("Century Gothic bold", 15))
    self.labelBuscarPorNome.place(relx=0.03, rely=0.13, anchor="nw")
    self.buscarPorNome = ctk.CTkEntry(self.frameTelaEstoque, corner_radius=5, font=("Century Gothic bold", 20))
    self.buscarPorNome.place(relx=0.03, rely=0.17, relwidth=0.22, anchor="nw")

    # Botões
    self.botaoBuscarProdutos = ctk.CTkButton(self.frameTelaEstoque,text="Buscar",command=lambda:buscarProdutos(self, self.buscarPorNome.get(), self.buscarPorCodigo.get(), 1))
    self.botaoBuscarProdutos.place(relx=0.05, rely=0.55, relwidth=0.15, anchor="nw")

    # self.botaoLimpar = ctk.CTkButton(self.frameTelaEstoque, text="Atualizar", command=self)
    # self.botaoLimpar.place(relx=0.05, rely=0.63, relwidth=0.15, anchor="nw")

    self.botaoVoltar = ctk.CTkButton(self.frameTelaEstoque, text="Voltar", command=self.frameTelaEstoque.destroy)
    self.botaoVoltar.place(relx=0.79, rely=0.94, relwidth=0.15, anchor="nw")

    # Cabeçalhos da tabela
    colunas = ["QTD", "Produto", "Preço", "CNPJ"]
    for i, coluna in enumerate(colunas):
        if coluna == "QTD":
            label = ctk.CTkLabel(self.frameProdutosNoEstoque, text=coluna, width=50, fg_color="#2C3E50", anchor="center")
        elif coluna == "Produto":
            label = ctk.CTkLabel(self.frameProdutosNoEstoque, text=coluna, width=250, fg_color="#2C3E50", anchor="center")
        else:
            label = ctk.CTkLabel(self.frameProdutosNoEstoque, text=coluna, width=150, fg_color="#2C3E50", anchor="center")
        label.grid(row=0, column=i, padx=1.5, pady=5)
        label.grid_columnconfigure(0, minsize=20)
