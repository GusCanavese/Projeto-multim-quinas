import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from funcoesTerceiras import confirmarAlteracoesNoPedido
from funcoesTerceiras import confirmarExclusaoDoPedido
from telas.telagerarFaturamento import telaGerarFaturamento
from componentes import criaBotao, criaFrame, criaLabel, criaLabelDescritivo, criarLabelEntry

def telaVerPedidos(self, p, d, desc):
    for i in desc:
        print(i.rsplit(' ', 1))
        print(i.rsplit(' ', 1))

    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)

    if p[4] == "Não confirmado":
        criaBotao(frame, 'Confirmar alterações',    0.38, 0.95, 0.20, lambda:confirmarAlteracoesNoPedido.confirmarAlteracoesNoPedido(self, self.dataDaVendaTelaVerPedidos.get(), p[0]))

        self.status = "Venda em aberto"
        dataDaVendaTelaVerPedidos = ''
        criarLabelEntry(frame, "Data de confirmação", 0.42, 0.08, 0.15, ctk.StringVar(value=dataDaVendaTelaVerPedidos))
        criaBotao(frame, 'Confirmar venda', 0.7, 0.12, 0.15, lambda:confirmarAlteracoesNoPedido.confirmarHoje(self, p[0]))
    else:
        self.status = "Confirmado"
        dataDaVendaTelaVerPedidos = p[4]
        criaLabelDescritivo(frame, "Data de confirmação", 0.42, 0.07, 0.15, "#38343c", ctk.StringVar(value=dataDaVendaTelaVerPedidos))
        criaLabelDescritivo(frame, 'Venda confirmada', 0.62, 0.07, 0.15, "green", None)
        






    # Primeira linha (relx espaçado em 0.2, rely em 0.05 e 0.1)
    criaLabelDescritivo(frame, "Número da venda",     0.02, 0.07, 0.15, "#38343c", ctk.StringVar(value=p[0]))
    criaLabelDescritivo(frame, "Data de criação",     0.22, 0.07, 0.15, "#38343c", ctk.StringVar(value=p[2]))
    criaLabelDescritivo(frame, "Vendedor(a)",         0.82, 0.07, 0.15, "#38343c", ctk.StringVar(value=p[1]))

    criaLabelDescritivo(frame, "Nome do cliente", 0.02, 0.25, 0.15, "#38343c", ctk.StringVar(value=d[0]))
    criaLabelDescritivo(frame, "Valor",           0.22, 0.25, 0.15, "#38343c", ctk.StringVar(value=p[3]))
    criaLabelDescritivo(frame, "CPF/CNPJ",        0.42, 0.25, 0.15, "#38343c", ctk.StringVar(value=d[1]))
    criaLabelDescritivo(frame, "Produto",         0.62, 0.25, 0.35, "#38343c", ctk.StringVar(value=desc[0]))

    criaLabelDescritivo(frame, "Endereço",        0.02, 0.43, 0.35, "#38343c", ctk.StringVar(value=d[2]))

    criaBotao(frame, 'Gerar faturamento', 0.495, 0.48, 0.15, lambda:confirmarAlteracoesNoPedido.confirmarHoje(self, p[0]))

  

    criaBotao(frame, 'Voltar',                  0.15, 0.95, 0.20, lambda:frame.destroy())
    botaoExclui = criaBotao(frame, 'Cancelar/Excluir pedido', 0.61, 0.95, 0.20, lambda:confirmarExclusaoDoPedido.confirmarExclusaoNoPedido(self, p[0], desc))
    botaoExclui.configure(fg_color="#8B0000")
