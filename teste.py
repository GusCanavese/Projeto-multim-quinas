import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Campo de Dinheiro")
        self.geometry("300x150")

        self.valor_formatado = ctk.StringVar(value="0,00")

        self.entrada = ctk.CTkEntry(self, textvariable=self.valor_formatado, font=("Arial", 20), width=150, justify="right")
        self.entrada.pack(pady=40)
        self.entrada.bind("<KeyRelease>", self.formatar_moeda)

    def formatar_moeda(self, event):
        # Permite backspace e outras teclas de controle
        if event.keysym in ("BackSpace", "Left", "Right", "Tab", "Shift_L", "Shift_R"):
            return

        texto = self.valor_formatado.get()
        texto_numerico = ''.join(filter(str.isdigit, texto))

        if not texto_numerico:
            texto_numerico = "0"

        # Garante no mínimo 3 dígitos para ter centavos
        while len(texto_numerico) < 3:
            texto_numerico = "0" + texto_numerico

        reais = texto_numerico[:-2]
        centavos = texto_numerico[-2:]

        valor = f"{int(reais)},{centavos}"
        self.valor_formatado.set(valor)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = App()
    app.mainloop()
