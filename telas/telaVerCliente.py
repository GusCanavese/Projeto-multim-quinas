import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
import customtkinter as ctk
from componentes import criaFrameJanela, criarLabelEntry, criaBotao


def telaVerCliente(self, cliente):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    nome, cpf, cnpj, telefone, cep, cidade, referencia, numero, bairro, rua = cliente

    tabs = ctk.CTkTabview(frame, fg_color="transparent")
    tabs.place(relx=0.5, rely=0.45, relwidth=0.92, relheight=0.78, anchor="center")

    tab_ident = tabs.add("Identificação")
    tab_endereco = tabs.add("Endereço")
    tabs.set("Identificação")

    x_esq = 0.05
    x_dir = 0.55
    largura = 0.4

    criarLabelEntry(tab_ident, "Nome", x_esq, 0.1, largura, ctk.StringVar(value=nome))
    criarLabelEntry(tab_ident, "CPF", x_esq, 0.25, largura, ctk.StringVar(value=cpf))
    criarLabelEntry(tab_ident, "CNPJ", x_esq, 0.4, largura, ctk.StringVar(value=cnpj))
    criarLabelEntry(tab_ident, "Telefone", x_dir, 0.1, largura, ctk.StringVar(value=telefone))
    criarLabelEntry(tab_ident, "Referência", x_dir, 0.25, largura, ctk.StringVar(value=referencia))

    criarLabelEntry(tab_endereco, "Rua", x_esq, 0.1, largura, ctk.StringVar(value=rua))
    criarLabelEntry(tab_endereco, "Número", x_esq, 0.25, largura, ctk.StringVar(value=numero))
    criarLabelEntry(tab_endereco, "Bairro", x_esq, 0.4, largura, ctk.StringVar(value=bairro))
    criarLabelEntry(tab_endereco, "Cidade", x_dir, 0.1, largura, ctk.StringVar(value=cidade))
    criarLabelEntry(tab_endereco, "CEP", x_dir, 0.25, largura, ctk.StringVar(value=cep))

    criaBotao(frame, "◀️ Voltar", 0.15, 0.94, 0.15, lambda: frame.destroy())
