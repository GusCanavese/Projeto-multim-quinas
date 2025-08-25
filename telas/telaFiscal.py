import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from componentes import criaFrameJanela, criaFrameJanela, criaBotao, criaFrameJanela
from telas.telaNotaFiscalSaida import telaNotaFiscalSaida 
from funcoesTerceiras.escolherNotaFiscal import escolherNotaFiscal



def telaFiscal(self):
        frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

        relatorioDeVendas = criaBotao(frame, "Emitir nota fiscal de saída", 0.66, 0.24, 0.24, lambda:telaNotaFiscalSaida(self, 1))
        relatorioDeVendas.configure(height=50, image=None, compound="left")

        estoque = criaBotao(frame, "Estoque", 0.66, 0.35, 0.24, lambda:None)
        estoque.configure(height=50, image=None, compound="left")

        gerarPedido = criaBotao(frame, "Importar XML", 0.33, 0.35, 0.24, lambda:escolherNotaFiscal)
        gerarPedido.configure(height=50, image=None, compound="left")

        gerarOrcamento = criaBotao(frame, "Gerar Sped fiscal", 0.33, 0.24, 0.24, lambda:None)
        gerarOrcamento.configure(height=50, image=None, compound="left")
