import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from telas.telaTotais import telaTotais
from componentes import criaFrameJanela, criaFrameJanela, criaBotao


def telaProdutosNotaSaida(self):
    self.frameTelaProdutos = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    variaveis = []
    lista = ["Produto", "Quantidade", "Valor", "Unitário", "Subtotal", "CFOP", "Em Estoque", "Totaliza Nota", "Desconto ($)", "Frete", "Seguro", "Outras"]
    posicaoX = 0.065
    posicaoY = 0.03

    for idx, cabecalho in enumerate(lista):
        if cabecalho == "Produto":
            label = ctk.CTkLabel(self.frameTelaProdutos, text=cabecalho, fg_color="#1C60A0", width=130)
            label.place(relx=posicaoX, rely=posicaoY, relwidth=0.096)
            posicaoX += 0.1
        else:
            label = ctk.CTkLabel(self.frameTelaProdutos, text=cabecalho, fg_color="#1C60A0", width=80)
            label.place(relx=posicaoX, rely=posicaoY, relwidth=0.066)
            posicaoX += 0.07

    itens = dadosNota["NFe"]["infNFe"]["det"] if isinstance(dadosNota["NFe"]["infNFe"]["det"], list) else [dadosNota["NFe"]["infNFe"]["det"]]


    totalDespesas=0.00
    for item in itens:
        posicaoX = 0.065
        posicaoY += 0.045

        nome_produto = item['prod']['xProd']['#text']
        try:
            ipi = item['imposto']['IPI']['IPITrib']['vIPI']['#text']
        except Exception:
            ipi = "0.00"
        print(f"Produto: {nome_produto} | IPI: R$ {ipi}")
        totalDespesas +=float(ipi)

        valores = {
            "Produto": item['prod']['xProd']['#text'],
            "Quantidade": f"{item['prod']['qCom']['#text']} {item['prod']['uCom']['#text']}",
            "Valor": f"R$ {float(item['prod']['vUnCom']['#text']):.2f}",
            "Unitário": f"R$ {float(item['prod']['vUnCom']['#text']):.2f}",
            "Subtotal": f"R$ {float(item['prod']['vProd']['#text']):.2f}",
            "CFOP": cfop.get(),
            "Em Estoque": "0.00",      
            "Totaliza Nota": "Sim",   
            "Desconto ($)": "0.00",    
            "Frete": "0.00",
            "Seguro": "0.00",
            "Outras": ipi          
        }
        


        for cabecalho in lista:
            if cabecalho == "Produto":
                entry = ctk.CTkEntry(self.frameTelaProdutos, corner_radius=0, width=130)
                entry.insert(0, valores.get(cabecalho, ""))
                entry.place(relx=posicaoX, rely=posicaoY, relwidth=0.096)
                posicaoX += 0.1
                variaveis.append(entry)
            else:
                entry = ctk.CTkEntry(self.frameTelaProdutos, width=80, corner_radius=0)
                entry.insert(0, valores.get(cabecalho, ""))
                entry.place(relx=posicaoX, rely=posicaoY, relwidth=0.066)
                posicaoX += 0.07
                variaveis.append(entry)





    self.dadosNotaPegar.append(itens)
            
    criaBotao(self.frameTelaProdutos, "Próximo - totais", 0.25, 0.94, 0.15, lambda: telaTotais(self, dadosNota, totalDespesas)).place(anchor="nw")
    criaBotao(self.frameTelaProdutos, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaProdutos.destroy()).place(anchor="nw")
