import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.registraClienteNoBanco import registraClienteNoBanco
from componentes import criaFrame, criarLabelEntry, criaBotao

def telaCadastroClientes(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)

    self.textoCadastro = ctk.CTkLabel(frame, width=950, height=0, text="Cadastrar cliente", font=("Century Gothic bold", 30))
    self.textoCadastro.place(relx=0.5, rely=0.08, anchor="center")

    #nome
    self.nomeCliente = criarLabelEntry(frame, "Nome", 0.1+0.05, 0.15, 0.30, None)
    self.CPF_PJcliente = criarLabelEntry(frame, "Documento", 0.1+0.05, 0.25, 0.30, None)
    self.IEcliente = criarLabelEntry(frame, "Inscrição Estadual", 0.1+0.05, 0.35, 0.30, None)
    self.RGcliente = criarLabelEntry(frame, "Insira o RG", 0.1+0.05, 0.45, 0.30, None)

    self.enderecoCliente = criarLabelEntry(frame, "Endereço", 0.45+0.05, 0.15, 0.35, None)
    self.CEPcliente = criarLabelEntry(frame, "CEP", 0.45+0.05, 0.25, 0.12, None)
    self.numeroCliente = criarLabelEntry(frame, "Número", 0.58+0.05, 0.25, 0.05, None)
    self.bairroCliente = criarLabelEntry(frame, "Bairro", 0.64+0.05, 0.25, 0.16, None)

    self.cidadeCliente = criarLabelEntry(frame, "Bairro", 0.45+0.05, 0.35, 0.30, None)

    # ================ Botões =====================#

    criaBotao(frame, "Voltar", 0.29, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.66, 0.80, 0.20, lambda:registraClienteNoBanco(self, frame))