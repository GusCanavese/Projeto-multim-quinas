import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import db
from tkinter import messagebox
import json
import re
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



    def insereClienteNoBanco(nome, cpf, cnpj, IE, RG, CEP, rua, numero, bairro, cidade, estado, referencia, telefone):
        queryInserirCliente = "INSERT INTO clientes(nome, cpf, cnpj, IE, RG, CEP, rua, numero, bairro, cidade, estado, referencia, telefone) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        db.cursor.execute(queryInserirCliente, (nome, cpf, cnpj, IE, RG, CEP, rua, numero, bairro, cidade, estado, referencia, telefone, ))
        db.conn.commit()
        messagebox.showinfo(title="Acessar Info", message="Registrado com Sucesso")


    def registraFaturamentoNoBanco(confirmado, vencimento, descricao, total, formaPag, qtdParcelas):
        queryInserirCliente = "INSERT INTO contasareceber(confirmado, vencimento, descricao, total, formaPag, qtdParcelas) VALUES(%s, %s, %s, %s, %s, %s);"
        db.cursor.execute(queryInserirCliente, (confirmado, vencimento, descricao, total, formaPag, qtdParcelas))
        db.conn.commit()

    
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
            
            db.cursor.execute(query, dados)
            db.conn.commit()
            messagebox.showinfo("Sucesso", "Nota fiscal inserida com sucesso!")


        else:
            pass
        



def inserir_nota_fiscal(self, tipo, xml_path=None, status=None):
    print("To aqui")

    def V(nome, default=""):
        v = getattr(self, nome, default)
        return v.get() if hasattr(v, "get") else (v if v is not None else default)

    def dig(s):
        s = "" if s is None else str(s)
        return "".join(ch for ch in s if ch.isdigit())

    def f(v):
        s = str(v).strip().replace(".", "").replace(",", ".")
        try:
            return float(s)
        except:
            return 0.0

    # tipo/modelo
    t = str(tipo)
    modelo_int = 65 if t.upper().startswith("NFC") else 55
    tipo_str = "NFCe" if modelo_int == 65 else t  # respeita parâmetro (NFe/NFeEntrada)

    # número e série (inteiros)
    num_str = dig(V("variavelNumeroDaNota", V("nNF", "")))
    serie_str = dig(V("variavelSerieDaNota", V("serie", "1")))
    numero_int = int(num_str) if num_str else 0
    serie_int = int(serie_str) if serie_str else 1

    # emitente/destinatário
    emitente_cnpj = dig(V("variavelCNPJRazaoSocialEmitente", ""))
    emitente_nome = str(V("variavelRazaoSocialEmitente", "")).strip()
    dest_cnpj     = dig(V("variavelCNPJDestinatario", ""))
    dest_nome     = str(V("variavelNomeRazaoDestinatario", "")).strip()

    # datas (DATETIME)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dhEmi = str(V("variavelDataEmissao", "")).strip() or now_str
    dhSaiEnt = str(V("variavelDataSaida", "")).strip() or dhEmi

    # chave e cUF
    xml_caminho = xml_path or ""
    chave_nfe = ""
    m = re.search(r"(\d{44})", xml_caminho)
    if m:
        chave_nfe = m.group(1)
    if not chave_nfe:
        chave_nfe = dig(V("chaveNFe", ""))
    cUF = chave_nfe[:2] if len(chave_nfe) >= 2 else "31"

    # ambiente e tipo da operação
    tpAmb = 2  # homologação por padrão
    ent_saida = str(getattr(self, "variavelEntradaOuSaida", "Saída")).lower()
    tpNF = 0 if "entra" in ent_saida else 1

    # totais
    valor_total        = f(V("variavelValorTotalNota", 0))
    valor_produtos     = f(V("variavelValorProdutos", 0))
    valor_desconto     = f(V("variavelValorDesconto", 0))
    valor_frete        = f(V("variavelValorFrete", 0))
    valor_seguro       = f(V("variavelValorSeguro", 0))
    valor_outros       = f(V("variavelOutros", 0))
    valor_bc_icms      = f(V("variavelBaseICMS", 0))
    valor_icms         = f(V("variavelValorICMS", 0))
    valor_icms_deson   = f(V("variavelICMSDesonerado", 0))
    valor_bc_icms_st   = f(V("variavelBaseICMSST", 0))
    valor_icms_st      = f(V("variavelValorICMSST", 0))
    valor_ipi          = f(V("variavelValorIPI", 0))
    valor_pis          = f(V("variavelValorPIS", 0))
    valor_cofins       = f(V("variavelValorCOFINS", 0))
    valor_bc_irrf      = f(V("variavelBaseIRRF", 0))

    # transporte
    transportadora_cnpj = dig(V("variavelCNPJTransportadora", ""))
    transportadora_nome = str(V("variavelNomeTransportadora", "")).strip()

    # status
    status_str = status or "AUTORIZADA"

    # itens JSON (lista simples da UI se existir)
    itens = getattr(self, "listaItensNotaSaida", None)
    if not isinstance(itens, (list, tuple)):
        itens = []
    itens_json = json.dumps(itens, ensure_ascii=False)

    # INSERT conforme sua tabela
    print("to aqui")
    db.cursor.execute(
        """
        INSERT INTO notas_fiscais (
            tipo, status, modelo, serie, numero, chave,
            cUF, tpAmb, tpNF,
            dhEmi, dhSaiEnt,
            emitente_cnpjcpf, emitente_nome,
            destinatario_cnpjcpf, destinatario_nome,
            valor_total, valor_produtos, valor_desconto,
            valor_frete, valor_seguro, valor_outras_despesas,
            valor_bc_icms, valor_icms, valor_icms_desonerado,
            valor_bc_icms_st, valor_icms_st,
            valor_ipi, valor_pis, valor_cofins, valor_bc_irrf,
            transportadora_cnpjcpf, transportadora_nome,
            xml_path, itens_json
        ) VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s,
            %s, %s,
            %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s,
            %s, %s, %s, %s,
            %s, %s,
            %s, %s
        )
        """,
        (
            tipo_str, status_str, int(modelo_int), int(serie_int), int(numero_int), chave_nfe,
            cUF, int(tpAmb), int(tpNF),
            dhEmi, dhSaiEnt,
            emitente_cnpj, emitente_nome,
            dest_cnpj, dest_nome,
            valor_total, valor_produtos, valor_desconto,
            valor_frete, valor_seguro, valor_outros,
            valor_bc_icms, valor_icms, valor_icms_deson,
            valor_bc_icms_st, valor_icms_st,
            valor_ipi, valor_pis, valor_cofins, valor_bc_irrf,
            transportadora_cnpj, transportadora_nome,
            xml_caminho, itens_json
        )
    )
    db.conn.commit()
    return getattr(db.cursor, "lastrowid", None)
