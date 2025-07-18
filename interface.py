import customtkinter as ctk
import telas 
import telas.telaAcoes
import telas.telaApresentadorDePdf
import telas.telaApresentarOrcamento
import telas.telaCadastroClientes
import telas.telaCadastroFornecedor
import telas.telaCadastroFuncionario
import telas.telaCadastroProdutos
import telas.telaCadastroTransportadoras
import telas.telaCadastros
import telas.telaCalculaVendas
import telas.telaEstoque
import telas.telaGerarPedido
import telas.telaLogin
import telas.telaProdutos
import telas.telaRegistraCredito
import telas.telaRelatorioDeVendas
import telas.telaTotais
import telas.telaTransporte
import telas.telaVerPedidos
import telas.telaVercontasApagar
import telas.telagerarFaturamento
import telas.telaContasAPagarEAReceber
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
        self.geometry(f"{self.larguraTela}x{self.alturaTela}")
        self.telas()



    def telas(self):
        telas.telaLogin.telaLogin(self)
        # telas.telaRelatorioDeVendas.telaRelatorioDeVendas(self)
        # telas.telaCadastroClientes.telaCadastroClientes(self)
        






           

if __name__ == "__main__":
    app = App()
    app.mainloop()
