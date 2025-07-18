import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox 
from consultas.insert import Insere

# é chamado quando é cadastrado um novo cliente
def registraClienteNoBanco(self, frame):







    nome   = self.nomeCliente.get()
    cpf    = self.cpf.get()
    cnpj   = self.cnpj.get()
    IE     = self.IEcliente.get()
    RG     = self.RGcliente.get()
    CEP    = self.CEPcliente.get()
    rua    = self.rua.get()
    bairro = self.bairroCliente.get()
    numero = self.numeroCliente.get()
    cidade = self.cidadeCliente.get()
    estado = self.estadoCliente.get()
    referencia = self.referencia.get()
    

    if not nome or not (cpf or cnpj) or not rua or not numero or not bairro or not cidade or not estado: 
        messagebox.showinfo(title="Registro falhou", message="Campos obrigatórios não podem estar em branco")
    else:
        Insere.insereClienteNoBanco(nome, cpf, cnpj, IE, RG, CEP, rua, numero, bairro, cidade, estado, referencia)
        frame.destroy()
