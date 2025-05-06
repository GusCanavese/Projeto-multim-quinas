import customtkinter as ctk
from PIL import Image, ImageTk
import fitz
from funcoesTerceiras.imprimirPDF import imprimirPdf
from telas.telaVerPedidos import telaVerPedidos

def telaApresentarOrcamento(self, caminhoPdf):
    # Cria o frame principal

    self.frameApresentarPedido = ctk.CTkFrame(self, height=850, width=1230, corner_radius=5)
    self.frameApresentarPedido.place(x=25, y=20)

    self.framePedidoSalvoNoBanco = ctk.CTkFrame(self.frameApresentarPedido, height=70, width=300, corner_radius=5, border_width=2, border_color="green",fg_color="transparent")
    self.framePedidoSalvoNoBanco.place(relx=0.27, y=80, anchor="center")
    self.pedidoSalvoNoBanco = ctk.CTkLabel(self.framePedidoSalvoNoBanco,  text="Pedido cadastrado com sucesso", font=("Arial", 18))
    self.pedidoSalvoNoBanco.place(x=20, y=20)

    self.textoSobnreSalvamentoNoBD = ctk.CTkLabel(self.frameApresentarPedido, wraplength=300, text="Seu pedido foi cadastrado com sucesso no banco de dados! Para acessar ele, vá na aba 'Consultar pedidos' ou clique no botão abaixo", width=100, font=("Arial", 22))
    self.textoSobnreSalvamentoNoBD.place(relx=0.27, y=220, anchor="center")
    
    documentoPdf = fitz.open(caminhoPdf)
    self.numeroPagina = 1
    
    def soma():
        if self.numeroPagina < documentoPdf.page_count:
            self.numeroPagina += 1
            self.textoPaginaN.configure(text=f"Página {self.numeroPagina}")
        pagina = documentoPdf.load_page(self.numeroPagina-1)  # Carrega a primeira página (índice 0)
        pixmap = pagina.get_pixmap()  # Converte a página em uma imagem (pixmap)
        imagemPdf = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

        imagemPdf = imagemPdf.resize((551, 779))  # Ajuste o tamanho conforme necessário
        imagemTk = ImageTk.PhotoImage(imagemPdf)

        labelPdf = ctk.CTkLabel(self.frameApresentarPedido, image=imagemTk, text="")
        labelPdf.place(x=650, y=35)

    def subtracao():
        if self.numeroPagina > 1:
            self.numeroPagina -= 1
            self.textoPaginaN.configure(text=f"Página {self.numeroPagina}")
        pagina = documentoPdf.load_page(self.numeroPagina-1)  # Carrega a primeira página (índice 0)
        pixmap = pagina.get_pixmap()  # Converte a página em uma imagem (pixmap)
        imagemPdf = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

        imagemPdf = imagemPdf.resize((551, 779))  # Ajuste o tamanho conforme necessário
        imagemTk = ImageTk.PhotoImage(imagemPdf)

        labelPdf = ctk.CTkLabel(self.frameApresentarPedido, image=imagemTk, text="")
        labelPdf.place(x=650, y=35)

    iconeDireita = ctk.CTkImage(light_image=Image.open("arquivos/direita.png"), size=(20, 20))
    iconeEsquerda = ctk.CTkImage(light_image=Image.open("arquivos/esquerda.png"), size=(20, 20))
    self.botaopagina1 = ctk.CTkButton(self.frameApresentarPedido, text="", image=iconeDireita, fg_color="#38343c", width=30, corner_radius=5 , command=soma)
    self.botaopagina1.place(x=980, y=820)
    self.textoPaginaN = ctk.CTkLabel(self.frameApresentarPedido, text=f"Página {self.numeroPagina}", width=100, font=("Arial", 16))
    self.textoPaginaN.place(x=883, y=820)
    self.botaopagina2 = ctk.CTkButton(self.frameApresentarPedido, text="", image=iconeEsquerda, fg_color="#38343c", width=30, corner_radius=5, command=subtracao)
    self.botaopagina2.place(x=850, y=820)

    
    pagina = documentoPdf.load_page(self.numeroPagina-1)
    pixmap = pagina.get_pixmap()
    imagemPdf = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

    imagemPdf = imagemPdf.resize((551, 779))
    imagemTk = ImageTk.PhotoImage(imagemPdf)

    labelPdf = ctk.CTkLabel(self.frameApresentarPedido, image=imagemTk, text="")
    labelPdf.place(x=650, y=35)

    
    def fecharPaginas():
        self.frameApresentarPedido.destroy()
        self.frameTelaGerarPedido.destroy()

    # voltar
    self.botaoVoltar = ctk.CTkButton(self.frameApresentarPedido, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=fecharPaginas)
    self.botaoVoltar.place(x=100, y=800)

    # imprime o pdf
    self.botaoImprimePedido = ctk.CTkButton(self.frameApresentarPedido, text="Imprimir", width=200, corner_radius=5, font=("Arial", 15), command= lambda:imprimirPdf("Pedido.pdf"))
    self.botaoImprimePedido.place(x=350, y=800)

    # consulta pedidos
    self.botaoConsultaPedidos = ctk.CTkButton(self.frameApresentarPedido, text="Consultar pedidos", width=200, corner_radius=5, font=("Arial", 15), command=lambda:telaVerPedidos(self))
    self.botaoConsultaPedidos.place(relx=0.27, y=350, anchor="center")
