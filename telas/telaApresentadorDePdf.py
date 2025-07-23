import customtkinter as ctk
from PIL import Image, ImageTk
import fitz
from funcoesTerceiras.imprimirPDF import imprimirPdf
from componentes import criaFrameJanela,  criaFrame, criaFrameJanela, criaBotao, criarLabelEntry, criaLabel, criaEntry, criaTextArea


def telaApresentarPDF(self, caminhoPdf, condicao):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
   
    # Variável para controle de redimensionamento
    self.last_width = frame.winfo_width()
    self.last_height = frame.winfo_height()
    
    if condicao:
        documentoPdf = fitz.open(caminhoPdf)
        self.numeroPagina = 1
        self.documentoPdf = documentoPdf



        def carregarPagina(force_size=None):
            try:
                pagina = documentoPdf.load_page(self.numeroPagina - 1)
                
                # Se force_size for fornecido, usa esses valores
                if force_size:
                    largura_max, altura_max = force_size
                else:
                    # Calcula com base no tamanho atual
                    largura_max = int(frame.winfo_width() * 0.6)
                    altura_max = int(frame.winfo_height() * 0.8)
                
                proporcao_original = pagina.rect.width / pagina.rect.height
                
                if largura_max / altura_max > proporcao_original:
                    nova_altura = altura_max
                    nova_largura = int(nova_altura * proporcao_original)
                else:
                    nova_largura = largura_max
                    nova_altura = int(nova_largura / proporcao_original)
                
                pixmap = pagina.get_pixmap()
                imagemPdf = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
                imagemPdf = imagemPdf.resize((nova_largura, nova_altura), Image.LANCZOS)
                
                return ImageTk.PhotoImage(imagemPdf)
            except Exception as e:
                print(f"Erro ao carregar página: {e}")
                return None












        tamanho_inicial = (800, 1000)  # Tamanho inicial razoável
        imagemTk = carregarPagina(force_size=tamanho_inicial)
        self.labelPdf = ctk.CTkLabel(frame, image=imagemTk, text="")
        self.labelPdf.image = imagemTk
        self.labelPdf.place(relx=0.34, rely=0.05)

        self.textoPaginaN = criaLabel(frame, f"Página {self.numeroPagina}", 0.673-0.2, 0.975, 0.05, None)
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
            if novaImagem:
                self.labelPdf.configure(image=novaImagem)
                self.labelPdf.image = novaImagem
                self.textoPaginaN.configure(text=f"Página {self.numeroPagina}")

        # Botões na posição original
        criaBotao(frame, '→', 0.752-0.2, 0.975, 0.03, soma).configure(fg_color="#38343c")
        criaBotao(frame, '←', 0.646-0.2, 0.975, 0.03, subtracao).configure(fg_color="#38343c")
        criaBotao(frame, "Voltar", 0.15, 0.95, 0.15, lambda: frame.destroy())
        criaBotao(frame, "Imprimir", 0.85, 0.95, 0.15, lambda: imprimirPdf("Pedido.pdf"))

        # Função para redimensionamento
        def on_resize(event):
            # Atualiza apenas se o tamanho mudou significativamente
            if hasattr(self, 'last_width'):
                if abs(event.width - self.last_width) > 10 or abs(event.height - self.last_height) > 10:
                    atualizarPagina()
            self.last_width = event.width
            self.last_height = event.height

        frame.bind("<Configure>", on_resize)

    else:
        # Mantém o código original para o caso else
        frameConfirmado = criaFrame(frame, 0.27, 0.15, 0.3, 0.1)
        frameConfirmado.configure(border_width=2, border_color="green", fg_color="transparent")

        criaLabel(frameConfirmado, "Pedido cadastrado com sucesso", 0.05, 0.5, 0.9, None).configure(font=("Arial", 18))
        criaLabel(frame, "Seu pedido foi cadastrado com sucesso no banco de dados! Para acessar ele, vá na aba 'Consultar pedidos' ou clique no botão abaixo",
                0.06, 0.3, 0.4, None).configure(wraplength=300, font=("Arial", 22))

        documentoPdf = fitz.open(caminhoPdf)
        self.numeroPagina = 1






        def carregarPagina(force_size=None):
            try:
                pagina = documentoPdf.load_page(self.numeroPagina - 1)
                
                # Se force_size for fornecido, usa esses valores
                if force_size:
                    largura_max, altura_max = force_size
                else:
                    # Calcula com base no tamanho atual
                    largura_max = int(frame.winfo_width() * 0.6)
                    altura_max = int(frame.winfo_height() * 0.8)
                
                proporcao_original = pagina.rect.width / pagina.rect.height
                
                if largura_max / altura_max > proporcao_original:
                    nova_altura = altura_max
                    nova_largura = int(nova_altura * proporcao_original)
                else:
                    nova_largura = largura_max
                    nova_altura = int(nova_largura / proporcao_original)
                
                pixmap = pagina.get_pixmap()
                imagemPdf = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
                imagemPdf = imagemPdf.resize((nova_largura, nova_altura), Image.LANCZOS)
                
                return ImageTk.PhotoImage(imagemPdf)
            except Exception as e:
                print(f"Erro ao carregar página: {e}")
                return None


        imagemTk = carregarPagina()
        self.labelPdf = ctk.CTkLabel(frame, image=imagemTk, text="")
        self.labelPdf.image = imagemTk
        self.labelPdf.place(relx=0.54, rely=0.05)

        self.textoPaginaN = criaLabel(frame, f"Página {self.numeroPagina}", 0.673, 0.9, 0.05, None)
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
            if novaImagem:
                self.labelPdf.configure(image=novaImagem)
                self.labelPdf.image = novaImagem
                self.textoPaginaN.configure(text=f"Página {self.numeroPagina}")

        # Botões na posição original
        criaBotao(frame, '→', 0.752, 0.9, 0.03, soma).configure(fg_color="#38343c")
        criaBotao(frame, '←', 0.646, 0.9, 0.03, subtracao).configure(fg_color="#38343c")
        criaBotao(frame, "Voltar", 0.15, 0.95, 0.15, lambda: frame.destroy())
        criaBotao(frame, "Imprimir", 0.35, 0.95, 0.15, lambda: imprimirPdf("Pedido.pdf"))

        # Função para redimensionamento
        def on_resize(event):
            if not hasattr(self, 'last_width') or \
               abs(event.width - self.last_width) > 10 or \
               abs(event.height - self.last_height) > 10:
                atualizarPagina()
                self.last_width = event.width
                self.last_height = event.height

        frame.bind("<Configure>", on_resize)
        
        # FORÇA UM REDIMENSIONAMENTO APÓS A CRIAÇÃO DA JANELA
        frame.after(100, lambda: [frame.event_generate("<Configure>", width=frame.winfo_width(), height=frame.winfo_height()),atualizarPagina()])