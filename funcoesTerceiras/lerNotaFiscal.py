import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from tkinter import filedialog
import xml.etree.ElementTree as ET
from telas.telaRegistraCredito import telaRegistroCredito


import xml.etree.ElementTree as ET
import json

def pegarDadosDaNota(caminhoNota):
    NAMESPACE = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

    def parse_element(element):
        if element is None:
            return None
        data = {}
        # Adiciona atributos do elemento, se houver
        if element.attrib:
            data.update(element.attrib)
        # Adiciona texto do elemento, se houver
        text = element.text.strip() if element.text else ''
        if text:
            data['#text'] = text
        # Processa elementos filhos
        for child in element:
            tag = child.tag.split('}')[-1]  # Remove namespace
            child_data = parse_element(child)
            if tag in data:
                if isinstance(data[tag], list):
                    data[tag].append(child_data)
                else:
                    data[tag] = [data[tag], child_data]
            else:
                data[tag] = child_data
        return data

    tree = ET.parse(caminhoNota)
    root = tree.getroot()
    dados = parse_element(root)
    return dados

# Exemplo de uso:
dados_nfe = pegarDadosDaNota("nota.xml")

# Exibir os dados de forma legível
print(dados_nfe["protNFe"]["infProt"]["digVal"]["#text"])




def lerNotaFiscal(self):

    try:
        self.variavel.set(filedialog.askopenfilename())

        if self.variavel.get() != "":
            dados = pegarDadosDaNota(self.variavel.get())
            buttonPegarDados = ctk.CTkButton(self.framePequeno, text="Prosseguir", command=lambda: telaRegistroCredito(self, dados))
            buttonPegarDados.place(relx=0.4, rely=0.6)
        else:
            self.variavel.set("Nenhum ficheiro selecionado")

    except:
        self.variavel.set("Arquivo escolhido não é valido")

    











