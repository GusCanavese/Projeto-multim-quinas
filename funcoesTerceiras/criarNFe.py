def criaTXT_ACBr(self, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        
        # ------------------- Identificacao -------------------
        f.write("[Identificacao]\n")
        f.write(f"cNF=\n")  # Código aleatório de 8 dígitos - você pode gerar se quiser
        f.write(f"natOp={self.variavelNatureza.get()}\n")
        f.write(f"indPag=0\n")
        f.write(f"mod=55\n")
        f.write(f"serie={self.variavelSerieDaNota.get()}\n")
        f.write(f"nNF={self.variavelNumeroDaNota.get()}\n")
        f.write(f"dhEmi={self.variavelDataDocumento.get()} {self.variavelHoraEntradaSaida.get()}\n")
        f.write(f"tpNF={self.variavelEntradaOuSaida.get()}\n")
        f.write(f"idDest=1\n")
        f.write(f"tpAmb=2\n")
        f.write(f"tpImp=1\n")
        f.write(f"tpEmis=1\n")
        f.write(f"finNFe=0\n")
        f.write(f"indFinal=0\n")
        f.write(f"indPres=9\n")
        f.write(f"procEmi=0\n")
        f.write(f"verProc=Sistema Python\n\n")

        # ------------------- Emitente -------------------
        f.write("[Emitente]\n")
        f.write(f"CNPJCPF={self.variavelCNPJRazaoSocialEmitente.get()}\n")
        f.write(f"xNome={self.variavelRazaoSocialEmitente.get()}\n")
        f.write(f"xFant=\n")
        f.write(f"IE=\n")
        f.write(f"xLgr=\n")
        f.write(f"nro=\n")
        f.write(f"xBairro=\n")
        f.write(f"cMun=\n")
        f.write(f"xMun=\n")
        f.write(f"UF=\n")
        f.write(f"CEP=\n")
        f.write(f"cPais=1058\n")
        f.write(f"xPais=BRASIL\n")
        f.write(f"Fone=\n\n")

        # ------------------- Destinatario -------------------
        f.write("[Destinatario]\n")
        f.write(f"CNPJCPF={self.variavelCNPJRazaoSocialRemetente.get()}\n")
        f.write(f"xNome={self.variavelRazaoSocialRemetente.get()}\n")
        f.write(f"indIEDest=3\n")
        f.write(f"IE=\n")
        f.write(f"xLgr=\n")
        f.write(f"nro=\n")
        f.write(f"xBairro=\n")
        f.write(f"cMun=\n")
        f.write(f"xMun=\n")
        f.write(f"UF=\n")
        f.write(f"CEP=\n")
        f.write(f"cPais=1058\n")
        f.write(f"xPais=BRASIL\n")
        f.write(f"Fone=\n\n")

        # ------------------- Produtos e Tributos -------------------
        produtos_completos = []
        for i, prod_basico in enumerate(getattr(self, "valoresDosItens", []), start=1):
            tributacao = {}
            if hasattr(self, "dadosProduto") and (i-1) < len(self.dadosProduto):
                tributacao = self.dadosProduto[i-1]
            produto_final = {**prod_basico, **tributacao}
            produtos_completos.append(produto_final)

            idx = str(i).zfill(3)

            # Produto
            f.write(f"[Produto{idx}]\n")
            f.write(f"cProd={produto_final.get('codigo','')}\n")
            f.write(f"xProd={produto_final.get('descricao','')}\n")
            f.write(f"NCM={produto_final.get('ncm','')}\n")
            f.write(f"CFOP={produto_final.get('cfop','')}\n")
            f.write(f"uCom={produto_final.get('unidade','')}\n")
            f.write(f"qCom={produto_final.get('quantidade','')}\n")
            f.write(f"vUnCom={produto_final.get('valor_unitario','')}\n")
            f.write(f"vProd={produto_final.get('valor_total','')}\n")
            f.write(f"indTot=1\n\n")

            # ICMS
            f.write(f"[ICMS{idx}]\n")
            f.write(f"CSOSN={produto_final.get('csosn','')}\n")
            f.write(f"orig={produto_final.get('origem','')}\n")
            f.write(f"CST={produto_final.get('cst','')}\n")
            f.write(f"vBC={produto_final.get('bc_icms','')}\n")
            f.write(f"pICMS={produto_final.get('aliq_icms','')}\n")
            f.write(f"vICMS={produto_final.get('valor_icms','')}\n\n")

            # PIS
            f.write(f"[PIS{idx}]\n")
            f.write(f"CST={produto_final.get('cst_pis','')}\n")
            f.write(f"vBC={produto_final.get('bc_pis','')}\n")
            f.write(f"pPIS={produto_final.get('aliq_pis','')}\n")
            f.write(f"vPIS={produto_final.get('valor_pis','')}\n\n")

            # COFINS
            f.write(f"[COFINS{idx}]\n")
            f.write(f"CST={produto_final.get('cst_cofins','')}\n")
            f.write(f"vBC={produto_final.get('bc_cofins','')}\n")
            f.write(f"pCOFINS={produto_final.get('aliq_cofins','')}\n")
            f.write(f"vCOFINS={produto_final.get('valor_cofins','')}\n\n")

        # ------------------- Total -------------------
        f.write("[Total]\n")
        f.write(f"vProd={self.valorTotalProdutos.get()}\n")
        f.write(f"vNF={self.valorLiquido.get()}\n")
        f.write(f"vFrete={self.totalFrete.get()}\n")
        f.write(f"vSeg={self.totalSeguro.get()}\n")
        f.write(f"vDesc={self.totalDesconto.get()}\n")
        f.write(f"vOutro={self.outrasDespesas.get()}\n")
        f.write(f"vICMS={self.valorICMS.get()}\n")
        f.write(f"vIPI={self.totalIPI.get()}\n")
        f.write(f"vPIS={self.totalPIS.get()}\n")
        f.write(f"vCOFINS={self.totalCOFINS.get()}\n\n")

def gerarNFe(self):
    print("chegou no gerarNfe")
    criaTXT_ACBr (self, "base.txt")