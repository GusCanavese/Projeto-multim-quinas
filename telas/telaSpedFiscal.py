import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from tkinter import messagebox
import calendar
from datetime import date
from componentes import criaFrameJanela, criaBotao, criarLabelComboBox, checkbox
from funcoesTerceiras.spedFiscalCompleto import gerar_sped_fiscal_completo

# Mantém o mesmo nome de função usado no projeto
def telaSpeedFiscal(self):
    frame = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    opcoesMes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    opcoesAno = [str(a) for a in range(2016, date.today().year + 1)]
    opcoesFinalidade = ["Remessa do arquivo original", "Remessa do arquivo substituto"]
    opcoesPerfil = ["Perfil A", "Perfil B", "Perfil C"]

    # Guarda os widgets para ler os valores “crus”
    self.cbMes         = criarLabelComboBox(frame, "Selecionar período", 0.2, 0.10, 0.15, opcoesMes)
    self.cbAno         = criarLabelComboBox(frame, "",                 0.40, 0.10, 0.15, opcoesAno)
    self.cbFinalidade  = criarLabelComboBox(frame, "Código da finalidade do arquivo", 0.2, 0.24, 0.35, opcoesFinalidade)
    self.cbPerfil      = criarLabelComboBox(frame, "Perfil de apresentação do arquivo fiscal", 0.2, 0.38, 0.35, opcoesPerfil)

    # Checkboxes com variáveis (criadas aqui para podermos ler o estado)
    self.varBloco0 = ctk.IntVar(value=1)
    self.varBlocoC = ctk.IntVar(value=1)
    self.varBlocoE = ctk.IntVar(value=1)
    self.varBlocoD = ctk.IntVar(value=0)
    self.varBlocoK = ctk.IntVar(value=0)
    self.varBloco1 = ctk.IntVar(value=1)
    self.varBloco9 = ctk.IntVar(value=1)


    checkbox(frame, "Bloco 0", 0.6, 0.125, self.varBloco0, None)
    checkbox(frame, "Bloco C", 0.6, 0.175, self.varBlocoC, None)
    checkbox(frame, "Bloco E", 0.6, 0.225, self.varBlocoE, None)
    checkbox(frame, "Bloco D", 0.6, 0.275, self.varBlocoD, None)
    checkbox(frame, "Bloco K", 0.6, 0.325, self.varBlocoK, None)
    checkbox(frame, "Bloco 1", 0.6, 0.375, self.varBloco1, None)
    checkbox(frame, "Bloco 9", 0.6, 0.425, self.varBloco9, None)

    # Defaults
    try:
        self.cbMes.set(opcoesMes[0])
        self.cbAno.set(str(date.today().year))
        self.cbFinalidade.set(opcoesFinalidade[0])
        self.cbPerfil.set(opcoesPerfil[0])
    except Exception:
        pass

    def criarSpeed():
        try:
            mes = self.cbMes.get()
            ano = int(self.cbAno.get())
            meses_map = {"Janeiro":1,"Fevereiro":2,"Março":3,"Abril":4,"Maio":5,"Junho":6, "Julho":7,"Agosto":8,"Setembro":9,"Outubro":10,"Novembro":11,"Dezembro":12}
            m = meses_map.get(mes)

            # Datas para o gerador (YYYYMMDD)
            di = f"{ano:04d}{m:02d}01"
            df = f"{ano:04d}{m:02d}{calendar.monthrange(ano, m)[1]:02d}"

            # Saída padrão em pasta SPED na raiz do projeto
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            saida_dir = os.path.join(base, "SPED")
            os.makedirs(saida_dir, exist_ok=True)
            caminho_txt = os.path.join(saida_dir, f"efd_icmsipi_{ano}_{m:02d}.txt")

            # Geração: o módulo completo já lê os dados diretamente de self (mesmo modelo do criarNFe/NFCe)
            gerar_sped_fiscal_completo(self, caminho_txt=caminho_txt, dt_ini=di, dt_fin=df)

            messagebox.showinfo("SPED Fiscal", f"Arquivo gerado com sucesso:\n{caminho_txt}")
        except Exception as e:
            messagebox.showerror("SPED Fiscal", f"Falha ao gerar SPED:\n{e}")

    criaBotao(frame, "◀️ Voltar", 0.33, 0.80, 0.18, lambda: frame.destroy())
    criaBotao(frame, "Criar Sped", 0.66, 0.80, 0.18, criarSpeed)
