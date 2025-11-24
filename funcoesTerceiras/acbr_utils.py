import os
import re
import glob
import sys
from pathlib import Path


def _base_dir() -> Path:
    """Retorna o diretório base do executável ou do projeto."""

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent.parent


def _candidatos_logs():
    """Gera caminhos prováveis para a pasta de logs do ACBr."""

    env_dir = os.environ.get("ACBR_LOG_DIR")

    base = _base_dir()
    cwd = Path.cwd()

    paths = [
        Path(env_dir) if env_dir else None,
        base / "NotaFiscal" / "Logs",
        base / "Logs",
        cwd / "NotaFiscal" / "Logs",
        cwd / "Logs",
        Path(r"C:\\ACBrMonitorPLUS\\Logs"),
    ]

    vistos = set()
    for p in paths:
        if not p:
            continue
        key = str(p.resolve())
        if key in vistos:
            continue
        vistos.add(key)
        yield p


def _buscar_por_nome(nome_arquivo: str) -> str:
    """Procura o XML por nome dentro dos diretórios candidatos."""

    if not nome_arquivo:
        return ""

    for pasta in _candidatos_logs():
        candidato = Path(pasta) / nome_arquivo
        if candidato.exists():
            return str(candidato)
    return ""


def _buscar_xml_recente() -> str:
    """Retorna o XML mais recente encontrado nos diretórios candidatos."""

    padroes = ("*-nfe.xml", "*-nfce.xml", "*-procNFe.xml", "*-procnfce.xml")
    candidatos = []
    for pasta in _candidatos_logs():
        if not pasta.exists():
            continue
        for padrao in padroes:
            candidatos.extend(glob.glob(os.path.join(pasta, padrao)))

    if not candidatos:
        return ""

    candidatos.sort(key=os.path.getmtime, reverse=True)
    return candidatos[0]


def extrair_caminho_xml(retorno: str) -> str:
    """
    Extrai o caminho do XML a partir do retorno do ACBr Monitor.
    Ex.: "OK: C:\\ACBrMonitorPLUS\\Logs\\3125...-nfe.xml"
    """

    if not retorno:
        return ""

    regexes = [
        r"OK:\s*([^\r\n]+?\.xml)",
        r"Arquivo\s*=\s*([^\r\n]+?\.xml)",
        r"([A-Z]:\\[^:\n\r]+?\.xml)",
        r"(/[^:\n\r]+?\.xml)",
    ]

    caminho_bruto = ""
    for padrao in regexes:
        m = re.search(padrao, retorno, flags=re.I)
        if m:
            caminho_bruto = m.group(1).strip()
            break

    # Se encontramos um caminho e ele existir, retornamos imediatamente
    if caminho_bruto and os.path.exists(caminho_bruto):
        return caminho_bruto

    # Se veio um caminho, mas não existe, tenta localizar pelo nome em pastas conhecidas
    if caminho_bruto:
        encontrado = _buscar_por_nome(Path(caminho_bruto).name)
        if encontrado:
            return encontrado

    # Último recurso: pega o XML mais recente na pasta de logs
    return _buscar_xml_recente()
