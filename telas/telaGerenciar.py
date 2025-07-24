import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from telas.telaCadastros import telaCadastros
from telas.telaGerarPedido import telaGerarPedido
from telas.telaRelatorioDeVendas import telaRelatorioDeVendas
from telas.telaEstoque import telaEstoque
from telas.telaGerenciarFuncionarios import telaGerenciarFuncionarios
from telas.telaGerarOrcamento  import telaGerarOrcamento
from telas.telaContasAPagarEAReceber import telaContasAPagarEAReceber
from funcoesTerceiras.escolherNotaFiscal import escolherNotaFiscal
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criaBotao

def telaGerenciar(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    label = ctk.CTkLabel(frame, text="Tela em desenvolvimento", font=("Arial", 20))
    label.place(relx=0.5, rely=0.5, anchor="center")

    criaBotao(frame, "◀️ Voltar", 0.33, 0.80, 0.18, lambda: frame.destroy())

    # criaBotao(frame, "Clientes", 0.5, 0.24, 0.24, lambda:telaGerenciarFuncionarios(self))
    # criaBotao(frame, "Clientes", 0.66, 0.24, 0.24, None)
    # criaBotao(frame, "Produtos", 0.33, 0.24, 0.24, None)
    # criaBotao(frame, "Fornecedores", 0.33, 0.30, 0.24, None)
    # criaBotao(frame, "Transportadoras", 0.33, 0.36, 0.24, None)
    # criaBotao(frame, "Funcionários", 0.66, 0.30, 0.24, None)