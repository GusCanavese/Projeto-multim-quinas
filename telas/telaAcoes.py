import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from telas.telaCadastros import telaCadastros
from telas.telaGerarPedido import telaGerarPedido
from telas.telaRelatorioDeVendas import telaRelatorioDeVendas
from telas.telaEstoque import telaEstoque
from telas.telaGerarOrcamento  import telaGerarOrcamento


def telaAcoes(self):
    self.frameTelaAcoes = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
    self.frameTelaAcoes.place(relx=0.5, rely=0.5, anchor="center")  
    self.frameTelaAcoes.grid_propagate(False)

    usuarioBloqueado = self.login.get()
    cargo = Buscas.buscaCargoUsuarioBloqueado(usuarioBloqueado)

    # título
    self.Acoes = ctk.CTkLabel(self.frameTelaAcoes, width=950, height=0, text="Ações", font=("Century Gothic bold", 30))
    self.Acoes.place(relx=0.5, y=50, anchor="center")

    if cargo == (('Vendedor(a) externo',),):
        self.botaoRelatorioDeVendas = ctk.CTkButton(self.frameTelaAcoes, text="Relatório de vendas/pedidos", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaRelatorioDeVendas(self))
        self.botaoRelatorioDeVendas.place(relx=0.66, y=200, anchor="center")

        self.botaogGerarPedido = ctk.CTkButton(self.frameTelaAcoes, text="Gerar pedido", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaGerarPedido(self))
        self.botaogGerarPedido.place(relx=0.33, y=250, anchor="center")

        self.botaoConsultarEstoque = ctk.CTkButton(self.frameTelaAcoes, text="Consultar estoque", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaEstoque(self))
        self.botaoConsultarEstoque.place(relx=0.66, y=250, anchor="center")

        self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaAcoes, text="Gerar orçamento", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaGerarOrcamento(self))
        self.botaoGerarOrcamento.place(relx=0.33, y=200, anchor="center")
    else:
        self.botaoCadastro = ctk.CTkButton(self.frameTelaAcoes, text="Cadastros", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaCadastros(self))
        self.botaoCadastro.place(relx=0.33, y=200, anchor="center")

        self.botaoRelatorioDeVendas = ctk.CTkButton(self.frameTelaAcoes, text="Relatório de vendas/pedidos", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaRelatorioDeVendas(self))
        self.botaoRelatorioDeVendas.place(relx=0.66, y=200, anchor="center")

        self.botaogGerarPedido = ctk.CTkButton(self.frameTelaAcoes, text="Gerar pedido", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaGerarPedido(self))
        self.botaogGerarPedido.place(relx=0.33, y=250, anchor="center")

        self.botaoContasPagarReceber = ctk.CTkButton(self.frameTelaAcoes, text="Contas a pagar/receber", width=300, corner_radius=5, font=("Arial", 18), command=self)
        self.botaoContasPagarReceber.place(relx=0.66, y=250, anchor="center")

        self.botaoConsultarEstoque = ctk.CTkButton(self.frameTelaAcoes, text="Consultar estoque", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaEstoque(self))
        self.botaoConsultarEstoque.place(relx=0.66, y=300, anchor="center")

        self.botaoGerarOrcamento = ctk.CTkButton(self.frameTelaAcoes, text="Gerar orçamento", width=300, corner_radius=5, font=("Arial", 18), command=lambda:telaGerarOrcamento(self))
        self.botaoGerarOrcamento.place(relx=0.33, y=300, anchor="center")

    # botão de trocar usuário 
    self.botaoTrocarUsuario = ctk.CTkButton(self.frameTelaAcoes, text="Trocar usuário", width=200, corner_radius=5, font=("Arial", 18), command=self.frameTelaAcoes.destroy)
    self.botaoTrocarUsuario.place(relx=0.33, y=650, anchor="center")
