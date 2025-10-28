import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
import customtkinter as ctk
from consultas.update import Atualiza
from funcoesTerceiras import confirmarExclusaoDoProduto, confirmarAlteracoesNoProduto
import messagebox
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criaLabelDescritivo, criaBotao, criarLabelEntry;

def telaVer(self, p):
    print(p)
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    # vars (valores dentro dos campos)
    status        = ctk.StringVar(value=(p[0]))
    tipo          = ctk.StringVar(value=(p[1]))
    op            = ctk.StringVar(value=(p[2]))
    destinatario  = ctk.StringVar(value=(p[3]))
    serie         = ctk.StringVar(value=(p[4]))
    valor_total   = ctk.StringVar(value=(p[5]))
    cfop          = ctk.StringVar(value=(p[6]))
    data_emissao  = ctk.StringVar(value=(p[7]))
    numero        = ctk.StringVar(value=(p[8]))

    # guardar o número ORIGINAL para o WHERE (mesmo que o usuário edite o campo)
    numero_original = str(p[8])

    x_esq = 0.10
    x_dir = 0.50
    y_ini = 0.07
    dy    = 0.08
    largura = 0.35

    criarLabelEntry(frame, "Status",          x_esq, y_ini + dy*0, largura, status)
    criarLabelEntry(frame, "Tipo",            x_esq, y_ini + dy*1, largura, tipo)
    criarLabelEntry(frame, "Op",              x_esq, y_ini + dy*2, largura, op)
    criarLabelEntry(frame, "Destinatário",    x_esq, y_ini + dy*3, largura, destinatario)
    criarLabelEntry(frame, "Série",           x_esq, y_ini + dy*4, largura, serie)

    criarLabelEntry(frame, "Valor total",     x_dir, y_ini + dy*0, largura, valor_total)
    criarLabelEntry(frame, "cfop",            x_dir, y_ini + dy*1, largura, cfop)
    criarLabelEntry(frame, "Data de emissão", x_dir, y_ini + dy*2, largura, data_emissao)
    criarLabelEntry(frame, "Numero",          x_dir, y_ini + dy*3, largura, numero)

    def atualiza():
        # LER os valores ATUAIS (após edição) na hora do clique
        params = (
            status.get(), tipo.get(), op.get(), destinatario.get(), serie.get(),
            valor_total.get(), cfop.get(), data_emissao.get(), numero.get()
        )
        try:
            Atualiza.atualizaNotaFiscal(params, numero_original)
            messagebox.showinfo(title="Notificação", message="Atualizado com Sucesso")
            frame.destroy()
        except Exception as e:
            messagebox.showinfo(title="Erro", message=f"Falha ao atualizar: {e}")

    criaBotao(frame, "💾 Salvar alterações", 0.42, 0.95, 0.25, lambda: atualiza())
    criaBotao(frame, "◀️ Voltar", 0.15, 0.95, 0.15, lambda: frame.destroy())