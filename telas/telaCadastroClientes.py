import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk


def telaCadastroClientes(self):
    self.frameTelaCadastroClientes = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
    self.frameTelaCadastroClientes.place(x=140, y=100)     
    self.frameTelaCadastroClientes.grid_propagate(False)

    # ================ widgets da tela cadastro =====================#
    # titulo
    self.textoCadastro = ctk.CTkLabel(self.frameTelaCadastroClientes, width=950, height=0, text="Cadastrar cliente", font=("Century Gothic bold", 30))
    self.textoCadastro.grid(row=0, column=0, padx=10, pady=20)

    # nome
    self.labelNomeCliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="Nome", font=("Century Gothic bold", 15))
    self.labelNomeCliente.place(x=100, y=100)
    self.nomeCliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="nomeCliente", width=350, corner_radius=5, font=("Century Gothic bold", 20))
    self.nomeCliente.place(x=100, y=130)

    #CPF/CNPJ
    self.labelCPF_PJcliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="CPF/CNPJ", font=("Century Gothic bold", 15))
    self.labelCPF_PJcliente.place(x=100, y=170)
    self.CPF_PJcliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="Documento", width=350, corner_radius=5, font=("Century Gothic bold", 20))
    self.CPF_PJcliente.place(x=100, y=200)

    #RG
    self.labelRGcliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="Insira o RG", font=("Century Gothic bold", 15))
    self.labelRGcliente.place(x=100, y=240)
    self.RGcliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="RG", width=350, corner_radius=5, font=("Century Gothic bold", 20))
    self.RGcliente.place(x=100, y=270) 