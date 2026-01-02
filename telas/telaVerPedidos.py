import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import confirmarAlteracoesNoPedido
from funcoesTerceiras import confirmarExclusaoDoPedido
from telas.telagerarFaturamento import telaGerarFaturamento
from componentes import criaFrameJanela, criaBotao, criarLabelEntry

def telaVerPedidos(self, p, d, desc, itens_pedido):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    itens_pedido = itens_pedido or []
    if isinstance(itens_pedido, dict):
        itens_pedido = list(itens_pedido.values())

    frame_acoes = ctk.CTkFrame(frame, fg_color="transparent")
    frame_acoes.place(relx=0.5, rely=0.08, relwidth=0.92, relheight=0.16, anchor="center")

    if p[5] == "Não confirmado":
        criaBotao(frame_acoes, 'Gerar faturamento', 0.68, 0.1, 0.18, lambda:telaGerarFaturamento(self, p[4], p[0], d[0]))
        criaBotao(
            frame_acoes,
            'Confirmar alterações',
            0.68,
            0.55,
            0.18,
            lambda:confirmarAlteracoesNoPedido.confirmarAlteracoesNoPedido(
                self,
                self.dataDaVendaTelaVerPedidos.get(),
                p[0],
                frame,
                p[4],
                d[0],
            ),
        )
        self.status = "Venda em aberto"
        dataDaVendaTelaVerPedidos = ''
        self.dataDaVendaTelaVerPedidos = criarLabelEntry(
            frame_acoes,
            "Data de confirmação",
            0.28,
            0.1,
            0.22,
            ctk.StringVar(value=dataDaVendaTelaVerPedidos),
        )
        ctk.CTkLabel(frame_acoes, text="Status: Venda em aberto").place(relx=0.02, rely=0.2, anchor="w")
        criaBotao(
            frame_acoes,
            'Confirmar venda',
            0.5,
            0.1,
            0.16,
            lambda:confirmarAlteracoesNoPedido.confirmarHoje(self, p[0], frame, p[4], d[0]),
        )
    else:
        self.status = "Confirmado"
        dataDaVendaTelaVerPedidos = p[5]
        ctk.CTkLabel(frame_acoes, text="Status: Venda confirmada", text_color="green").place(relx=0.02, rely=0.2, anchor="w")
        criarLabelEntry(
            frame_acoes,
            "Data de confirmação",
            0.28,
            0.1,
            0.22,
            ctk.StringVar(value=dataDaVendaTelaVerPedidos),
        )

    tabs = ctk.CTkTabview(frame, fg_color="transparent")
    tabs.place(relx=0.5, rely=0.5, relwidth=0.92, relheight=0.56, anchor="center")
    tab_resumo = tabs.add("Resumo")
    tab_cliente = tabs.add("Cliente")
    tab_itens = tabs.add("Itens")
    tabs.set("Resumo")

    x_esq = 0.05
    x_dir = 0.55
    largura = 0.4

    criarLabelEntry(tab_resumo, "Número da venda", x_esq, 0.08, largura, ctk.StringVar(value=p[0]))
    criarLabelEntry(tab_resumo, "Data de criação", x_esq, 0.3, largura, ctk.StringVar(value=p[3]))
    criarLabelEntry(tab_resumo, "Vendedor(a)", x_esq, 0.52, largura, ctk.StringVar(value=p[2]))
    criarLabelEntry(tab_resumo, "Valor", x_dir, 0.08, largura, ctk.StringVar(value=p[4]))
    criarLabelEntry(tab_resumo, "Status", x_dir, 0.3, largura, ctk.StringVar(value=self.status))
    criarLabelEntry(tab_resumo, "Data de confirmação", x_dir, 0.52, largura, ctk.StringVar(value=p[5] or ""))

    criarLabelEntry(tab_cliente, "Nome do cliente", x_esq, 0.08, largura, ctk.StringVar(value=d[0]))
    criarLabelEntry(tab_cliente, "CPF/CNPJ", x_esq, 0.3, largura, ctk.StringVar(value=d[1]))
    criarLabelEntry(tab_cliente, "Endereço", x_dir, 0.08, largura, ctk.StringVar(value=d[2]))

    itens_frame = ctk.CTkScrollableFrame(tab_itens, fg_color="transparent")
    itens_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8, anchor="nw")
    ctk.CTkLabel(itens_frame, text="Produto", anchor="w").place(relx=0.02, rely=0.02, relwidth=0.6)
    ctk.CTkLabel(itens_frame, text="Qtd", anchor="w").place(relx=0.66, rely=0.02, relwidth=0.1)
    ctk.CTkLabel(itens_frame, text="Preço", anchor="w").place(relx=0.78, rely=0.02, relwidth=0.2)

    if itens_pedido:
        for index, item in enumerate(itens_pedido):
            descricao = str(item.get("descricao", ""))
            quantidade = str(item.get("quantidade", ""))
            preco = str(item.get("preco", item.get("valor", "")))
            y = 0.14 + (index * 0.12)
            ctk.CTkLabel(itens_frame, text=descricao, anchor="w").place(relx=0.02, rely=y, relwidth=0.6)
            ctk.CTkLabel(itens_frame, text=quantidade, anchor="w").place(relx=0.66, rely=y, relwidth=0.1)
            ctk.CTkLabel(itens_frame, text=preco, anchor="w").place(relx=0.78, rely=y, relwidth=0.2)
    else:
        ctk.CTkLabel(itens_frame, text="Nenhum item informado.", anchor="w").place(relx=0.02, rely=0.14)

    frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
    frame_botoes.place(relx=0.5, rely=0.92, relwidth=0.92, relheight=0.08, anchor="center")

    criaBotao(frame_botoes, '◀️ Voltar', 0.15, 0.5, 0.2, lambda:frame.destroy())
    botaoExclui = criaBotao(
        frame_botoes,
        'Cancelar/Excluir pedido',
        0.82,
        0.5,
        0.2,
        lambda:confirmarExclusaoDoPedido.confirmarExclusaoNoPedido(self, p[0], desc, frame),
    )
    botaoExclui.configure(fg_color=self.corNegado)


    def imprimirPedido():
        itens = []
        for item in itens_pedido:
            itens.append({
                "descricao": item.get("descricao", ""),
                "quantidade": item.get("quantidade", ""),
                "preco": item.get("preco", item.get("valor", "")),
                "subtotal": item.get("subtotal", p[4]),
                "desconto_porcentagem": item.get("desconto_porcentagem", 0.0),
                "desconto_reais": item.get("desconto_reais", 0.0),
                "acrescimo": item.get("acrescimo", 0.0),
            })

        dados = {
            "vendedor": p[1],
            "frete": 0.0,

            "valor_total": p[4],
            "total_subtotal": p[4],
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
            "data_emissao": p[3],

            "subtotal": 1,
            "observacoes1": "",
            "observacoes2": ""
        }

        from funcoesTerceiras import geradorDePedido
        from telas.telaApresentadorDePdf import telaApresentarPDF

        geradorDePedido.gerar_recibo("Pedido.pdf", dados)
        telaApresentarPDF(self, "Pedido.pdf", 1)

    criaBotao(frame_botoes, 'Imprimir pedido', 0.45, 0.5, 0.2, imprimirPedido)
