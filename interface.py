import customtkinter as ctk
from funcoesTerceiras.geradorDePedido import gerar_recibo
import telas 
import telas.telaAcoes
import telas.telaApresentadorDePdf
import telas.telaApresentarOrcamento
import telas.telaCadastroClientes
import telas.telaCadastroFuncionario
import telas.telaCadastros
import telas.telaCalculaVendas
import telas.telaEstoque
import telas.telaGerarPedido
import telas.telaLogin
import telas.telaRelatorioDeVendas
import telas.telaVerPedidos
import telas.telagerarFaturamento
# import random

# ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.janela() 

        
    def janela(self):
        self.resizable(True, True)
        self.alturaTela = 900
        self.larguraTela = 1280
        # self.geometry(f"{self.larguraTela}x{self.alturaTela}+-1500+100")
        # self.geometry(f"{self.larguraTela}x{self.alturaTela}+2000+0") 
        self.geometry(f"{self.larguraTela}x{self.alturaTela}") 
        self.telas()



    def telas(self):
        # telas.telaGerarPedido.telaGerarPedido(self)
        # telas.telaApresentadorDePdf.telaApresentarPDF(self, "Pedido.pdf")
        # telas.telaApresentarOrcamento.telaApresentarOrcamento(self, "Orcamento.pdf")
        telas.telagerarFaturamento.telaGerarFaturamento(self, 50) #VALOR SOMENTE PARA TESTE
        # telas.telaLogin.telaLogin(self)



           

if __name__ == "__main__":
    app = App()
    app.mainloop()
