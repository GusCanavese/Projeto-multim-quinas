import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consultas.select import Buscas
import datetime
from funcoesTerceiras.geradorDePedido import gerar_recibo

def telaImprimirPedido(self):
    dataAgora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    resultados = Buscas.buscaDadosCliente(self.nomeDoClienteBuscado.get())
    for i, row in enumerate(resultados):
        telefone = row[2]
    print(self.valoresDosItens)
    self.dados = {
        "frete":self.valorFrete,
        "valor_total": self.valorFinal,
        "total_subtotal":self.totalSubtotal,
        "total_acrescimo":self.totalAcrescimo,
        "total_desc_real":self.variavelTotalDescontoReal,
        "total_desc_porc":self.variavelTotalDescontoPorcentagem,
        "total_quantidade": self.totalQuantidade,
        "itens": self.valoresDosItens,
        "referencia": self.entradaReferenciaEnderecoEntrega.get(),
        "endereco": self.entradaEnderecoNoPedido.get(),
        "cep": self.entradaCEP.get(),
        "telefone": telefone,
        "cnpj": self.CPFCliente.get(),
        "cpf": self.CPFCliente.get(),
        "destinatario": self.entradaEnderecoNoPedido.get(),
        "data_confirmacao":self.dataDaVenda.get() ,
        "numero_recibo":self.numeroDeVenda.get(),
        "data_emissao":dataAgora,
        "subtotal": self.totalSubtotal,
    }

    gerar_recibo("Pedido.pdf", self.dados)
    