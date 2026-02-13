import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from telas.telaCadastros import telaCadastros
from telas.telaGerarPedido import telaGerarPedido
from telas.telaRelatorioDeVendas import telaRelatorioDeVendas
from telas.telaEstoque import telaEstoque
from telas.telaGerenciar import telaGerenciar
from telas.telaGerarOrcamento  import telaGerarOrcamento
from telas.telaContasAPagarEAReceber import telaContasAPagarEAReceber
from telas.telaFiscal import telaFiscal
from componentes import criaFrameJanela, criaFrameJanela, criaBotao
from PIL import Image, ImageTk
from funcoesTerceiras.carregamentoDasImagens import resource_path
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries





def telaAcoes(self):
    imgPedido = resource_path("arquivos/pedido.png")
    imgCadastros = resource_path("arquivos/cadastros.png")
    imgOrcamento = resource_path("arquivos/orcamento.png")
    imgGerenciar = resource_path("arquivos/gerenciar.png")
    imgRelatorio = resource_path("arquivos/relatorio.png")
    imgContas = resource_path("arquivos/contas.png")
    imgEstoque = resource_path("arquivos/estoque.png")
    fotoPedido = ImageTk.PhotoImage(Image.open(imgPedido).resize((60, 60)))
    fotoCadastros = ImageTk.PhotoImage(Image.open(imgCadastros).resize((55, 55)))
    fotoOrcamento = ImageTk.PhotoImage(Image.open(imgOrcamento).resize((55, 55)))
    fotoGerenciar = ImageTk.PhotoImage(Image.open(imgGerenciar).resize((55, 55)))
    fotoRelatorio = ImageTk.PhotoImage(Image.open(imgRelatorio).resize((55, 55)))
    fotoContas = ImageTk.PhotoImage(Image.open(imgContas).resize((55, 55)))
    fotoEstoque = ImageTk.PhotoImage(Image.open(imgEstoque).resize((55, 55)))


    
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    usuarioBloqueado = self.logado
    self.cargo = Buscas.buscaCargoUsuarioBloqueado(usuarioBloqueado)

    self.Acoes = ctk.CTkLabel(frame, width=950, height=0, text="Ações", font=("Century Gothic bold", 30))
    self.Acoes.place(relx=0.5, y=50, anchor="center")


    if self.cargo == (('Vendedor(a) externo',),) or self.cargo == (('Vendedor(a) interno',),):
        relatorioDeVendas = criaBotao(frame, "Vendas", 0.66, 0.24, 0.24, lambda: telaRelatorioDeVendas(self))
        relatorioDeVendas.configure(height=50, image=fotoRelatorio, compound="left")

        estoque = criaBotao(frame, "Estoque/Produtos", 0.66, 0.35, 0.24, lambda: telaEstoque(self))
        estoque.configure(height=50, image=fotoEstoque, compound="left")

        gerarPedido = criaBotao(frame, "Gerar pedido", 0.33, 0.35, 0.24, lambda: telaGerarPedido(self))
        gerarPedido.configure(height=50, image=fotoPedido, compound="left")

        gerarOrcamento = criaBotao(frame, "Gerar orçamento", 0.33, 0.46, 0.24, lambda: telaGerarOrcamento(self))
        gerarOrcamento.configure(height=50, image=fotoOrcamento, compound="left")

        cadastros = criaBotao(frame, "Cadastros", 0.33, 0.24, 0.24, lambda: telaCadastros(self))
        cadastros.configure(height=50, image=fotoCadastros, compound="left")

        criaBotao(frame, "Trocar usuário", 0.33, 0.80, 0.18, lambda: frame.destroy())


    elif self.cargo == (('Financeiro',),) or self.cargo == (('Gerente',),) or self.cargo == (('adm',),):

        cadastros = criaBotao(frame, "Cadastros", 0.33, 0.24, 0.24, lambda: telaCadastros(self))
        cadastros.configure(height=50, image=fotoCadastros, compound="left")
        
        gerarPedido = criaBotao(frame, "Gerar pedido", 0.33, 0.35, 0.24, lambda: telaGerarPedido(self))
        gerarPedido.configure(height=50, image=fotoPedido, compound="left")
        
        gerarOrcamento = criaBotao(frame, "Gerar orçamento", 0.33, 0.46, 0.24, lambda: telaGerarOrcamento(self))
        gerarOrcamento.configure(height=50, image=fotoOrcamento, compound="left")

        gerenciar = criaBotao(frame, "Gerenciar cadastros", 0.33, 0.57, 0.24, lambda: telaGerenciar(self))
        gerenciar.configure(height=50, image=fotoGerenciar, compound="left")

        relatorioDeVendas = criaBotao(frame, "Vendas", 0.66, 0.24, 0.24, lambda: telaRelatorioDeVendas(self))
        relatorioDeVendas.configure(height=50, image=fotoRelatorio, compound="left")
        
        contasAPagar = criaBotao(frame, "Contas a pagar/receber", 0.66, 0.35, 0.24, lambda: telaContasAPagarEAReceber(self))
        contasAPagar.configure(height=50, image=fotoContas, compound="left")
        
        estoque = criaBotao(frame, "Estoque/Produtos", 0.66, 0.46, 0.24, lambda: telaEstoque(self))
        estoque.configure(height=50, image=fotoEstoque, compound="left")

        fiscal = criaBotao(frame, "Fiscal", 0.66, 0.57, 0.24, lambda: telaFiscal(self))
        fiscal.configure(height=50, image=None, compound="left")

        criaBotao(frame, "Trocar usuário", 0.33, 0.80, 0.18, lambda: frame.destroy())
    aplicar_maiusculo_em_todos_entries(self)
