import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from consultas.update import Atualiza
from consultas.select import Buscas
from componentes import criaFrameJanela, criaBotao, criarLabelEntry
from funcoesTerceiras.acbr_comandos import cancelar_nfe, inutilizar_nfe


def telaVer(self, p):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    numero_original = str(p[8])
    dados_completos = Buscas.buscaNotaFiscalCompleta(numero_original)

    def valor_campo(chave, idx=None):
        if dados_completos and chave in dados_completos:
            valor = dados_completos[chave]
            return "" if valor is None else str(valor)
        if idx is not None and idx < len(p):
            valor = p[idx]
            return "" if valor is None else str(valor)
        return ""

    status = ctk.StringVar(value=valor_campo("status", 0))
    tipo = ctk.StringVar(value=valor_campo("tipo", 1))
    op = ctk.StringVar(value=valor_campo("operacao", 2))
    destinatario = ctk.StringVar(value=valor_campo("destinatario_nome", 3))
    destinatario_documento = ctk.StringVar(value=valor_campo("destinatario_cnpjcpf"))
    destinatario_ie_var = ctk.StringVar(value=valor_campo("destinatario_ie"))
    serie = ctk.StringVar(value=valor_campo("serie", 4))
    modelo = ctk.StringVar(value=valor_campo("modelo"))
    valor_total = ctk.StringVar(value=valor_campo("valor_total", 5))
    cfop = ctk.StringVar(value=valor_campo("cfop", 6))
    data_emissao = ctk.StringVar(value=valor_campo("dhEmi", 7))
    data_vencimento = ctk.StringVar(value=valor_campo("data_vencimento"))
    numero = ctk.StringVar(value=valor_campo("numero", 8))
    chave = ctk.StringVar(value=valor_campo("chave"))
    protocolo = ctk.StringVar(value=valor_campo("protocolo"))
    recibo = ctk.StringVar(value=valor_campo("nRec"))
    qrcode_url = ctk.StringVar(value=valor_campo("qrcode_url"))
    emitente_nome = ctk.StringVar(value=valor_campo("emitente_nome"))
    emitente_documento = ctk.StringVar(value=valor_campo("emitente_cnpjcpf"))
    emitente_ie_var = ctk.StringVar(value=valor_campo("emitente_ie"))
    valor_produtos = ctk.StringVar(value=valor_campo("valor_produtos"))
    valor_desconto = ctk.StringVar(value=valor_campo("valor_desconto"))
    valor_frete = ctk.StringVar(value=valor_campo("valor_frete"))
    valor_seguro = ctk.StringVar(value=valor_campo("valor_seguro"))
    valor_outras_despesas = ctk.StringVar(value=valor_campo("valor_outras_despesas"))
    valor_bc_icms = ctk.StringVar(value=valor_campo("valor_bc_icms"))
    valor_icms = ctk.StringVar(value=valor_campo("valor_icms"))
    valor_icms_desonerado = ctk.StringVar(value=valor_campo("valor_icms_desonerado"))
    valor_bc_icms_st = ctk.StringVar(value=valor_campo("valor_bc_icms_st"))
    valor_icms_st = ctk.StringVar(value=valor_campo("valor_icms_st"))
    valor_fcp = ctk.StringVar(value=valor_campo("valor_fcp"))
    valor_ipi = ctk.StringVar(value=valor_campo("valor_ipi"))
    valor_pis = ctk.StringVar(value=valor_campo("valor_pis"))
    valor_cofins = ctk.StringVar(value=valor_campo("valor_cofins"))

    tabs = ctk.CTkTabview(frame, fg_color="transparent")
    tabs.place(relx=0.5, rely=0.45, relwidth=0.92, relheight=0.78, anchor="center")

    tab_ident = tabs.add("Identificação")
    tab_partes = tabs.add("Participantes")
    tab_totais = tabs.add("Totais")
    tabs.set("Identificação")

    x_esq = 0.05
    x_dir = 0.55
    largura = 0.4

    criarLabelEntry(tab_ident, "Status", x_esq, 0.05, largura, status)
    criarLabelEntry(tab_ident, "Tipo", x_esq, 0.15, largura, tipo)
    criarLabelEntry(tab_ident, "Operação", x_esq, 0.25, largura, op)
    criarLabelEntry(tab_ident, "Série", x_esq, 0.35, largura, serie)
    criarLabelEntry(tab_ident, "Modelo", x_esq, 0.45, largura, modelo)

    criarLabelEntry(tab_ident, "Valor total", x_dir, 0.05, largura, valor_total)
    criarLabelEntry(tab_ident, "CFOP", x_dir, 0.15, largura, cfop)
    criarLabelEntry(tab_ident, "Data de emissão", x_dir, 0.25, largura, data_emissao)
    criarLabelEntry(tab_ident, "Número", x_dir, 0.35, largura, numero)
    criarLabelEntry(tab_ident, "Data de vencimento", x_dir, 0.45, largura, data_vencimento)

    criarLabelEntry(tab_ident, "Chave de acesso", 0.05, 0.58, 0.9, chave)
    criarLabelEntry(tab_ident, "Protocolo", 0.05, 0.7, 0.43, protocolo)
    criarLabelEntry(tab_ident, "Número do recibo", 0.52, 0.7, 0.43, recibo)
    criarLabelEntry(tab_ident, "URL do QR-Code", 0.05, 0.82, 0.9, qrcode_url)

    criarLabelEntry(tab_partes, "Destinatário", 0.05, 0.08, 0.4, destinatario)
    criarLabelEntry(tab_partes, "Dest. CNPJ/CPF", 0.05, 0.25, 0.4, destinatario_documento)
    criarLabelEntry(tab_partes, "Dest. IE", 0.05, 0.42, 0.4, destinatario_ie_var)

    criarLabelEntry(tab_partes, "Emitente", 0.55, 0.08, 0.4, emitente_nome)
    criarLabelEntry(tab_partes, "Emitente CNPJ/CPF", 0.55, 0.25, 0.4, emitente_documento)
    criarLabelEntry(tab_partes, "Emitente IE", 0.55, 0.42, 0.4, emitente_ie_var)

    criarLabelEntry(tab_totais, "Valor dos produtos", x_esq, 0.05, largura, valor_produtos)
    criarLabelEntry(tab_totais, "Valor de desconto", x_esq, 0.15, largura, valor_desconto)
    criarLabelEntry(tab_totais, "Valor do frete", x_esq, 0.25, largura, valor_frete)
    criarLabelEntry(tab_totais, "Valor do seguro", x_esq, 0.35, largura, valor_seguro)
    criarLabelEntry(tab_totais, "Outras despesas", x_esq, 0.45, largura, valor_outras_despesas)
    criarLabelEntry(tab_totais, "Base ICMS", x_esq, 0.55, largura, valor_bc_icms)
    criarLabelEntry(tab_totais, "Base ICMS ST", x_esq, 0.65, largura, valor_bc_icms_st)

    criarLabelEntry(tab_totais, "Valor ICMS", x_dir, 0.05, largura, valor_icms)
    criarLabelEntry(tab_totais, "Valor ICMS ST", x_dir, 0.15, largura, valor_icms_st)
    criarLabelEntry(tab_totais, "ICMS Desonerado", x_dir, 0.25, largura, valor_icms_desonerado)
    criarLabelEntry(tab_totais, "Valor FCP", x_dir, 0.35, largura, valor_fcp)
    criarLabelEntry(tab_totais, "Valor IPI", x_dir, 0.45, largura, valor_ipi)
    criarLabelEntry(tab_totais, "Valor PIS", x_dir, 0.55, largura, valor_pis)
    criarLabelEntry(tab_totais, "Valor COFINS", x_dir, 0.65, largura, valor_cofins)

    def numero_atualizado():
        valor = (numero.get() or "").strip()
        return valor if valor else numero_original

    def obter_parametros():
        return (
            status.get(), tipo.get(), op.get(), destinatario.get(), serie.get(),
            valor_total.get(), cfop.get(), data_emissao.get(), numero_atualizado()
        )

    def gravar_dados(mostrar_msg=True, fechar=False):
        try:
            Atualiza.atualizaNotaFiscal(obter_parametros(), numero_original)
            if mostrar_msg:
                messagebox.showinfo(title="Notificação", message="Atualizado com sucesso")
            if fechar:
                frame.destroy()
            return True
        except Exception as e:
            messagebox.showinfo(title="Erro", message=f"Falha ao atualizar: {e}")
            return False

    def atualiza():
        gravar_dados(mostrar_msg=True, fechar=True)

    def solicitar_justificativa(titulo, mensagem):
        try:
            dialogo = ctk.CTkInputDialog(title=titulo, text=mensagem)
        except Exception:
            return None
        resposta = dialogo.get_input()
        return resposta.strip() if resposta else None

    def ano_para_inutilizacao():
        texto_data = (data_emissao.get() or "").strip()
        formatos = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y", "%d/%m/%Y %H:%M:%S"]
        for fmt in formatos:
            try:
                return datetime.strptime(texto_data[:len(fmt)], fmt).year
            except Exception:
                continue
        return datetime.now().year

    def somente_digitos(valor):
        return "".join(filter(str.isdigit, str(valor or "")))

    def executar_acao():
        acao = combo_acoes.get()
        numero_atual = numero.get() or numero_original
        if acao == "Cancelar NFe":
            chave_atual = (chave.get() or "").strip()
            protocolo_atual = (protocolo.get() or "").strip()
            cnpj_emitente_atual = somente_digitos(emitente_documento.get())

            if len(somente_digitos(chave_atual)) != 44:
                messagebox.showwarning("Cancelar NFe", "Chave de acesso inválida para cancelamento.")
                return
            if not protocolo_atual:
                messagebox.showwarning("Cancelar NFe", "Informe o protocolo de autorização antes de cancelar.")
                return
            if len(cnpj_emitente_atual) != 14:
                messagebox.showwarning("Cancelar NFe", "Informe o CNPJ do emitente para concluir o cancelamento.")
                return

            justificativa = solicitar_justificativa(
                "Cancelar NFe",
                "Descreva o motivo do cancelamento (mínimo 15 caracteres)."
            )
            if not justificativa:
                return

            try:
                retorno = cancelar_nfe(chave_atual, justificativa, protocolo_atual, cnpj_emitente_atual)
            except Exception as exc:
                messagebox.showerror("Cancelar NFe", f"Falha ao cancelar a nota: {exc}")
                return

            if retorno.get("sucesso"):
                status.set("Cancelada")
                gravar_dados(mostrar_msg=False)
                mensagem = retorno.get("motivo") or "Cancelamento efetuado com sucesso."
                if retorno.get("protocolo"):
                    mensagem += f"\nProtocolo: {retorno['protocolo']}"
                messagebox.showinfo("Cancelar NFe", mensagem)
            else:
                mensagem = retorno.get("motivo") or "Cancelamento rejeitado pela SEFAZ."
                messagebox.showerror("Cancelar NFe", mensagem)
        elif acao == "Inutilizar NFe":
            cnpj_emitente_atual = somente_digitos(emitente_documento.get())
            if len(cnpj_emitente_atual) != 14:
                messagebox.showwarning("Inutilizar NFe", "Informe o CNPJ do emitente para inutilizar a numeração.")
                return

            numero_inicial = somente_digitos(numero_atual)
            if not numero_inicial:
                messagebox.showwarning("Inutilizar NFe", "Número da nota inválido para inutilização.")
                return

            justificativa = solicitar_justificativa(
                "Inutilizar NFe",
                "Descreva o motivo da inutilização (mínimo 15 caracteres)."
            )
            if not justificativa:
                return

            ano_referencia = str(ano_para_inutilizacao())

            try:
                retorno = inutilizar_nfe(
                    cnpj_emitente_atual,
                    justificativa,
                    ano_referencia,
                    modelo.get() or "55",
                    serie.get() or "1",
                    numero_inicial,
                )
            except Exception as exc:
                messagebox.showerror("Inutilizar NFe", f"Falha ao inutilizar a numeração: {exc}")
                return

            if retorno.get("sucesso"):
                status.set("Inutilizada")
                gravar_dados(mostrar_msg=False)
                mensagem = retorno.get("motivo") or "Numeração inutilizada com sucesso."
                messagebox.showinfo("Inutilizar NFe", mensagem)
            else:
                mensagem = retorno.get("motivo") or "Inutilização rejeitada pela SEFAZ."
                messagebox.showerror("Inutilizar NFe", mensagem)
        elif acao == "Enviar XML":
            chave_atual = chave.get().strip()
            if not chave_atual:
                messagebox.showwarning("Enviar XML", "Nenhuma chave de acesso disponível para localizar o XML.")
                return
            caminho_logs = getattr(self, "caminhoLogsAcbr", r"C:\\ACBrMonitorPLUS\\Logs")
            xml_path = os.path.join(caminho_logs, f"{chave_atual}-nfe.xml")
            messagebox.showinfo(
                "Enviar XML",
                f"Envie o arquivo XML localizado em:\n{xml_path}"
            )
        else:
            messagebox.showwarning("Ações", "Selecione uma ação antes de continuar.")

    combo_acoes = ctk.CTkComboBox(frame, values=["Cancelar NFe", "Inutilizar NFe", "Enviar XML"])
    combo_acoes.set("Selecione uma ação")
    combo_acoes.place(relx=0.5, rely=0.8, relwidth=0.3, anchor="center")

    criaBotao(frame, "Executar ação", 0.5, 0.9, 0.18, executar_acao)
    criaBotao(frame, "💾 Salvar alterações", 0.78, 0.95, 0.25, atualiza)
    criaBotao(frame, "◀️ Voltar", 0.15, 0.95, 0.15, lambda: frame.destroy())