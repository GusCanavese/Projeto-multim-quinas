import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
import gc
from funcoesTerceiras.registraFornecedorNoBanco import registraFornecedorNoBanco 



def telaCadastroFornecedores(self):
    # função criada somente para verificar qual checkbox ta marcado e qual
    def meDesmarque(checkboxSelecionada):
        match checkboxSelecionada:
                case 1:
                    self.checkboxInativo.deselect()
                    return 1
                case 2:
                    self.checkboxAtivo.deselect()
                    return 2
                case 3:
                    self.checkboxPJ.deselect()
                    self.labelCPFfornecedor = ctk.CTkLabel(self.frameTelaCadastroFornecedores, width=100, text="Insira o CPF", font=("Century Gothic bold", 15), anchor="w")
                    self.labelCPFfornecedor.place(x=800, y=200)
                    self.CPFfornecedor = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="CPF", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                    self.CPFfornecedor.place(x=800, y=230)
                    if hasattr(self, "CNPJFornecedor"):
                        self.CNPJFornecedor.destroy()
                        del self.CNPJFornecedor
                        gc.collect
                    return 3
                case 4:
                    self.checkboxCPF.deselect()
                    self.labelCNPJFornecedor = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="Insira o CNPJ", font=("Century Gothic bold", 15))
                    self.labelCNPJFornecedor.place(x=800, y=200)
                    self.CNPJFornecedor = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="CNPJ", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                    self.CNPJFornecedor.place(x=800, y=230)
                    if hasattr(self, "CPFfornecedor"):
                        self.CPFfornecedor.destroy()
                        del self.CPFfornecedor
                        gc.collect
                    return 4
                case 5:
                    self.checkboxEstrangeira.deselect()
                    return 5
                case 6:
                    self.checkboxNacional.deselect()
                    return 6
                case 7:
                    self.checkboxNaoFabricante.deselect()
                    return 7
                case 8:
                    self.checkboxFabricante.deselect()
                    return 8
                case 9:
                    self.checkboxNaoRecebeEmail.deselect()
                    self.labelEmailFornecedor = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="Email", font=("Century Gothic bold", 15))
                    self.labelEmailFornecedor.place(x=100, y=400)
                    self.emailFornecedor = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Email", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                    self.emailFornecedor.place(x=100, y=430)
                    return 9
                case 10:
                    if hasattr(self, "emailFornecedor"):
                        self.emailFornecedor.destroy()
                        del self.emailFornecedor
                        gc.collect()

                    if hasattr(self, "labelEmailFornecedor"):
                        self.labelEmailFornecedor.destroy()
                        del self.labelEmailFornecedor
                        gc.collect()

                    self.checkboxRecebeEmail.deselect()
                    return 10

    self.frameTelaCadastroFornecedores = ctk.CTkFrame(self, height=700, width=1200, corner_radius=5)
    self.frameTelaCadastroFornecedores.place(x=40, y=100)      
    self.frameTelaCadastroFornecedores.grid_propagate(False)
    
    # titulo
    self.textoCadastroFornecedores = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="Cadastrar fornecedores", font=("Century Gothic bold", 30))
    self.textoCadastroFornecedores.place(relx=0.5, y=40, anchor="center")

    # checkbox ATIVO
    self.checkboxAtivo = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Sim", command=lambda: self.after(10, lambda: meDesmarque(1)))
    self.checkboxAtivo.place(x=150, y=120, anchor="center")
    self.checkboxInativo = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Não", command=lambda: self.after(10, lambda: meDesmarque(2)))
    self.checkboxInativo.place(x=210, y=120, anchor="center")
    self.checkboxAtivoLabel = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="ATIVO?", font=("Century Gothic bold", 14))
    self.checkboxAtivoLabel.place(x=125, y=90, anchor="center")
    
    # checkbox TIPO
    self.checkboxCPF = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="CPF", command=lambda: self.after(10, lambda: meDesmarque(3)))
    self.checkboxCPF.place(x=330, y=120, anchor="center")
    self.checkboxPJ = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="CNPJ", command=lambda: self.after(10, lambda: meDesmarque(4)))
    self.checkboxPJ.place(x=390, y=120, anchor="center")
    self.checkboxCPFouPJLabel = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="TIPO", font=("Century Gothic bold", 14))
    self.checkboxCPFouPJLabel.place(x=295, y=90, anchor="center")

    # checkbox ORIGEM
    self.checkboxNacional = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Nacional", command=lambda: self.after(10, lambda: meDesmarque(5)))
    self.checkboxNacional.place(x=540, y=120, anchor="center")
    self.checkboxEstrangeira = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Estrangeira", command=lambda: self.after(10, lambda: meDesmarque(6)))
    self.checkboxEstrangeira.place(x=9, y=120, anchor="center")
    self.checkboxOrigemLabel = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="ORIGEM", font=("Century Gothic bold", 14))
    self.checkboxOrigemLabel.place(x=520, y=90, anchor="center")

    # checkbox FABRICANTE
    self.checkboxFabricante = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Sim", command=lambda: self.after(10, lambda: meDesmarque(7)))
    self.checkboxFabricante.place(x=800, y=120, anchor="center")
    self.checkboxNaoFabricante = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Não", command=lambda: self.after(10, lambda: meDesmarque(8)))
    self.checkboxNaoFabricante.place(x=860, y=120, anchor="center")
    self.checkboxFabricanteLabel = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="FABRICANTE", font=("Century Gothic bold", 14))
    self.checkboxFabricanteLabel.place(x=795, y=90, anchor="center")

    # checkbox EMAIL
    self.checkboxRecebeEmail = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Sim", command=lambda: self.after(10, lambda: meDesmarque(9)))
    self.checkboxRecebeEmail.place(x=1010, y=120, anchor="center")
    self.checkboxNaoRecebeEmail = ctk.CTkCheckBox(self.frameTelaCadastroFornecedores, text="Não", command=lambda: self.after(10, lambda: meDesmarque(10)))
    self.checkboxNaoRecebeEmail.place(x=1090, y=120, anchor="center")
    self.checkboxEmailLabel = ctk.CTkLabel(self.frameTelaCadastroFornecedores, height=0, text="RECEBE EMAIL?", font=("Century Gothic bold", 14))
    self.checkboxEmailLabel.place(x=1015, y=90, anchor="center")

    # nome real
    self.labelNome = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="Razão social", font=("Century Gothic bold", 15))
    self.labelNome.place(x=100, y=200)
    self.nomeFornecedor = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Nome", width=300, corner_radius=5, font=("Century Gothic bold", 20))
    self.nomeFornecedor.place(x=100, y=230)

    # nome fantasia
    self.labelNome = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="Nome fantasia", font=("Century Gothic bold", 15))
    self.labelNome.place(x=450, y=200)
    self.nomeFantasia = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Nome", width=300, corner_radius=5, font=("Century Gothic bold", 20))
    self.nomeFantasia.place(x=450, y=230)

    # inscrição estadual
    self.labelinscriçãoEstadual = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="Inscrição estadual", font=("Century Gothic bold", 15))
    self.labelinscriçãoEstadual.place(x=100, y=300)
    self.inscriçãoEstadual = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Nº inscrição", width=300, corner_radius=5, font=("Century Gothic bold", 20))
    self.inscriçãoEstadual.place(x=100, y=330)

    # código crt
    self.labelcodigoCRT = ctk.CTkLabel(self.frameTelaCadastroFornecedores, text="CRT", font=("Century Gothic bold", 15))
    self.labelcodigoCRT.place(x=450, y=300)
    self.codigoCRT = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Código", width=300, corner_radius=5, font=("Century Gothic bold", 20))
    self.codigoCRT.place(x=450, y=330)

    # Telefone
    self.labelTelefone = ctk.CTkLabel(self.frameTelaCadastroFornecedores, width=100, text="Telefone", font=("Century Gothic bold", 15), anchor="w")
    self.labelTelefone.place(x=800, y=300)
    self.telefone = ctk.CTkEntry(self.frameTelaCadastroFornecedores, placeholder_text="Telefone", width=300, corner_radius=5, font=("Century Gothic bold", 20))
    self.telefone.place(x=800, y=330)

    # voltar
    self.botaoVoltar = ctk.CTkButton(self.frameTelaCadastroFornecedores, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaCadastroFornecedores.destroy)
    self.botaoVoltar.place(x=200, y=600)
    
    # registra no bd
    self.botaoCadastrarUsuario = ctk.CTkButton(self.frameTelaCadastroFornecedores, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=lambda:registraFornecedorNoBanco(self))
    self.botaoCadastrarUsuario.place(x=800, y=600)
