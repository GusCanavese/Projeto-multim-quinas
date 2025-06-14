import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from telas.telaCadastroProdutos import telaCadastroProdutos
from telas.telaCadastroFuncionario import telaCadastroFuncionario
from telas.telaCadastroFornecedor import telaCadastroFornecedores
from telas.telaCadastroTransportadoras import telaCadastroTransportadoras 
from telas.telaCadastroClientes import telaCadastroClientes
from componentes import criaFrame, criaBotao


def telaCadastros(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)

    # título

    self.Acoes = ctk.CTkLabel(frame, width=950, height=0, text="Cadastros", font=("Century Gothic bold", 30))
    self.Acoes.place(relx=0.5, y=50, anchor="center")
    
    criaBotao(frame, "Produtos", 0.33, 0.24, 0.24, lambda:telaCadastroProdutos(self))
    criaBotao(frame, "Fornecedores", 0.33, 0.30, 0.24, lambda:telaCadastroFornecedores(self))
    criaBotao(frame, "Transportadoras", 0.33, 0.36, 0.24, lambda:telaCadastroTransportadoras(self))
    
    criaBotao(frame, "Clientes", 0.66, 0.24, 0.24, lambda:telaCadastroClientes(self))
    criaBotao(frame, "Funcionários", 0.66, 0.30, 0.24, lambda:telaCadastroFuncionario(self))

    criaBotao(frame, "Voltar", 0.33, 0.80, 0.18, lambda:frame.destroy())

