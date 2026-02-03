import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere
import gc

def registraFornecedorNoBanco(self, frame):
    nome_real = self.nomeFornecedor.get()
    nome_fantasia = self.nomeFantasiaFornecedor.get()
    cpf_cnpj = self.CPFFornecedor.get()
    telefone = self.telefoneFornecedor.get()
    inscricao_estadual = self.inscricaoEstadualFornecedor.get()
    descricao = self.descricaoFornecedor.get()
    email = self.emailFornecedor.get()
    cep = self.CEPFornecedor.get()
    rua = self.rua.get()
    bairro = self.bairroFornecedor.get()
    numero = self.numeroFornecedor.get()
    cidade = self.cidadeFornecedor.get()
    estado = self.estadoFornecedor.get()
    referencia = self.referencia.get()
    crt = self.codigoCRT.get()

    ativo = self.ativoInativo[3].get()
    recebe_email = self.transpRecebeEmail[3].get()
    origem = self.Origem[3].get()
    eh_fabricante = self.eFabricante[3].get()

    if (
        not nome_real
        or not nome_fantasia
        or not cpf_cnpj
        or not telefone
        or not inscricao_estadual
        or not email
        or not cep
        or not rua
        or not bairro
        or not numero
        or not cidade
        or not estado
    ):
        messagebox.showinfo("Erro!", "Preencha todos os campos obrigatórios!")
    else:
        dados = {
            "ativo": ativo,
            "CPF_CNPJ": cpf_cnpj,
            "origem": origem,
            "fabricante": eh_fabricante,
            "recebe_email": recebe_email,
            "email": email,
            "nome_real": nome_real,
            "nome_fantasia": nome_fantasia,
            "inscricao_estadual": inscricao_estadual,
            "CRT": crt,
            "telefone": telefone,
            "descricao": descricao,
            "cep": cep,
            "rua": rua,
            "bairro": bairro,
            "numero": numero,
            "cidade": cidade,
            "estado": estado,
            "referencia": referencia,
        }

        Insere.registraFornecedorNoBanco(dados)
        frame.destroy()
        gc.collect()
        
    
