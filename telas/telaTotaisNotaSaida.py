
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from telas.telaFaturamentoEntradaNota import telaGerarFaturamentoEntradaNota
from componentes import criaFrameJanela, criarLabelLateralEntry, criaBotao
from decimal import Decimal, ROUND_HALF_UP


def telaTotaisNotaSaida(self, EhNotaDoConsumidor):
    self.frameTelaTotais = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)

    # DEBUG: listar tudo que foi salvo na tributação por produto
    def acessar(dados, *caminho, default="0.00"):
        atual = dados
        for chave in caminho:
            if isinstance(atual, dict) and chave in atual:
                atual = atual[chave]
            else:
                return default
        if isinstance(atual, dict) and "#text" in atual:
            atual = atual["#text"]
        if atual in (None, ""):
            return default
        return str(atual)

    # Variáveis individuais
    def nova_var():
        v = ctk.StringVar()
        v.set("0.00")
        return v

    def _decimal_from_var(var):
        try:
            return Decimal(str(var.get()).replace(",", "."))
        except Exception:
            return Decimal("0.00")

    def _decimal_from_number(valor):
        try:
            return Decimal(str(valor).replace(",", "."))
        except Exception:
            return Decimal("0.00")

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

    dados_nfe = getattr(self, "dadosNota", None)

    if isinstance(dados_nfe, dict):
        self.totalFrete.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vFrete", default="0.00"))
        self.totalSeguro.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vSeg", default="0.00"))
        self.totalDesconto.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vDesc", default="0.00"))
        self.outrasDespesas.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vOutro", default="0.00"))

        self.valorTotalProdutos.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vProd", default="0.00"))
        self.valorServico.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ISSQNtot", "vServ", default="0.00"))
        self.totalBCICMS.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vBC", default="0.00"))
        self.valorICMS.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vICMS", default="0.00"))
        self.totalBCICMSST.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vBCST", default="0.00"))

        self.totalICMSST.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vST", default="0.00"))
        self.totalDois.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vTotTrib", default="0.00"))
        self.totalIPI.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vIPI", default="0.00"))
        self.totalPIS.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vPIS", default="0.00"))
        self.icmsComplementar.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vICMSDeson", default="0.00"))

        self.totalCOFINSST.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vCOFINSST", default="0.00"))
        self.totalPISST.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vPISST", default="0.00"))
        self.totalCOFINS.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vCOFINS", default="0.00"))
        self.valorLiquido.set(acessar(dados_nfe, "NFe", "infNFe", "total", "ICMSTot", "vNF", default="0.00"))

        self.valorPISRetido.set(acessar(dados_nfe, "NFe", "infNFe", "total", "retTrib", "vPIS", default="0.00"))
        self.valorCOFINSRetido.set(acessar(dados_nfe, "NFe", "infNFe", "total", "retTrib", "vCOFINS", default="0.00"))
        self.valorRetidoCSLL.set(acessar(dados_nfe, "NFe", "infNFe", "total", "retTrib", "vCSLL", default="0.00"))
        self.bcIRRF.set(acessar(dados_nfe, "NFe", "infNFe", "total", "retTrib", "vBCIRRF", default="0.00"))
        self.valorRetidoIRRF.set(acessar(dados_nfe, "NFe", "infNFe", "total", "retTrib", "vIRRF", default="0.00"))
        self.bcPrevidencia.set(acessar(dados_nfe, "NFe", "infNFe", "total", "retTrib", "vBCRetPrev", default="0.00"))
        self.valorPrevidencia.set(acessar(dados_nfe, "NFe", "infNFe", "total", "retTrib", "vRetPrev", default="0.00"))

        try:
            self.valorSubtotalFaturamento = float(str(self.valorLiquido.get()).replace(',', '.'))
        except Exception:
            self.valorSubtotalFaturamento = 0.0
    else:
        # ============================
        # SOMA DOS TRIBUTOS POR ITEM
        # (preenche os totais da tela)
        # ============================
        try:
            itens = getattr(self, "dadosProdutos", {}) or {}
            print(itens)

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
                v = (it.get("bc_icms") or it.get("vBC_ICMS") or it.get("vBC") or "").strip()
                if v:
                    try:
                        tot_bc_icms += D(v)
                    except:
                        pass

                v = (it.get("vr_icms") or it.get("vICMS") or it.get("valor_icms") or "").strip()
                if v:
                    try:
                        tot_v_icms += D(v)
                    except:
                        pass

                v = (it.get("bc_icms_st") or it.get("vBCST") or it.get("vr_bc_icms_st_ret") or "").strip()
                if v:
                    try:
                        tot_bc_icms_st += D(v)
                    except:
                        pass

                v = (it.get("vr_icms_st") or it.get("vr_icms_subst") or it.get("vICMSST") or it.get("vr_icms_st_ret") or "").strip()
                if v:
                    try:
                        tot_v_icms_st += D(v)
                    except:
                        pass

                v = (it.get("vr_pis") or it.get("vPIS") or it.get("valor_pis") or "").strip()
                if v:
                    try:
                        tot_pis += D(v)
                    except:
                        pass

                v = (it.get("vr_pis_st") or it.get("vPISST") or "").strip()
                if v:
                    try:
                        tot_pis_st += D(v)
                    except:
                        pass

                v = (it.get("vr_cofins") or it.get("vCOFINS") or it.get("valor_cofins") or "").strip()
                if v:
                    try:
                        tot_cofins += D(v)
                    except:
                        pass

                v = (it.get("vr_cofins_st") or it.get("vCOFINSST") or "").strip()
                if v:
                    try:
                        tot_cofins_st += D(v)
                    except:
                        pass

                v = (it.get("vr_ipi") or it.get("vIPI") or it.get("valor_ipi") or "").strip()
                if v:
                    try:
                        tot_ipi += D(v)
                    except:
                        pass

            try:
                self.valorTotalProdutos.set(
                    f"{Decimal(str(getattr(self, 'valorSubtotalFaturamento', 0.0))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"
                )
            except Exception:
                pass

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
            print("Aviso (soma de tributos):", e)

    def atualizar_total_para_faturamento():
        base_produtos = _decimal_from_var(self.valorTotalProdutos)
        if base_produtos == Decimal("0.00") and hasattr(self, "valorSubtotalFaturamento"):
            base_produtos = _decimal_from_number(getattr(self, "valorSubtotalFaturamento", 0.0))

        frete = _decimal_from_var(self.totalFrete)
        seguro = _decimal_from_var(self.totalSeguro)
        desconto = _decimal_from_var(self.totalDesconto)
        outras_despesas = _decimal_from_var(self.outrasDespesas)
        valor_servico = _decimal_from_var(self.valorServico)

        total = base_produtos + frete + seguro + outras_despesas + valor_servico - desconto
        total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.valorLiquido.set(f"{total:.2f}")
        self.valorSubtotalFaturamento = float(total)

    def registrar_totais_importados():
        atualizar_total_para_faturamento()
        self.totaisNotaImportada = {
            "frete": self.totalFrete.get(),
            "seguro": self.totalSeguro.get(),
            "desconto": self.totalDesconto.get(),
            "outras_despesas": self.outrasDespesas.get(),
            "valor_produtos": self.valorTotalProdutos.get(),
            "valor_servico": self.valorServico.get(),
            "bc_icms": self.totalBCICMS.get(),
            "valor_icms": self.valorICMS.get(),
            "bc_icms_st": self.totalBCICMSST.get(),
            "valor_icms_st": self.totalICMSST.get(),
            "total_2": self.totalDois.get(),
            "ipi": self.totalIPI.get(),
            "pis": self.totalPIS.get(),
            "pis_st": self.totalPISST.get(),
            "cofins": self.totalCOFINS.get(),
            "cofins_st": self.totalCOFINSST.get(),
            "icms_complementar": self.icmsComplementar.get(),
            "valor_liquido": self.valorLiquido.get(),
            "pis_retido": self.valorPISRetido.get(),
            "cofins_retido": self.valorCOFINSRetido.get(),
            "csll_retido": self.valorRetidoCSLL.get(),
            "bc_irrf": self.bcIRRF.get(),
            "valor_irrf": self.valorRetidoIRRF.get(),
            "bc_previdencia": self.bcPrevidencia.get(),
            "valor_previdencia": self.valorPrevidencia.get(),
        }

    atualizar_total_para_faturamento()
    registrar_totais_importados()

    # Primeira coluna
    entradaTotalFrete = criarLabelLateralEntry(self.frameTelaTotais, "Total frete",     0.12, 0.05, 0.11, self.totalFrete)
    entradaTotalSeguro = criarLabelLateralEntry(self.frameTelaTotais, "Total Seguro",    0.12, 0.10, 0.11, self.totalSeguro)
    entradaTotalDesconto = criarLabelLateralEntry(self.frameTelaTotais, "Total Desconto",  0.12, 0.15, 0.11, self.totalDesconto)
    entradaOutrasDespesas = criarLabelLateralEntry(self.frameTelaTotais, "Outras despesas", 0.12, 0.20, 0.11, self.outrasDespesas)

    # Segunda coluna
    entradaTotalProdutos = criarLabelLateralEntry(self.frameTelaTotais, "Total Produtos",   0.35, 0.05, 0.11, self.valorTotalProdutos)
    entradaValorServico = criarLabelLateralEntry(self.frameTelaTotais, "Valor do serviço", 0.35, 0.10, 0.11, self.valorServico)
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

    for entrada in (
        entradaTotalFrete,
        entradaTotalSeguro,
        entradaTotalDesconto,
        entradaOutrasDespesas,
        entradaTotalProdutos,
        entradaValorServico,
    ):
        entrada.bind("<KeyRelease>", lambda event: atualizar_total_para_faturamento())

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

    def ir_para_faturamento():
        registrar_totais_importados()
        nota_para_faturamento = dados_nfe if isinstance(dados_nfe, dict) else None
        telaGerarFaturamentoEntradaNota(self, nota_para_faturamento, self.valorLiquido, EhNotaDoConsumidor)

    criaBotao(
        self.frameTelaTotais,
        "Próximo - Tela de faturamento",
        0.25,
        0.94,
        0.15,
        lambda: ir_para_faturamento(),
    ).place(anchor="nw")
    criaBotao(self.frameTelaTotais, "Voltar", 0.05, 0.94, 0.15, lambda: self.frameTelaTotais.destroy()).place(anchor="nw")
