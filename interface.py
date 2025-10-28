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
import telas.telaSpedFiscal
import telas.telaTransporteNotaSaida
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

        # ===== INÍCIO: abrir no segundo monitor (lado direito) e maximizar (Windows) =====
        if sys.platform == "win32":
            try:
                import ctypes
                from ctypes import WINFUNCTYPE, c_int, c_double, POINTER, c_long

                class RECT(ctypes.Structure):
                    _fields_ = [("left", c_long), ("top", c_long),
                                ("right", c_long), ("bottom", c_long)]

                monitors = []

                # callback EnumDisplayMonitors
                MonitorEnumProc = WINFUNCTYPE(c_int, c_int, c_int, POINTER(RECT), c_double)

                def _cb(hMonitor, hdcMonitor, lprcMonitor, lParam):
                    r = lprcMonitor.contents
                    # (left, top, width, height)
                    monitors.append((r.left, r.top, r.right - r.left, r.bottom - r.top))
                    return 1

                ctypes.windll.user32.EnumDisplayMonitors(
                    0, 0, MonitorEnumProc(_cb), 0
                )

                if len(monitors) >= 2:
                    # pega o monitor mais à direita (maior 'left')
                    rightmost = max(monitors, key=lambda m: m[0])
                    x, y = rightmost[0], rightmost[1]
                    # posiciona a janela no topo do monitor da direita
                    self.geometry(f"+{x}+{y}")
            except Exception:
                # se algo falhar, apenas segue e maximiza no principal
                pass

        # garante posicionamento aplicado antes de maximizar
        self.update_idletasks()
        try:
            self.state("zoomed")  # maximiza (Windows)
        except Exception:
            pass
        # ===== FIM: abrir no segundo monitor (lado direito) e maximizar (Windows) =====

        self.telas()
        self.report_callback_exception = self.exibir_erro_global

    def gerar_erro(self):
        1 / 0

    def exibir_erro_global(self, exctype, value, tb):
        mensagem = f"Ocorreu um erro: {value} \n\nContate o administrador"

        if hasattr(self, "frameErro") and self.frameErro.winfo_exists():
            self.frameErro.destroy()

        self.frameErro = ctk.CTkFrame(self, height=100, width=500, corner_radius=5,
                                      border_width=2, border_color="red", fg_color="transparent")
        self.frameErro.place(relx=0.5, y=550, anchor="center")
        label = ctk.CTkLabel(self.frameErro, text=mensagem, font=("Arial", 16))
        label.place(relx=0.5, rely=0.5, anchor="center")

        traceback.print_exception(exctype, value, tb)

        self.after(5000, lambda: self.frameErro.destroy()
                   if self.frameErro.winfo_exists() else None)

    def telas(self):

        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#242424")
        self.corFundo = "#2b2b2b"
        self.cor = "#5a3e3e"
        self.corNegado = "#922B21"
        self.corAfirma = "#196F3D"
        self.corModal = "#404040"

        telas.telaLogin.telaLogin(self)
        # telas.telaSpedFiscal.telaSpeedFiscal(self)
        # telas.telaEstoque.telaEstoque(self)
        # telas.telaProdutoNotaSaida.telaProdutosNotaSaida(self, 1)
        # telas.telaNotaFiscalSaida.telaNotaFiscalSaida(self, 0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
