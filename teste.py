    def botaoTribut(self):
        frame = criaFrameJanela(frameTelaNotaProduto, 0.5, 0.5, 0.6, 0.9, self.corModal)
        
        nomeDoProduto = ctk.StringVar()
        nomeDoProduto.set()

        for widget in frameTelaNotaProduto.winfo_children():
            try:
                widget.configure(state="disabled")
            except:
                pass

        for widget in frame.winfo_children():
            try:
                widget.configure(state="normal")
            except:
                pass
        
        def destroyModal(self):
            for widget in frameTelaNotaProduto.winfo_children():
                try:
                    widget.configure(state="normal")
                except:
                    pass
            frame.destroy()

        criaEntry


        botaoFechar = ctk.CTkButton(frame, text="X", width=10, height=10, corner_radius=0, command=lambda:destroyModal(self))
        botaoFechar.place(relx=0.989, rely=0.018, anchor="center")