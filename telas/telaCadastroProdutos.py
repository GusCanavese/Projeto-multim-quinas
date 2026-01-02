import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.registraProdutoNoBanco import registraProdutoNoBanco
from componentes import criaFrameJanela,  criarLabelEntry, criaFrame, criaBotao, criarLabelComboBox
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries

def telaCadastroProdutos(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    self.valor_formatado = ctk.StringVar(value="0,00")


    def formatar_moeda(event):
        entrada = event.widget  # widget que disparou o evento
        texto = entrada.get()

        texto_numerico = ''.join(filter(str.isdigit, texto))

        if not texto_numerico:
            texto_numerico = "0"

        while len(texto_numerico) < 3:
            texto_numerico = "0" + texto_numerico

        reais = texto_numerico[:-2]
        centavos = texto_numerico[-2:]

        valor = f"{int(reais)}.{centavos}"

        # Evita piscar o cursor para o final
        entrada.delete(0, "end")
        entrada.insert(0, valor)

    # opções
    opcoesCNPJ = ["Multimáquinas", "Polimáquinas", "Nutrigel", "Usados"]

    # titulo
    self.textoCadastro = ctk.CTkLabel(frame, width=950, height=0, text="Cadastrar Produto", font=("Century Gothic bold", 30))
    self.textoCadastro.place(relx=0.5, y=50, anchor="center")

    # Nome
    self.nomeProduto = criarLabelEntry(frame, "Nome do produto *", 0.1, 0.135, 0.20, None)
    self.marca = criarLabelEntry(frame, "Marca *", 0.33, 0.135, 0.15, None)
    self.ValorCusto = criarLabelEntry(frame, "Valor de custo *", 0.51, 0.135, 0.10, None)
    self.ValorVenda = criarLabelEntry(frame, "Valor de venda *", 0.64, 0.135, 0.12, None)

    self.ValorCusto.bind("<KeyRelease>", formatar_moeda)
    self.ValorVenda.bind("<KeyRelease>", formatar_moeda)

    self.Quantidade = criarLabelEntry(frame, "Quantidade", 0.79, 0.135, 0.10, None)


    self.CodigoInterno = criarLabelEntry(frame, "Código interno", 0.1, 0.26, 0.20, None)
    self.NCM = criarLabelEntry(frame, "Código NCM", 0.33, 0.26, 0.17, None)
    self.CFOP = criarLabelEntry(frame, "Código CFOP", 0.53, 0.26, 0.17, None)
    self.CEST = criarLabelEntry(frame, "Código CEST", 0.73, 0.26, 0.16, None)

    self.OrigemCST = criarLabelEntry(frame, "Origem (CST A)", 0.1, 0.4, 0.20, None)
    self.Descricao = criarLabelEntry(frame, "Descrição", 0.33, 0.4, 0.265, None)
    self.CNPJ = criarLabelComboBox(frame, "CNPJ *", 0.63, 0.4, 0.26, opcoesCNPJ)

    criaBotao(frame, "◀️ Voltar", 0.29, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.66, 0.80, 0.20, lambda:registraProdutoNoBanco(self, frame))
    aplicar_maiusculo_em_todos_entries(self)
