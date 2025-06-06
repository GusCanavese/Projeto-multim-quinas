import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Exemplo")
        self.geometry("300x150")

        ctk.CTkLabel(self, text="FABRICANTE", font=("Arial", 14)).pack(pady=(10, 0))

        # Variável de controle compartilhada
        self.fabricante_var = ctk.StringVar(value="")

        # Frame para agrupar os botões
        radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        radio_frame.pack(pady=5)

        ctk.CTkRadioButton(radio_frame, text="Sim", variable=self.fabricante_var, value="sim").pack(side="left", padx=10)
        ctk.CTkRadioButton(radio_frame, text="Não", variable=self.fabricante_var, value="nao").pack(side="left", padx=10)

        # Botão para imprimir valor selecionado
        ctk.CTkButton(self, text="Verificar", command=self.verificar).pack(pady=10)

    def verificar(self):
        print("Selecionado:", self.fabricante_var.get())

app = App()
app.mainloop()