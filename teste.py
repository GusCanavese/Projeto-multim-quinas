import requests
import customtkinter as ctk
import db

# # Função para buscar o CEP e preencher os campos
# def buscar_cep():
#     cep = entry_cep.get()
#     url = f"https://cep.awesomeapi.com.br/json/{cep}"
    
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             dados = response.json()
            
#             # Preenchendo os campos automaticamente
#             entry_cidade.delete(0, ctk.END)
#             entry_estado.delete(0, ctk.END)
#             entry_bairro.delete(0, ctk.END)
#             entry_endereco.delete(0, ctk.END)

#             entry_cidade.insert(0, dados.get('city', ''))
#             entry_estado.insert(0, dados.get('state', ''))
#             entry_bairro.insert(0, dados.get('district', ''))
#             entry_endereco.insert(0, dados.get('address', ''))
#         else:
#             label_status.configure(text="CEP não encontrado!", text_color="red")
#     except requests.RequestException:
#         label_status.configure(text="Erro na requisição!", text_color="red")

# # Configuração da janela
# ctk.set_appearance_mode("dark")  # Modo escuro
# root = ctk.CTk()
# root.title("Busca de CEP")
# root.geometry("400x400")

# # Entrada do CEP
# ctk.CTkLabel(root, text="Digite o CEP:", font=("Arial", 14)).pack(pady=5)
# entry_cep = ctk.CTkEntry(root, width=200)
# entry_cep.pack(pady=5)

# # Botão de busca
# botao_buscar = ctk.CTkButton(root, text="Buscar", command=buscar_cep)
# botao_buscar.pack(pady=10)

# # Status de busca
# label_status = ctk.CTkLabel(root, text="", font=("Arial", 12))
# label_status.pack(pady=5)

# # Campos de preenchimento automático
# ctk.CTkLabel(root, text="Cidade:", font=("Arial", 12)).pack()
# entry_cidade = ctk.CTkEntry(root, width=250)
# entry_cidade.pack(pady=5)

# ctk.CTkLabel(root, text="Estado:", font=("Arial", 12)).pack()
# entry_estado = ctk.CTkEntry(root, width=250)
# entry_estado.pack(pady=5)

# ctk.CTkLabel(root, text="Bairro:", font=("Arial", 12)).pack()
# entry_bairro = ctk.CTkEntry(root, width=250)
# entry_bairro.pack(pady=5)

# ctk.CTkLabel(root, text="Endereço:", font=("Arial", 12)).pack()
# entry_endereco = ctk.CTkEntry(root, width=250)
# entry_endereco.pack(pady=5)

# # Iniciar loop da interface
# root.mainloop()







# Configuração do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Conectar ao MySQL


# Função para buscar produto no banco de dados
# def buscar_produto():
#     termo = entry_busca.get()
    
#     if not termo.strip():
#         resultado_label.configure(text="Digite um nome ou código!")
#         return

#     query = "SELECT id, nome FROM clientes WHERE nome LIKE %s OR id = %s"
#     db.cursor.execute(query, (f"%{termo}%", termo if termo.isdigit() else None))

#     resultados = db.cursor.fetchall()

#     if resultados:
#         texto_resultado = "\n".join([f"ID: {r[0]} | Nome: {r[1]} | Preço: R$ {r[2]:.2f}" for r in resultados])
#     else:
#         texto_resultado = "Produto não encontrado."

#     resultado_label.configure(text=texto_resultado)

# # Criar a Janela Principal
# janela = ctk.CTk()
# janela.geometry("500x400")
# janela.title("Busca de Produtos")

# # Campo de Busca
# entry_busca = ctk.CTkEntry(janela, placeholder_text="Digite um nome ou código")
# entry_busca.pack(pady=20)

# # Botão de Buscar
# botao_buscar = ctk.CTkButton(janela, text="Buscar", command=buscar_produto)
# botao_buscar.pack()

# # Label para Mostrar Resultados
# resultado_label = ctk.CTkLabel(janela, text="")
# resultado_label.pack(pady=20)

# # Rodar a aplicação
# janela.mainloop()



# import customtkinter as ctk

# class App(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title("Gerar Pedido")
#         self.geometry("1200x600")

#         self.frameTelaGerarPedido = ctk.CTkFrame(self, width=1100, height=500)
#         self.frameTelaGerarPedido.pack(pady=20)

#         self.y_atual = 300  # Posição inicial para o primeiro item
#         self.y_incremento = 40  # Espaço entre os itens

