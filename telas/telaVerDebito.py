import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from telas.telaProdutos import telaProdutos
from componentes import criarLabelLateralEntry, criaBotao, criarLabelEntry, criaFrame, criarLabelLateralComboBox, criarLabelComboBox

def telaVerDebito(self, lista):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)

    criarLabelEntry(frame, "Número da NF", 0.1, 0.05, 0.07, lista[4])
    criarLabelEntry(frame, "Série", 0.2, 0.05, 0.07, lista[7])
    criarLabelEntry(frame, "Chave da NF", 0.3, 0.05, 0.3, lista[6])

    destinatario = ctk.CTkLabel(frame, text="Destinatário----------")
    destinatario.place(relx=0.1, rely=0.15)
    criarLabelEntry(frame, "Razão social", 0.1, 0.20, 0.3, lista[12])
    criarLabelEntry(frame, "CNPJ", 0.45, 0.20, 0.15, lista[11])

    emitente = ctk.CTkLabel(frame, text="Emitente----------")
    emitente.place(relx=0.1, rely=0.3)
    criarLabelEntry(frame, "Razão social", 0.1, 0.35, 0.3, lista[5])
    criarLabelEntry(frame, "CNPJ", 0.45, 0.35, 0.15, lista[10])
    print(lista[9].get())
    dataHora = "2025-05-28 15:53:00"
    data = dataHora.split(" ")[0]
    hora = dataHora.split(" ")[1]

    criarLabelLateralEntry(frame, "Status",             0.75, 0.09, 0.1, lista[0])
    criarLabelLateralEntry(frame, "Data documento",     0.75, 0.14, 0.1, lista[9])
    criarLabelLateralEntry(frame, "Hora entrada/saída", 0.75, 0.24, 0.1, lista[9])
    criarLabelLateralEntry(frame, "Data criação",       0.75, 0.29, 0.1, lista[26])
    criarLabelLateralEntry(frame, "Data confirmação",   0.75, 0.34, 0.1, None)
    criarLabelLateralComboBox(frame, "Data finalidade", 0.75, 0.39, 0.1, None)
    criarLabelLateralComboBox(frame, "Data situação",   0.75, 0.44, 0.1, None)

    criarLabelEntry(frame, "CFOP", 0.1, 0.49, 0.07, None)
    criarLabelEntry(frame, "Natureza da Operação", 0.2, 0.49, 0.4, None)

    transporte = ctk.CTkLabel(frame, text="Transporte----------")
    transporte.place(relx=0.1, rely=0.59)
    self.modalidadeDoFrete = criarLabelComboBox(frame, "Modalidade do frete", 0.1, 0.64, 0.27, None)
    criarLabelComboBox(frame, "Forma de pagamento", 0.4, 0.64, 0.2, None)

    criaBotao(frame, "Próximo - Tela de Produtos", 0.25, 0.94, 0.15, lambda:telaProdutos(self, lista)).place(anchor="nw")
    criaBotao(frame, "Voltar", 0.05, 0.94, 0.15, lambda: frame.destroy()).place(anchor="nw")