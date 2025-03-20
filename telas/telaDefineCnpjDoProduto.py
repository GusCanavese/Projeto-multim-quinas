import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
import gc
from telas.telaGerarPedido import telaGerarPedido




def telaDefineCnpjDoProduto(self):
    self.frameDefineCnpjDoProduto = ctk.CTkFrame(self, height=700, width=1000, corner_radius=5)
    self.frameDefineCnpjDoProduto.place(x=140, y=100)     
    self.frameDefineCnpjDoProduto.grid_propagate(False)
    
    def confereCNPJpreenchido():
        if self.consultaCNPJ.get() != "Nenhum":
            telaGerarPedido(self)
        else:
            if hasattr(self, "labelCNPJNaoPreenchido"):
                del self.labelCNPJNaoPreenchido
                gc.collect
            self.labelCNPJNaoPreenchido = ctk.CTkLabel(self.frameDefineCnpjDoProduto, text="Nenhum CNPJ selecionado", text_color="red", font=("Century Gothic bold", 15))
            self.labelCNPJNaoPreenchido.place(relx=0.5, y=400, anchor="center")

    # título
    self.tituloDefineCnpj = ctk.CTkLabel(self.frameDefineCnpjDoProduto, height=0, text="Escolha o cnpj para a venda", font=("Century Gothic bold", 30))
    self.tituloDefineCnpj.place(relx=0.5, y=40, anchor="center")

    # cnpj que será a consulta no banco de dados
    self.labelConsultaCNPJ = ctk.CTkLabel(self.frameDefineCnpjDoProduto, text="Digite o cnpj que a venda será efetuada", font=("Century Gothic bold", 15))
    self.labelConsultaCNPJ.place(relx=0.5, y=300, anchor="center")
    opcoesCNPJ = ["Nenhum","Multimáquinas", "Polimáquinas", "Refrimaquinas"]
    self.consultaCNPJ = ctk.CTkComboBox(self.frameDefineCnpjDoProduto, width=310, corner_radius=5, font=("Century Gothic bold", 20), values=opcoesCNPJ)
    self.consultaCNPJ.place(relx=0.5, y=330, anchor="center")

    # voltar
    self.botaoVoltar = ctk.CTkButton(self.frameDefineCnpjDoProduto, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameDefineCnpjDoProduto.destroy)
    self.botaoVoltar.place(x=200, y=600)
    
    # ir para gerar pedido
    self.botaoCadastrarUsuario = ctk.CTkButton(self.frameDefineCnpjDoProduto, text="Cadastrar", width=200, corner_radius=5, font=("Arial", 15), command=confereCNPJpreenchido)
    self.botaoCadastrarUsuario.place(x=600, y=600)
