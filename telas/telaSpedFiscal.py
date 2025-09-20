import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from componentes import criaFrameJanela, criaFrameJanela, criaBotao, criaLabel, criarLabelComboBox, criaComboBox, checkbox

def telaSpeedFiscal(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    opcoesMes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    opcoesAno = ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
    opcoesFinalidade = ["Remessa do arquivo original", "Remessa do arquivo substituto"]
    opcoesPerfil = ["Perfil A", "Perfil B", "Perfil C"]



    criarLabelComboBox(frame, "Selecionar período", 0.2, 0.1, 0.15, opcoesMes)
    criaComboBox(frame, 0.45, 0.14, 0.15, opcoesAno, None)
    criarLabelComboBox(frame, "Código da finalidade do arquivo", 0.2, 0.25, 0.325, opcoesFinalidade)
    criarLabelComboBox(frame, "Perfil de apresentação do arquivo fiscal", 0.2, 0.4, 0.325, opcoesPerfil)

    checkbox(frame, "Bloco 0", 0.6, 0.125, None)
    checkbox(frame, "Bloco C", 0.6, 0.175, None)
    checkbox(frame, "Bloco E", 0.6, 0.225, None)
    checkbox(frame, "Bloco D", 0.6, 0.275, None)
    checkbox(frame, "Bloco K", 0.6, 0.325, None)
    checkbox(frame, "Bloco 1", 0.6, 0.375, None)
    checkbox(frame, "Bloco 9", 0.6, 0.425, None)



    criaBotao(frame, "◀️ Voltar", 0.33, 0.80, 0.18, lambda: frame.destroy())
    criaBotao(frame, "Criar Sped", 0.66, 0.80, 0.18, lambda: criarSpeed())
