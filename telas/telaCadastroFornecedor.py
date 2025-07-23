import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
import gc
from funcoesTerceiras.registraFornecedorNoBanco import registraFornecedorNoBanco 
from componentes import criaFrame, criaFrameJanela, criaSimouNao, criarLabelEntry, criaBotao, criarLabelEntryEmail
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries




def telaCadastroFornecedores(self):
    # função criada somente para verificar qual checkbox ta marcado e qual
    def meDesmarque(checkboxSelecionada):
        print(checkboxSelecionada)
        match checkboxSelecionada:
                
                case "CPF":
                    if hasattr(self, "cpfFornecedor"):
                        self.cpfFornecedor.destroy()
                        del self.cpfFornecedor
                        gc.collect
                    if hasattr(self, "cnpjFornecedor"):
                        self.cnpjFornecedor.destroy()
                        del self.cnpjFornecedor
                        gc.collect
                    self.cpfFornecedor = criarLabelEntry(frame, "CPF *", 0.64, 0.386, 0.25, None)

                case "CNPJ":
                    if hasattr(self, "cnpjFornecedor"):
                        self.cnpjFornecedor.destroy()
                        del self.cnpjFornecedor
                        gc.collect
                    if hasattr(self, "cpfFornecedor"):
                        self.cpfFornecedor.destroy()
                        del self.cpfFornecedor
                        gc.collect
                    self.cnpjFornecedor = criarLabelEntry(frame, "CNPJ *", 0.64, 0.246, 0.25, None)

                case "Sim.":
                    if hasattr(self, "campoRecebeEmail"):
                        self.campoRecebeEmail[0].destroy()
                        self.campoRecebeEmail[1].destroy()
                        gc.collect
                    self.campoRecebeEmail = criarLabelEntryEmail(frame, "Email *", 0.08, 0.562, 0.25,None)

                case "Não.":
                    if hasattr(self, "campoRecebeEmail"):
                        self.campoRecebeEmail[0].destroy()
                        self.campoRecebeEmail[1].destroy()
                        gc.collect


    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    
    # titulo
    self.textoCadastroFornecedores = ctk.CTkLabel(frame, height=0, text="Cadastrar fornecedores", font=("Century Gothic bold", 30))
    self.textoCadastroFornecedores.place(relx=0.5, y=40, anchor="center")


    self.ativoInativo = criaSimouNao(frame, "Ativo?", "Sim", "Não", 0.12, 0.1, comando=meDesmarque)
    self.cpfoupj = criaSimouNao(frame, "Tipo", "CPF", "CNPJ", 0.28, 0.1, comando=meDesmarque)
    self.Origem = criaSimouNao(frame, "Origem", "Nacion.", "Estrang.", 0.44, 0.1, comando=meDesmarque)
    self.eFabricante = criaSimouNao(frame, "É fabricante?", "Sim", "Não", 0.60, 0.1, comando=meDesmarque)
    self.recebeEmail = criaSimouNao(frame, "Recebe email?", "Sim.", "Não.", 0.76, 0.1, comando=meDesmarque)

    self.nomeReal = criarLabelEntry(frame, "Razão social *", 0.08, 0.246, 0.25, None)
    self.nomeFantasia = criarLabelEntry(frame, "Nome fantasia *", 0.36, 0.246, 0.25, None)
    self.telefone = criarLabelEntry(frame, "Telefone *", 0.64, 0.246, 0.25, None)


    self.inscricaoEstadual = criarLabelEntry(frame, "Inscrição estadual *", 0.08, 0.386, 0.25,None)
    self.codigoCRT = criarLabelEntry(frame, "CRT *", 0.36, 0.386, 0.25, None)

    criaBotao(frame, "Voltar", 0.29, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.66, 0.80, 0.20, lambda:registraFornecedorNoBanco(self, frame))
    aplicar_maiusculo_em_todos_entries(self)

