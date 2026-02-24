import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tkinter import messagebox
from consultas.update import Atualiza


def confirmarHoje(self, identificador, frame):
    resposta = messagebox.askquestion('Aviso!', 'A o pedido será confirmado com a data de hoje, deseja prosseguir?', icon='question')
    if resposta == 'yes':
        Atualiza.atualizaPedido(identificador)
        frame.destroy()


def confirmarAlteracoesNoPedido(
    self,
    identificador,
    subtotal,
    cliente,
    dados_atualizacao=None,
):
    resposta = messagebox.askquestion(
        "Confirmação",
        "Você irá alterar dados no pedido, deseja continuar?",
        icon='question'
    )
    if resposta != "yes":
        return False

    dados = dados_atualizacao or {}
    try:
        Atualiza.atualizaDadosPedido(
            identificador,
            dados.get("vendedor", ""),
            dados.get("destinatario", cliente),
            dados.get("cpf", ""),
            dados.get("endereco", ""),
            dados.get("subtotal", subtotal),
            dados.get("itens_json", "[]"),
        )
    except Exception as exc:
        messagebox.showerror("Alterações", f"Não foi possível salvar as alterações: {exc}")
        return False

    messagebox.showinfo("Alterações", "Alterações do pedido salvas com sucesso.")
    return True
