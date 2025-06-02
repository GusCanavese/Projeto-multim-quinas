import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from tkinter import filedialog
import xml.etree.ElementTree as ET


def pegarDadosDaNota(caminhoNota):
    print(caminhoNota)
    NAMESPACE = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

    tree = ET.parse(caminhoNota)
    root = tree.getroot()
    infNFe = root.find('.//ns:infNFe', NAMESPACE)

    def get_text(elem, tag):
        found = elem.find(f'ns:{tag}', NAMESPACE)
        return found.text if found is not None else None

    dados = {
        'ide': {tag: get_text(infNFe.find('ns:ide', NAMESPACE), tag) for tag in [
            'cUF', 'cNF', 'natOp', 'mod', 'serie', 'nNF', 'dhEmi', 'dhSaiEnt', 'tpNF', 'idDest',
            'cMunFG', 'tpImp', 'tpEmis', 'cDV', 'tpAmb', 'finNFe', 'indFinal', 'indPres',
            'indIntermed', 'procEmi', 'verProc'
        ]},
        'emit': {
            'CNPJ': get_text(infNFe.find('ns:emit', NAMESPACE), 'CNPJ'),
            'xNome': get_text(infNFe.find('ns:emit', NAMESPACE), 'xNome'),
            'xFant': get_text(infNFe.find('ns:emit', NAMESPACE), 'xFant'),
            'IE': get_text(infNFe.find('ns:emit', NAMESPACE), 'IE'),
            'IM': get_text(infNFe.find('ns:emit', NAMESPACE), 'IM'),
            'CNAE': get_text(infNFe.find('ns:emit', NAMESPACE), 'CNAE'),
            'CRT': get_text(infNFe.find('ns:emit', NAMESPACE), 'CRT'),
            'enderEmit': {tag: get_text(infNFe.find('ns:emit/ns:enderEmit', NAMESPACE), tag) for tag in [
                'xLgr', 'nro', 'xCpl', 'xBairro', 'cMun', 'xMun', 'UF', 'CEP', 'cPais', 'xPais', 'fone'
            ]}
        },
        'dest': {
            'CNPJ': get_text(infNFe.find('ns:dest', NAMESPACE), 'CNPJ'),
            'xNome': get_text(infNFe.find('ns:dest', NAMESPACE), 'xNome'),
            'IE': get_text(infNFe.find('ns:dest', NAMESPACE), 'IE'),
            'email': get_text(infNFe.find('ns:dest', NAMESPACE), 'email'),
            'indIEDest': get_text(infNFe.find('ns:dest', NAMESPACE), 'indIEDest'),
            'enderDest': {tag: get_text(infNFe.find('ns:dest/ns:enderDest', NAMESPACE), tag) for tag in [
                'xLgr', 'nro', 'xCpl', 'xBairro', 'cMun', 'xMun', 'UF', 'CEP', 'cPais', 'xPais', 'fone'
            ]}
        },
        'produtos': []
    }

    for det in infNFe.findall('ns:det', NAMESPACE):
        prod = det.find('ns:prod', NAMESPACE)
        imposto = det.find('ns:imposto', NAMESPACE)

        icms = imposto.find('.//ns:ICMS00', NAMESPACE)
        ipi = imposto.find('.//ns:IPITrib', NAMESPACE)
        pis = imposto.find('.//ns:PISAliq', NAMESPACE)
        cofins = imposto.find('.//ns:COFINSAliq', NAMESPACE)

        dados['produtos'].append({
            'nItem': det.attrib.get('nItem'),
            'produto': {tag: get_text(prod, tag) for tag in [
                'cProd', 'cEAN', 'xProd', 'NCM', 'CFOP', 'uCom', 'qCom', 'vUnCom', 'vProd',
                'cEANTrib', 'uTrib', 'qTrib', 'vUnTrib', 'indTot'
            ]},
            'ICMS': {tag: get_text(icms, tag) for tag in ['orig', 'CST', 'modBC', 'vBC', 'pICMS', 'vICMS']} if icms is not None else {},
            'IPI': {tag: get_text(ipi, tag) for tag in ['CST', 'vBC', 'pIPI', 'vIPI']} if ipi is not None else {},
            'PIS': {tag: get_text(pis, tag) for tag in ['CST', 'vBC', 'pPIS', 'vPIS']} if pis is not None else {},
            'COFINS': {tag: get_text(cofins, tag) for tag in ['CST', 'vBC', 'pCOFINS', 'vCOFINS']} if cofins is not None else {}
        })

    # Transporte
    transp = infNFe.find('ns:transp', NAMESPACE)
    dados['transporte'] = {
        'modFrete': get_text(transp, 'modFrete'),
        'transportadora': {
            'CNPJ': get_text(transp.find('ns:transporta', NAMESPACE), 'CNPJ'),
            'xNome': get_text(transp.find('ns:transporta', NAMESPACE), 'xNome'),
            'IE': get_text(transp.find('ns:transporta', NAMESPACE), 'IE'),
            'xEnder': get_text(transp.find('ns:transporta', NAMESPACE), 'xEnder'),
            'xMun': get_text(transp.find('ns:transporta', NAMESPACE), 'xMun'),
            'UF': get_text(transp.find('ns:transporta', NAMESPACE), 'UF'),
        },
        'volume': {tag: get_text(transp.find('ns:vol', NAMESPACE), tag) for tag in ['qVol', 'esp', 'marca', 'pesoL', 'pesoB']}
    }

    # Totais
    icms_tot = infNFe.find('ns:total/ns:ICMSTot', NAMESPACE)
    dados['total'] = {tag: get_text(icms_tot, tag) for tag in [
        'vBC', 'vICMS', 'vICMSDeson', 'vFCP', 'vBCST', 'vST', 'vFCPST', 'vFCPSTRet', 'vProd', 
        'vFrete', 'vSeg', 'vDesc', 'vII', 'vIPI', 'vIPIDevol', 'vPIS', 'vCOFINS', 'vOutro', 'vNF'
    ]}

    # Cobrança
    cobr = infNFe.find('ns:cobr', NAMESPACE)
    fat = cobr.find('ns:fat', NAMESPACE)
    dup = cobr.find('ns:dup', NAMESPACE)
    dados['cobranca'] = {
        'fatura': {tag: get_text(fat, tag) for tag in ['nFat', 'vOrig', 'vDesc', 'vLiq']},
        'duplicata': {tag: get_text(dup, tag) for tag in ['nDup', 'dVenc', 'vDup']}
    }

    # Pagamento
    pag = infNFe.find('ns:pag/ns:detPag', NAMESPACE)
    dados['pagamento'] = {tag: get_text(pag, tag) for tag in ['indPag', 'tPag', 'vPag']}

    # Informações adicionais
    infAdic = infNFe.find('ns:infAdic', NAMESPACE)
    dados['info_adicional'] = {
        'infCpl': get_text(infAdic, 'infCpl')
    }

    # Responsável técnico
    respTec = infNFe.find('ns:infRespTec', NAMESPACE)
    dados['responsavel_tecnico'] = {tag: get_text(respTec, tag) for tag in ['CNPJ', 'xContato', 'email', 'fone']}

    # Exemplo de visualização:
    print("\n========== DADOS DA NOTA ==========")
    for k, v in dados['ide'].items():
        print(f"{k}: {v}")

    print("\n========== EMITENTE ==========")
    print(f"CNPJ: {dados['emit']['CNPJ']}")
    print(f"Nome: {dados['emit']['xNome']}")
    print(f"Fantasia: {dados['emit']['xFant']}")
    print(f"IE: {dados['emit']['IE']}")
    print(f"IM: {dados['emit']['IM']}")
    print("Endereço:")
    for k, v in dados['emit']['enderEmit'].items():
        print(f"  {k}: {v}")

    print("\n========== DESTINATÁRIO ==========")
    print(f"CNPJ: {dados['dest']['CNPJ']}")
    print(f"Nome: {dados['dest']['xNome']}")
    print(f"IE: {dados['dest']['IE']}")
    print(f"E-mail: {dados['dest']['email']}")
    print("Endereço:")
    for k, v in dados['dest']['enderDest'].items():
        print(f"  {k}: {v}")

    print("\n========== PRODUTOS ==========")
    for i, item in enumerate(dados['produtos'], start=1):
        print(f"\n--- Produto {i} ---")
        for k, v in item['produto'].items():
            print(f"{k}: {v}")
        print("ICMS:")
        for k, v in item['ICMS'].items():
            print(f"  {k}: {v}")
        print("IPI:")
        for k, v in item['IPI'].items():
            print(f"  {k}: {v}")
        print("PIS:")
        for k, v in item['PIS'].items():
            print(f"  {k}: {v}")
        print("COFINS:")
        for k, v in item['COFINS'].items():
            print(f"  {k}: {v}")

    print("\n========== TRANSPORTE ==========")
    print(f"Modalidade Frete: {dados['transporte']['modFrete']}")
    print("Transportadora:")
    for k, v in dados['transporte']['transportadora'].items():
        print(f"  {k}: {v}")
    print("Volume:")
    for k, v in dados['transporte']['volume'].items():
        print(f"  {k}: {v}")

    print("\n========== COBRANÇA ==========")
    print("Fatura:")
    for k, v in dados['cobranca']['fatura'].items():
        print(f"  {k}: {v}")
    print("Duplicata:")
    for k, v in dados['cobranca']['duplicata'].items():
        print(f"  {k}: {v}")

    print("\n========== PAGAMENTO ==========")
    for k, v in dados['pagamento'].items():
        print(f"{k}: {v}")

    print("\n========== TOTAIS ==========")
    for k, v in dados['total'].items():
        print(f"{k}: {v}")

    print("\n========== INFO ADICIONAL ==========")
    print(f"Complemento: {dados['info_adicional']['infCpl']}")

    print("\n========== RESPONSÁVEL TÉCNICO ==========")
    for k, v in dados['responsavel_tecnico'].items():
        print(f"{k}: {v}")


def lerNotaFiscal(self):
    entry = ctk.CTkEntry(self)
    entry.place(relx=0.2, rely=0.2)

    button = ctk.CTkButton(self, text="texto", command=lambda: entry.insert(0, filedialog.askopenfilename()))
    button.place(relx=0.2, rely=0.3)
    
    buttonPegarDados = ctk.CTkButton(self, text="Pegar dados", command=lambda: pegarDadosDaNota(entry.get()))
    buttonPegarDados.place(relx=0.4, rely=0.4)








