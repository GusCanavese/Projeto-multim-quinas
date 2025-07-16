import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consultas.select import Buscas 
from datetime import datetime
from componentes import criaLabel, criaBotao
from telas.telaVercontasApagar import telaVercontasApagar
#! PARA A BUSCA COM DATAS FUNCIONAR, 
# É NECESSÁRIO CADASTRAR A CONTAARECEBER 
# E PAGAR COM O FORMATO DATETIME SEM A 
# HORA, SOMENTE COM A DATA
def filtrarContas(self, frame, valor, pagina=1):
    if hasattr(self, "datePickerInicio") and hasattr(self, "datePickerFim"):
        inicio = self.datePickerInicio.get()
        fim = self.datePickerFim.get()
        inicio = datetime.strptime(inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
        fim = datetime.strptime(fim, "%d/%m/%Y").strftime("%Y-%m-%d")
    else:
        inicio = None
        fim = None

    contasReceber = Buscas.buscaContasAReceber(valor, inicio, fim)
    contasPagar = Buscas.buscaContasAPagar(valor, inicio, fim)
    contas = contasReceber + contasPagar



    if hasattr(self, "dadosTelaFiltrarContas"):
        for item in self.dadosTelaFiltrarContas:
            item.destroy()
    self.dadosTelaFiltrarContas = []

    # Calcula o intervalo de pedidos a mostrar
    inicioContas = (pagina - 1) * 10
    fimContas = pagina * 10
    contasPagina = contas[inicioContas:fimContas]
    
    y = 0.1

    for rowProduto, conta in enumerate(contasPagina, start=1):
        corDeFundo = "#1C60A0"
        dadosProduto = [conta[0], conta[2], conta[1], conta[3], conta[4]]
        print(dadosProduto)
        try:
            datetime.strptime(conta[1], "%d/%m/%Y")
        except:
            dataOriginal = dadosProduto[2]
            dataOriginal = str(dataOriginal)
            try:
                dataFormatada = datetime.strptime(dataOriginal, "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                dataFormatada = datetime.strptime(dataOriginal, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
            dadosProduto[2] = dataFormatada

        x = 0.03


        for colNum, valor in enumerate(dadosProduto):
            if colNum == 0:
                if "Não" in conta[0]:
                    corDeFundo = "#922B21"
                elif "Sim" in conta[2]:
                    corDeFundo = "#196F3D"
                label = criaLabel(frame, valor, x, y, 0.08, corDeFundo)
                x+=0.085
            elif colNum ==1:
                corDeFundo = "#1C60A0"
                label = criaLabel(frame, valor, x, y, 0.4, corDeFundo)
                x+=0.405
            elif colNum ==2:
                corDeFundo = "#1C60A0"
                label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
                x+=0.175
            elif colNum ==3:
                if "lançamento referente a nota" in conta[2]:
                    valor1 = conta[3]
                    valor1 = valor *-1
                    corDeFundo = "#922B21"
                    label = criaLabel(frame, valor1, x, y, 0.17, corDeFundo)
                if "lançamento referente ao pedido" in conta[2]:
                    corDeFundo = "#196F3D" 
                    label = criaLabel(frame, valor, x, y, 0.17, corDeFundo)
                
                x+=0.175

            self.dadosTelaFiltrarContas.append(label)

        btn = criaBotao(frame, "Ver", 0.937, y, 0.05, lambda p=conta: telaVercontasApagar(self, p))
        self.dadosTelaFiltrarContas.append(btn)

        y += 0.059
    
    if len(contas) > 10:

        
        params = {
            'pagina': pagina,
        }

        if pagina > 1:
            btnAnterior = criaBotao(frame, "← Anterior", 0.33, 0.6, 0.2, lambda p=params: filtrarContas(self, frame, p['pagina']-1))
            self.dadosTelaFiltrarContas.append(btnAnterior)

        if fimContas < len(contas):
            btnProxima = criaBotao(frame, "Próximo →", 0.66, 0.6, 0.2, lambda p=params: filtrarContas(self, frame, p['pagina']+1))
            self.dadosTelaFiltrarContas.append(btnProxima)
