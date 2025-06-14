import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.registraProdutoNoBanco import registraProdutoNoBanco
from componentes import criarLabelEntry, criaFrame, criaBotao, criarLabelComboBox

def telaCadastroProdutos(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    # opções
    opcoesDescricao = ["Nenhum","Uso consumo", "Mercadoria para revenda", "Peças para reposição"]
    opcoesCNPJ = ["Nenhum","Multimáquinas", "Polimáquinas", "Refrimaquinas"]

    # titulo
    self.textoCadastro = ctk.CTkLabel(frame, width=950, height=0, text="Cadastrar Produto", font=("Century Gothic bold", 30))
    self.textoCadastro.place(relx=0.5, y=50, anchor="center")

    # Nome
    self.nomeProduto = criarLabelEntry(frame, "Nome do produto", 0.1, 0.135, 0.20, None)
    self.ValorCusto = criarLabelEntry(frame, "Valor de custo", 0.33, 0.135, 0.20, None)
    self.ValorVenda = criarLabelEntry(frame, "Valor de venda", 0.56, 0.135, 0.20, None)
    self.Quantidade = criarLabelEntry(frame, "Quantidade", 0.79, 0.135, 0.10, None)

    self.CodigoInterno = criarLabelEntry(frame, "Código interno", 0.1, 0.26, 0.20, None)
    self.NCM = criarLabelEntry(frame, "Código NCM", 0.33, 0.26, 0.17, None)
    self.CFOP = criarLabelEntry(frame, "Código CFOP", 0.53, 0.26, 0.17, None)
    self.CEST = criarLabelEntry(frame, "Código CEST", 0.73, 0.26, 0.16, None)

    self.OrigemCST = criarLabelEntry(frame, "Origem (CST A)", 0.1, 0.4, 0.20, None)
    self.Descricao = criarLabelComboBox(frame, "Descrição", 0.33, 0.4, 0.265, opcoesDescricao)
    self.CNPJ = criarLabelComboBox(frame, "CNPJ", 0.63, 0.4, 0.26, opcoesCNPJ)

    criaBotao(frame, "Voltar", 0.29, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.66, 0.80, 0.20, lambda:registraProdutoNoBanco(self, frame))
