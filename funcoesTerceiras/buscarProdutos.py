import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from consultas.select import Buscas 

def buscarProdutos(self, nome, codigo, pagina=1):
    produtos = Buscas.buscaEstoqueProdutos(nome, codigo)

    # Remove dados anteriores da tabela
    if hasattr(self, "dadosTelaVerPedidos"):
        for item in self.dadosTelaVerPedidos:
            item.destroy()
    self.dadosTelaVerPedidos = []

    # Calcula o intervalo de pedidos a mostrar
    inicioProduto = (pagina - 1) * 10
    fimPedido = pagina * 10
    pedidosPagina = produtos[inicioProduto:fimPedido]

    for rowPedido, produtos in enumerate(pedidosPagina, start=1):
        corDeFundo = "#1C60A0" 
        dadosProduto = [produtos[0], produtos[1], produtos[2], produtos[3]]

        # Cria os labels com os dados do pedido
        for colNum, valor in enumerate(dadosProduto):
            print(colNum)
            if colNum == 0:
                label = ctk.CTkLabel(self.frameProdutosNoEstoque, text=valor, width=50, fg_color=corDeFundo, anchor="center")
            elif colNum ==1:
                label = ctk.CTkLabel(self.frameProdutosNoEstoque, text=valor, width=400, fg_color=corDeFundo, anchor="center")
            elif colNum ==2:
                label = ctk.CTkLabel(self.frameProdutosNoEstoque, text=valor, width=100, fg_color=corDeFundo, anchor="center")
            elif colNum ==3:
                label = ctk.CTkLabel(self.frameProdutosNoEstoque, text=valor, width=100, fg_color=corDeFundo, anchor="center")


            label.grid(row=rowPedido, column=colNum, padx=2, pady=2)
            self.dadosTelaVerPedidos.append(label)

        # Cria botão na última coluna (coluna 5)
        # def botaoVerDadosProduto(p=dadosProduto):
        #     print("Pedido selecionado:", p)
        #     telaVerPedidos(self, p)

        # botao = ctk.CTkButton(self.frameParaVendasNoRelatorio, text="Ver", width=60, command=botaoVerDadosPedido)
        # botao.grid(row=rowPedido, column=len(dadosPedido), padx=2, pady=2)
        # self.dadosTelaVerPedidos.append(botao)

    # Adiciona botões de navegação se houver mais pedidos
    # if len(pedidos) > 10:
    #     frame_navegacao = ctk.CTkFrame(self.frameParaVendasNoRelatorio)
    #     frame_navegacao.grid(row=12, column=0, columnspan=6, pady=5)
    #     self.dadosTelaVerPedidos.append(frame_navegacao)

    #     # Armazena os parâmetros em variáveis locais para usar nos callbacks
    #     params = {
    #         'vendedor': vendedor,
    #         'numero': numero,
    #         'inicio': inicio,
    #         'fim': fim,
    #         'checkbox': checkbox,
    #         'pagina': pagina
    #     }

    #     if pagina > 1:
    #         btn_anterior = ctk.CTkButton(frame_navegacao, text="← Anterior", width=100,command=lambda p=params: Buscas.buscaEstoqueProdutos(self, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']-1))
    #         btn_anterior.pack(side="left", padx=5)
    #         self.dadosTelaVerPedidos.append(btn_anterior)

    #     if fim_pedido < len(pedidos):
    #         btn_proximo = ctk.CTkButton(frame_navegacao, text="Próximo →", width=100,command=lambda p=params: filtrarPedidos(self, p['vendedor'], p['numero'], p['inicio'], p['fim'], p['checkbox'], p['pagina']+1))
    #         btn_proximo.pack(side="right", padx=5)
    #         self.dadosTelaVerPedidos.append(btn_proximo)