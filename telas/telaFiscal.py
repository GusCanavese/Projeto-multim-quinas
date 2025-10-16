import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from componentes import criaFrameJanela, criaFrameJanela, criaBotao, criaFrameJanela
from telas.telaNotaFiscalSaida import telaNotaFiscalSaida 
from funcoesTerceiras.escolherNotaFiscal import escolherNotaFiscal
from telas.telaEstoqueFiscal import telaEstoqueFiscal
from telas.telaSpedFiscal import telaSpeedFiscal



def telaFiscal(self):
        frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

        relatorioDeVendas = criaBotao(frame, "Emitir nota de saída", 0.66, 0.24, 0.24, lambda:telaNotaFiscalSaida(self, 1, 0))
        relatorioDeVendas.configure(height=50, image=None, compound="left")

        estoque = criaBotao(frame, "Estoque", 0.66, 0.35, 0.24, lambda:telaEstoqueFiscal(self))
        estoque.configure(height=50, image=None, compound="left")

        gerarPedido = criaBotao(frame, "Emitir nota de entrada (Importar XML)", 0.33, 0.24, 0.24, lambda:escolherNotaFiscal(self))
        gerarPedido.configure(height=50, image=None, compound="left")

        gerarOrcamento = criaBotao(frame, "Gerar Sped fiscal", 0.33, 0.35, 0.24, lambda:telaSpeedFiscal(self))
        gerarOrcamento.configure(height=50, image=None, compound="left")

        gerarOrcamento = criaBotao(frame, "Gerar NFC-e", 0.33, 0.46, 0.24, lambda:telaNotaFiscalSaida(self, 0, 1))
        gerarOrcamento.configure(height=50, image=None, compound="left")

        criaBotao(frame, "◀️ Voltar", 0.15, 0.94, 0.15, lambda:frame.destroy())
