import sys
import os
from tkinter import messagebox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consultas.select import Buscas
from consultas.insert import Insere
from consultas.update import Atualiza
import datetime
from funcoesTerceiras import geradorDeOrcamento
from telas.telaApresentarOrcamento import telaApresentarOrcamento
import json

def passaDadosParaOrcamento(self):
    dataAgora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    resultados = Buscas.buscaDadosCliente(self.nomeDoClienteBuscado.get())

    for i, row in enumerate(resultados):
        telefone = row[2]
        if telefone == "":
            telefone = "N/A"


    if self.entradaEnderecoNoPedido.get() =="" or self.entradaReferenciaEnderecoEntrega.get()=="" or self.entradaNumero.get() =="" or self.CPFCliente.get()=="" or self.nomeDoClienteBuscado.get()=="":
        messagebox.showerror("erro", "Preencha todos os campos obrigatórios")
    elif self.entradaProduto.get()=="":
        messagebox.showerror("erro", "Selecione pelo menos um produto")

    else:
        self.dados = {
            "vendedor": self.funcionariaPedido.get(),
            "frete": self.valorFrete.get() or 0.0,
            
            "valor_total": self.totalSubtotal.get(),
            "total_subtotal": self.totalSubtotal.get(),
            "total_acrescimo": self.totalAcrescimo.get(),
            "total_desc_real": self.totalDescontoReal.get(),
            "total_desc_porc": self.totalDescontoPorcentagem.get(),
            
            "itens": self.valoresDosItens,
            
            "referencia": self.entradaReferenciaEnderecoEntrega.get(),
            "endereco": self.entradaEnderecoNoPedido.get(),
            "cep": self.entradaCEP.get(),
            "telefone": telefone,  # já é string fora de Entry, ok aqui
            "cnpj": self.CPFCliente.get(),
            "cpf": self.CPFCliente.get(),
            "destinatario": self.nomeDoClienteBuscado.get(),
            
            "data_confirmacao": self.dataDaVenda.get(),
            "numero_recibo": self.numeroDeVenda.get(),  # corrigido, estava self..get()
            "data_emissao": dataAgora,  # OK, já é string
            
            "subtotal": self.totalSubtotal.get(),
        }

        # Insere.registraPedidoNoBanco(self.dados)
        geradorDeOrcamento.gerarOrcamento("Orcamento.pdf", self.dados)


        if "Orcamento.pdf":
            telaApresentarOrcamento(self, "Orcamento.pdf")
        
    