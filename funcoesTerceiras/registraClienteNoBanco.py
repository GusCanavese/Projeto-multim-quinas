import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere

# é chamado quando é cadastrado um novo cliente
def registraClienteNoBanco(self, frame):
    nome = self.nomeCliente.get()
    cpf = self.cpf.get()
    cnpj = self.cnpj.get()
    IE = self.IEcliente.get()
    RG = self.RGcliente.get()
    endereco = 1
    CEP = self.CEPcliente.get()
    numero = self.numeroCliente.get()
    bairro = self.bairroCliente.get()
    cidade = self.cidadeCliente.get()

    if not nome or not (cpf or cnpj) or not IE or not RG or not endereco or not numero or not bairro or not cidade: 
        messagebox.showinfo(title="Registro falhou", message="Campos obrigatórios não podem estar em branco")
    else:
        #Pega da classe insere, a query que ta sendo feita la
        Insere.insereClienteNoBanco(nome, cpf, cnpj, IE, RG, endereco, CEP, numero, bairro, cidade)
        frame.destroy()
