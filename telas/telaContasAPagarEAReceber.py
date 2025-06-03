import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.escolherNotaFiscal import escolherNotaFiscal

def telaContasAPagarEAReceber(self):
    self.frameTelaContasAPagarEAReceber = ctk.CTkFrame(self)
    self.frameTelaContasAPagarEAReceber.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)

    # Frame rolável (conteúdo principal)
    self.frameParaContasAPagarEReceber = ctk.CTkScrollableFrame(self.frameTelaContasAPagarEAReceber)
    self.frameParaContasAPagarEReceber.place(relx=0.3, rely=0.01, relwidth=0.68, relheight=0.93)

    def escolheTela(valor):
        print(valor)
        if valor=="Entrada/Débito":
            print("sem tela no momento")
        if valor=="Saída/Crédito":
            escolherNotaFiscal(self)
            
    def creditoOuDebito():
        if hasattr(self, "creditoOuDebito"):
            self.creditoOuDebito.destroy()
        else:
            opcoes = ["Nenhum", "Entrada/Débito", "Saída/Crédito"]
            self.creditoOuDebito = ctk.CTkComboBox(self.frameTelaContasAPagarEAReceber, font=("Century Gothic bold", 15), values=opcoes, command=lambda valor:escolheTela(valor))
            self.creditoOuDebito.place(relx=0.07, rely=0.2)
            
    
    botaoNovo = ctk.CTkButton(self.frameTelaContasAPagarEAReceber, text="Registrar credito/débito", fg_color="#006D5B", command=lambda:creditoOuDebito())
    botaoNovo.place(relx=0.07, rely=0.1)

    # Botões
    self.botaoFiltrar = ctk.CTkButton(self.frameTelaContasAPagarEAReceber,text="Buscar", command=lambda: filtrarPedidos.filtrarPedidos( self, self.filtrarPorVendedor.get(), self.filtrarPorNumero.get(), self.datePickerInicio.get() if hasattr(self, "datePickerInicio") else None, self.datePickerFim.get() if hasattr(self, "datePickerFim") else None, self.selecionarPeriodo.get()))
    self.botaoFiltrar.place(relx=0.05, rely=0.55, relwidth=0.15, anchor="nw")

    botaoVoltar = ctk.CTkButton(self.frameTelaContasAPagarEAReceber, text="Voltar", command=self.frameTelaContasAPagarEAReceber.destroy)
    botaoVoltar.place(relx=0.05, rely=0.94, relwidth=0.15, anchor="nw")

    # Cabeçalhos da tabela
    colunas = ["Pedido", "Vendedor", "Data de emissão", "Subtotal", "Confirmação da venda"]
    for i, coluna in enumerate(colunas):
        label = ctk.CTkLabel(self.frameParaContasAPagarEReceber, text=coluna, width=150, fg_color="#2C3E50", anchor="center")
        label.grid(row=0, column=i, padx=2, pady=5)
        label.grid_columnconfigure(0, minsize=20)
