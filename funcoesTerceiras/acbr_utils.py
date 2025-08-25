import os, re, glob

def extrair_caminho_xml(retorno: str) -> str:
    """
    Extrai o caminho do XML a partir do retorno do ACBr Monitor.
    Ex.: "OK: C:\ACBrMonitorPLUS\Logs\3125...-nfe.xml"
    """
    if not retorno:
        return ""
    # tenta pegar caminho após "OK:"
    m = re.search(r"OK:\s*(.+?\.xml)", retorno, flags=re.I)
    if m and os.path.exists(m.group(1)):
        return m.group(1)

    # tenta padrões comuns
    m = re.search(r"([A-Z]:\\[^:\n\r]+?-nfe\.xml)", retorno, flags=re.I)
    if m and os.path.exists(m.group(1)):
        return m.group(1)

    # fallback: procurar no diretório padrão do ACBr Monitor
    logs_dir = r"C:\ACBrMonitorPLUS\Logs"
    if os.path.isdir(logs_dir):
        candidatos = sorted(glob.glob(os.path.join(logs_dir, "*-nfe.xml")), key=os.path.getmtime, reverse=True)
        if candidatos:
            return candidatos[0]
    return ""