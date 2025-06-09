import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere
import gc

def registraFornecedorNoBanco(self, frame):
    cpfoupjVariavel = 0
    if all([
        self.ativoInativo[3].get(),
        self.cpfoupj[3].get(),
        self.Origem[3].get(),
        self.eFabricante[3].get(),
        self.recebeEmail[3].get(),
        self.nomeReal.get(),
        self.nomeFantasia.get(),
        self.inscricaoEstadual.get(),
        self.codigoCRT.get(),
        self.telefone.get()

    ]):
        try:
            cnpjfornecedor = self.cnpjFornecedor.get()
            cpfoupjVariavel = cnpjfornecedor
            print("pegou cnpj")
        except:
            cpffornecedor = self.cpfFornecedor.get()
            cpfoupjVariavel = cpffornecedor
            print("pegou cpf")
        if self.recebeEmail[3].get() == "Sim." and self.campoRecebeEmail.get() == "":
            messagebox.showerror("erro", "valores estão em branco")
            condicao = True
        condicao = True
    else:
        messagebox.showerror("erro", "valores estão em branco")
        condicao = False
    

    if condicao:
        dados = {
            "ativo": self.ativoInativo[3].get(),
            "tipo": self.cpfoupj[3].get(),
            "CPF_CNPJ": cpfoupjVariavel,
            "origem": self.Origem[3].get(),
            "fabricante": self.eFabricante[3].get(),
            "recebe_email": self.recebeEmail[3].get(),
            
            "email": self.campoRecebeEmail[0].get() if hasattr(self, "campoRecebeEmail") else None,
            "nome_real": self.nomeReal.get(),
            "nome_fantasia": self.nomeFantasia.get(),
            "inscricao_estadual": self.inscricaoEstadual.get(),
            "CRT": self.codigoCRT.get(),
            "telefone": self.telefone.get()
        }

        # Remover campos vazios, se quiser deixar o insert dinâmico
        dados = {k: v for k, v in dados.items() if v is not None and v != ""}

        # Enviar para o banco
        Insere.registraFornecedorNoBanco(dados)

        # Limpar a tela
        messagebox.showinfo("Sucesso!", "Fornecedor cadastrado com sucesso!")
        frame.destroy()
        gc.collect()
    
