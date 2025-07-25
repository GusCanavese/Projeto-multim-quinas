import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere
import gc

def registraFornecedorNoBanco(self, frame):
    if all([
        self.nomeFornecedor.get(),
        self.nomeFantasiaFornecedor.get(),
        self.CPFFornecedor.get(),
        self.telefoneFornecedor.get(),
        self.inscricaoEstadualFornecedor.get(),
        self.emailFornecedor.get(),
        self.CEPFornecedor.get(),
        self.rua.get(),
        self.codigoCRT.get(),
        self.bairroFornecedor.get(),
        self.numeroFornecedor.get(),
        self.cidadeFornecedor.get(),
        self.estadoFornecedor.get(),
    ]):

        dados = {
            "nome_real": self.nomeFornecedor.get(),
            "nome_fantasia": self.nomeFantasiaFornecedor.get(),
            "cpf_cnpj": self.CPFFornecedor.get(),
            "telefone": self.telefoneFornecedor.get(),
            "inscricao_estadual": self.inscricaoEstadualFornecedor.get(),
            "descricao": self.descricaoFornecedor.get(),
            "email": self.emailFornecedor.get(),
            "cep": self.CEPFornecedor.get(),
            "CRT": self.codigoCRT.get(),
            "rua": self.rua.get(),
            "bairro": self.bairroFornecedor.get(),
            "numero": self.numeroFornecedor.get(),
            "cidade": self.cidadeFornecedor.get(),
            "estado": self.estadoFornecedor.get(),
            "referencia": self.referencia.get()
        }

        dados = {k: v for k, v in dados.items() if v is not None and v != ""}

        # Enviar para o banco
        Insere.registraFornecedorNoBanco(dados)

        # Limpar a tela
        messagebox.showinfo("Sucesso!", "Fornecedor cadastrado com sucesso!")
        frame.destroy()
        gc.collect()
    else: 
        messagebox.showinfo("Erro!", "Preencha todos os campos obrigatórios!")
        
    
