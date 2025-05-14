
    # def verificaParcelas(self, valor):
    #     print(valor)
    #     if valor != "a vista":
    #         self.labelQtdParcelas = ctk.CTkLabel(self.frameTelaGerarOrcamento,  text="QTD parcelas", font=("Century Gothic bold", 14))
    #         self.labelQtdParcelas.place(x=250, y=235)
    #         self.QtdParcelas = ctk.CTkEntry(self.frameTelaGerarOrcamento, width=180, corner_radius=5, font=("Arial", 15))
    #         self.QtdParcelas.place(x=250, y=260)

    #     else:
    #         if hasattr(self, "QtdParcelas"):
    #             self.labelQtdParcelas.destroy()
    #             del self.labelQtdParcelas
    #             self.QtdParcelas.destroy()
    #         else:
    #             pass

    # opcoesPagamento = ["a vista", "cartão a prazo", "boleto a prazo"]
    # self.labelformaDePagamento = ctk.CTkLabel(self.frameTelaGerarOrcamento,  text="Forma de pagamento", font=("Century Gothic bold", 14))
    # self.labelformaDePagamento.place(relx=470/largura, y=235)
    # self.formaDePagamento = ctk.CTkComboBox(self.frameTelaGerarOrcamento,values=opcoesPagamento, width=180, corner_radius=5, font=("Arial", 15), command=lambda valor:verificaParcelas(self, valor))
    # self.formaDePagamento.place(relx=470/largura, y=260)