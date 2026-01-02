import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from funcoesTerceiras import filtrar
from componentes import criaFrameJanela, criarLabelEntry, criaBotao, criaLabel
from telas.telaCadastroClientes import telaCadastroClientes


def telaGerenciarClientes(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    frameClientes = criaFrameJanela(frame, 0.5, 0.5, 0.95, 0.7, self.corFundo)

    filtroCliente = criarLabelEntry(frame, "Filtrar", 0.055, 0.04, 0.22, None)

    if self.cargo == (('Vendedor(a) externo',),) or self.cargo == (('Vendedor(a) interno',),):
        cadastrar = criaBotao(frame, "+ Cadastrar clientes", 0.6, 0.08, 0.24, lambda: telaCadastroClientes(self))
        cadastrar.configure(height=50)
    else:
        cadastrar = criaBotao(frame, "+ Cadastrar clientes", 0.6, 0.08, 0.24, lambda: telaCadastroClientes(self, False))
        cadastrar.configure(height=50)

    criaBotao(
        frame,
        "Buscar",
        0.84,
        0.08,
        0.1,
        lambda: filtrar.filtrarClientes(self, frameClientes, filtroCliente.get()),
    )
    criaBotao(frame, "◀️ Voltar", 0.15, 0.94, 0.15, lambda: frame.destroy())

    colunas = ["Cliente", "CPF/CNPJ", "Telefone", "Cidade", "CEP"]
    x = 0.03
    y = 0.05

    for i, coluna in enumerate(colunas):
        if i == 0:
            criaLabel(frameClientes, coluna, x, y, 0.25, self.cor)
            x += 0.255
        elif i == 1:
            criaLabel(frameClientes, coluna, x, y, 0.17, self.cor)
            x += 0.175
        elif i == 2:
            criaLabel(frameClientes, coluna, x, y, 0.12, self.cor)
            x += 0.125
        elif i == 3:
            criaLabel(frameClientes, coluna, x, y, 0.15, self.cor)
            x += 0.155
        else:
            criaLabel(frameClientes, coluna, x, y, 0.1, self.cor)
            x += 0.105

    filtrar.filtrarClientes(self, frameClientes, filtroCliente.get())
