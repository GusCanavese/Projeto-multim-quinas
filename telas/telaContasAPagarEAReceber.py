import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras.escolherNotaFiscal import escolherNotaFiscal
from funcoesTerceiras import filtrar, verificaSeQuerFiltrarPorPeriodo
from componentes import criaFrameJanela, criaFrameJanela, criaLabel, criaBotao, criaComboBox, criarLabelEntry
from telas.telaNotaFiscalSaida import telaNotaFiscalSaida 


def telaContasAPagarEAReceber(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    frameContas = criaFrameJanela(frame, 0.5, 0.50, 0.95, 0.7, self.corFundo)
    opcoes = ["Nenhum", "Entrada/Débito", "Saída/Crédito"]

    self.selecionarPeriodoContas = ctk.CTkCheckBox(frame, text="Selecionar período")
    self.selecionarPeriodoContas.place(relx=0.55, rely=0.03, anchor="nw")
    self.selecionarPeriodoContas.bind("<Button-1>", command=lambda event: verificaSeQuerFiltrarPorPeriodo.verificaSeQuerFiltrarPorPeriodoContas(self, frame, self.selecionarPeriodoContas.get(), event))
    
    filtrarPorNumero = criarLabelEntry(frame, "Filtrar", 0.25, 0.01, 0.22, None)
    if hasattr(self, "datePickerInicio"):
        criaBotao(frame, "Buscar", 0.36, 0.11, 0.22,lambda: filtrar.filtrarContas(self,frameContas,filtrarPorNumero.get(),self.datePickerInicio.get(), pagina=1))
    else:
        criaBotao(frame, "Buscar", 0.36, 0.11, 0.22,lambda: filtrar.filtrarContas(self,frameContas,filtrarPorNumero.get(), pagina=1))


    def escolheTela(valor):
        if valor=="Saída/Crédito":
            telaNotaFiscalSaida()
        if valor=="Entrada/Débito":
            escolherNotaFiscal(self)
            
    def creditoOuDebito():
        if hasattr(self, "creditoOuDebito"):
            self.creditoOuDebito.destroy()
            self.creditoOuDebito = criaComboBox(frame, 0.13, 0.11, 0.15, opcoes, lambda valor:escolheTela(valor))
        else:
            self.creditoOuDebito = criaComboBox(frame, 0.13, 0.11, 0.15, opcoes, lambda valor:escolheTela(valor))

            
    criaBotao(frame, "Registrar credito/débito", 0.13, 0.05, 0.15, lambda:creditoOuDebito()).configure(fg_color="#009351")
    criaBotao(frame, "◀️ Voltar", 0.15, 0.94, 0.15, lambda:frame.destroy())

    # Cabeçalhos da tabela
    colunas = ["Confirmado", "Descriçao", "Vencimento", "Total"]
    x = 0.03
    y = 0.05

    for i, coluna in enumerate(colunas):
        if i == 0:
            criaLabel(frameContas, coluna, x, y, 0.08, self.cor)
            x+=0.085
        elif i == 1:
            criaLabel(frameContas, coluna, x, y, 0.4, self.cor)
            x+=0.405
        elif i == 2:
            criaLabel(frameContas, coluna, x, y, 0.17, self.cor)
            x+=0.175
        elif i == 3:
            criaLabel(frameContas, coluna, x, y, 0.17, self.cor)
            x+=0.175

 