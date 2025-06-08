import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere
import gc


def registraTransportadoraNoBanco(self):
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
            print("pegou cnpj")
        except:
            cpfTransport = self.CPFTransportadora.get()
            cpfoupjVariavel = cpfTransport
            print("pegou cpf")
            print(self.transpRecebeEmail[3].get())
        if self.transpRecebeEmail[3].get() == "Sim." and self.emailTransportadora.get() == "":
            messagebox.showerror("erro", "valores estão em branco")
            condicao = True
        condicao = True
    else:
        messagebox.showerror("erro", "valores estão em branco")
        condicao = False


    if condicao:
        dados = {
            "ativo": self.ehAtivo[3].get(),
            "tipo": self.ehCpfCnpj[3].get(),
            "documento": cpfoupjVariavel,
            "recebe_email": self.transpRecebeEmail[3].get(),
            "email": self.emailTransportadora.get() if hasattr(self, "emailTransportadora") else None,
            "nome_real": self.nomeTransportadora.get(),
            "nome_fantasia": self.nomeFantasiaTransportadora.get(),
            "inscricao_estadual": self.inscricaoEstadualTransportadora.get(),
        }

        dados = {k: v for k, v in dados.items() if v is not None and v != ""}

        Insere.registraFornecedorNoBanco(dados)

        self.frameTelaCadastroFornecedores.destroy()
        gc.collect()
                
    else:
        messagebox.showerror("erro", "valores estão em branco")
