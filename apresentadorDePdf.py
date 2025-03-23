import customtkinter as ctk
from PIL import Image, ImageTk
import fitz 
from funcoesTerceiras.imprimirPDF import imprimirPdf

def telaApresentarPDF(self, caminhoPdf):
    # Cria o frame principal
    self.frameApresentarPedido = ctk.CTkFrame(self, height=850, width=1230, corner_radius=5)
    self.frameApresentarPedido.place(x=25, y=20)

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
    self.botaoVoltar.place(x=50, y=800)
    
    # imprime o pdf
    self.botaoImprimePedido = ctk.CTkButton(self.frameApresentarPedido, text="Imprimir", width=200, corner_radius=5, font=("Arial", 15), command= lambda:imprimirPdf("Pedido.pdf"))
    self.botaoImprimePedido.place(x=300, y=800)
