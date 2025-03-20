import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from telas.telaCadastros import telaCadastros
from telas.telaDefineCnpjDoProduto import telaDefineCnpjDoProduto

def telaAcoes(self):
    self.frameTelaAcoes = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
    self.frameTelaAcoes.place(x=140, y=100)     
    self.frameTelaAcoes.grid_propagate(False)
    usuarioBloqueado = self.login.get()
    cargo = Buscas.buscaCargoUsuarioBloqueado(usuarioBloqueado)


    
    # título
    self.Acoes = ctk.CTkLabel(self.frameTelaAcoes, width=950, height=0, text="Ações", font=("Century Gothic bold", 30))
    self.Acoes.place(relx=0.5, y=50, anchor="center")

    # condição que bloqueia o acesso dos vendedores externos
    if cargo == (('Vendedor(a) externo',),):
        # botão de relatório de vendas # ! ainda não está ativo nem possui uma tela criada para ele 
        self.botaoRelatorioDeVendas = ctk.CTkButton(self.frameTelaAcoes, text="Relatório de vendas", width=300, corner_radius=5, font=("Arial", 18), command=self)
        self.botaoRelatorioDeVendas.place(relx=0.66, y=200, anchor="center")

        # botão de gerar pedidos # ! ainda não está ativo nem possui uma tela criada para ele
        self.botaogGerarPedido = ctk.CTkButton(self.frameTelaAcoes, text="Gerar pedido", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaDefineCnpjDoProduto(self))
        self.botaogGerarPedido.place(relx=0.33, y=250, anchor="center")

        # botão de consultar estoque # ! ainda não está ativo nem possui uma tela criada para ele 
        self.botaoConsultarEstoque = ctk.CTkButton(self.frameTelaAcoes, text="Consultar estoque", width=300, corner_radius=5, font=("Arial", 18), command=self)
        self.botaoConsultarEstoque.place(relx=0.66, y=250, anchor="center")

        # botão de gerar orçamento # ! ainda não está ativo nem possui uma tela criada para ele 
        self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaAcoes, text="Gerar orçamento", width=300, corner_radius=5, font=("Arial", 18), command=self)
        self.botaoGerarOrcamento.place(relx=0.33, y=200, anchor="center") 
    else:
        # botão do cada
        self.botaoCadastro = ctk.CTkButton(self.frameTelaAcoes, text="Cadastros", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaCadastros(self))
        self.botaoCadastro.place(relx=0.33, y=200, anchor="center")

        # botão de relatório de vendas # ! ainda não está ativo nem possui uma tela criada para ele 
        self.botaoRelatorioDeVendas = ctk.CTkButton(self.frameTelaAcoes, text="Relatório de vendas", width=300, corner_radius=5, font=("Arial", 18), command=self)
        self.botaoRelatorioDeVendas.place(relx=0.66, y=200, anchor="center")

        # botão de gerar pedidos
        self.botaogGerarPedido = ctk.CTkButton(self.frameTelaAcoes, text="Gerar pedido", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaDefineCnpjDoProduto(self))
        self.botaogGerarPedido.place(relx=0.33, y=250, anchor="center")

        # botão de contas a pagar e a receber da loja # ! ainda não está ativo nem possui uma tela criada para ele 
        self.botaoContasPagarReceber = ctk.CTkButton(self.frameTelaAcoes, text="Contas a pagar/receber", width=300, corner_radius=5, font=("Arial", 18), command=self)
        self.botaoContasPagarReceber.place(relx=0.66, y=250, anchor="center")

        # botão de gerar faturamento # ! ainda não está ativo nem possui uma tela criada para ele 
        self.botaoGerarFaturamento = ctk.CTkButton(self.frameTelaAcoes, text="Gerar faturamento", width=300, corner_radius=5, font=("Arial", 18), command=self)
        self.botaoGerarFaturamento.place(relx=0.33, y=300, anchor="center")

        # botão de consultar estoque # ! ainda não está ativo nem possui uma tela criada para ele 
        self.botaoConsultarEstoque = ctk.CTkButton(self.frameTelaAcoes, text="Consultar estoque", width=300, corner_radius=5, font=("Arial", 18), command=self)
        self.botaoConsultarEstoque.place(relx=0.66, y=300, anchor="center")

        # botão de gerar orçamento # ! ainda não está ativo nem possui uma tela criada para ele 
        self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaAcoes, text="Gerar orçamento", width=300, corner_radius=5, font=("Arial", 18), command=self)
        self.botaoGerarOrcamento.place(relx=0.33, y=350, anchor="center")

    # botão de trocar usuário 
    self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaAcoes, text="Trocar usuário", width=200, corner_radius=5, font=("Arial", 18), command=self.frameTelaAcoes.destroy)
    self.botaoGerarOrcamento.place(relx=0.33, y=650, anchor="center")

