import customtkinter as ctk
from PIL import Image, ImageTk
import fitz 
from funcoesTerceiras.imprimirPDF import imprimirPdf

def telaApresentarPDF(self, caminhoPdf):
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
    pagina = documentoPdf.load_page(0)  # Carrega a primeira página (índice 0)
    pixmap = pagina.get_pixmap()  # Converte a página em uma imagem (pixmap)
    imagemPdf = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

    imagemPdf = imagemPdf.resize((551, 779))  # Ajuste o tamanho conforme necessário
    imagemTk = ImageTk.PhotoImage(imagemPdf)

    labelPdf = ctk.CTkLabel(self.frameApresentarPedido, image=imagemTk, text="")
    labelPdf.image = imagemTk  # Mantém uma referência para evitar garbage collection
    labelPdf.place(x=650, y=35)

    # voltar
    self.botaoVoltar = ctk.CTkButton(self.frameApresentarPedido, text="Voltar", width=200, corner_radius=5, font=("Arial", 15), command=self.frameApresentarPedido.destroy)
    self.botaoVoltar.place(x=100, y=800)
    
    # imprime o pdf
    self.botaoImprimePedido = ctk.CTkButton(self.frameApresentarPedido, text="Imprimir", width=200, corner_radius=5, font=("Arial", 15), command= lambda:imprimirPdf("Pedido.pdf"))
    self.botaoImprimePedido.place(x=350, y=800)

    # consulta pedidos
    self.botaoConsultaPedidos = ctk.CTkButton(self.frameApresentarPedido, text="Consultar pedidos", width=200, corner_radius=5, font=("Arial", 15), command= lambda:self)
    self.botaoConsultaPedidos.place(relx=0.27, y=350, anchor="center")