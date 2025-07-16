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

    usuarioBloqueado = self.logado
    cargo = Buscas.buscaCargoUsuarioBloqueado(usuarioBloqueado)

    self.Acoes = ctk.CTkLabel(frame, width=950, height=0, text="Ações", font=("Century Gothic bold", 30))
    self.Acoes.place(relx=0.5, y=50, anchor="center")


    if cargo == (('Vendedor(a) externo',),) or cargo == (('Vendedor(a) interno',),):
        criaBotao(frame, "Relatório de vendas/pedidos", 0.66, 0.24, 0.24, lambda: telaRelatorioDeVendas(self))
        criaBotao(frame, "Consultar estoque", 0.66, 0.30, 0.24, lambda: telaEstoque(self))
        criaBotao(frame, "Gerar pedido", 0.33, 0.24, 0.24, lambda: telaGerarPedido(self))
        criaBotao(frame, "Gerar orçamento", 0.33, 0.30, 0.24, lambda: telaGerarOrcamento(self))
        criaBotao(frame, "Trocar usuário", 0.33, 0.80, 0.18, lambda: frame.destroy())

    elif cargo == (('Financeiro',),) or cargo == (('Gerente',),):
        criaBotao(frame, "Cadastros", 0.33, 0.24, 0.24, lambda: telaCadastros(self))
        criaBotao(frame, "Gerar pedido", 0.33, 0.30, 0.24, lambda: telaGerarPedido(self))
        criaBotao(frame, "Gerar orçamento", 0.33, 0.36, 0.24, lambda: telaGerarOrcamento(self))
        criaBotao(frame, "Relatório de vendas/pedidos", 0.66, 0.24, 0.24, lambda: telaRelatorioDeVendas(self))
        criaBotao(frame, "Contas a pagar/receber", 0.66, 0.30, 0.24, lambda: telaContasAPagarEAReceber(self))
        criaBotao(frame, "Consultar estoque", 0.66, 0.36, 0.24, lambda: telaEstoque(self))
        criaBotao(frame, "Trocar usuário", 0.33, 0.80, 0.18, lambda: frame.destroy())