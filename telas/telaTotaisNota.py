
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import datetime
from telas.telaFaturamentoEntradaNota import telaGerarFaturamentoEntradaNota
from componentes import criaFrameJanela, criarLabelLateralEntry, criaBotao
from decimal import Decimal, ROUND_HALF_UP


def telaTotaisNotaSaida(self):
    self.frameTelaTotais = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    # DEBUG: listar tudo que foi salvo na tributação por produto


    # Variáveis individuais
    def nova_var():
        v = ctk.StringVar()
        v.set("0.00")
        return v

    self.totalFrete                 = nova_var()
    self.totalSeguro                = nova_var()
    self.totalDesconto              = nova_var()
    self.outrasDespesas             = nova_var()

    self.valorTotalProdutos         = nova_var()
    self.valorServico               = nova_var()
    self.totalBCICMS                = nova_var()
    self.valorICMS                  = nova_var()
    self.totalBCICMSST              = nova_var()

    self.totalICMSST                = nova_var()
    self.totalDois                  = nova_var()
    self.totalIPI                   = nova_var()
    self.totalPIS                   = nova_var()
    self.icmsComplementar           = nova_var()

    self.totalCOFINSST              = nova_var()
    self.totalPISST                 = nova_var()
    self.totalCOFINS                = nova_var()
    self.valorLiquido               = nova_var()

    self.valorPISRetido             = nova_var()
    self.valorCOFINSRetido          = nova_var()
    self.valorRetidoCSLL            = nova_var()
    self.bcIRRF                     = nova_var()
    self.valorRetidoIRRF            = nova_var()
    self.bcPrevidencia              = nova_var()
    self.valorPrevidencia           = nova_var()



       # ============================
    # SOMA DOS TRIBUTOS POR ITEM
    # (preenche os totais da tela)
    # ============================
    try:
        itens = getattr(self, "dadosProdutos", {}) or {}

        # acumuladores locais (apenas nesta função)
        tot_bc_icms = Decimal("0.00")
        tot_v_icms = Decimal("0.00")
        tot_bc_icms_st = Decimal("0.00")
        tot_v_icms_st = Decimal("0.00")
        tot_pis = Decimal("0.00")
        tot_pis_st = Decimal("0.00")
        tot_cofins = Decimal("0.00")
        tot_cofins_st = Decimal("0.00")
        def D(x):
            try:
                return Decimal(str(x).replace(",", ".")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            except:
                return Decimal("0.00")

        tot_ipi = Decimal("0.00")

        for it in itens.values():
            # ---- BC ICMS
            v = (it.get("bc_icms") or it.get("vBC_ICMS") or it.get("vBC") or "").strip()
            if v:
                try: tot_bc_icms += D(v)
                except: pass

            # ---- ICMS
            v = (it.get("vr_icms") or it.get("vICMS") or it.get("valor_icms") or "").strip()
            if v:
                try: tot_v_icms += D(v)
                except: pass

            # ---- BC ICMS ST
            v = (it.get("bc_icms_st") or it.get("vBCST") or it.get("vr_bc_icms_st_ret") or "").strip()
            if v:
                try: tot_bc_icms_st += D(v)
                except: pass

            # ---- ICMS ST
            v = (it.get("vr_icms_st") or it.get("vr_icms_subst") or it.get("vICMSST") or it.get("vr_icms_st_ret") or "").strip()
            if v:
                try: tot_v_icms_st += D(v)
                except: pass

            # ---- PIS
            v = (it.get("vr_pis") or it.get("vPIS") or it.get("valor_pis") or "").strip()
            if v:
                try: tot_pis += D(v)
                except: pass

            # ---- PIS ST
            v = (it.get("vr_pis_st") or it.get("vPISST") or "").strip()
            if v:
                try: tot_pis_st += D(v)
                except: pass

            # ---- COFINS
            v = (it.get("vr_cofins") or it.get("vCOFINS") or it.get("valor_cofins") or "").strip()
            if v:
                try: tot_cofins += D(v)
                except: pass

            # ---- COFINS ST
            v = (it.get("vr_cofins_st") or it.get("vCOFINSST") or "").strip()
            if v:
                try: tot_cofins_st += D(v)
                except: pass

            # ---- IPI (se houver no item)
            v = (it.get("vr_ipi") or it.get("vIPI") or it.get("valor_ipi") or "").strip()
            if v:
                try: tot_ipi += D(v)
                except: pass

        # >>> AQUI EU ATRIBUO AS SOMAS AOS CAMPOS DA TELA <<<
        self.totalBCICMS.set(f"{tot_bc_icms:.2f}")
        self.valorICMS.set(f"{tot_v_icms:.2f}")
        self.totalBCICMSST.set(f"{tot_bc_icms_st:.2f}")
        self.totalICMSST.set(f"{tot_v_icms_st:.2f}")
        self.totalPIS.set(f"{tot_pis:.2f}")
        self.totalPISST.set(f"{tot_pis_st:.2f}")
        self.totalCOFINS.set(f"{tot_cofins:.2f}")
        self.totalCOFINSST.set(f"{tot_cofins_st:.2f}")
        self.totalIPI.set(f"{tot_ipi:.2f}")

    except Exception as e:
        # não quebra a tela; só loga
        print("Aviso (soma de tributos):", e)

    # Primeira coluna
    criarLabelLateralEntry(self.frameTelaTotais, "Total frete",     0.12, 0.05, 0.11, self.totalFrete)
    criarLabelLateralEntry(self.frameTelaTotais, "Total Seguro",    0.12, 0.10, 0.11, self.totalSeguro)
    criarLabelLateralEntry(self.frameTelaTotais, "Total Desconto",  0.12, 0.15, 0.11, self.totalDesconto)
    criarLabelLateralEntry(self.frameTelaTotais, "Outras despesas", 0.12, 0.20, 0.11, self.outrasDespesas)

    # Segunda coluna
    criarLabelLateralEntry(self.frameTelaTotais, "Total Produtos",   0.35, 0.05, 0.11, self.valorTotalProdutos)
    criarLabelLateralEntry(self.frameTelaTotais, "Valor do serviço", 0.35, 0.10, 0.11, self.valorServico)
    criarLabelLateralEntry(self.frameTelaTotais, "Total BC ICMS",    0.35, 0.15, 0.11, self.totalBCICMS)
    criarLabelLateralEntry(self.frameTelaTotais, "ICMS",             0.35, 0.20, 0.11, self.valorICMS)
    criarLabelLateralEntry(self.frameTelaTotais, "Total BC ICMS ST", 0.35, 0.25, 0.11, self.totalBCICMSST)

    # Terceira coluna
    criarLabelLateralEntry(self.frameTelaTotais, "Total ICMS ST", 0.6, 0.05, 0.11, self.totalICMSST)
    criarLabelLateralEntry(self.frameTelaTotais, "Total 2",       0.6, 0.10, 0.11, self.totalDois)
    criarLabelLateralEntry(self.frameTelaTotais, "Total IPI",     0.6, 0.15, 0.11, self.totalIPI)
    criarLabelLateralEntry(self.frameTelaTotais, "Total PIS",     0.6, 0.20, 0.11, self.totalPIS)
    criarLabelLateralEntry(self.frameTelaTotais, "Comple. ICMS",  0.6, 0.25, 0.11, self.icmsComplementar)

    # Quarta coluna
    criarLabelLateralEntry(self.frameTelaTotais, "Total COFINS ST",  0.85, 0.05, 0.11, self.totalCOFINSST)
    criarLabelLateralEntry(self.frameTelaTotais, "Total PIS ST",     0.85, 0.10, 0.11, self.totalPISST)
    criarLabelLateralEntry(self.frameTelaTotais, "Total COFINS",     0.85, 0.15, 0.11, self.totalCOFINS)
    criarLabelLateralEntry(self.frameTelaTotais, "Valor líquido",    0.85, 0.20, 0.11, self.valorLiquido)

    destinatario = ctk.CTkLabel(self.frameTelaTotais, text="Valores retidos-----------------------------------------------------------------------------")
    destinatario.place(relx=0.02, rely=0.45)

    # Retenções
    criarLabelLateralEntry(self.frameTelaTotais, "Valor PIS retido",       0.22, 0.50, 0.11, self.valorPISRetido)
    criarLabelLateralEntry(self.frameTelaTotais, "Valor do COFINS Retido", 0.22, 0.55, 0.11, self.valorCOFINSRetido)
    criarLabelLateralEntry(self.frameTelaTotais, "Valores Retido CSLL",    0.22, 0.60, 0.11, self.valorRetidoCSLL)
    criarLabelLateralEntry(self.frameTelaTotais, "BC do IRRF",             0.22, 0.65, 0.11, self.bcIRRF)
    
    criarLabelLateralEntry(self.frameTelaTotais, "Valor Retido IRRF",        0.48, 0.50, 0.11, self.valorRetidoIRRF)
    criarLabelLateralEntry(self.frameTelaTotais, "BC da Previdência Social", 0.48, 0.55, 0.11, self.bcPrevidencia)
    criarLabelLateralEntry(self.frameTelaTotais, "VR Previdência Social",    0.48, 0.60, 0.11, self.valorPrevidencia)

    criaBotao(self.frameTelaTotais, "Próximo - Tela de faturamento", 0.25, 0.94, 0.15, lambda: telaGerarFaturamentoEntradaNota(self, None, 0)).place(anchor="nw")
    criaBotao(self.frameTelaTotais, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaTotais.destroy()).place(anchor="nw")
