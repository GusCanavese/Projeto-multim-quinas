import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import db
import json
from tkinter import messagebox
import re
import unicodedata
from datetime import datetime



class Insere:


    def insereTransportadoraNoBanco(dados):
        colunas = list(dados.keys())
        valores = [f"'{str(valor)}'" for valor in dados.values()]
        query = f"INSERT INTO transportadoras ({', '.join(colunas)}) VALUES ({', '.join(valores)})"
        db.cursor.execute(query)
        db.conn.commit()



    def insereProdutosNoBanco(nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ, marca):
        queryInserirProdutos = "INSERT INTO produtos(nome_do_produto, valor_de_custo, valor_de_venda, quantidade, codigo_interno, codigo_ncm, codigo_cfop, codigo_cest, origem_cst, descricao, CNPJ, marca) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        db.cursor.execute(queryInserirProdutos, (nome, valorCusto, valorVenda, quantidade, codigoInterno, NCM, CFOP, CEST, origemCST, descricao, CNPJ, marca))
        db.conn.commit()
        messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")


    def insereUsuarioNoBanco(nome, cargo, login, senha):
        queryInserirFuncionario = "INSERT INTO funcionarios(nome, cargo, login, senha) VALUES(%s, %s, %s, %s);"
        db.cursor.execute(queryInserirFuncionario, (nome, cargo, login, senha,))
        db.conn.commit()
        messagebox.showinfo(title="Info", message="Registrado com Sucesso")
    

    def registraFornecedorNoBanco(dados):
        colunas = list(dados.keys())
        valores = [f"'{str(valor)}'" for valor in dados.values()]
        query = f"INSERT INTO fornecedores ({', '.join(colunas)}) VALUES ({', '.join(valores)})"
        db.cursor.execute(query)
        db.conn.commit()



    def insereClienteNoBanco(nome, cpf, cnpj, IE, RG, CEP, rua, numero, bairro, cidade, estado, referencia, telefone, fiscal):
        if fiscal:
            print("entrou, eh fiscal")
            queryInserirCliente = "INSERT INTO clientes_fiscal(nome_razao_social, CPF_CNPJ, inscricao_estadual, CEP, Logradouro, Numero, Bairro, Cidade, Estado) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            db.cursor.execute(queryInserirCliente, (nome, cpf, IE, CEP, rua, numero, bairro, cidade, estado, ))
        else:
            print("entrou, não fiscal")
            queryInserirCliente = "INSERT INTO clientes(nome, cpf, cnpj, IE, RG, CEP, rua, numero, bairro, cidade, estado, referencia, telefone) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            db.cursor.execute(queryInserirCliente, (nome, cpf, cnpj, IE, RG, CEP, rua, numero, bairro, cidade, estado, referencia, telefone, ))
        db.conn.commit()
        messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")


    def registraFaturamentoNoBanco(confirmado, vencimento, descricao, total, formaPag, qtdParcelas):
        queryInserirCliente = "INSERT INTO contasareceber(confirmado, vencimento, descricao, total, formaPag, qtdParcelas) VALUES(%s, %s, %s, %s, %s, %s);"
        db.cursor.execute(queryInserirCliente, (confirmado, vencimento, descricao, total, formaPag, qtdParcelas))
        db.conn.commit()

    def registraFaturamentoEntradaNoBanco(
        confirmado,
        vencimento,
        descricao,
        total,
        numero_nfe,
        emitente_nome,
        dados_completos=None,
        numero_parcela=None,
    ):
        dados = dados_completos or {}
        hoje = datetime.now().strftime("%Y-%m-%d")
        data_emissao = dados.get("data_emissao") or hoje
        data_saida = dados.get("data_saida") or data_emissao
        dados_atualizados = {
            **dados,
            "data_emissao": data_emissao,
            "data_saida": data_saida,
        }
        itens = dados.get("itens") or dados.get("items") or []
        if isinstance(itens, dict):
            itens = list(itens.values())
        try:
            itens = json.dumps(itens)
        except Exception:
            itens = "[]"
        if not itens:
            itens = "[]"

        chave_base = dados_atualizados.get("chave_nfe", "")
        chave_parcela = f"{chave_base}-{numero_parcela}" if numero_parcela else chave_base

        campos = [
            "chave_nfe",
            "numero_nfe",
            "serie_nfe",
            "data_emissao",
            "data_saida",
            "emitente_cnpj",
            "emitente_nome",
            "destinatario_cnpj",
            "destinatario_nome",
            "valor_total",
            "valor_produtos",
            "valor_bc_icms",
            "valor_icms",
            "valor_icms_desonerado",
            "valor_bc_icms_st",
            "valor_icms_st",
            "valor_ipi",
            "valor_pis",
            "valor_cofins",
            "valor_bc_irrf",
            "transportadora_cnpj",
            "transportadora_nome",
            "itens",
            "data_registro",
            "confirmado",
            "descricao",
            "data_vencimento",
        ]

        descricao_valor = descricao if descricao is not None else ""
        vencimento_valor = vencimento if vencimento is not None else ""

        valores = [
            chave_parcela,
            numero_nfe,
            dados_atualizados.get("serie_nfe", ""),
            dados_atualizados.get("data_emissao", None),
            dados_atualizados.get("data_saida", None),
            dados_atualizados.get("emitente_cnpj", ""),
            emitente_nome,
            dados_atualizados.get("destinatario_cnpj", ""),
            dados_atualizados.get("destinatario_nome", ""),
            total,
            dados_atualizados.get("valor_produtos", 0),
            dados_atualizados.get("valor_bc_icms", 0),
            dados_atualizados.get("valor_icms", 0),
            dados_atualizados.get("valor_icms_desonerado", 0),
            dados_atualizados.get("valor_bc_icms_st", 0),
            dados_atualizados.get("valor_icms_st", 0),
            dados_atualizados.get("valor_ipi", 0),
            dados_atualizados.get("valor_pis", 0),
            dados_atualizados.get("valor_cofins", 0),
            dados_atualizados.get("valor_bc_irrf", 0),
            dados_atualizados.get("transportadora_cnpj", ""),
            dados_atualizados.get("transportadora_nome", ""),
            itens,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            confirmado,
            descricao_valor,
            vencimento_valor,
        ]

        placeholders = ", ".join(["%s"] * len(campos))
        query = f"INSERT INTO contasapagar ({', '.join(campos)}) VALUES ({placeholders});"
        db.cursor.execute(query, tuple(valores))
        db.conn.commit()

        if numero_nfe:
            try:
                db.cursor.execute(
                    "SELECT 1 FROM notas_fiscais WHERE numero = %s AND serie = %s LIMIT 1",
                    (numero_nfe, dados_atualizados.get("serie_nfe", "")),
                )
                existe = db.cursor.fetchone()
                if not existe:
                    query_nota = """
                        INSERT INTO notas_fiscais (
                            status, tipo, operacao, destinatario_nome, serie,
                            valor_total, cfop, dhEmi, numero, entradaOuSaida,
                            chave, emitente_nome, emitente_cnpjcpf, destinatario_cnpjcpf
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    db.cursor.execute(
                        query_nota,
                        (
                            "Registrada",
                            "NFe",
                            "Entrada",
                            dados_atualizados.get("destinatario_nome", emitente_nome),
                            dados_atualizados.get("serie_nfe", ""),
                            dados_atualizados.get("valor_total", total),
                            dados_atualizados.get("cfop", ""),
                            dados_atualizados.get("data_emissao", hoje),
                            numero_nfe,
                            "Entrada",
            chave_parcela,
                            emitente_nome,
                            dados_atualizados.get("emitente_cnpj", ""),
                            dados_atualizados.get("destinatario_cnpj", ""),
                        ),
                    )
                    db.conn.commit()
            except Exception:
                pass

    
    def registraPedidoNoBanco(dadosPedido):     
        itens_json = json.dumps(dadosPedido['itens'])

        db.cursor.execute("""INSERT INTO pedidos (
                numero_recibo, data_emissao, data_confirmacao, destinatario,
                cpf, cnpj, telefone, endereco, referencia, cep, vendedor,
                frete, valor_total, total_subtotal, total_acrescimo,
                total_desc_real, total_desc_porc,
                subtotal, itens
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
            (
                dadosPedido['numero_recibo'],
                dadosPedido['data_emissao'],
                dadosPedido.get('data_confirmacao', ''),
                dadosPedido['destinatario'],
                dadosPedido.get('cpf', ''),
                dadosPedido.get('cnpj', ''),
                dadosPedido.get('telefone', ''),
                dadosPedido['endereco'],
                dadosPedido.get('referencia', ''),
                dadosPedido.get('cep', ''),
                dadosPedido.get('vendedor', ''),
                float(dadosPedido.get('frete', 0.0) or 0.0),
                float(dadosPedido.get('valor_total') or 0.0),
                float(dadosPedido.get('total_subtotal') or 0.0),
                float(dadosPedido.get('total_acrescimo') or 0.0),
                float(dadosPedido.get('total_desc_real') or 0.0),
                float(dadosPedido.get('total_desc_porc') or 0.0),
                # int(dadosPedido.get('total_quantidade') or 0),
                float(dadosPedido.get('subtotal') or 0.0),
                itens_json
            )
        )

        db.conn.commit()

    def inserir_nota_fiscal(chave_nfe, numero_nfe, serie_nfe, data_emissao, data_saida,
                       emitente_cnpj, emitente_nome, destinatario_cnpj, destinatario_nome,
                       valor_total, valor_produtos, valor_bc_icms, valor_icms,
                       valor_icms_desonerado, valor_bc_icms_st, valor_icms_st,
                       valor_ipi, valor_pis, valor_cofins, valor_bc_irrf,
                       transportadora_cnpj, transportadora_nome, itens_json, data_vencimento):
        print("entrou aqui agora")
        
        resposta = messagebox.askquestion("Aviso", "Você tem certeza que deseja inserir essa nota fiscal?")
        if resposta == 'yes':
            descricao = f"lançamento referente a nota {numero_nfe}, com o fornecedor {emitente_nome}"
            confirmado = "Não"

            query = """INSERT INTO contasapagar (
                chave_nfe, numero_nfe, serie_nfe, data_emissao, data_saida,
                emitente_cnpj, emitente_nome, destinatario_cnpj, destinatario_nome,
                valor_total, valor_produtos, valor_bc_icms, valor_icms,
                valor_icms_desonerado, valor_bc_icms_st, valor_icms_st,
                valor_ipi, valor_pis, valor_cofins, valor_bc_irrf,
                transportadora_cnpj, transportadora_nome, itens, data_vencimento, confirmado, descricao 
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            
            dados = (
                chave_nfe, numero_nfe, serie_nfe, data_emissao, data_saida,
                emitente_cnpj, emitente_nome, destinatario_cnpj, destinatario_nome,
                valor_total, valor_produtos, valor_bc_icms, valor_icms,
                valor_icms_desonerado, valor_bc_icms_st, valor_icms_st,
                valor_ipi, valor_pis, valor_cofins, valor_bc_irrf,
                transportadora_cnpj, transportadora_nome, itens_json, data_vencimento, confirmado, descricao, 
            )
            print("inseriu a nota")
            db.cursor.execute(query, dados)
            db.conn.commit()

            print("chamou para inserir produto")
            def registrar_produtos_entrada():
                def extrair_valor_numerico(valor):
                    if isinstance(valor, dict):
                        valor = valor.get("#text", 0)
                    return float(valor or 0)

                def normalizar_texto(texto):
                    texto = unicodedata.normalize("NFKD", str(texto or ""))
                    texto = texto.encode("ASCII", "ignore").decode("ASCII")
                    return re.sub(r"[^a-z0-9]+", "", texto.lower())

                def cnpj_por_nome(razao_social):
                    print("assim veio o cnpj ", razao_social)
                    termo = normalizar_texto(razao_social)
                    print("assim veio o cnpj normalizado ", razao_social)
                    if any(nome in termo for nome in ["nutrigel", "multimaquinas", "polimaquinas", "refrimaquinas"]):
                        return destinatario_cnpj or ""
                    return destinatario_cnpj or ""

                if not itens_json:
                    itens = []
                elif isinstance(itens_json, str):
                    itens = json.loads(itens_json)
                else:
                    itens = itens_json

                if isinstance(itens, dict):
                    itens = [itens]

                cnpj_produto = (
                    cnpj_por_nome(destinatario_nome)
                    or destinatario_cnpj
                    or cnpj_por_nome(emitente_nome)
                )
                print(cnpj_produto)

                for item in itens:
                    prod = item.get("prod", {}) if isinstance(item, dict) else {}
                    nome = prod.get("xProd", "")
                    valor_custo = extrair_valor_numerico(prod.get("vUnCom", 0))
                    valor_venda = extrair_valor_numerico(prod.get("vProd", valor_custo))
                    quantidade = extrair_valor_numerico(prod.get("qCom", 0))
                    codigo_interno = prod.get("cProd", "")
                    ncm = prod.get("NCM", "")
                    cfop = prod.get("CFOP", "")
                    cest = prod.get("CEST", "")
                    origem_cst = prod.get("orig", "")
                    codigo_barras = prod.get("cEAN", "")
                    codigo_grade = prod.get("cEANTrib", "")
                    custo = valor_custo
                    cst = prod.get("CSOSN", "") or prod.get("CST", "") or ""
                    marca = prod.get("xProd", "")

                    query_produto_fiscal = (
                        "INSERT INTO produtos_fiscal("
                        "descricao_do_produto, cadigo_interno, codigo_de_barras, codigo_grade, "
                        "codigo_NCM, CST_A, valor_venda, custo, quantidade_em_estoque, CFOP, "
                        "estoque_MIN, estoque_MAX, CEST, cnpj"
                        ") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE quantidade_em_estoque = quantidade_em_estoque + VALUES(quantidade_em_estoque)"
                    )

                    query_produto = (
                        "INSERT INTO produtos("
                        "nome_do_produto, valor_de_custo, valor_de_venda, quantidade, "
                        "codigo_interno, codigo_ncm, codigo_cfop, codigo_cest, origem_cst, descricao, CNPJ, marca"
                        ") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE quantidade = quantidade + VALUES(quantidade)"
                    )

                    db.cursor.execute(
                        query_produto_fiscal,
                        (nome,codigo_interno,codigo_barras,codigo_grade,ncm,cst,valor_venda,custo,quantidade,cfop,0,0,cest,cnpj_produto,),)

                    db.cursor.execute(
                        query_produto,
                        ( nome, valor_custo, valor_venda, quantidade, codigo_interno, ncm, cfop, cest, origem_cst, nome, cnpj_produto, marca,),)
                    print("query para fiscal", query_produto_fiscal)
                    print("query para geral", query_produto)
                    db.conn.commit()


            registrar_produtos_entrada()
            messagebox.showinfo("Sucesso", "Nota fiscal inserida com sucesso!")


        else:
            pass
        



    def inserir_nota_fiscal_saida(tipo,modelo,serie,numero,chave,cUF,
        uf_emit,uf_dest,tpAmb,tpNF,idDest,natOp,dhEmi, dhSaiEnt,emitente_cnpjcpf,emitente_nome,
        emitente_ie,destinatario_cnpjcpf,destinatario_nome,destinatario_ie,valor_total,valor_produtos,
        valor_desconto,valor_frete,valor_seguro,valor_outras_despesas,valor_bc_icms,valor_icms,
        valor_icms_desonerado,valor_fcp,valor_bc_icms_st,valor_icms_st,valor_ipi,valor_pis,valor_cofins,
        valor_bc_irrf,transportadora_cnpjcpf,transportadora_nome,mod_frete,placa_veiculo,uf_veiculo,rntc,volum_qVol,
        volum_esp,volum_marca,volum_nVol,peso_liquido,peso_bruto,cStat,xMotivo,protocolo,nRec,dhRecbto,status,qrcode_url,
        data_vencimento,itens_json,cfop,operacao, ehEntradaOuSaida):
        
        query = """ INSERT INTO notas_fiscais (tipo,modelo,serie,numero,chave,cUF,
                                     uf_emit,uf_dest,tpAmb,tpNF,idDest,natOp,dhEmi,
                                     dhSaiEnt,emitente_cnpjcpf,emitente_nome,
                                     emitente_ie,destinatario_cnpjcpf,destinatario_nome,
                                     destinatario_ie,valor_total,valor_produtos,
                                     valor_desconto,valor_frete,valor_seguro,
                                     valor_outras_despesas,valor_bc_icms,valor_icms,
                                     valor_icms_desonerado,valor_fcp,valor_bc_icms_st,
                                     valor_icms_st,valor_ipi,valor_pis,valor_cofins,
                                     valor_bc_irrf,transportadora_cnpjcpf,transportadora_nome,
                                     mod_frete,placa_veiculo,uf_veiculo,rntc,volum_qVol,
                                     volum_esp,volum_marca,volum_nVol,peso_liquido,peso_bruto,
                                     cStat,xMotivo,protocolo,nRec,dhRecbto,status,qrcode_url,
                                     data_vencimento,itens_json,cfop,operacao, entradaOuSaida) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                                                                                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                                                                                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                                                                                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        dados = (tipo,modelo,serie,numero,chave,cUF,uf_emit,uf_dest,tpAmb,
                 tpNF,idDest,natOp,dhEmi, dhSaiEnt,emitente_cnpjcpf,emitente_nome,emitente_ie,destinatario_cnpjcpf,destinatario_nome,
                 destinatario_ie,valor_total,valor_produtos,valor_desconto,valor_frete,valor_seguro,valor_outras_despesas,valor_bc_icms,valor_icms,valor_icms_desonerado,
                 valor_fcp,valor_bc_icms_st,valor_icms_st,valor_ipi,valor_pis,valor_cofins,valor_bc_irrf,transportadora_cnpjcpf,transportadora_nome,mod_frete,
                 placa_veiculo,uf_veiculo,rntc,volum_qVol,volum_esp,volum_marca,volum_nVol,peso_liquido,peso_bruto,cStat,
                 xMotivo,protocolo,nRec,dhRecbto,status,qrcode_url,data_vencimento,itens_json,cfop,operacao,ehEntradaOuSaida,
        )

        db.cursor.execute(query, dados)
        db.conn.commit()
        messagebox.showinfo("Sucesso", "Nota fiscal criada e inserida com sucesso!")
