import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from telas.telaTotais import telaTotais


def telaProdutos(self, dadosNota):
    frame = self.frameTelaProdutosETotais = ctk.CTkFrame(self)
    frame.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.9)
    
    variaveis = []
    lista = ["Produto", "Quantidade", "Valor", "Unitário", "Subtotal", "CFOP", "Em Estoque", "Totaliza Nota", "Desconto ($)", "Frete", "Seguro", "Outras"]
    posicaoX = 0.065
    posicaoY = 0.03

    for idx, cabecalho in enumerate(lista):
        if cabecalho == "Produto":
            label = ctk.CTkLabel(frame, text=cabecalho, fg_color="#1C60A0", width=130)
            label.place(relx=posicaoX, rely=posicaoY, relwidth=0.096)
            posicaoX += 0.1
        else:
            label = ctk.CTkLabel(frame, text=cabecalho, fg_color="#1C60A0", width=80)
            label.place(relx=posicaoX, rely=posicaoY, relwidth=0.066)
            posicaoX += 0.07

    itens = dadosNota["NFe"]["infNFe"]["det"] if isinstance(dadosNota["NFe"]["infNFe"]["det"], list) else [dadosNota["NFe"]["infNFe"]["det"]]

    # Preenchimento dinâmico dos produtos
    for item in itens:
        posicaoX = 0.065
        posicaoY += 0.045
        
        valores = {
            "Produto": item['prod']['xProd']['#text'],
            "Quantidade": f"{item['prod']['qCom']['#text']} {item['prod']['uCom']['#text']}",
            "Valor": f"R$ {float(item['prod']['vUnCom']['#text']):.2f}",
            "Unitário": f"R$ {float(item['prod']['vUnCom']['#text']):.2f}",
            "Subtotal": f"R$ {float(item['prod']['vProd']['#text']):.2f}",
            "CFOP": item['prod']['CFOP']['#text'],
            "Em Estoque": "0.00",      
            "Totaliza Nota": "Sim",   
            "Desconto ($)": "0.00",    
            "Frete": "0.00",
            "Seguro": "0.00",
            "Outras": "0.00"          
        }
        
        for cabecalho in lista:
            if cabecalho == "Produto":
                entry = ctk.CTkEntry(frame, corner_radius=0, width=130)
                entry.insert(0, valores.get(cabecalho, ""))
                entry.place(relx=posicaoX, rely=posicaoY, relwidth=0.096)
                posicaoX += 0.1
                variaveis.append(entry)
                print("oi")
            else:
                entry = ctk.CTkEntry(frame, width=80, corner_radius=0)
                entry.insert(0, valores.get(cabecalho, ""))
                entry.place(relx=posicaoX, rely=posicaoY, relwidth=0.066)
                posicaoX += 0.07
                variaveis.append(entry)
            

    proximo = ctk.CTkButton(frame, text="Próximo - Totais", command=lambda:telaTotais(self, dadosNota))
    proximo.place(relx=0.25, rely=0.94, relwidth=0.15, anchor="nw")

    botaoVoltar = ctk.CTkButton(frame, text="Voltar", command=frame.destroy)
    botaoVoltar.place(relx=0.05, rely=0.94, relwidth=0.15, anchor="nw")