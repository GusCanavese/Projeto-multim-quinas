import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
import gc
from funcoesTerceiras.registraTransportadoraNoBanco import registraTransportadoraNoBanco
from componentes import criaFrame, criaSimouNao, criarLabelEntry, criaBotao, criarLabelEntryEmail
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries


def telaCadastroTransportadoras(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)


    def meDesmarqueTransportadora(checkboxSelecionada):
        print(checkboxSelecionada)
        match checkboxSelecionada:
            case "CPF":
                if hasattr(self, "CPFTransportadora"):
                    self.CPFTransportadora.destroy()
                    del self.CPFTransportadora
                    gc.collect
                if hasattr(self, "CNPJTransportadora"):
                    self.CNPJTransportadora.destroy()
                    del self.CNPJTransportadora
                    gc.collect()
                self.CPFTransportadora=criarLabelEntry(frame, "CPF *", 0.1, 0.55, 0.25, None) 
            case "CNPJ":
                if hasattr(self, "CPFTransportadora"):
                    self.CPFTransportadora.destroy()
                    del self.CPFTransportadora
                    gc.collect
                if hasattr(self, "CNPJTransportadora"):
                    self.CNPJTransportadora.destroy()
                    del self.CNPJTransportadora
                    gc.collect()
                self.CNPJTransportadora=criarLabelEntry(frame, "CNPJ *", 0.1, 0.55, 0.25, None)
            case "Sim.":
                if hasattr(self, "emailTransportadora"):
                    self.emailTransportadora[0].destroy()
                    self.emailTransportadora[1].destroy()
                    gc.collect()
                self.emailTransportadora=criarLabelEntryEmail(frame, "Email *", 0.37, 0.55, 0.25, None)
            case "Não.":
                if hasattr(self, "emailTransportadora"):
                    self.emailTransportadora[0].destroy()
                    self.emailTransportadora[1].destroy()
                    gc.collect()

    self.tituloCadastroTransportadora = ctk.CTkLabel(frame, height=0, text="Cadastrar Transportadoras", font=("Century Gothic bold", 30))
    self.tituloCadastroTransportadora.place(relx=0.5, y=40, anchor="center")

    self.ehAtivo = criaSimouNao(frame, "Ativo?", "Sim", "Não", 0.12, 0.1, comando=meDesmarqueTransportadora)
    self.ehCpfCnpj = criaSimouNao(frame, "Tipo", "CPF", "CNPJ", 0.28, 0.1, comando=meDesmarqueTransportadora)
    self.transpRecebeEmail = criaSimouNao(frame, "Recebe email?", "Sim.", "Não.", 0.44, 0.1, comando=meDesmarqueTransportadora)

    self.nomeTransportadora = criarLabelEntry(frame, "Razão social *", 0.1, 0.27, 0.25, None)
    self.nomeFantasiaTransportadora = criarLabelEntry(frame, "Nome *", 0.37, 0.27, 0.25, None)
    self.telefoneTransportadora = criarLabelEntry(frame, "Telefone *", 0.639, 0.27, 0.25, None)

    self.inscricaoEstadualTransportadora = criarLabelEntry(frame, "Inscrição estadual *", 0.1, 0.41, 0.25, None)
    self.descricaoTransportadora = criarLabelEntry(frame, "Descrição *", 0.37, 0.41, 0.55, None)

    criaBotao(frame, "Voltar", 0.29, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.66, 0.80, 0.20, lambda:registraTransportadoraNoBanco(self, frame))

    aplicar_maiusculo_em_todos_entries(self)