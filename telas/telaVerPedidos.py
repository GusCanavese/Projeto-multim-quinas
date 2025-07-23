import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import confirmarAlteracoesNoPedido
from funcoesTerceiras import confirmarExclusaoDoPedido
from funcoesTerceiras import geradorDePedido
from telas.telaApresentadorDePdf import telaApresentarPDF
from telas.telagerarFaturamento import telaGerarFaturamento
from componentes import criaFrameJanela,  criaBotao, criaFrame, criaLabelDescritivo, criarLabelEntry

def telaVerPedidos(self, p, d, desc):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    if p[5] == "Não confirmado":
        
        criaBotao(frame, 'Gerar faturamento', 0.495, 0.48, 0.15, lambda:telaGerarFaturamento(self, p[3], p[0], d[0]))
        criaBotao(frame, 'Confirmar alterações',    0.38, 0.95, 0.20, lambda:confirmarAlteracoesNoPedido.confirmarAlteracoesNoPedido(self, self.dataDaVendaTelaVerPedidos.get(), p[0], frame))
        self.status = "Venda em aberto"
        dataDaVendaTelaVerPedidos = ''
        criarLabelEntry(frame, "Data de confirmação", 0.42, 0.08, 0.15, ctk.StringVar(value=dataDaVendaTelaVerPedidos))
        criaBotao(frame, 'Confirmar venda', 0.7, 0.12, 0.15, lambda:confirmarAlteracoesNoPedido.confirmarHoje(self, p[0], frame))
    else:
        self.status = "Confirmado"
        dataDaVendaTelaVerPedidos = p[4]
        criaLabelDescritivo(frame, "Data de confirmação", 0.42, 0.07, 0.15, self.cor, ctk.StringVar(value=dataDaVendaTelaVerPedidos))
        criaLabelDescritivo(frame, 'Venda confirmada', 0.62, 0.07, 0.15, "green", None)
        
    # Primeira linha (relx espaçado em 0.2, rely em 0.05 e 0.1)
    criaLabelDescritivo(frame, "Número da venda",     0.02, 0.07, 0.15, self.cor, ctk.StringVar(value=p[0]))
    criaLabelDescritivo(frame, "Data de criação",     0.22, 0.07, 0.15, self.cor, ctk.StringVar(value=p[2]))
    criaLabelDescritivo(frame, "Vendedor(a)",         0.82, 0.07, 0.15, self.cor, ctk.StringVar(value=p[1]))

    criaLabelDescritivo(frame, "Nome do cliente", 0.02, 0.25, 0.15, self.cor, ctk.StringVar(value=d[0]))
    criaLabelDescritivo(frame, "Valor",           0.22, 0.25, 0.15, self.cor, ctk.StringVar(value=p[3]))
    criaLabelDescritivo(frame, "CPF/CNPJ",        0.42, 0.25, 0.15, self.cor, ctk.StringVar(value=d[1]))
    criaLabelDescritivo(frame, "Produto",         0.62, 0.25, 0.35, self.cor, ctk.StringVar(value=desc[0]))

    criaLabelDescritivo(frame, "Endereço",        0.02, 0.43, 0.35, self.cor, ctk.StringVar(value=d[2]))

    criaBotao(frame, 'Voltar', 0.15, 0.95, 0.20, lambda:frame.destroy())
    botaoExclui = criaBotao(frame, 'Cancelar/Excluir pedido', 0.61, 0.95, 0.20, lambda:confirmarExclusaoDoPedido.confirmarExclusaoNoPedido(self, p[0], desc, frame))
    botaoExclui.configure(fg_color=self.corNegado)


    def imprimirPedido():
        itens = []
        for item in desc:
            partes = item.split()
            if len(partes) < 2:
                continue  # ignora itens mal formatados

            descricao = " ".join(partes[:-1])
            quantidade = partes[-1]

            itens.append({
                "descricao": descricao,
                "quantidade": quantidade,
                "subtotal": p[4],
                "desconto_porcentagem": 0.0,
                "desconto_reais": 0.0,
                "acrescimo": 0.0,
            })

        dados = {
            "vendedor": p[1],
            "frete": 0.0,

            "valor_total": p[3],
            "total_subtotal": p[3],
            "total_acrescimo": 0.0,
            "total_desc_real": 0.0,
            "total_desc_porc": 0.0,

            "itens": itens,

            "referencia": "", 
            "endereco": d[2],
            "cep": "", 
            "telefone": "", 
            "cnpj": d[1],
            "cpf": d[1],
            "destinatario": d[0],

            "numero_recibo": p[0],
            "data_emissao": p[2],

            "subtotal": 1,
            "observacoes1": "",
            "observacoes2": ""
        }

        from funcoesTerceiras import geradorDePedido
        from telas.telaApresentadorDePdf import telaApresentarPDF

        geradorDePedido.gerar_recibo("Pedido.pdf", dados)
        telaApresentarPDF(self, "Pedido.pdf", 1)

    criaBotao(frame, 'Imprimir pedido', 0.38, 0.89, 0.20, imprimirPedido)
