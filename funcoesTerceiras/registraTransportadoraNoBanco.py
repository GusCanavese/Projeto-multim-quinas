import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere
import gc


def registraTransportadoraNoBanco(self, frame):
    cpfoupjVariavel=0
    if all([
        self.ehAtivo[3].get(),
        self.ehCpfCnpj[3].get(),
        self.transpRecebeEmail[3].get(),
        self.nomeTransportadora.get(),
        self.nomeFantasiaTransportadora.get(),
        self.inscricaoEstadualTransportadora.get(),
        self.telefoneTransportadora.get(),
        self.descricaoTransportadora.get(),

    ]):
        try:
            cnpjTransport = self.CNPJTransportadora.get()
            cpfoupjVariavel = cnpjTransport

        except:
            cpfTransport = self.CPFTransportadora.get()
            cpfoupjVariavel = cpfTransport

        if self.transpRecebeEmail[3].get() == "Sim." and self.emailTransportadora[0].get() == "":
            messagebox.showerror("erro", "valores estão em branco")
            condicao = False
        else:
            condicao = True
    else:
        messagebox.showerror("erro", "valores estão em branco")
        condicao = False


    if condicao:
        dados = {
            "ativo": self.ehAtivo[3].get(),
            "tipo": self.ehCpfCnpj[3].get(),
            "CPF_CNPJ": cpfoupjVariavel,
            "recebe_email": self.transpRecebeEmail[3].get(),
            "email": self.emailTransportadora[0].get() if hasattr(self, "emailTransportadora") else None,
            "nome_real": self.nomeTransportadora.get(),
            "nome_fantasia": self.nomeFantasiaTransportadora.get(),
            "inscricao_estadual": self.inscricaoEstadualTransportadora.get(),
        }

        dados = {k: v for k, v in dados.items() if v is not None and v != ""}

        Insere.registraFornecedorNoBanco(dados)
        messagebox.showinfo("Sucesso!", "Fornecedor cadastrado com sucesso!")
        frame.destroy()
        gc.collect()
                
    else:
        messagebox.showerror("erro", "valores estão em branco")
