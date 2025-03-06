import customtkinter as ctk
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import io

class PDFViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer")
        self.root.geometry("800x600")
        ctk.set_appearance_mode("dark")  # Modo escuro

        # Canvas para exibir o PDF
        self.canvas = ctk.CTkCanvas(self.root, bg="#2c2c2c", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Gera um PDF dinamicamente
        self.pdf_pages = self.generate_pdf()

        # Exibe a primeira página do PDF
        self.display_page()

    def generate_pdf(self):
        """Gera um PDF simples com uma página."""
        pdf_bytes = io.BytesIO()
        document = fitz.open()  # Cria um novo documento PDF
        page = document.new_page(width=600, height=800)  # Define o tamanho da página
        page.insert_text((50, 50), "Este é um PDF gerado dinamicamente!", fontsize=30, color=(0, 0, 0))
        document.save(pdf_bytes) 
        document.close()  
        pdf_bytes.seek(0)  # Volta ao início do buffer para leitura
        return self.extract_pages(pdf_bytes)

    def extract_pages(self, pdf_bytes):
        """Extrai as páginas do PDF e as converte em imagens."""
        pdf_document = fitz.open("pdf", pdf_bytes)  # Abre o PDF a partir do buffer
        pages = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)  # Carrega a página
            pix = page.get_pixmap()  # Renderiza a página como uma imagem
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # Converte para imagem PIL
            pages.append(img)
        return pages

    def display_page(self):
        """Exibe a página atual no Canvas."""
        if self.pdf_pages:
            img = self.pdf_pages[0]  # Pega a primeira página

            # Define o tamanho desejado para o PDF no Canvas
            new_width = 600  # Largura desejada
            new_height = 800  # Altura desejada

            # Redimensiona a imagem do PDF
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(img)

            # Limpa o Canvas e exibe a imagem centralizada
            self.canvas.delete("all")
            self.canvas.create_image(
                self.canvas.winfo_width() // 2,  # Centraliza horizontalmente
                self.canvas.winfo_height() // 2,  # Centraliza verticalmente
                anchor="center",
                image=self.tk_image
            )

# Executa o aplicativo
app_root = ctk.CTk()
app = PDFViewerApp(app_root)
app_root.mainloop()