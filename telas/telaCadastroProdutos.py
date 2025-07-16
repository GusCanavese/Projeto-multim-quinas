import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.registraProdutoNoBanco import registraProdutoNoBanco
from componentes import criarLabelEntry, criaFrame, criaBotao, criarLabelComboBox

def telaCadastroProdutos(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    # opções
    opcoesCNPJ = ["Multimáquinas", "Polimáquinas", "Nutrigel", "Usados"]

    # titulo
    self.textoCadastro = ctk.CTkLabel(frame, width=950, height=0, text="Cadastrar Produto", font=("Century Gothic bold", 30))
    self.textoCadastro.place(relx=0.5, y=50, anchor="center")

    # Nome
    self.nomeProduto = criarLabelEntry(frame, "Nome do produto", 0.1, 0.135, 0.20, None)
    self.valorCusto = criarLabelEntry(frame, "Valor de custo", 0.33, 0.135, 0.20, None)
    self.ValorVenda = criarLabelEntry(frame, "Valor de venda", 0.56, 0.135, 0.20, None)
    self.Quantidade = criarLabelEntry(frame, "Quantidade", 0.79, 0.135, 0.10, None)
    self.valorCusto.configure(placeholder_text="R$ 0,00")  
    self.ValorVenda.configure(placeholder_text="R$ 0,00")

    self.CodigoInterno = criarLabelEntry(frame, "Código interno", 0.1, 0.26, 0.20, None)
    self.NCM = criarLabelEntry(frame, "Código NCM", 0.33, 0.26, 0.17, None)
    self.CFOP = criarLabelEntry(frame, "Código CFOP", 0.53, 0.26, 0.17, None)
    self.CEST = criarLabelEntry(frame, "Código CEST", 0.73, 0.26, 0.16, None)

    self.OrigemCST = criarLabelEntry(frame, "Origem (CST A)", 0.1, 0.4, 0.20, None)
    self.Descricao = criarLabelEntry(frame, "Descrição", 0.33, 0.4, 0.265, None)
    self.CNPJ = criarLabelComboBox(frame, "CNPJ", 0.63, 0.4, 0.26, opcoesCNPJ)

    self.valorCusto.bind("<Button-1>", lambda e: self.valorCusto.delete(0, "end") if self.valorCusto.get() in ("0", "0,00", "0.00") else None)
    criaBotao(frame, "Voltar", 0.29, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.66, 0.80, 0.20, lambda:registraProdutoNoBanco(self, frame))
