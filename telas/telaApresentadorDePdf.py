import customtkinter as ctk
from PIL import Image, ImageTk
import fitz
from funcoesTerceiras.imprimirPDF import imprimirPdf
from telas.telaVerPedidos import telaVerPedidos
from componentes import criaFrame, criaBotao, criarLabelEntry, criaLabel, criaEntry, criaTextArea


def telaApresentarPDF(self, caminhoPdf):
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    frameConfirmado = criaFrame(frame, 0.27, 0.15, 0.3, 0.1)
    frameConfirmado.configure(border_width=2, border_color="green", fg_color="transparent")

    criaLabel(frameConfirmado, "Pedido cadastrado com sucesso", 0.05, 0.5, 0.9, None).configure(font=("Arial", 18))
    criaLabel(frame, "Seu pedido foi cadastrado com sucesso no banco de dados! Para acessar ele, vá na aba 'Consultar pedidos' ou clique no botão abaixo",
              0.06, 0.3, 0.4, None).configure(wraplength=300, font=("Arial", 22))

    documentoPdf = fitz.open(caminhoPdf)
    self.numeroPagina = 1

    # Carrega e converte a imagem da página atual
    def carregarPagina():
        pagina = documentoPdf.load_page(self.numeroPagina - 1)
        pixmap = pagina.get_pixmap()
        imagemPdf = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        imagemPdf = imagemPdf.resize((551, 779))
        return ImageTk.PhotoImage(imagemPdf)

    imagemTk = carregarPagina()
    labelPdf = ctk.CTkLabel(frame, image=imagemTk, text="")
    labelPdf.image = imagemTk  # Impede que a imagem seja coletada pelo garbage collector
    labelPdf.place(relx=0.54, rely=0.05)

    self.textoPaginaN = criaLabel(frame, f"Página {self.numeroPagina}", 0.673, 0.975, 0.05, None)
    self.textoPaginaN.configure(font=("Arial", 16))

    def soma():
        if self.numeroPagina < documentoPdf.page_count:
            self.numeroPagina += 1
            atualizarPagina()

    def subtracao():
        if self.numeroPagina > 1:
            self.numeroPagina -= 1
            atualizarPagina()

    def atualizarPagina():
        novaImagem = carregarPagina()
        labelPdf.configure(image=novaImagem)
        labelPdf.image = novaImagem  # Atualiza a imagem corretamente
        self.textoPaginaN.configure(text=f"Página {self.numeroPagina}")

    criaBotao(frame, '→', 0.752, 0.975, 0.03, soma).configure(fg_color="#38343c")
    criaBotao(frame, '←', 0.646, 0.975, 0.03, subtracao).configure(fg_color="#38343c")

    criaBotao(frame, "Voltar", 0.15, 0.95, 0.15, lambda: frame.destroy())
    criaBotao(frame, "Imprimir", 0.35, 0.95, 0.15, lambda: imprimirPdf("Pedido.pdf"))

