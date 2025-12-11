from consultas.update import Atualiza
from consultas.insert import Insere
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tkinter import messagebox


def confirmarSalvamentoDoFaturamento(self, quantidade, valor, formaPag, data, pedido, cliente, repeticao):
    print(repeticao)

    confirmado = "Não"
    resposta = messagebox.askquestion('Aviso!', 'O faturamento será salvo referente ao pedido tal.', icon='question')
    if resposta == 'yes':
        qtdParcelas = quantidade[0].get()
        valorTotal = valor[0].get()
        formaPagamento = formaPag[0].get()
        dataFaturamento = data.get()
        descricao = f"lançamento referente ao pedido de número {pedido}, com o cliente {cliente}"

        dataBase = datetime.strptime(dataFaturamento, "%d/%m/%Y")

        valorParcela = round(float(valorTotal) / int(qtdParcelas), 2)
        total_parcelas = int(qtdParcelas)

        for i in range(total_parcelas):
            if repeticao == "Mensal":
                dataParcela = dataBase + relativedelta(months=i)
            elif repeticao == "Bimestral":
                dataParcela = dataBase + relativedelta(months=2 * i)
            elif repeticao == "Semestral":
                dataParcela = dataBase + relativedelta(months=6 * i)
            elif repeticao == "Anual":
                dataParcela = dataBase + relativedelta(years=i)

            dataFormatada = dataParcela.strftime("%Y-%m-%d")

            Insere.registraFaturamentoNoBanco(confirmado, dataFormatada, descricao, valorParcela, formaPagamento, 1)
        messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")

    else:
        pass



def confirmarSalvamentoDoFaturamentoNota(self, quantidade, valor, formaPag, data, repeticao):

    confirmado = "Não"
    qtdParcelas = quantidade[0].get()
    valorTotal = valor[0].get()
    formaPagamento = formaPag[0].get()
    numero_fatura = getattr(self, "NumeroDaFatura", None)
    emitente_nome = getattr(self, "emitente_nome", "") if hasattr(self, "emitente_nome") else ""
    try:
        dataFaturamento = data.get()
    except Exception:
        dataFaturamento = data
    try:
        dataBase = datetime.strptime(dataFaturamento, "%d/%m/%Y")

        valorParcela = round(float(valorTotal) / float(qtdParcelas), 2)
        itens_da_nota = (
            getattr(self, "itens", None)
            or getattr(self, "dadosProdutos", None)
            or getattr(self, "valoresDosItens", None)
        )
        if isinstance(itens_da_nota, dict):
            itens_da_nota = list(itens_da_nota.values())

        dados_completos = {
            "chave_nfe": getattr(self, "chave_nfe", ""),
            "serie_nfe": getattr(self, "serie_nfe", ""),
            "data_emissao": getattr(self, "data_emissao", None),
            "data_saida": getattr(self, "data_saida", None),
            "valor_total": float(valorTotal or 0),
            "emitente_cnpj": getattr(self, "emitente_cnpj", ""),
            "destinatario_cnpj": getattr(self, "destinatario_cnpj", ""),
            "destinatario_nome": getattr(self, "destinatario_nome", ""),
            "valor_produtos": getattr(self, "valor_produtos", 0),
            "valor_bc_icms": getattr(self, "valor_bc_icms", 0),
            "valor_icms": getattr(self, "valor_icms", 0),
            "valor_icms_desonerado": getattr(self, "valor_icms_desonerado", 0),
            "valor_bc_icms_st": getattr(self, "valor_bc_icms_st", 0),
            "valor_icms_st": getattr(self, "valor_icms_st", 0),
            "valor_ipi": getattr(self, "valor_ipi", 0),
            "valor_pis": getattr(self, "valor_pis", 0),
            "valor_cofins": getattr(self, "valor_cofins", 0),
            "valor_bc_irrf": getattr(self, "valor_bc_irrf", 0),
            "transportadora_cnpj": getattr(self, "transportadora_cnpj", ""),
            "transportadora_nome": getattr(self, "transportadora_nome", ""),
            "itens": itens_da_nota,
        }

        total_parcelas = int(qtdParcelas)

        for i in range(total_parcelas):
            if repeticao == "Mensal":
                dataParcela = dataBase + relativedelta(months=i)
            elif repeticao == "Bimestral":
                dataParcela = dataBase + relativedelta(months=2 * i)
            elif repeticao == "Semestral":
                dataParcela = dataBase + relativedelta(months=6 * i)
            elif repeticao == "Anual":
                dataParcela = dataBase + relativedelta(years=i)

            dataFormatada = dataParcela.strftime("%Y-%m-%d")
            numero_parcela = i + 1
            descricao = "lançamento referente a nota fiscal de entrada"
            identificador = numero_fatura.get() if numero_fatura else getattr(self, "numero_nfe", "")
            if identificador:
                descricao += f" {identificador}"

            descricao += f" - Parcela {numero_parcela}/{total_parcelas}"
            Insere.registraFaturamentoEntradaNoBanco(
                confirmado,
                dataFormatada,
                descricao,
                valorParcela,
                identificador,
                emitente_nome,
                dados_completos=dados_completos,
                numero_parcela=numero_parcela,
            )
    except Exception as exc:
        messagebox.showerror("Erro", f"Não foi possível salvar o faturamento da nota: {exc}")
