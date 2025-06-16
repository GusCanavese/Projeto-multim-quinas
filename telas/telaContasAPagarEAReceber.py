import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.escolherNotaFiscal import escolherNotaFiscal
from funcoesTerceiras import filtrarPedidos
from componentes import criaFrame, criaLabel, criaBotao, criaComboBox

def telaContasAPagarEAReceber(self):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    frameVendas = criaFrame(frame, 0.65, 0.5, 0.68, 0.93)
    opcoes = ["Nenhum", "Entrada/Débito", "Saída/Crédito"]



    def escolheTela(valor):
        print(valor)
        if valor=="Entrada/Débito":
            print("sem tela no momento")
        if valor=="Saída/Crédito":
            escolherNotaFiscal(self)
            
    def creditoOuDebito():
        if hasattr(self, "creditoOuDebito"):
            self.creditoOuDebito.destroy()
            self.creditoOuDebito = criaComboBox(frame, 0.15, 0.2, 0.15, opcoes, lambda valor:escolheTela(valor))
        else:
            self.creditoOuDebito = criaComboBox(frame, 0.15, 0.2, 0.15, opcoes, lambda valor:escolheTela(valor))

            
    botaoCriaNovo = criaBotao(frame, "Registrar credito/débito", 0.15, 0.1, 0.15, lambda:creditoOuDebito())
    botaoCriaNovo.configure(fg_color="#006D5B")

    criaBotao(frame, "Buscar", 0.15, 0.55, 0.15, lambda:filtrarPedidos.filtrarPedidos( self, frameVendas, self.filtrarPorVendedor.get(), self.filtrarPorNumero.get(), self.datePickerInicio.get() if hasattr(self, "datePickerInicio") else None, self.datePickerFim.get() if hasattr(self, "datePickerFim") else None, self.selecionarPeriodo.get()))
    criaBotao(frame, "Voltar", 0.15, 0.94, 0.15, lambda:frame.destroy())

    # Cabeçalhos da tabela
    colunas = ["Pedido", "Vendedor", "Data de emissão", "Subtotal", "Confirmação da venda"]
    x = 0.03
    y = 0.05

    for i, coluna in enumerate(colunas):
        criaLabel(frameVendas, coluna, x, y, 0.17, "#2C3E50")
        x+=0.175

 