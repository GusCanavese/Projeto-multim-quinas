import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas
from tkinter import messagebox
import requests
from funcoesTerceiras.registraClienteNoBanco import registraClienteNoBanco
from componentes import criaFrame, criarLabelEntry, criaBotao, criaBotaoPequeno
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries

def telaCadastroClientes(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    bairro = ctk.StringVar()

    self.textoCadastro = ctk.CTkLabel(frame, width=950, height=0, text="Cadastrar cliente", font=("Century Gothic bold", 30))
    self.textoCadastro.place(relx=0.5, rely=0.08, anchor="center")
    

    #nome
    self.nomeCliente = criarLabelEntry(frame, "Nome *", 0.15, 0.15, 0.30, None)
    self.cpf = criarLabelEntry(frame, "CPF *", 0.15, 0.25, 0.30, None)
    self.cnpj = criarLabelEntry(frame, "CNPJ", 0.15, 0.35, 0.30, None)
    self.IEcliente = criarLabelEntry(frame, "Inscrição Estadual", 0.15, 0.45, 0.30, None)
    self.RGcliente = criarLabelEntry(frame, "Insira o RG", 0.15, 0.55, 0.30, None)

    self.CEPcliente    = criarLabelEntry(frame, "CEP *", 0.45+0.05, 0.15, 0.12, None)
    self.numeroCliente = criarLabelEntry(frame, "Número *", 0.58+0.05, 0.15, 0.05, None)
    self.bairroCliente = criarLabelEntry(frame, "Bairro *", 0.64+0.05, 0.15, 0.16, bairro)
    self.cidadeCliente = criarLabelEntry(frame, "Endereço *", 0.45+0.05, 0.25, 0.35, None)
    self.referencia    = criarLabelEntry(frame, "Referência *", 0.45+0.05, 0.35, 0.35, None)




    criaBotaoPequeno(frame, "Buscar CEP", 0.815, 0.45, 0.07, lambda:buscaCep(self.CEPcliente.get(), self.numeroCliente.get()))

    self.CEPcliente.bind("<Return>", lambda event: buscaCep(self.CEPcliente.get(), self.numeroCliente.get()))
    self.numeroCliente.bind("<Return>", lambda event: buscaCep(self.CEPcliente.get(), self.numeroCliente.get()))

    def buscaCep(cep, numero):
        url = f"https://cep.awesomeapi.com.br/json/{cep}"
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            endereco_completo = f"{dados.get('address', '')} - {numero} - {dados.get('district', '')} - {dados.get('city', '')} - {dados.get('state', '')}"
            bairro.set(dados.get('district', ''))
            if numero == '':
                messagebox.showerror(title="Não encontrado", message="Campo 'Número não deve ficar em branco'")
            else:
                self.cidadeCliente.delete(0, ctk.END)
                self.cidadeCliente.insert(0, endereco_completo)
        else:
            messagebox.showerror(title="Não encontrado", message="CEP não foi encontrado")

    # ================ Botões =====================#

    criaBotao(frame, "Voltar", 0.29, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.66, 0.80, 0.20, lambda:registraClienteNoBanco(self, frame))
    aplicar_maiusculo_em_todos_entries(self)