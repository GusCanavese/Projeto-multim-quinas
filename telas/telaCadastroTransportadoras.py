import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
import gc
from funcoesTerceiras.registraTransportadoraNoBanco import registraTransportadoraNoBanco


def telaCadastroTransportadoras(self):
    self.frameTelaCadastroTransportadoras = ctk.CTkFrame(self, height=700, width=1200, corner_radius=5)
    self.frameTelaCadastroTransportadoras.place(x=40, y=100)      
    self.frameTelaCadastroTransportadoras.grid_propagate(False)

    def meDesmarqueTransportadora(checkboxSelecionada):
        match checkboxSelecionada:
            case 1:
                self.checkboxInativoTransportadora.deselect()
                return 1
            case 2:
                self.checkboxAtivoTransportadora.deselect()
                return 2
            case 3:
                self.checkboxPJTransportadora.deselect()
                self.labelCPFTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, width=100, text="Insira o CPF", font=("Century Gothic bold", 15), anchor="w")
                self.labelCPFTransportadora.place(x=800, y=200)
                self.CPFTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="CPF", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                self.CPFTransportadora.place(x=800, y=230)
                if hasattr(self, "CNPJTransportadora"):
                    self.CNPJTransportadora.destroy()
                    del self.CNPJTransportadora
                    gc.collect()
                return 3
            case 4:
                self.checkboxCPFTransportadora.deselect()
                self.labelCNPJTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, text="Insira o CNPJ", font=("Century Gothic bold", 15))
                self.labelCNPJTransportadora.place(x=800, y=200)
                self.CNPJTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="CNPJ", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                self.CNPJTransportadora.place(x=800, y=230)
                if hasattr(self, "CPFTransportadora"):
                    self.CPFTransportadora.destroy()
                    del self.CPFTransportadora
                    gc.collect()
                return 4
            case 5:
                self.checkboxNaoRecebeEmailTransportadora.deselect()
                self.labelEmailTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, text="Email", font=("Century Gothic bold", 15))
                self.labelEmailTransportadora.place(x=800, y=300)
                self.emailTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Email", width=300, corner_radius=5, font=("Century Gothic bold", 20))
                self.emailTransportadora.place(x=800, y=330)
                return 5
            case 6:
                if hasattr(self, "emailTransportadora"):
                    self.emailTransportadora.destroy()
                    del self.emailTransportadora
                    gc.collect()

                if hasattr(self, "labelEmailTransportadora"):
                    self.labelEmailTransportadora.destroy()
                    del self.labelEmailTransportadora
                    gc.collect()

                self.checkboxRecebeEmailTransportadora.deselect()
                return 6

    # titulo
    self.tituloCadastroTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, height=0, text="Cadastrar Transportadoras", font=("Century Gothic bold", 30))
    self.tituloCadastroTransportadora.place(relx=0.5, y=40, anchor="center")

    # checkbox ATIVO
    self.checkboxAtivoTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="Sim", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(1)))
    self.checkboxAtivoTransportadora.place(x=150, y=120, anchor="center")
    self.checkboxInativoTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="Não", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(2)))
    self.checkboxInativoTransportadora.place(x=210, y=120, anchor="center")
    self.checkboxAtivoTransportadoraLabel = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, height=0, text="ATIVO?", font=("Century Gothic bold", 14))
    self.checkboxAtivoTransportadoraLabel.place(x=125, y=90, anchor="center")
    
    # checkbox TIPO
    self.checkboxCPFTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="CPF", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(3)))
    self.checkboxCPFTransportadora.place(x=330, y=120, anchor="center")
    self.checkboxPJTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="CNPJ", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(4)))
    self.checkboxPJTransportadora.place(x=390, y=120, anchor="center")
    self.checkboxCPFouPJTransportadoraLabel = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, height=0, text="TIPO", font=("Century Gothic bold", 14))
    self.checkboxCPFouPJTransportadoraLabel.place(x=295, y=90, anchor="center")

    # checkbox EMAIL
    self.checkboxRecebeEmailTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="Sim", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(5)))
    self.checkboxRecebeEmailTransportadora.place(x=510, y=120, anchor="center")
    self.checkboxNaoRecebeEmailTransportadora = ctk.CTkCheckBox(self.frameTelaCadastroTransportadoras, text="Não", command=lambda: self.after(10, lambda: meDesmarqueTransportadora(6)))
    self.checkboxNaoRecebeEmailTransportadora.place(x=570, y=120, anchor="center")
    self.checkboxEmailTransportadoraLabel = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, height=0, text="RECEBE EMAIL?", font=("Century Gothic bold", 14))
    self.checkboxEmailTransportadoraLabel.place(x=515, y=90, anchor="center")

    # nome real
    self.labelNomeTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, text="Razão social", font=("Century Gothic bold", 15))
    self.labelNomeTransportadora.place(x=100, y=200)
    self.nomeTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Nome", width=300, corner_radius=5, font=("Century Gothic bold", 20))
    self.nomeTransportadora.place(x=100, y=230)

    # nome fantasia
    self.labelNomeTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, text="Nome fantasia", font=("Century Gothic bold", 15))
    self.labelNomeTransportadora.place(x=450, y=200)
    self.nomeFantasiaTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Nome", width=300, corner_radius=5, font=("Century Gothic bold", 20))
    self.nomeFantasiaTransportadora.place(x=450, y=230)

    # inscrição estadual
    self.labelinscriçãoEstadualTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, text="Inscrição estadual", font=("Century Gothic bold", 15))
    self.labelinscriçãoEstadualTransportadora.place(x=100, y=300)
    self.inscriçãoEstadualTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Nº inscrição", width=300, corner_radius=5, font=("Century Gothic bold", 20))
    self.inscriçãoEstadualTransportadora.place(x=100, y=330)

    # Telefone
    self.labelTelefoneTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, width=100, text="Telefone", font=("Century Gothic bold", 15), anchor="w")
    self.labelTelefoneTransportadora.place(x=450, y=300)
    self.telefoneTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Telefone", width=300, corner_radius=5, font=("Century Gothic bold", 20))
    self.telefoneTransportadora.place(x=450, y=330)

    # Descrição
    self.labelDescricaoTransportadora = ctk.CTkLabel(self.frameTelaCadastroTransportadoras, width=100, text="Descrição", font=("Century Gothic bold", 15), anchor="w")
    self.labelDescricaoTransportadora.place(x=100, y=400)
    self.descricaoTransportadora = ctk.CTkEntry(self.frameTelaCadastroTransportadoras, placeholder_text="Descrição", width=1000, corner_radius=5, font=("Century Gothic bold", 20))
    self.descricaoTransportadora.place(x=100, y=430)


    # voltar
    self.botaoVoltar = ctk.CTkButton(self.frameTelaCadastroTransportadoras, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameTelaCadastroTransportadoras.destroy)
    self.botaoVoltar.place(x=200, y=600)
    
    # registra no bd
    self.botaoCadastrarUsuario = ctk.CTkButton(self.frameTelaCadastroTransportadoras, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=lambda:registraTransportadoraNoBanco(self))
    self.botaoCadastrarUsuario.place(x=800, y=600)
