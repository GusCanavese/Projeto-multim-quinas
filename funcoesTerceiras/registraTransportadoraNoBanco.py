import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere
import gc


def registraTransportadoraNoBanco(self):
    # pegando checkbox
    ativoTransportadora   = self.checkboxAtivoTransportadora.get()
    inativoTransportadora = self.checkboxInativoTransportadora.get()
    varCPFTransportadora = self.checkboxCPFTransportadora.get()
    PJTransportadora = self.checkboxPJTransportadora.get()
    recebeEmailTransportadora = self.checkboxRecebeEmailTransportadora.get()
    naoRecebeEmailTransportadora = self.checkboxNaoRecebeEmailTransportadora.get()

    # pegando entradas
    nomeTransportadora = self.nomeTransportadora.get()
    nomeFantasiaTranportadora = self.nomeFantasiaTransportadora.get()
    inscricaoEstadualtransportadora = self.inscriçãoEstadualTransportadora.get()
    telefoneTransportadora = self.telefoneTransportadora.get()
    descricaoTransportadora = self.descricaoTransportadora.get()

    if hasattr(self, "CNPJTransportadora") and self.CNPJTransportadora:
        print("tem cnpj")
        cnpjTransportadora = self.CNPJTransportadora.get()
        if hasattr(self, "emailTransportadora"):
            print("tem email")
            varEmailTransportadora = self.emailTransportadora.get()
            if varEmailTransportadora:
                condicaoQueryTransportadora = (ativoTransportadora or inativoTransportadora) and (varCPFTransportadora or PJTransportadora) and (recebeEmailTransportadora or naoRecebeEmailTransportadora) and nomeTransportadora and nomeFantasiaTranportadora and inscricaoEstadualtransportadora and telefoneTransportadora and descricaoTransportadora and cnpjTransportadora and varEmailTransportadora
            else:
                messagebox.showerror("erro", "campos estão em branco")
        else:
            condicaoQueryTransportadora = (ativoTransportadora or inativoTransportadora) and (varCPFTransportadora or PJTransportadora) and (recebeEmailTransportadora or naoRecebeEmailTransportadora) and nomeTransportadora and nomeFantasiaTranportadora and inscricaoEstadualtransportadora and telefoneTransportadora and descricaoTransportadora and cnpjTransportadora
    
    elif hasattr(self, "CPFTransportadora") and self.CPFTransportadora:
        print("tem cpf")
        cpfTransportadora = self.CPFTransportadora.get()
        if hasattr(self, "emailTransportadora"):
            print("tem email")
            varEmailTransportadora = self.emailTransportadora.get()
            if varEmailTransportadora:
                condicaoQueryTransportadora = (ativoTransportadora or inativoTransportadora) and (varCPFTransportadora or PJTransportadora) and (recebeEmailTransportadora or naoRecebeEmailTransportadora) and nomeTransportadora and nomeFantasiaTranportadora and inscricaoEstadualtransportadora and telefoneTransportadora and descricaoTransportadora and cpfTransportadora and varEmailTransportadora
            else:
                messagebox.showerror("erro", "campos estão em branco")
        else:
            condicaoQueryTransportadora = (ativoTransportadora or inativoTransportadora) and (varCPFTransportadora or PJTransportadora) and (recebeEmailTransportadora or naoRecebeEmailTransportadora) and nomeTransportadora and nomeFantasiaTranportadora and inscricaoEstadualtransportadora and telefoneTransportadora and descricaoTransportadora and cpfTransportadora
    
    else:
        messagebox.showerror("Erro", "campos estão em branco")
                

    if condicaoQueryTransportadora:
        colunas = []
        valores = []
        if self.checkboxAtivoTransportadora.get():
            colunas.append("ativo")
            valores.append("'Sim'")
        if self.checkboxInativoTransportadora.get():
            colunas.append("ativo")
            valores.append("'Não'")
        if self.checkboxCPFTransportadora.get():
            colunas.append("tipo")
            valores.append("'CPF'")
            if self.CPFTransportadora.get():
                colunas.append("CPF")
                valores.append(f"'{self.CPFTransportadora.get()}'")
        if self.checkboxPJTransportadora.get():
            colunas.append("tipo")
            valores.append("'CNPJ'")
            if self.CNPJTransportadora.get():
                colunas.append("CNPJ")
                valores.append(f"'{self.CNPJTransportadora.get()}'")
        if self.checkboxRecebeEmailTransportadora.get():
            colunas.append("recebe_email")
            valores.append("'Sim'")
            if hasattr(self, "emailTransportadora"):
                if self.emailTransportadora.get():
                    colunas.append("email")
                    valores.append(f"'{self.emailTransportadora.get()}'")
        if self.checkboxNaoRecebeEmailTransportadora.get():
            colunas.append("recebe_email")
            valores.append("'Não'")
            print("email nao existe")
        if self.nomeTransportadora.get():
            colunas.append("nome_real")
            valores.append(f"'{self.nomeTransportadora.get()}'")
        if self.nomeFantasiaTransportadora.get():
            colunas.append("nome_fantasia")
            valores.append(f"'{self.nomeFantasiaTransportadora.get()}'")
        if self.inscriçãoEstadualTransportadora.get():
            colunas.append("inscricao_estadual")
            valores.append(f"'{self.inscriçãoEstadualTransportadora.get()}'")
        if self.telefoneTransportadora.get():
            colunas.append("telefone")
            valores.append(f"'{self.telefoneTransportadora.get()}'")

        Insere.insereTransportadoraNoBanco(colunas, valores)
        self.frameTelaCadastroTransportadoras.destroy()
        gc.collect()

    
    else:
        messagebox.showerror("erro", "valores estão em branco")
