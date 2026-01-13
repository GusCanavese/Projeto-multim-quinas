import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from telas.telaCadastroProdutos import telaCadastroProdutos
from telas.telaCadastroFuncionario import telaCadastroFuncionario
from telas.telaCadastroFornecedor import telaCadastroFornecedores
from telas.telaCadastroTransportadoras import telaCadastroTransportadoras 
from telas.telaCadastroClientes import telaCadastroClientes
from componentes import criaFrameJanela, criaFrameJanela, criaBotao
from funcoesTerceiras.carregamentoDasImagens import resource_path
from PIL import Image, ImageTk






def telaCadastros(self):


    imgCliente = resource_path("arquivos/clientes.png")
    imgProduto = resource_path("arquivos/produto.png")
    imgFornecedor = resource_path("arquivos/fornecedor.png")
    imgTransportadora = resource_path("arquivos/transporte.png")
    imgFuncionario = resource_path("arquivos/funcionarios.png")
    fotoCliente = ImageTk.PhotoImage(Image.open(imgCliente).resize((60, 60)))
    fotoProduto = ImageTk.PhotoImage(Image.open(imgProduto).resize((60, 60)))
    fotoFornecedor = ImageTk.PhotoImage(Image.open(imgFornecedor).resize((60, 60)))
    fotoTransportadora = ImageTk.PhotoImage(Image.open(imgTransportadora).resize((60, 60)))
    fotoFuncionario = ImageTk.PhotoImage(Image.open(imgFuncionario).resize((60, 60)))


    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    self.Acoes = ctk.CTkLabel(frame, width=950, height=0, text="Cadastros", font=("Century Gothic bold", 30))
    self.Acoes.place(relx=0.5, y=50, anchor="center")
    
    if self.cargo == (('Vendedor(a) externo',),) or self.cargo == (('Vendedor(a) interno',),):

        clientes = criaBotao(frame, "Clientes", 0.5, 0.24, 0.24, lambda:telaCadastroClientes(self, False))
        clientes.configure(height=50, image=fotoCliente, anchor="center")

    elif self.cargo == (('Financeiro',),) or self.cargo == (('Gerente',),):
        
        clientes = criaBotao(frame, "Clientes", 0.66, 0.24, 0.24, lambda:telaCadastroClientes(self, False))
        clientes.configure(height=50, image=fotoCliente, compound="left")

        produtos = criaBotao(frame, "Produtos", 0.33, 0.24, 0.24, lambda:telaCadastroProdutos(self))
        produtos.configure(height=50, image=fotoProduto, compound="left")

        fornecedores = criaBotao(frame, "Fornecedores", 0.33, 0.35, 0.24, lambda:telaCadastroFornecedores(self))
        fornecedores.configure(height=50, image=fotoFornecedor, compound="left")

        transportadoras = criaBotao(frame, "Transportadoras", 0.66, 0.35, 0.24, lambda:telaCadastroTransportadoras(self))
        transportadoras.configure(height=50, image=fotoTransportadora, compound="left")

        funcionarios = criaBotao(frame, "Funcionários", 0.66, 0.46, 0.24, lambda:telaCadastroFuncionario(self))
        funcionarios.configure(height=50, image=fotoFuncionario, compound="left")


    criaBotao(frame, "Voltar", 0.33, 0.80, 0.18, lambda:frame.destroy())

