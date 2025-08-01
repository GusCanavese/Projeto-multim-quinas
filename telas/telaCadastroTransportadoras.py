import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
import gc
from funcoesTerceiras.registraTransportadoraNoBanco import registraTransportadoraNoBanco
from componentes import criaFrameJanela, criaFrameJanela, criaSimouNao, criarLabelEntry, criaBotao
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries
from tkinter import messagebox
import requests



def telaCadastroTransportadoras(self):
    bairro = ctk.StringVar()
    rua = ctk.StringVar()
    cidade = ctk.StringVar()
    estado = ctk.StringVar()

    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    self.tituloCadastroTransportadora = ctk.CTkLabel(frame, height=0, text="Cadastrar Transportadoras", font=("Century Gothic bold", 30))
    self.tituloCadastroTransportadora.place(relx=0.5, y=40, anchor="center")
    


    def meDesmarqueTransportadora(checkboxSelecionada):
        if checkboxSelecionada == "Sim.":
            self.emailTransportadora.configure(state="normal")
        else:
            self.emailTransportadora.configure(state="disabled")
    def passe(self):
        pass

    self.ehAtivo = criaSimouNao(frame, "Ativo?", "Sim", "Não", 0.12, 0.1, passe)
    self.transpRecebeEmail = criaSimouNao(frame, "Recebe email?", "Sim.", "Não.", 0.28, 0.1, comando=meDesmarqueTransportadora)

 
    self.nomeTransportadora              = criarLabelEntry(frame, "Razão social *",       0.1  - 0.03, 0.25, 0.2, None)
    self.nomeFantasiaTransportadora      = criarLabelEntry(frame, "Nome *",               0.32 - 0.03, 0.25, 0.2, None)
    self.CPFTransportadora               = criarLabelEntry(frame, "CPF/CNPJ *",             0.1  - 0.03, 0.35, 0.2, None)
    self.telefoneTransportadora          = criarLabelEntry(frame, "Telefone *",           0.32 - 0.03, 0.35, 0.2, None)
    self.inscricaoEstadualTransportadora = criarLabelEntry(frame, "Inscrição estadual *", 0.1  - 0.03, 0.45, 0.2, None)
    
    self.descricaoTransportadora         = criarLabelEntry(frame, "Descrição",            0.32 - 0.03, 0.45, 0.2, None)
    self.emailTransportadora             = criarLabelEntry(frame, "Email *",              0.1  - 0.03, 0.55, 0.2, None)
    
    self.CEPTransportadora               = criarLabelEntry(frame, "CEP *",                  0.54 - 0.03, 0.25, 0.2, None)
    self.rua                             = criarLabelEntry(frame, "Rua *",                0.76 - 0.03, 0.25, 0.2, rua)
    self.bairroTransportadora            = criarLabelEntry(frame, "Bairro *",             0.54 - 0.03, 0.35, 0.2, bairro)
    self.numeroTransportadora            = criarLabelEntry(frame, "Número *",             0.76 - 0.03, 0.35, 0.2, None)
    self.cidadeTransportadora            = criarLabelEntry(frame, "Cidade *",             0.54 - 0.03, 0.45, 0.2, cidade)
    self.estadoTransportadora            = criarLabelEntry(frame, "Estado *",             0.76 - 0.03, 0.45, 0.2, estado)
    self.referencia                      = criarLabelEntry(frame, "Referência ",          0.54 - 0.03, 0.55, 0.2, None)

    self.CEPTransportadora.bind("<Return>", lambda event: buscaCep(self.CEPTransportadora.get(), self.numeroTransportadora.get()))
    self.CEPTransportadora.bind("<Tab>", lambda event: buscaCep(self.CEPTransportadora.get(), self.numeroTransportadora.get()) if self.CEPTransportadora.get().strip() else None)
    self.numeroTransportadora.bind("<Return>", lambda event: buscaCep(self.CEPTransportadora.get(), self.numeroTransportadora.get()))


    def buscaCep(cep, numero):
        cep_limpo = ''.join(filter(str.isdigit, cep))
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        response = requests.get(url)

        if response.status_code == 200:
            dados = response.json()
            if "erro" in dados:
                messagebox.showerror("Erro", "CEP não encontrado.")
            else:
                bairro.set(dados.get("bairro", ""))
                rua.set(dados.get("logradouro", ""))
                cidade.set(dados.get("localidade", ""))
                estado.set(dados.get("uf", ""))
        else:
            messagebox.showerror("Erro", "CEP não encontrado.")




    criaBotao(frame, "◀️ Voltar", 0.29, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.66, 0.80, 0.20, lambda:registraTransportadoraNoBanco(self, frame))

    aplicar_maiusculo_em_todos_entries(self)