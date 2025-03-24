import sys
import os
from tkinter import messagebox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consultas.select import Buscas
import datetime
from funcoesTerceiras.geradorDePedido import gerar_recibo
from apresentadorDePdf import telaApresentarPDF

def PassaDadosParaPedido(self):
    dataAgora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    resultados = Buscas.buscaDadosCliente(self.nomeDoClienteBuscado.get())
    print(self.textArea1.get("1.0", "end-1c"))

    for i, row in enumerate(resultados):
        telefone = row[2]
        if telefone == "":
            telefone = "Cliente nao possui telefone para contato"


    if self.entradaEnderecoNoPedido.get() =="" or self.entradaReferenciaEnderecoEntrega.get()=="" or self.entradaNumero.get() =="" or self.CPFCliente.get()=="":
        messagebox.showerror("erro", "Preencha todos os campos obrigatórios")

    else:
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
            "observacoes1":self.textArea1.get("1.0", "end-1c"),
            "observacoes2":self.textArea2.get("1.0", "end-1c"),
        }
    
        gerar_recibo("Pedido.pdf", self.dados)

        if "Pedido.pdf":
            telaApresentarPDF(self, "Pedido.pdf")
        
    