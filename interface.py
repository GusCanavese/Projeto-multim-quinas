import customtkinter as ctk
import sys
import traceback 
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
import telas.telaNotaFiscalSaida
import telas.telaProdutoNotaSaida
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


        self.report_callback_exception = self.exibir_erro_global


    def gerar_erro(self):
        1 / 0


    def exibir_erro_global(self, exctype, value, tb):
        mensagem = f"Ocorreu um erro: {value} \n\nContate o administrador"

        if hasattr(self, "frameErro") and self.frameErro.winfo_exists():
            self.frameErro.destroy()

        self.frameErro = ctk.CTkFrame(self, height=100, width=500, corner_radius=5, border_width=2, border_color="red", fg_color="transparent")
        self.frameErro.place(relx=0.5, y=550, anchor="center")
        label = ctk.CTkLabel(self.frameErro, text=mensagem, font=("Arial", 16))
        label.place(relx=0.5, rely=0.5, anchor="center")

        traceback.print_exception(exctype, value, tb)

        self.after(5000, lambda: self.frameErro.destroy() if self.frameErro.winfo_exists() else None)



    def telas(self):

        telas.telaLogin.telaLogin(self)
        # telas.telaProdutoNotaSaida.telaProdutosNotaSaida(self)
        # telas.telaNotaFiscalSaida.telaNotaFiscalSaida(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