#         self.statusDoPedido = ctk.CTkButton(
#             self.frameTelaGerarPedido,
#             text="Adicionar Item",
#             width=130, height=30,
#             corner_radius=5,
#             font=("Arial", 15),
#             command=self.adicionar_item
#         )
#         self.statusDoPedido.place(x=30, y=self.y_atual + 80)  # Posicionamento inicial

#     def adicionar_item(self):
#         """Adiciona um novo item na interface e move o botão para baixo."""
#         # Criando o índice do item
#         labelNumeroItem = ctk.CTkLabel(
#             self.frameTelaGerarPedido, text=f"{(self.y_atual - 260) // self.y_incremento + 1}",
#             fg_color="#38343c", height=30, width=50, corner_radius=0
#         )
#         labelNumeroItem.place(x=30, y=self.y_atual)

#         # Campo do produto
#         entradaProdutoPesquisado = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=200, corner_radius=0)
#         entradaProdutoPesquisado.place(x=82, y=self.y_atual)

#         # Preço
#         entradaPreco = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaPreco.place(x=284, y=self.y_atual)

#         # Quantidade
#         entradaQuantidade = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaQuantidade.place(x=406, y=self.y_atual)

#         # Unidade de Medida
#         entradaUnidadeMedida = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaUnidadeMedida.place(x=528, y=self.y_atual)

#         # Desconto em Real
#         entradaDescontosReal = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaDescontosReal.place(x=650, y=self.y_atual)

#         # Desconto em Porcentagem
#         entradaDescontosPorcentagem = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaDescontosPorcentagem.place(x=772, y=self.y_atual)

#         # Acréscimo
#         entradaAcrescimo = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaAcrescimo.place(x=894, y=self.y_atual)

#         # Subtotal
#         entradaSubtotal = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaSubtotal.place(x=1016, y=self.y_atual)

#         # Atualiza a posição Y e move o botão para baixo
#         self.y_atual += self.y_incremento
#         self.statusDoPedido.place(x=30, y=self.y_atual + 40)

# # Inicializa a aplicação
# app = App()
# app.mainloop()




# import customtkinter as ctk
# import tkinter as tk  # Para o Scrollbar

# class App(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title("Gerar Pedido")
#         self.geometry("1200x600")

#         # Frame principal
#         container = ctk.CTkFrame(self, width=1100, height=500)
#         container.pack(pady=20, padx=20, fill="both", expand=True)

#         # Canvas para rolagem
#         self.canvas = tk.Canvas(container, bg="#2b2b2b", highlightthickness=0)
#         self.canvas.pack(side="left", fill="both", expand=True)

#         # Barra de rolagem
#         scrollbar = ctk.CTkScrollbar(container, command=self.canvas.yview)
#         scrollbar.pack(side="right", fill="y")
#         self.canvas.configure(yscrollcommand=scrollbar.set)

#         # Frame dentro do canvas (onde os widgets serão adicionados)
#         self.frameTelaGerarPedido = ctk.CTkFrame(self.canvas, width=1080, fg_color="transparent")
#         self.window = self.canvas.create_window((0, 0), window=self.frameTelaGerarPedido, anchor="nw")

#         # Variáveis de controle do layout
#         self.y_atual = 10  # Posição inicial para o primeiro item
#         self.y_incremento = 40  # Espaço entre os itens

#         # Botão para adicionar itens
#         self.statusDoPedido = ctk.CTkButton(
#             self.frameTelaGerarPedido,
#             text="Adicionar Item",
#             width=130, height=30,
#             corner_radius=5,
#             font=("Arial", 15),
#             command=self.adicionar_item
#         )
#         self.statusDoPedido.place(x=30, y=self.y_atual + 80)

#         # Ajustar rolagem
#         self.frameTelaGerarPedido.bind("<Configure>", self.on_frame_configure)

#     def adicionar_item(self):
#         """Adiciona um novo item e ajusta a rolagem."""
#         # Criando o índice do item
#         labelNumeroItem = ctk.CTkLabel(
#             self.frameTelaGerarPedido, text=f"{(self.y_atual - 10) // self.y_incremento + 1}",
#             fg_color="#38343c", height=30, width=50, corner_radius=0
#         )
#         labelNumeroItem.place(x=30, y=self.y_atual)

#         # Campo do produto
#         entradaProdutoPesquisado = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=200, corner_radius=0)
#         entradaProdutoPesquisado.place(x=82, y=self.y_atual)

#         # Preço
#         entradaPreco = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaPreco.place(x=284, y=self.y_atual)

#         # Quantidade
#         entradaQuantidade = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaQuantidade.place(x=406, y=self.y_atual)

#         # Unidade de Medida
#         entradaUnidadeMedida = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaUnidadeMedida.place(x=528, y=self.y_atual)

