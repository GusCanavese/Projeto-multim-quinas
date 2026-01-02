import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from tkinter import messagebox
from consultas.select import Buscas
from telas.telaCadastros import telaCadastros
from telas.telaGerarPedido import telaGerarPedido
from telas.telaRelatorioDeVendas import telaRelatorioDeVendas
from telas.telaEstoque import telaEstoque
from telas.telaGerenciarFuncionarios import telaGerenciarFuncionarios
from telas.telaGerenciarClientes import telaGerenciarClientes
from telas.telaGerarOrcamento  import telaGerarOrcamento
from telas.telaContasAPagarEAReceber import telaContasAPagarEAReceber
from funcoesTerceiras.escolherNotaFiscal import escolherNotaFiscal
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criaBotao

def telaGerenciar(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    def mostrar_tela_em_desenvolvimento():
        messagebox.showinfo(title="Aviso", message="Tela em desenvolvimento")

    clientes = criaBotao(frame, "Gerenciar clientes", 0.33, 0.24, 0.24, lambda: telaGerenciarClientes(self))
    clientes.configure(height=50)
    fornecedores = criaBotao(frame, "Gerenciar fornecedores", 0.66, 0.24, 0.24, mostrar_tela_em_desenvolvimento)
    fornecedores.configure(height=50)
    transportadoras = criaBotao(frame, "Gerenciar transportadoras", 0.33, 0.35, 0.24, mostrar_tela_em_desenvolvimento)
    transportadoras.configure(height=50)

    criaBotao(frame, "◀️ Voltar", 0.15, 0.94, 0.15, lambda: frame.destroy())

    # criaBotao(frame, "Clientes", 0.5, 0.24, 0.24, lambda:telaGerenciarFuncionarios(self))
    # criaBotao(frame, "Clientes", 0.66, 0.24, 0.24, None)
    # criaBotao(frame, "Produtos", 0.33, 0.24, 0.24, None)
    # criaBotao(frame, "Fornecedores", 0.33, 0.30, 0.24, None)
    # criaBotao(frame, "Transportadoras", 0.33, 0.36, 0.24, None)
    # criaBotao(frame, "Funcionários", 0.66, 0.30, 0.24, None)
