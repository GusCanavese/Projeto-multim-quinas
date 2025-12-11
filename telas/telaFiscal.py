import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from componentes import criaFrameJanela, criaFrameJanela, criaBotao, criaFrameJanela
from telas.telaNotaFiscalSaida import telaNotaFiscalSaida 
from funcoesTerceiras.escolherNotaFiscal import escolherNotaFiscal
from telas.telaEstoqueFiscal import telaEstoqueFiscal
from telas.telaSpedFiscal import telaSpeedFiscal
from telas.telaRelatorioDeNotasFiscais import telaRelatorioDeNotasFiscais



def telaFiscal(self):
        self.frameTelaFiscal = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

        relatorioDeVendas = criaBotao(self.frameTelaFiscal, "Emitir nota de saída", 0.66, 0.24, 0.24, lambda:telaNotaFiscalSaida(self, 1, 0))
        relatorioDeVendas.configure(height=50, image=None, compound="left")

        estoque = criaBotao(self.frameTelaFiscal, "Estoque", 0.66, 0.35, 0.24, lambda:telaEstoqueFiscal(self))
        estoque.configure(height=50, image=None, compound="left")

        gerarPedido = criaBotao(self.frameTelaFiscal, "Emitir nota de entrada (Importar XML)", 0.33, 0.24, 0.24, lambda:escolherNotaFiscal(self))
        gerarPedido.configure(height=50, image=None, compound="left")

        gerarOrcamento = criaBotao(self.frameTelaFiscal, "Gerar Sped fiscal", 0.33, 0.35, 0.24, lambda:telaSpeedFiscal(self))
        gerarOrcamento.configure(height=50, image=None, compound="left")

        gerarOrcamento = criaBotao(self.frameTelaFiscal, "Gerar NFC-e", 0.33, 0.46, 0.24, lambda:telaNotaFiscalSaida(self, 0, 1))
        gerarOrcamento.configure(height=50, image=None, compound="left")

        verTodasAsNotas = criaBotao(self.frameTelaFiscal, "Ver todas as notas", 0.66, 0.46, 0.24, lambda:telaRelatorioDeNotasFiscais(self))
        verTodasAsNotas.configure(height=50, image=None, compound="left")

        criaBotao(self.frameTelaFiscal, "◀️ Voltar", 0.15, 0.94, 0.15, lambda:self.frameTelaFiscal.destroy())
