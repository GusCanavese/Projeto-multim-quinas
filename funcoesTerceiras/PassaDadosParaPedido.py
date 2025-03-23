import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consultas.select import Buscas
import datetime
from funcoesTerceiras.geradorDePedido import gerar_recibo
from apresentadorDePdf import telaApresentarPDF

def PassaDadosParaPedido(self):
    dataAgora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    resultados = Buscas.buscaDadosCliente(self.nomeDoClienteBuscado.get())
    for i, row in enumerate(resultados):
        telefone = row[2]
    print(self.valoresDosItens)
    self.dados = {
        "frete":self.valorFrete.get() or 0.0,
        "valor_total": self.totalSubtotal,
        "total_subtotal":self.totalSubtotal,
        "total_acrescimo":self.totalAcrescimo,
        "total_desc_real":self.totalDescontoReal,
        "total_desc_porc":self.totalDescontoPorcentagem,
        "total_quantidade": self.totalQuantidade,
        "itens": self.valoresDosItens,
        "referencia": self.entradaReferenciaEnderecoEntrega.get(),
        "endereco": self.entradaEnderecoNoPedido.get(),
        "cep": self.entradaCEP.get(),
        "telefone": telefone,
        "cnpj": self.CPFCliente.get(),
        "cpf": self.CPFCliente.get(),
        "destinatario": self.nomeDoClienteBuscado.get(),
        "data_confirmacao":self.dataDaVenda.get() ,
        "numero_recibo":self.numeroDeVenda.get(),
        "data_emissao":dataAgora,
        "subtotal": self.totalSubtotal,
    }

    gerar_recibo("Pedido.pdf", self.dados)

    if "Pedido.pdf":
        telaApresentarPDF(self, "Pedido.pdf")
    else: pass
    