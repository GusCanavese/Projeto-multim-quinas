import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import confirmarAlteracoesNoPedido
from funcoesTerceiras import confirmarExclusaoDoPedido
from funcoesTerceiras.normalizarItens import normalizar_itens_pedido
from telas.telagerarFaturamento import telaGerarFaturamento
from componentes import criaFrameJanela, criaBotao, criarLabelEntry


def telaVerPedidos(self, p, d, desc, itens_pedido, pedido=None, on_refresh=None):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    itens_pedido = normalizar_itens_pedido(itens_pedido)

    numero = pedido[0] if pedido else p[0]
    data_emissao = pedido[1] if pedido else p[3]
    vendedor = pedido[2] if pedido else p[2]
    subtotal = pedido[3] if pedido else p[4]
    data_confirmacao = pedido[4] if pedido else ""
    destinatario = pedido[5] if pedido else d[0]
    cpf_cnpj = pedido[6] if pedido else d[1]
    endereco = pedido[7] if pedido else d[2]

    status_confirmado = bool(data_confirmacao) or p[5] != "Não confirmado"
    status_texto = "Venda confirmada" if status_confirmado else "Venda em aberto"

    def _atualizar_lista():
        if on_refresh:
            on_refresh()

    def _voltar():
        frame.destroy()
        _atualizar_lista()

    titulo = ctk.CTkLabel(frame, text="Venda Simples", font=("Century Gothic bold", 26))
    titulo.place(relx=0.5, rely=0.04, anchor="center")

    frame_acoes = ctk.CTkFrame(frame, fg_color="transparent")
    frame_acoes.place(relx=0.5, rely=0.11, relwidth=0.92, relheight=0.08, anchor="center")

    status_cor = "green" if status_confirmado else "#f0b24a"
    ctk.CTkLabel(
        frame_acoes,
        text=f"Status: {status_texto}",
        font=("TkDefaultFont", 16, "bold"),
        text_color=status_cor,
    ).place(relx=0.02, rely=0.5, anchor="w")

    def _confirmar_hoje():
        confirmarAlteracoesNoPedido.confirmarHoje(self, numero, frame, subtotal, destinatario)
        _atualizar_lista()

    def _confirmar_alteracoes():
        confirmarAlteracoesNoPedido.confirmarAlteracoesNoPedido(
            self,
            self.dataDaVendaTelaVerPedidos.get(),
            numero,
            frame,
            subtotal,
            destinatario,
        )
        _atualizar_lista()

    if not status_confirmado:
        criaBotao(
            frame_acoes,
            "Confirmar venda",
            0.48,
            0.5,
            0.16,
            _confirmar_hoje,
        )
        criaBotao(
            frame_acoes,
            "Confirmar alterações",
            0.66,
            0.5,
            0.18,
            _confirmar_alteracoes,
        )
        criaBotao(
            frame_acoes,
            "Gerar faturamento",
            0.86,
            0.5,
            0.18,
            lambda: telaGerarFaturamento(self, subtotal, numero, destinatario),
        )

    frame_info = ctk.CTkFrame(frame, fg_color="transparent")
    frame_info.place(relx=0.5, rely=0.26, relwidth=0.92, relheight=0.26, anchor="center")

    def _criar_entry(frame_alvo, texto, relx, rely, width, valor, desbloqueado=False):
        variavel = ctk.StringVar(value=valor)
        entry = criarLabelEntry(frame_alvo, texto, relx, rely, width, variavel)
        if not desbloqueado:
            entry.configure(state="disabled")
        return entry

    _criar_entry(frame_info, "Número", 0.02, 0.05, 0.12, numero)
    _criar_entry(frame_info, "Data da criação", 0.18, 0.05, 0.16, data_emissao)
    self.dataDaVendaTelaVerPedidos = _criar_entry(
        frame_info,
        "Data de confirmação",
        0.38,
        0.05,
        0.16,
        data_confirmacao or "",
        desbloqueado=not status_confirmado,
    )
    _criar_entry(frame_info, "Status", 0.58, 0.05, 0.16, status_texto)
    _criar_entry(frame_info, "Vendedor", 0.78, 0.05, 0.2, vendedor)

    _criar_entry(frame_info, "Nome do cliente", 0.02, 0.42, 0.36, destinatario)
    _criar_entry(frame_info, "CPF/CNPJ", 0.42, 0.42, 0.18, cpf_cnpj)
    _criar_entry(frame_info, "Endereço", 0.64, 0.42, 0.34, endereco)

    frame_itens = ctk.CTkFrame(frame, fg_color="transparent")
    frame_itens.place(relx=0.5, rely=0.62, relwidth=0.92, relheight=0.26, anchor="center")
    frame_itens.grid_columnconfigure(0, weight=3)
    frame_itens.grid_columnconfigure(1, weight=1)
    frame_itens.grid_columnconfigure(2, weight=1)
    frame_itens.grid_columnconfigure(3, weight=1)
    frame_itens.grid_columnconfigure(4, weight=1)
    frame_itens.grid_columnconfigure(5, weight=1)

    def criar_celula(texto, row, column, padx=(0, 0)):
        entry = ctk.CTkEntry(
            frame_itens,
            state="disabled",
            corner_radius=6,
            border_width=1,
        )
        entry.grid(row=row, column=column, sticky="ew", padx=padx, pady=(6, 0))
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, texto)
        entry.configure(state="disabled")
        return entry

    criar_celula("Produto/Serviço", 0, 0)
    criar_celula("Qtd", 0, 1, padx=(10, 0))
    criar_celula("Valor Unitário", 0, 2, padx=(10, 0))
    criar_celula("Desc($)", 0, 3, padx=(10, 0))
    criar_celula("Desc(%)", 0, 4, padx=(10, 0))
    criar_celula("Subtotal", 0, 5, padx=(10, 0))

    if itens_pedido:
        for index, item in enumerate(itens_pedido, start=1):
            if not isinstance(item, dict):
                continue
            descricao = str(item.get("descricao", ""))
            quantidade = str(item.get("quantidade", ""))
            preco = str(item.get("preco", item.get("valor", "")))
            desconto_reais = str(item.get("desconto_reais", 0.0))
            desconto_porcentagem = str(item.get("desconto_porcentagem", 0.0))
            subtotal_item = str(item.get("subtotal", ""))
            criar_celula(descricao, index, 0)
            criar_celula(quantidade, index, 1, padx=(10, 0))
            criar_celula(preco, index, 2, padx=(10, 0))
            criar_celula(desconto_reais, index, 3, padx=(10, 0))
            criar_celula(desconto_porcentagem, index, 4, padx=(10, 0))
            criar_celula(subtotal_item, index, 5, padx=(10, 0))
    else:
        criar_celula("Nenhum item informado.", 1, 0)

    frame_resumo = ctk.CTkFrame(frame, fg_color="transparent")
    frame_resumo.place(relx=0.5, rely=0.82, relwidth=0.92, relheight=0.1, anchor="center")

    ctk.CTkLabel(
        frame_resumo,
        text="Condição de pagamento: À vista",
        font=("TkDefaultFont", 14, "bold"),
    ).place(relx=0.02, rely=0.5, anchor="w")

    ctk.CTkLabel(
        frame_resumo,
        text=f"Total: {subtotal}",
        font=("TkDefaultFont", 18, "bold"),
    ).place(relx=0.98, rely=0.5, anchor="e")

    frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
    frame_botoes.place(relx=0.5, rely=0.92, relwidth=0.92, relheight=0.08, anchor="center")

    criaBotao(frame_botoes, "◀️ Voltar", 0.15, 0.5, 0.2, _voltar)

    def _confirmar_exclusao():
        confirmarExclusaoDoPedido.confirmarExclusaoNoPedido(self, numero, desc, frame)
        _atualizar_lista()

    botaoExclui = criaBotao(
        frame_botoes,
        "Cancelar/Excluir pedido",
        0.82,
        0.5,
        0.2,
        _confirmar_exclusao,
    )
    botaoExclui.configure(fg_color=self.corNegado)

    def imprimirPedido():
        itens = []
        for item in itens_pedido:
            itens.append({
                "descricao": item.get("descricao", ""),
                "quantidade": item.get("quantidade", ""),
                "preco": item.get("preco", item.get("valor", "")),
                "subtotal": item.get("subtotal", subtotal),
                "desconto_porcentagem": item.get("desconto_porcentagem", 0.0),
                "desconto_reais": item.get("desconto_reais", 0.0),
                "acrescimo": item.get("acrescimo", 0.0),
            })

        dados = {
            "vendedor": vendedor,
            "frete": 0.0,
            "valor_total": subtotal,
            "total_subtotal": subtotal,
            "total_acrescimo": 0.0,
            "total_desc_real": 0.0,
            "total_desc_porc": 0.0,
            "itens": itens,
            "referencia": "",
            "endereco": endereco,
            "cep": "",
            "telefone": "",
            "cnpj": cpf_cnpj,
            "cpf": cpf_cnpj,
            "destinatario": destinatario,
            "numero_recibo": numero,
            "data_emissao": data_emissao,
            "subtotal": 1,
            "observacoes1": "",
            "observacoes2": "",
        }

        from funcoesTerceiras import geradorDePedido
        from telas.telaApresentadorDePdf import telaApresentarPDF

        pdf_bytes = geradorDePedido.gerar_recibo(None, dados)
        telaApresentarPDF(self, None, 1, pdf_bytes=pdf_bytes)

    criaBotao(frame_botoes, "Imprimir pedido", 0.45, 0.5, 0.2, imprimirPedido)
