import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere
import gc


def registraTransportadoraNoBanco(self, frame):
    cpfoupjVariavel=0
    if all([
        self.nomeTransportadora.get(),
        self.nomeFantasiaTransportadora.get(),
        self.CPFTransportadora.get(),
        self.telefoneTransportadora.get(),
        self.inscricaoEstadualTransportadora.get(),
        self.emailTransportadora.get(),
        self.CEPTransportadora.get(),
        self.rua.get(),
        self.bairroTransportadora.get(),
        self.numeroTransportadora.get(),
        self.cidadeTransportadora.get(),
        self.estadoTransportadora.get(),
    ]):

        dados = {
            "nome_real": self.nomeTransportadora.get(),
            "nome_fantasia": self.nomeFantasiaTransportadora.get(),
            "cpf_cnpj": self.CPFTransportadora.get(),
            "telefone": self.telefoneTransportadora.get(),
            "inscricao_estadual": self.inscricaoEstadualTransportadora.get(),
            "descricao": self.descricaoTransportadora.get(),
            "email": self.emailTransportadora.get(),
            "cep": self.CEPTransportadora.get(),
            "rua": self.rua.get(),
            "bairro": self.bairroTransportadora.get(),
            "numero": self.numeroTransportadora.get(),
            "cidade": self.cidadeTransportadora.get(),
            "estado": self.estadoTransportadora.get(),
            "referencia": self.referencia.get()
        }

        dados = {k: v for k, v in dados.items() if v is not None and v != ""}

        Insere.insereTransportadoraNoBanco(dados)
        messagebox.showinfo("Sucesso!", "Transportadora cadastrado com sucesso!")
        frame.destroy()
        gc.collect()
                
    else:
        messagebox.showerror("erro", "valores estão em branco")
