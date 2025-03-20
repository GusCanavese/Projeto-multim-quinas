import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.registraProdutoNoBanco import registraProdutoNoBanco

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
    self.botaoCadastrarUsuario = ctk.CTkButton(self.frameTelaCadastroProduto, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=lambda:registraProdutoNoBanco(self))
    self.botaoCadastrarUsuario.place(x=800, y=600)


    # cadastro de funcionários/usuários
