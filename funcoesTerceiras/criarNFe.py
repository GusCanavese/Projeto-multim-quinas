def criaTXT(nome_arquivo, self):
    produtos_completos = []

    for i, prod_basico in enumerate(getattr(self, "valoresDosItens", [])):
        tributacao = {}
        # Se houver dados de tributação correspondentes
        if hasattr(self, "dadosProduto") and i < len(self.dadosProduto):
            tributacao = self.dadosProduto[i]

        # Junta os dois dicionários (básico + tributação)
        produto_final = {**prod_basico, **tributacao}
        produtos_completos.append(produto_final)

        
    dados = {
        "nota": {
            "numero": self.variavelNumeroDaNota.get(),
            "serie": self.variavelSerieDaNota.get(),
            "chave": self.variavelChaveDaNota.get(),
            "razaoSocialRemetente": self.variavelRazaoSocialRemetente.get(),
            "cnpjRazaoSocialRemetente": self.variavelCNPJRazaoSocialRemetente.get(),
            "razaoSocialEmitente": self.variavelRazaoSocialEmitente.get(),
            "cnpjRazaoSocialEmitente": self.variavelCNPJRazaoSocialEmitente.get(),
            "cfop": self.variavelCFOP.get(),
            "natureza": self.variavelNatureza.get(),
            "status": self.variavelStatus.get(),
            "dataDocumento": self.variavelDataDocumento.get(),
            "horaEntradaSaida": self.variavelHoraEntradaSaida.get(),
            "dataCriacao": self.variavelDataCriacao.get(),
            "dataConfirmacao": self.variavelDataConfirmacao.get(),
            "vendedor": self.variavelVendedor.get(),
            "entradaOuSaida": self.variavelEntradaOuSaida.get(),
            "formaDePagamento": self.formaDePagamento.get(),
            "opcoesFinalidade": self.opcoesFinalidade,  # lista
            "opcoesSituacao": self.opcoesSituacao       # lista
        },
        "produtos":produtos_completos,
        "totais": {
            "totalFrete": self.totalFrete.get(),
            "totalSeguro": self.totalSeguro.get(),
            "totalDesconto": self.totalDesconto.get(),
            "outrasDespesas": self.outrasDespesas.get(),
            "valorTotalProdutos": self.valorTotalProdutos.get(),
            "valorServico": self.valorServico.get(),
            "totalBCICMS": self.totalBCICMS.get(),
            "valorICMS": self.valorICMS.get(),
            "totalBCICMSST": self.totalBCICMSST.get(),
            "totalICMSST": self.totalICMSST.get(),
            "totalDois": self.totalDois.get(),
            "totalIPI": self.totalIPI.get(),
            "totalPIS": self.totalPIS.get(),
            "icmsComplementar": self.icmsComplementar.get(),
            "totalCOFINSST": self.totalCOFINSST.get(),
            "totalPISST": self.totalPISST.get(),
            "totalCOFINS": self.totalCOFINS.get(),
            "valorLiquido": self.valorLiquido.get(),
            "valorPISRetido": self.valorPISRetido.get(),
            "valorCOFINSRetido": self.valorCOFINSRetido.get(),
            "valorRetidoCSLL": self.valorRetidoCSLL.get(),
            "bcIRRF": self.bcIRRF.get(),
            "valorRetidoIRRF": self.valorRetidoIRRF.get(),
            "bcPrevidencia": self.bcPrevidencia.get(),
            "valorPrevidencia": self.valorPrevidencia.get()
        },
        "faturamento": {
            "totaisFormasDePagamento": self.totaisFormasDePagamento.get(),
            "descontoTotalVindoDoPedido": self.descontoTotalVindoDoPedido.get(),
            "acrescimoTotalVindoDoPedido": self.acrescimoTotalVindoDoPedido.get(),
            "variavelQuantidade": self.variavelQuantidade.get(),
            "valorDoPedidoVariavel": self.valorDoPedidoVariavel.get(),
            "variavelObsFisco": self.variavelObsFisco.get(),
            "variavelObsContribuinte": self.variavelObsContribuinte.get()
        }
    }





    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write('\n\n')
        
        for secao, campos in dados.items():
            f.write(f"[{secao}]\n")
            
            if secao == "produtos":
                # campos é uma lista de produtos
                for i, produto in enumerate(campos, start=1):
                    f.write(f"# Produto {i}\n")
                    for chave, valor in produto.items():
                        f.write(f"{chave} = {valor}\n")
                    f.write("\n")
            else:
                # demais seções são dicionários
                for chave, valor in campos.items():
                    f.write(f"{chave} = {valor}\n")
                f.write("\n")

    # # dados da nota
    # self.variavelNumeroDaNota
    # self.variavelSerieDaNota
    # self.variavelChaveDaNota
    # self.variavelRazaoSocialRemetente
    # self.variavelCNPJRazaoSocialRemetente
    # self.variavelRazaoSocialEmitente
    # self.variavelCNPJRazaoSocialEmitente
    # self.variavelCFOP
    # self.variavelNatureza
    # self.variavelStatus
    # self.variavelDataDocumento
    # self.data
    # self.variavelHoraEntradaSaida
    # self.variavelDataCriacao
    # self.variavelDataConfirmacao
    # self.variavelVendedor
    # self.variavelEntradaOuSaida
    # self.formaDePagamento
    # self.opcoesFinalidade #<--lista
    # self.opcoesSituacao #<--lista

    # # dados produto 
    # self.codigoEntry
    # self.NCMEntry
    # self.CSETEntry
    # self.quantidadeEntry
    # self.beneficioEntry
    # self.aliquEntry
    # self.credICMSEntry
    # self.bc_icms
    # self.aliq_icms
    # self.vr_icms
    # self.csosn
    # self.cst_a
    # self.cst_b
    # self.mod_bc_icms
    # self.red_bc_icms
    # self.mod_bc_icms_st
    # self.vr_bc_icms
    # self.mva_icms_st
    # self.bc_icms_st
    # self.red_bc_icms_st
    # self.vr_icms_st
    # self.vr_bc_icms_st_ret
    # self.vr_icms_st_ret
    # self.aliq_icms_cfop
    # self.bc_icms_st_dest
    # self.vr_icms_subst
    # self.aliq_icms_st
    # self.vr_icms_st_dest
    # self.bc_FCP
    # self.aliq_fcp_porc
    # self.vr_FCP
    # self.aliq_fcp_dif
    # self.bc_fcp_st
    # self.aliq_fcp_st
    # self.vr_fcp_st
    # self.vr_fcp_dif
    # self.bc_fcp_st_ret
    # self.aliq_fcp_st_ret
    # self.vr_fcp_st_ret
    # self.vr_fcp_efet
    # self.aliqIOFEntry
    # self.aliqIIEntry
    # self.BCIIEntry
    # self.VrIOFEntry
    # self.VrIIEntry
    # self.VRDespAduaneira
    # self.aliq_pis
    # self.bc_pis
    # self.vr_pis
    # self.aliq_pis_st
    # self.bc_pis_st
    # self.vr_pis_st
    # self.aliq_cofins
    # self.bc_cofins
    # self.vr_cofins
    # self.aliq_cofins_st
    # self.bc_cofins_st
    # self.vr_cofins_st

    # # dados totais
    # self.totalFrete
    # self.totalSeguro
    # self.totalDesconto
    # self.outrasDespesas
    # self.valorTotalProdutos
    # self.valorServico
    # self.totalBCICMS
    # self.valorICMS
    # self.totalBCICMSST
    # self.totalICMSST
    # self.totalDois
    # self.totalIPI
    # self.totalPIS
    # self.icmsComplementar
    # self.totalCOFINSST
    # self.totalPISST
    # self.totalCOFINS
    # self.valorLiquido
    # self.valorPISRetido
    # self.valorCOFINSRetido
    # self.valorRetidoCSLL
    # self.bcIRRF
    # self.valorRetidoIRRF
    # self.bcPrevidencia
    # self.valorPrevidencia

    # # tela faturmento
    # self.totaisFormasDePagamento
    # self.descontoTotalVindoDoPedido
    # self.acrescimoTotalVindoDoPedido
    # self.variavelQuantidade
    # self.valorDoPedidoVariavel
    # self.variavelObsFisco
    # self.variavelObsContribuinte




# dados = {
#     "infNFe": {
#         "versao": "4.00"
#     },
#     "Identificacao": {
#         "cNF": 18,
#         "natOp": "Venda",
#         "mod": 55
#     },
#     "Destinatario": {
#         "CNPJCPF": "45098699835",
#         "xNome": "Vitor Kaique de Lariva Penteado"
#     },
#     "Produto001": {
#         "cProd": 4,
#         "xProd": "Areia grossa",
#         "vProd": 540.00
#     }
# }

# # Gerar o arquivo
# criaTXT("saida.txt", dados)
# print("Arquivo 'saida.txt' gerado com sucesso!")



def gerarNFe(self):
    print("chegou no gerarNfe")
    criaTXT("base.txt", self)