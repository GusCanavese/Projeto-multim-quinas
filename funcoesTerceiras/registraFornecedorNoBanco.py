import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere
import gc

def registraFornecedorNoBanco(self):
    ativo = self.checkboxAtivo.get()
    inativo = self.checkboxInativo.get()
    CPFfornecedor = self.checkboxCPF.get()
    PJfornecedor = self.checkboxPJ.get()
    nacional = self.checkboxNacional.get()
    estrangeira = self.checkboxEstrangeira.get()
    fabricante = self.checkboxFabricante.get()
    naoFabricante = self.checkboxNaoFabricante.get()
    recebeEmail = self.checkboxRecebeEmail.get()
    naoRecebeEmail = self.checkboxNaoRecebeEmail.get()

    nomeReal = self.nomeFornecedor.get()
    nomeFantasia = self.nomeFantasia.get()
    inscricaoestadual = self.inscriçãoEstadual.get()
    CRT = self.codigoCRT.get()
    telefone = self.telefone.get()
    
    #! coloca a checkbox esteja em branco


    if hasattr(self, "CNPJFornecedor"):
        print("tem cnpj")
        cnpjfornecedor = self.CNPJFornecedor.get()
        print(cnpjfornecedor)
        if hasattr(self, "emailFornecedor"):
            emailFornecedor = self.emailFornecedor.get()
            if emailFornecedor:
                condicaoEmailFornecedor = (ativo or inativo) and (CPFfornecedor or PJfornecedor) and (nacional or estrangeira) and (fabricante or naoFabricante) and (naoRecebeEmail or recebeEmail) and cnpjfornecedor and emailFornecedor and nomeReal and nomeFantasia and inscricaoestadual and CRT and telefone
            else:
                messagebox.showerror("erro", "valores estão em branco")
        else:
            condicaoEmailFornecedor = (ativo or inativo) and (CPFfornecedor or PJfornecedor) and (nacional or estrangeira) and (fabricante or naoFabricante) and (naoRecebeEmail or recebeEmail) and nomeReal and nomeFantasia and inscricaoestadual and CRT and telefone
    
    elif hasattr(self, "CPFfornecedor") and self.CPFfornecedor:
        print("tem cpf")
        cpffornecedor = self.CPFfornecedor.get()
        print(cpffornecedor)
        if hasattr(self, "emailFornecedor"):
            emailFornecedor = self.emailFornecedor.get()
            if emailFornecedor:
                condicaoEmailFornecedor = (ativo or inativo) and (CPFfornecedor or PJfornecedor) and (nacional or estrangeira) and (fabricante or naoFabricante) and (naoRecebeEmail or recebeEmail) and cpffornecedor and emailFornecedor and nomeReal and nomeFantasia and inscricaoestadual and CRT and telefone
            else:
                messagebox.showerror("erro", "valores estão em branco")
        else:
            condicaoEmailFornecedor = (ativo or inativo) and (CPFfornecedor or PJfornecedor) and (nacional or estrangeira) and (fabricante or naoFabricante) and (naoRecebeEmail or recebeEmail) and nomeReal and nomeFantasia and inscricaoestadual and CRT and telefone
    else:
        messagebox.showerror("erro", "valores estão em branco")


    if condicaoEmailFornecedor:
        colunas = []
        valores = []
        if self.checkboxAtivo.get():
            colunas.append("ativo")
            valores.append("'Sim'")
        if self.checkboxInativo.get():
            colunas.append("ativo")
            valores.append("'Não'")
        if self.checkboxCPF.get():
            colunas.append("tipo")
            valores.append("'CPF'")
            if self.CPFfornecedor.get():
                colunas.append("CPF")
                valores.append(f"'{self.CPFfornecedor.get()}'")
        if self.checkboxPJ.get():
            colunas.append("tipo")
            valores.append("'CNPJ'")
            if self.CNPJFornecedor.get():
                colunas.append("CNPJ")
                valores.append(f"'{self.CNPJFornecedor.get()}'")
        if self.checkboxNacional.get():
            colunas.append("origem")
            valores.append("'Nacional'")
        if self.checkboxEstrangeira.get():
            colunas.append("origem")
            valores.append("'Estrangeira'")
        if self.checkboxFabricante.get():
            colunas.append("fabricante")
            valores.append("'Sim'")
        if self.checkboxNaoFabricante.get():
            colunas.append("fabricante")
            valores.append("'Não'")
        if self.checkboxRecebeEmail.get():
            colunas.append("recebe_email")
            valores.append("'Sim'")
            if hasattr(self, "emailFornecedor"):
                if self.emailFornecedor.get():
                    colunas.append("email")
                    valores.append(f"'{self.emailFornecedor.get()}'")
        if self.checkboxNaoRecebeEmail.get():
            colunas.append("recebe_email")
            valores.append("'Não'")
            print("email nao existe")
        if self.nomeFornecedor.get():
            colunas.append("nome_real")
            valores.append(f"'{self.nomeFornecedor.get()}'")
        if self.nomeFantasia.get():
            colunas.append("nome_fantasia")
            valores.append(f"'{self.nomeFantasia.get()}'")
        if self.inscriçãoEstadual.get():
            colunas.append("inscricao_estadual")
            valores.append(f"'{self.inscriçãoEstadual.get()}'")
        if self.codigoCRT.get():
            colunas.append("CRT")
            valores.append(f"'{self.codigoCRT.get()}'")
        if self.telefone.get():
            colunas.append("telefone")
            valores.append(f"'{self.telefone.get()}'")

        Insere.registraFornecedorNoBanco(colunas, valores)
        self.frameTelaCadastroFornecedores.destroy()
        gc.collect()


    
    else:
        messagebox.showerror("erro", "valores estão em branco")
