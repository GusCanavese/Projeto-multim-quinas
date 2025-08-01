import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
import gc
from funcoesTerceiras.registraFornecedorNoBanco import registraFornecedorNoBanco 
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criaSimouNao, criarLabelEntry, criaBotao, criarLabelEntryEmail
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries




def telaCadastroFornecedores(self):
    bairro = ctk.StringVar()
    rua = ctk.StringVar()
    cidade = ctk.StringVar()
    estado = ctk.StringVar()


    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    self.textoCadastroFornecedores = ctk.CTkLabel(frame, height=0, text="Cadastrar fornecedores", font=("Century Gothic bold", 30))
    self.textoCadastroFornecedores.place(relx=0.5, y=40, anchor="center")

    def meDesmarqueFornecedor(checkboxSelecionada):
        if checkboxSelecionada == "Sim.":
            self.emailFornecedor.configure(state="normal")
        else:
            self.emailFornecedor.configure(state="disabled")

    def passe(self):
        pass

    self.ativoInativo = criaSimouNao(frame, "Ativo?", "Sim", "Não", 0.12, 0.1, passe)
    self.transpRecebeEmail = criaSimouNao(frame, "Recebe email?", "Sim.", "Não.", 0.28, 0.1, comando=meDesmarqueFornecedor)
    self.Origem = criaSimouNao(frame, "Origem", "Nacion.", "Estrang.", 0.44, 0.1, passe)
    self.eFabricante = criaSimouNao(frame, "É fabricante?", "Sim", "Não", 0.60, 0.1, passe)


    self.nomeFornecedor              = criarLabelEntry(frame, "Razão social *",       0.1  - 0.03, 0.25, 0.2, None)
    self.nomeFantasiaFornecedor      = criarLabelEntry(frame, "Nome *",               0.32 - 0.03, 0.25, 0.2, None)
    self.CPFFornecedor               = criarLabelEntry(frame, "CPF/CNPJ *",           0.1  - 0.03, 0.35, 0.2, None)
    self.telefoneFornecedor          = criarLabelEntry(frame, "Telefone *",           0.32 - 0.03, 0.35, 0.2, None)
    self.inscricaoEstadualFornecedor = criarLabelEntry(frame, "Inscrição estadual *", 0.1  - 0.03, 0.45, 0.2, None)
    self.descricaoFornecedor         = criarLabelEntry(frame, "Descrição",            0.32 - 0.03, 0.45, 0.2, None)
    self.emailFornecedor             = criarLabelEntry(frame, "Email *",              0.1  - 0.03, 0.55, 0.2, None)
    self.codigoCRT                   = criarLabelEntry(frame, "CRT *",                0.32 - 0.03, 0.55, 0.2, None)

    self.CEPFornecedor               = criarLabelEntry(frame, "CEP *",                0.54 - 0.03, 0.25, 0.2, None)
    self.rua                         = criarLabelEntry(frame, "Rua *",                0.76 - 0.03, 0.25, 0.2, rua)
    self.bairroFornecedor            = criarLabelEntry(frame, "Bairro *",             0.54 - 0.03, 0.35, 0.2, bairro)
    self.numeroFornecedor            = criarLabelEntry(frame, "Número *",             0.76 - 0.03, 0.35, 0.2, None)
    self.cidadeFornecedor            = criarLabelEntry(frame, "Cidade *",             0.54 - 0.03, 0.45, 0.2, cidade)
    self.estadoFornecedor            = criarLabelEntry(frame, "Estado *",             0.76 - 0.03, 0.45, 0.2, estado)
    self.referencia                  = criarLabelEntry(frame, "Referência ",          0.54 - 0.03, 0.55, 0.2, None)




    criaBotao(frame, "◀️ Voltar", 0.29, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.66, 0.80, 0.20, lambda:registraFornecedorNoBanco(self, frame))
    aplicar_maiusculo_em_todos_entries(self)

