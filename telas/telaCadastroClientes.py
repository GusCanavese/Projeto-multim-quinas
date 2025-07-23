import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from tkinter import messagebox
import requests
from funcoesTerceiras.registraClienteNoBanco import registraClienteNoBanco
from componentes import criaFrame, criaFrameJanela, criarLabelEntry, criaBotao, criaBotaoPequeno
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries

def telaCadastroClientes(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    bairro = ctk.StringVar()
    rua = ctk.StringVar()
    cidade = ctk.StringVar()
    estado = ctk.StringVar()

    self.textoCadastro = ctk.CTkLabel(frame, width=950, height=0, text="Cadastrar cliente", font=("Century Gothic bold", 30))
    self.textoCadastro.place(relx=0.5, rely=0.08, anchor="center")
    

    #nome
    self.nomeCliente = criarLabelEntry(frame, "Nome *", 0.15, 0.15, 0.30, None)
    self.cpf = criarLabelEntry(frame, "CPF *", 0.15, 0.25, 0.30, None)
    self.cnpj = criarLabelEntry(frame, "CNPJ", 0.15, 0.35, 0.30, None)
    self.IEcliente = criarLabelEntry(frame, "Inscrição Estadual", 0.15, 0.45, 0.30, None)
    self.RGcliente = criarLabelEntry(frame, "Insira o RG", 0.15, 0.55, 0.15, None)
    self.telefoneCliente = criarLabelEntry(frame, "Telefone *", 0.31, 0.55, 0.14, None)

    self.CEPcliente    = criarLabelEntry(frame, "CEP", 0.45+0.05, 0.15, 0.12, None)
    self.rua = criarLabelEntry(frame, "Rua *", 0.63, 0.15, 0.22, rua)

    self.bairroCliente = criarLabelEntry(frame, "Bairro *", 0.50, 0.25, 0.20, bairro)
    self.numeroCliente = criarLabelEntry(frame, "Número *", 0.71, 0.25, 0.14, None)

    self.cidadeCliente = criarLabelEntry(frame, "Cidade *", 0.50, 0.35, 0.24, cidade)
    self.estadoCliente = criarLabelEntry(frame, "Estado *", 0.75, 0.35, 0.10, estado)

    self.referencia    = criarLabelEntry(frame, "Referência ", 0.45+0.05, 0.45, 0.35, None)

    self.CEPcliente.bind("<Return>", lambda event: buscaCep(self.CEPcliente.get(), self.numeroCliente.get()))
    self.CEPcliente.bind("<Tab>", lambda event: buscaCep(self.CEPcliente.get(), self.numeroCliente.get()) if self.CEPcliente.get().strip() else None)
    self.numeroCliente.bind("<Return>", lambda event: buscaCep(self.CEPcliente.get(), self.numeroCliente.get()))

    def buscaCep(cep, numero):
        url = f"https://cep.awesomeapi.com.br/json/{cep}"
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            bairro.set(dados.get('district', ''))
            rua.set(dados.get('address', ''))
            cidade.set(dados.get('city', ''))
            estado.set(dados.get('state', ''))
        else:
            messagebox.showerror(title="Não encontrado", message="CEP não foi encontrado")

    # ================ Botões =====================#

    criaBotao(frame, "Voltar", 0.29, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.66, 0.80, 0.20, lambda:registraClienteNoBanco(self, frame))
    aplicar_maiusculo_em_todos_entries(self)