import sys
import os
from tkinter import messagebox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consultas.select import Buscas
from consultas.insert import Insere
from consultas.update import Atualiza
import datetime
from funcoesTerceiras import geradorDePedido
from telas.telaApresentadorDePdf import telaApresentarPDF
import json

def PassaDadosParaPedido(self, frame):
    dataAgora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    resultados = Buscas.buscaDadosCliente(self.nomeDoClienteBuscado.get())

    for i, row in enumerate(resultados):
        telefone = row[2]
        if telefone == "":
            telefone = "N/A"


    if self.entradaEnderecoNoPedido.get() =="" or self.entradaNumero.get() =="" or self.CPFCliente.get()=="" or self.nomeDoClienteBuscado.get()=="":
        messagebox.showerror("erro", "Preencha todos os campos obrigatórios")

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
            "telefone": telefone,  
            "cnpj": self.CPFCliente.get(),
            "cpf": self.CPFCliente.get(),
            "destinatario": self.nomeDoClienteBuscado.get(),
            
            "numero_recibo": self.numeroDeVenda.get(),  
            "data_emissao": dataAgora,  
            
            "subtotal": self.totalSubtotal.get(),
            "observacoes1": self.textArea1.get("1.0", "end-1c"),
            "observacoes2": self.textArea2.get("1.0", "end-1c")
        }

        Insere.registraPedidoNoBanco(self.dados)
        geradorDePedido.gerar_recibo("Pedido.pdf", self.dados)

        pedidos = Buscas.buscaPedidos(self.funcionariaPedido.get(), self.numeroDeVenda.get(), None, None, 0)

        for rowPedido, pedido in enumerate(pedidos, start=1):
            dadosDoProdutoDoPedido = json.loads(pedido[8])

            descricaoProdutos = [f"{produto['descricao']} {produto['quantidade']}" for produto in dadosDoProdutoDoPedido]
            Atualiza.removeUnidadesDeProdutos(desc=descricaoProdutos)
            frame.destroy()
        


        if "Pedido.pdf":
            telaApresentarPDF(self, "Pedido.pdf", 0)
        
    