#         # Desconto em Real
#         entradaDescontosReal = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaDescontosReal.place(x=650, y=self.y_atual)

#         # Desconto em Porcentagem
#         entradaDescontosPorcentagem = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaDescontosPorcentagem.place(x=772, y=self.y_atual)

#         # Acréscimo
#         entradaAcrescimo = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaAcrescimo.place(x=894, y=self.y_atual)

#         # Subtotal
#         entradaSubtotal = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
#         entradaSubtotal.place(x=1016, y=self.y_atual)

#         # Atualiza a posição Y e move o botão para baixo
#         self.y_atual += self.y_incremento
#         self.statusDoPedido.place(x=30, y=self.y_atual + 40)

#         # Atualizar área rolável
#         self.frameTelaGerarPedido.update_idletasks()
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))

#     def on_frame_configure(self, event):
#         """Ajusta o tamanho do canvas conforme o conteúdo cresce."""
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))

# # Inicializa a aplicação
# app = App()
# app.mainloop()



import customtkinter as ctk

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x700")
        
        # Frame principal
        self.frameTelaGerarPedido = ctk.CTkFrame(self.root, width=1200, height=700)
        self.frameTelaGerarPedido.pack(fill="both", expand=True)

        self.yAtualBotao = 364
        self.yFuturoBotao = 32

        # Lista para armazenar os itens adicionados
        self.itensCriados = []

        # Botão para adicionar item
        self.botaoAdicionar = ctk.CTkButton(self.frameTelaGerarPedido, text="Adicionar Item", width=130, height=20,
                                            corner_radius=5, font=("Arial", 15), command=self.adicionarItem)
        self.botaoAdicionar.place(x=1011, y=380)

    def adicionarItem(self):
        """ Adiciona um novo item na interface """
        numero_item = len(self.itensCriados) + 1

        labelNumeroItem = ctk.CTkLabel(self.frameTelaGerarPedido, text=f"{numero_item}", fg_color="#38343c", height=30, width=50, corner_radius=0)
        labelNumeroItem.place(x=30, y=self.yAtualBotao)

        entradaProdutoPesquisado = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=200, corner_radius=0)
        entradaProdutoPesquisado.place(x=82, y=self.yAtualBotao)

        entradaPreco = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
        entradaPreco.place(x=284, y=self.yAtualBotao)

        entradaQuantidade = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
        entradaQuantidade.place(x=406, y=self.yAtualBotao)

        entradaUnidadeMedida = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
        entradaUnidadeMedida.place(x=528, y=self.yAtualBotao)

        entradaDescontosReal = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
        entradaDescontosReal.place(x=650, y=self.yAtualBotao)

        entradaDescontosPorcentagem = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
        entradaDescontosPorcentagem.place(x=772, y=self.yAtualBotao)

        entradaAcrescimo = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
        entradaAcrescimo.place(x=894, y=self.yAtualBotao)

        entradaSubtotal = ctk.CTkEntry(self.frameTelaGerarPedido, height=30, width=120, corner_radius=0)
        entradaSubtotal.place(x=1016, y=self.yAtualBotao)

        # Botão de Remover Item
        botaoRemover = ctk.CTkButton(self.frameTelaGerarPedido, text="X", width=30, height=30, fg_color="red",
                                     corner_radius=5, command=lambda: self.removerItem(numero_item - 1))
        botaoRemover.place(x=1140, y=self.yAtualBotao)

        # Adiciona os widgets na lista
        self.itensCriados.append((labelNumeroItem, entradaProdutoPesquisado, entradaPreco, entradaQuantidade,
                                  entradaUnidadeMedida, entradaDescontosReal, entradaDescontosPorcentagem,
                                  entradaAcrescimo, entradaSubtotal, botaoRemover))

        # Atualiza a posição Y e move o botão para baixo
        self.yAtualBotao += self.yFuturoBotao
        self.botaoAdicionar.place(x=1011, y=self.yAtualBotao + 40)

    def removerItem(self, index):
        """ Remove um item da interface """
        if 0 <= index < len(self.itensCriados):
            # Apaga todos os widgets do item correspondente
            for widget in self.itensCriados[index]:
                widget.destroy()

            # Remove o item da lista
            del self.itensCriados[index]

            # Atualiza os números dos itens restantes
            for i in range(index, len(self.itensCriados)):
                self.itensCriados[i][0].configure(text=str(i + 1))
            
            # Atualiza a posição Y do botão de adicionar
            self.yAtualBotao -= self.yFuturoBotao
            self.botaoAdicionar.place(x=1011, y=self.yAtualBotao + 40)

if __name__ == "__main__":
    root = ctk.CTk()
    app = Aplicacao(root)
    root.mainloop()
