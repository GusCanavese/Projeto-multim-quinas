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

    #nome
    self.labelNomeCliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="Nome", font=("Century Gothic bold", 15))
    self.labelNomeCliente.place(x=100, y=100)
    self.nomeCliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="nomeCliente", width=350, corner_radius=5, font=("Century Gothic bold", 20))
    self.nomeCliente.place(x=100, y=130)

    #CPF/CNPJ
    self.labelCPF_PJcliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="CPF/CNPJ", font=("Century Gothic bold", 15))
    self.labelCPF_PJcliente.place(x=100, y=170)
    self.CPF_PJcliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="Documento", width=350, corner_radius=5, font=("Century Gothic bold", 20))
    self.CPF_PJcliente.place(x=100, y=200)

    #Inscrição Estadual
    self.labelIEcliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="Inscrição Estadual", font=("Century Gothic bold", 15))
    self.labelIEcliente.place(x=100, y=240)
    self.IEcliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="IE", width=350, corner_radius=5, font=("Century Gothic bold", 20))
    self.IEcliente.place(x=100, y=270) 

    #RG
    self.labelRGcliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="Insira o RG", font=("Century Gothic bold", 15))
    self.labelRGcliente.place(x=100, y=310)
    self.RGcliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="RG", width=350, corner_radius=5, font=("Century Gothic bold", 20))
    self.RGcliente.place(x=100, y=340) 
        
    #Endereço
    self.labelEnderecoCliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="Endereço", font=("Century Gothic bold", 15))
    self.labelEnderecoCliente.place(x=500, y=100)
    self.enderecoCliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="Endereço", width=450, corner_radius=5, font=("Century Gothic bold", 20))
    self.enderecoCliente.place(x=500, y=130)

    #CEP
    self.labelCEPCliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="CEP", font=("Century Gothic bold", 15))
    self.labelCEPCliente.place(x=500, y=170)
    self.CEPCliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="CEP", width=190, corner_radius=5, font=("Century Gothic bold", 20))
    self.CEPCliente.place(x=500, y=200)

    #Número
    self.labelNumeroCliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="Número", font=("Century Gothic bold", 15))
    self.labelNumeroCliente.place(x=700, y=170)
    self.numeroCliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="00", width=60, corner_radius=5, font=("Century Gothic bold", 20))
    self.numeroCliente.place(x=700, y=200)

    #Bairro
    self.labelBairroCliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="Bairro", font=("Century Gothic bold", 15))
    self.labelBairroCliente.place(x=770, y=170)
    self.bairroCliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="Bairro", width=180, corner_radius=5, font=("Century Gothic bold", 20))
    self.bairroCliente.place(x=770, y=200)

    #Cidade
    self.labelCidadeCliente = ctk.CTkLabel(self.frameTelaCadastroClientes, text="Cidade do Endereço", font=("Century Gothic bold", 15))
    self.labelCidadeCliente.place(x=500, y=240)
    self.cidadeCliente = ctk.CTkEntry(self.frameTelaCadastroClientes, placeholder_text="Cidade", width=260, corner_radius=5, font=("Century Gothic bold", 20))
    self.cidadeCliente.place(x=500, y=270)

    # botão para voltar para a tela
    self.botaoVoltar = ctk.CTkButton(self.frameTelaCadastroClientes, text="Voltar", width=200, corner_radius=5, font=("Arial", 18), command=self.frameTelaCadastroClientes.destroy)
    self.botaoVoltar.place(relx=0.33, y=650, anchor="center")