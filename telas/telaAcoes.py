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
from telas.telaContasAPagarEAReceber import telaContasAPagarEAReceber
from funcoesTerceiras.escolherNotaFiscal import escolherNotaFiscal
from componentes import criaFrame, criaBotao


def telaAcoes(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)

    usuarioBloqueado = self.login.get()
    cargo = Buscas.buscaCargoUsuarioBloqueado(usuarioBloqueado)

    # título
    self.Acoes = ctk.CTkLabel(frame, width=950, height=0, text="Ações", font=("Century Gothic bold", 30))
    self.Acoes.place(relx=0.5, y=50, anchor="center")

    if cargo == (('Vendedor(a) externo',),):
        criaBotao(frame, "Relatório de vendas/pedidos", 0.66, 0.24, 0.24, lambda:telaRelatorioDeVendas(self))
        criaBotao(frame, "Consultar estoque", 0.66, 0.24, 0.24, lambda:telaEstoque(self))

        criaBotao(frame, "Gerar pedido", 0.33, 0.30, 0.24, lambda:telaGerarPedido(self))
        criaBotao(frame, "Gerar orçamento", 0.33, 0.36, 0.24, lambda:telaGerarOrcamento(self))
        criaBotao(frame, "Trocar usuário", 0.33, 0.80, 0.18, lambda:frame.destroy())

    else:
        # REFATORADA
        criaBotao(frame, "Cadastros", 0.33, 0.24, 0.24, lambda:telaCadastros(self))

        #! em andamento
        criaBotao(frame, "Gerar pedido", 0.33, 0.30, 0.24, lambda:telaGerarPedido(self))

        # NÃO REFATORADA
        criaBotao(frame, "Gerar orçamento", 0.33, 0.36, 0.24, lambda:telaGerarOrcamento(self))

        # REFATORADA
        criaBotao(frame, "Relatório de vendas/pedidos", 0.66, 0.24, 0.24, lambda:telaRelatorioDeVendas(self))

        # REFATORADA
        criaBotao(frame, "Contas a pagar/receber", 0.66, 0.30, 0.24, lambda:telaContasAPagarEAReceber(self))

        # REFATORADA  
        criaBotao(frame, "Consultar estoque", 0.66, 0.36, 0.24, lambda:telaEstoque(self))
        
        # REFATORADA
        criaBotao(frame, "Trocar usuário", 0.33, 0.80, 0.18, lambda:frame.destroy())