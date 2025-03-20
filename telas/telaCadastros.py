import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from telas.telaCadastroProdutos import telaCadastroProdutos
from telas.telaCadastroFuncionario import telaCadastroFuncionario
from telas.telaCadastroFornecedor import telaCadastroFornecedores
from telas.telaCadastroTransportadoras import telaCadastroTransportadoras 
from telas.telaCadastroClientes import telaCadastroClientes


def telaCadastros(self):
    self.frameTelaCadastros = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
    self.frameTelaCadastros.place(x=140, y=100)   
    self.frameTelaCadastros.grid_propagate(False)
    
    # título
    self.Acoes = ctk.CTkLabel(self.frameTelaCadastros, width=950, height=0, text="Cadastros", font=("Century Gothic bold", 30))
    self.Acoes.place(relx=0.5, y=50, anchor="center")
    
    # botão do cadastro de funcionarios # ! ainda não está ativo nem possui uma tela criada para ele
    self.botaoCadastro = ctk.CTkButton(self.frameTelaCadastros, text="Produtos", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaCadastroProdutos(self))
    self.botaoCadastro.place(relx=0.33, y=200, anchor="center")

    # botão de cadastrar clientes # ! ainda não está ativo nem possui uma tela criada para ele 
    self.botaoRelatorioDeVendas = ctk.CTkButton(self.frameTelaCadastros, text="Clientes", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaCadastroClientes(self))
    self.botaoRelatorioDeVendas.place(relx=0.66, y=200, anchor="center")

    # botão de cadastrar fornecedores
    self.botaogGerarPedido = ctk.CTkButton(self.frameTelaCadastros, text="Fornecedores", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaCadastroFornecedores(self))
    self.botaogGerarPedido.place(relx=0.33, y=250, anchor="center")

    # botão de cadastrar funcionários
    self.botaoContasPagarReceber = ctk.CTkButton(self.frameTelaCadastros, text="Funcionários", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaCadastroFuncionario(self))
    self.botaoContasPagarReceber.place(relx=0.66, y=250, anchor="center")

    # botão cadastrar transportadoras  
    self.botaoGerarFaturamento = ctk.CTkButton(self.frameTelaCadastros, text="Transportadoras", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaCadastroTransportadoras(self))
    self.botaoGerarFaturamento.place(relx=0.33, y=300, anchor="center")

    # botão para voltar para a tela
    self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaCadastros, text="Voltar", width=200, corner_radius=5, font=("Arial", 18), command=self.frameTelaCadastros.destroy)
    self.botaoGerarOrcamento.place(relx=0.33, y=650, anchor="center")
