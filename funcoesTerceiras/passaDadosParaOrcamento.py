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

def PassaDadosParaOrcamento(self):
    dataAgora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    resultados = Buscas.buscaDadosCliente(self.nomeDoClienteBuscado.get())

    for i, row in enumerate(resultados):
        telefone = row[2]
        if telefone == "":
            telefone = "N/A"


    if self.entradaEnderecoNoPedido.get() =="" or self.entradaReferenciaEnderecoEntrega.get()=="" or self.entradaNumero.get() =="" or self.CPFCliente.get()=="" or self.nomeDoClienteBuscado.get()=="":
        messagebox.showerror("erro", "Preencha todos os campos obrigatórios")
    elif self.entradaProdutoPesquisado.get()=="":
        messagebox.showerror("erro", "Selecione pelo menos um produto")

    else:
        self.parcelas = 0
        if hasattr(self, "QtdParcelas"):
            self.parcelas = self.QtdParcelas.get()
        else: None
        self.dados = {
            "vendedor":self.funcionariaPedido.get(),
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
            "observacoes1":self.textArea1.get("1.0", "end-1c"),
            "observacoes2":self.textArea2.get("1.0", "end-1c"),
            "forma_pagamento":self.formaDePagamento.get(),
            "parcelas": self.parcelas
                 
        }
        # Insere.registraPedidoNoBanco(self.dados)
        geradorDeOrcamento.gerarOrcamento("Orcamento.pdf", self.dados)

        # pedidos = Buscas.buscaPedidos(self.funcionariaPedido.get(), self.numeroDeVenda.get(), None, None, 0)

        # for rowPedido, pedido in enumerate(pedidos, start=1):
        #     dadosDoProdutoDoPedido = json.loads(pedido[8])

        #     descricaoProdutos = [f"{produto['descricao']} {produto['quantidade']}" for produto in dadosDoProdutoDoPedido]
        #     print(descricaoProdutos)
        #     print(descricaoProdutos)
        #     Atualiza.removeUnidadesDeProdutos(desc=descricaoProdutos)
        


        if "Orcamento.pdf":
            telaApresentarOrcamento(self, "Orcamento.pdf")
        
    