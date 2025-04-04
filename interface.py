import customtkinter as ctk
from funcoesTerceiras.geradorDePedido import gerar_recibo
import telas 
import telas.telaAcoes
import telas.telaApresentadorDePdf
import telas.telaCadastroClientes
import telas.telaCadastroFuncionario
import telas.telaCadastros
import telas.telaGerarPedido
import telas.telaLogin
import telas.telaRelatorioDeVendas
import telas.telaVerPedidos
# import random

# ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.janela()
    

    # define as propriedades da janela
    def janela(self):
        self.resizable(False, False)
        self.alturaTela = 900
        self.larguraTela = 1280
        self.geometry(f"{self.larguraTela}x{self.alturaTela}+-1500+100")
        self.telas()


    def telas(self):
        telas.telaRelatorioDeVendas.telaRelatorioDeVendas(self)
        # telas.telaGerarPedido.telaGerarPedido(self)


           

if __name__ == "__main__":
    app = App()
    app.mainloop()
