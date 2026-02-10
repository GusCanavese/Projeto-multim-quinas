import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from tkinter import messagebox
from funcoesTerceiras import confirmarAlteracoesNoPedido
from funcoesTerceiras import confirmarExclusaoDoPedido
from funcoesTerceiras.normalizarItens import normalizar_itens_pedido
from consultas.select import Buscas
from consultas.update import Atualiza
from telas.telagerarFaturamento import telaGerarFaturamento
from componentes import criaFrameJanela, criaBotao, criarLabelEntry


def telaVerPedidos(self, p, d, desc, itens_pedido, pedido=None, on_refresh=None):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    itens_pedido = normalizar_itens_pedido(itens_pedido)
    itens_por_pagina = 6

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

    def _parse_float(valor):
        if valor is None:
            return 0.0
        if isinstance(valor, (int, float)):
            return float(valor)
        texto = str(valor).strip()
        if not texto:
            return 0.0
        texto = texto.replace("R$", "").strip()
        if "," in texto and "." in texto:
            texto = texto.replace(".", "").replace(",", ".")
        else:
            texto = texto.replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            return 0.0

    def _atualizar_lista():
        if on_refresh:
            on_refresh()

    def _voltar():
        frame.destroy()
        _atualizar_lista()

    def _criar_campo(texto, relx, rely, width, valor, desbloqueado=False):
        variavel = ctk.StringVar(value=valor)
        entry = criarLabelEntry(frame, texto, relx, rely, width, variavel)
        if not desbloqueado:
            entry.configure(state="disabled")
        return entry

    def _abrir_observacoes(texto):
        frame_obs = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
        ctk.CTkLabel(frame_obs, text="Observações", font=("Century Gothic bold", 24)).place(
            relx=0.5, rely=0.08, anchor="center"
        )
        criarLabelEntry(
            frame_obs,
            "Observações",
            0.05,
            0.2,
            0.9,
            ctk.StringVar(value=texto),
        ).configure(state="disabled")
        criaBotao(frame_obs, "◀️ Voltar", 0.15, 0.9, 0.2, frame_obs.destroy)

    def _abrir_faturamento():
        faturamentos = Buscas.buscaFaturamentoPedido(numero)
        if not faturamentos:
            messagebox.showinfo(
                title="Faturamento",
                message="Nenhum faturamento cadastrado para este pedido.",
            )
            return

        frame_faturamento = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
        ctk.CTkLabel(
            frame_faturamento,
            text=f"Faturamento do pedido {numero}",
            font=("Century Gothic bold", 24),
        ).place(relx=0.5, rely=0.06, anchor="center")

        ctk.CTkLabel(
            frame_faturamento,
            text="Parcelas",
            font=("TkDefaultFont", 16, "bold"),
        ).place(relx=0.05, rely=0.12, anchor="w")

        lista_parcelas = ctk.CTkScrollableFrame(
            frame_faturamento,
            fg_color="transparent",
        )
        lista_parcelas.place(relx=0.05, rely=0.18, relwidth=0.9, relheight=0.64, anchor="nw")

        def _cor_status(valor_confirmado):
            return self.corAfirma if str(valor_confirmado).strip().lower() == "sim" else self.corNegado

        def _texto_status(valor_confirmado):
            return "Pago" if str(valor_confirmado).strip().lower() == "sim" else "Em aberto"

        def _toggle_confirmacao(parcela, status_label):
            confirmado, vencimento, descricao, total, forma, parcelas = parcela
            novo_status = "Não" if str(confirmado).strip().lower() == "sim" else "Sim"
            try:
                Atualiza.atualizaContaAReceber(
                    novo_status,
                    vencimento,
                    descricao,
                    total,
                    forma,
                    parcelas,
                )
            except Exception as exc:
                messagebox.showerror("Faturamento", f"Não foi possível atualizar a parcela: {exc}")
                return
            parcela[0] = novo_status
            status_label.configure(text=_texto_status(novo_status), text_color=_cor_status(novo_status))

        for indice, parcela in enumerate(faturamentos, start=1):
            parcela = list(parcela)
            confirmado, vencimento, descricao, total, forma, parcelas = parcela
            card = ctk.CTkFrame(lista_parcelas, corner_radius=10, fg_color=self.cor)
            card.pack(fill="x", pady=6, padx=6)

            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=10, pady=(8, 2))
            ctk.CTkLabel(
                header,
                text=f"Parcela {indice}",
                font=("TkDefaultFont", 14, "bold"),
            ).pack(side="left")

            status_label = ctk.CTkLabel(
                header,
                text=_texto_status(confirmado),
                text_color=_cor_status(confirmado),
                font=("TkDefaultFont", 12, "bold"),
            )
            status_label.pack(side="right")

            corpo = ctk.CTkFrame(card, fg_color="transparent")
            corpo.pack(fill="x", padx=10, pady=(0, 8))

            def _linha(campo, valor, relx, rely, largura):
                criarLabelEntry(
                    corpo,
                    campo,
                    relx,
                    rely,
                    largura,
                    ctk.StringVar(value=str(valor)),
                ).configure(state="disabled")

            _linha("Vencimento", vencimento, 0.0, 0.05, 0.22)
            _linha("Forma", forma, 0.24, 0.05, 0.18)
            _linha("Total", total, 0.44, 0.05, 0.18)
            _linha("Parcelas", parcelas, 0.64, 0.05, 0.18)
            _linha("Descrição", descricao, 0.0, 0.35, 0.82)

            botao_status = criaBotao(
                corpo,
                "Confirmar Pgt." if str(confirmado).strip().lower() != "sim" else "Desconfirmar",
                0.90,
                0.40,
                0.14,
                lambda p=parcela, lbl=status_label, btn=None: None,
            )

            def _configurar_botao(botao, parcela_ref, label_ref):
                def _acao():
                    _toggle_confirmacao(parcela_ref, label_ref)
                    botao.configure(
                        text="Confirmar Pgt."
                        if str(parcela_ref[0]).strip().lower() != "sim"
                        else "Desconfirmar"
                    )
                botao.configure(command=_acao)

            _configurar_botao(botao_status, parcela, status_label)

        criaBotao(frame_faturamento, "◀️ Voltar", 0.15, 0.9, 0.2, frame_faturamento.destroy)

    titulo = ctk.CTkLabel(frame, text="Venda Simples", font=("Century Gothic bold", 26))
    titulo.place(relx=0.5, rely=0.04, anchor="center")

    status_cor = "green" if status_confirmado else "#f0b24a"
    status_label = ctk.CTkLabel(
        frame,
        text=f"Status: {status_texto}",
        font=("TkDefaultFont", 16, "bold"),
        text_color=status_cor,
    )
    status_label.place(relx=0.04, rely=0.12, anchor="w")

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
        criaBotao(frame, "Confirmar venda", 0.48, 0.12, 0.16, _confirmar_hoje)
        criaBotao(frame, "Confirmar alterações", 0.66, 0.12, 0.18, _confirmar_alteracoes)
        criaBotao(
            frame,
            "Gerar faturamento",
            0.86,
            0.12,
            0.18,
            lambda: telaGerarFaturamento(self, subtotal, numero, destinatario),
        )
    else:
        criaBotao(frame, "Ver faturamento", 0.86, 0.12, 0.18, _abrir_faturamento)

    _criar_campo("Número", 0.04, 0.18, 0.12, numero)
    _criar_campo("Data da criação", 0.18, 0.18, 0.14, data_emissao)
    self.dataDaVendaTelaVerPedidos = _criar_campo(
        "Data de confirmação",
        0.34,
        0.18,
        0.14,
        data_confirmacao or "",
        desbloqueado=not status_confirmado,
    )
    status_entry = _criar_campo("Status", 0.50, 0.18, 0.18, status_texto)
    status_entry.configure(text_color=status_cor)
    _criar_campo("Vendedor", 0.70, 0.18, 0.26, vendedor)

    _criar_campo("Nome do cliente", 0.04, 0.30, 0.32, destinatario)
    _criar_campo("CPF/CNPJ", 0.38, 0.30, 0.18, cpf_cnpj)
    _criar_campo("Endereço", 0.58, 0.30, 0.38, endereco)

    frame_itens = ctk.CTkFrame(frame, fg_color="transparent")
    frame_itens.place(relx=0.5, rely=0.52, relwidth=0.92, relheight=0.26, anchor="center")
    ctk.CTkLabel(frame_itens, text="Itens", font=("TkDefaultFont", 14, "bold")).grid(
        row=0, column=0, columnspan=6, sticky="w", pady=(0, 6)
    )
    frame_itens.grid_columnconfigure(0, weight=4)
    frame_itens.grid_columnconfigure(1, weight=1)
    frame_itens.grid_columnconfigure(2, weight=2)
    frame_itens.grid_columnconfigure(3, weight=2)
    frame_itens.grid_columnconfigure(4, weight=2)
    frame_itens.grid_columnconfigure(5, weight=2)

    def _criar_celula(texto, row, column, padx=(0, 0)):
        entry = ctk.CTkEntry(
            frame_itens,
            state="disabled",
            corner_radius=6,
            border_width=1,
        )
        entry.grid(row=row, column=column, sticky="ew", padx=padx, pady=(4, 0))
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, texto)
        entry.configure(state="disabled")
        return entry

    _criar_celula("Produto/Serviço", 1, 0)
    _criar_celula("Qtd", 1, 1, padx=(10, 0))
    _criar_celula("Valor Unitário", 1, 2, padx=(10, 0))
    _criar_celula("Desc($)", 1, 3, padx=(10, 0))
    _criar_celula("Desc(%)", 1, 4, padx=(10, 0))
    _criar_celula("Subtotal", 1, 5, padx=(10, 0))

    itens_visiveis = itens_pedido[:itens_por_pagina]
    if itens_visiveis:
        for index, item in enumerate(itens_visiveis, start=1):
            if not isinstance(item, dict):
                continue
            descricao = str(item.get("descricao", ""))
            quantidade = str(item.get("quantidade", ""))
            preco = str(item.get("preco", item.get("valor", "")))
            desconto_reais = str(item.get("desconto_reais", 0.0))
            desconto_porcentagem = str(item.get("desconto_porcentagem", 0.0))
            subtotal_item = str(item.get("subtotal", ""))
            _criar_celula(descricao, index + 1, 0)
            _criar_celula(quantidade, index + 1, 1, padx=(10, 0))
            _criar_celula(preco, index + 1, 2, padx=(10, 0))
            _criar_celula(desconto_reais, index + 1, 3, padx=(10, 0))
            _criar_celula(desconto_porcentagem, index + 1, 4, padx=(10, 0))
            _criar_celula(subtotal_item, index + 1, 5, padx=(10, 0))
    else:
        _criar_celula("Nenhum item informado.", 2, 0)

    total_desc_reais = 0.0
    total_desc_porc = 0.0
    total_acrescimo = 0.0
    for item in itens_pedido:
        if not isinstance(item, dict):
            continue
        total_desc_reais += _parse_float(item.get("desconto_reais", 0.0))
        total_desc_porc += _parse_float(item.get("desconto_porcentagem", 0.0))
        total_acrescimo += _parse_float(item.get("acrescimo", 0.0))

    total_subtotal = _parse_float(subtotal)
    observacoes_texto = "\n".join(desc) if desc else "Sem observações."
    precisa_pagina_observacoes = len(itens_pedido) > itens_por_pagina
    if not precisa_pagina_observacoes:
        _criar_campo("Observações", 0.04, 0.68, 0.44, observacoes_texto)
    else:
        criaBotao(frame, "Ver observações", 0.04, 0.68, 0.2, lambda: _abrir_observacoes(observacoes_texto))
    _criar_campo("Desconto total($)", 0.52, 0.68, 0.18, f"{total_desc_reais:.2f}")
    _criar_campo("Desconto total(%)", 0.72, 0.68, 0.18, f"{total_desc_porc:.2f}")
    _criar_campo("Acréscimo total", 0.52, 0.78, 0.18, f"{total_acrescimo:.2f}")
    _criar_campo("TOTAL:", 0.72, 0.78, 0.18, f"{total_subtotal:.2f}")

    ctk.CTkLabel(frame,text="Condição de pagamento: À vista",font=("TkDefaultFont", 12, "bold"),).place(relx=0.04, rely=0.8, anchor="w")
    criaBotao(frame, "◀️ Voltar", 0.15, 0.88, 0.2, _voltar)

    def _confirmar_exclusao():
        confirmarExclusaoDoPedido.confirmarExclusaoNoPedido(self, numero, desc, frame)
        _atualizar_lista()

    botaoExclui = criaBotao(frame, "Cancelar/Excluir pedido", 0.82, 0.88, 0.2, _confirmar_exclusao)
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

    criaBotao(frame, "Imprimir pedido", 0.45, 0.88, 0.2, imprimirPedido)
