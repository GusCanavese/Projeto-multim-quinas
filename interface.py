import customtkinter as ctk
import telas 
import funcoesTerceiras.escolherNotaFiscal
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
        self.configure(fg_color="#242424")
        self.corFundo = "#2b2b2b"
        self.cor = "#5a3e3e"
        self.corNegado = "#922B21"
        self.corAfirma = "#196F3D"
        self.corModal = "#404040"
        # telas.telaLogin.telaLogin(self)
        funcoesTerceiras.escolherNotaFiscal.escolherNotaFiscal(self)
        # telas.telaRelatorioDeVendas.telaRelatorioDeVendas(self)
        # telas.telaApresentadorDePdf.telaApresentarPDF(self, "Pedido.pdf", True)
        # telas.telaRelatorioDeVendas.telaRelatorioDeVendas(self)
        # telas.telaCadastroClientes.telaCadastroClientes(self)
        






           

if __name__ == "__main__":
    app = App()
    app.mainloop()
