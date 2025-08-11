import customtkinter as ctk
from tkinter import messagebox
from componentes import criaFrameJanela, criaBotao, criaTextArea
from funcoesTerceiras import criarNFe


def telaObservacoesNotaSaida(self):
    self.frameTelaObservacoes = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    variavelObsFisco = ctk.StringVar()
    variavelObsContribuinte = ctk.StringVar()

    area1 = criaTextArea(self.frameTelaObservacoes, 0.5, 0.15, 0.4, "INFORMAÇÕES DO INTERESSE DO CONTRIBUINTE", variavelObsContribuinte.get())
    area1.place(relheight=0.3)
    area2 = criaTextArea(self.frameTelaObservacoes, 0.05, 0.15, 0.4, "INFORMAÇÕES DO INTERESSE DO FISCO", variavelObsFisco.get())
    area2.place(relheight=0.3)


    def pegatudo():
        obs_contribuinte = area1.get("1.0", "end").strip()
        obs_fisco = area2.get("1.0", "end").strip()

        produtos = getattr(self, "valoresDosItens", [])

        totais = {}
        campos_totais = [
            "totalFrete", "totalSeguro", "totalDesconto", "outrasDespesas",
            "valorTotalProdutos", "valorServico", "totalBCICMS", "valorICMS",
            "totalBCICMSST", "totalICMSST", "totalDois", "totalIPI", "totalPIS",
            "icmsComplementar", "totalCOFINSST", "totalPISST", "totalCOFINS",
            "valorLiquido", "valorPISRetido", "valorCOFINSRetido", "valorRetidoCSLL",
            "bcIRRF", "valorRetidoIRRF", "bcPrevidencia", "valorPrevidencia"
        ]
        for campo in campos_totais:
            if hasattr(self, campo):
                totais[campo] = getattr(self, campo).get()

        print("🔵 OBSERVAÇÕES CONTRIBUINTE:", obs_contribuinte)
        print("🟣 OBSERVAÇÕES FISCO:", obs_fisco)
        print("🟠 PRODUTOS:")
        for p in produtos:
            print("   -", p)

        print("🟢 TOTAIS:")
        for k, v in totais.items():
            print(f"   {k}: {v}")


        dados_completos = {
            "obs_contribuinte": obs_contribuinte,
            "obs_fisco": obs_fisco,
            "produtos": produtos,
            "totais": totais,
            "parcelas": self.faturamento,
        }
        criarNFe.criaJsonNFe(dados_completos)

        print(dados_completos['parcelas'])
        # Exibe mensagem visual ao usuário
        messagebox.showinfo("Dados coletados", "Todos os dados foram coletados com sucesso.")


    criaBotao(self.frameTelaObservacoes, "salvar", 0.25, 0.94, 0.15, lambda: pegatudo()).place(anchor="nw")
    criaBotao(self.frameTelaObservacoes, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaObservacoes.destroy()).place(anchor="nw")
