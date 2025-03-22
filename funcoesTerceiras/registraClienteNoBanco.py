import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere

# é chamado quando é cadastrado um novo cliente
def registraClienteNoBanco(self):
    nome = self.nomeCliente.get()
    CPF_CNPJ = self.CPF_PJcliente.get()
    IE = self.IEcliente.get()
    RG = self.RGcliente.get()
    endereco = self.enderecoCliente.get()
    CEP = self.CEPcliente.get()
    numero = self.numeroCliente.get()
    bairro = self.bairroCliente.get()
    cidade = self.cidadeCliente.get()

    if not nome or not CPF_CNPJ or not IE or not RG or not endereco or not CEP or not numero or not bairro or not cidade: 
        messagebox.showinfo(title="Registro falhou", message="Campos obrigatórios não podem estar em branco")
    else:
        #Pega da classe insere, a query que ta sendo feita la
        Insere.insereClienteNoBanco(nome, CPF_CNPJ, IE, RG, endereco, CEP, numero, bairro, cidade)
        self.frameTelaCadastroClientes.destroy()
