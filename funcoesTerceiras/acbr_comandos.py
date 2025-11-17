import os
import re
import time
from typing import Dict, Optional

ACBR_CMD_DIR = os.path.join("NotaFiscal", "EnviarComando")
ACBR_RSP_DIR = os.path.join("NotaFiscal", "ReceberComando")
_SUCESSO_CSTAT = {"100", "101", "102", "104", "135", "151", "155"}


def _so_digitos(valor: str) -> str:
    return re.sub(r"\D+", "", valor or "")


def _normalizar_justificativa(texto: str) -> str:
    texto = (texto or "").strip()
    if len(texto) < 15:
        raise ValueError("A justificativa deve possuir ao menos 15 caracteres.")
    return texto[:255].replace('"', "'")


def _aguardar_resposta(resp_path: str, timeout: int = 20, intervalo: float = 0.4) -> str:
    inicio = time.time()
    ultima_leitura = ""
    while time.time() - inicio < timeout:
        if os.path.exists(resp_path):
            try:
                with open(resp_path, "r", encoding="utf-8", errors="ignore") as arquivo:
                    conteudo = arquivo.read().strip()
                if conteudo and conteudo != ultima_leitura:
                    return conteudo
            except Exception:
                pass
        time.sleep(intervalo)
    return ultima_leitura


def _interpretar_resposta(texto: str) -> Dict[str, str]:
    texto = texto or ""

    def _match(pattern: str) -> str:
        encontrado = re.search(pattern, texto, flags=re.IGNORECASE)
        return encontrado.group(1).strip() if encontrado else ""

    cstat = _match(r"\bCStat\s*=\s*([0-9]{2,3})")
    msg = _match(r"\bMsg\s*=\s*(.+)")
    motivo = _match(r"\bxMotivo\s*=\s*(.+)")
    protocolo = _match(r"\bNProt\s*=\s*([0-9]+)")
    arquivo = _match(r"\bArquivo\s*=\s*(.+?\.xml)")
    primeira_linha = texto.strip().splitlines()[0] if texto.strip() else ""

    sucesso = bool(primeira_linha.upper().startswith("OK")) or cstat in _SUCESSO_CSTAT
    if "ERRO" in texto.upper() or "REJEI" in (motivo or msg).upper():
        sucesso = False

    mensagem = motivo or msg or primeira_linha or "Retorno desconhecido do ACBr Monitor."

    return {
        "sucesso": sucesso,
        "cStat": cstat,
        "motivo": mensagem.strip(),
        "protocolo": protocolo,
        "arquivo": arquivo,
        "resposta": texto.strip(),
    }


def _executar_comando(conteudo: str, prefixo: str, timeout: int = 20) -> Dict[str, str]:
    os.makedirs(ACBR_CMD_DIR, exist_ok=True)
    os.makedirs(ACBR_RSP_DIR, exist_ok=True)

    timestamp = int(time.time() * 1000)
    base_nome = f"{prefixo}-{timestamp}"
    cmd_path = os.path.join(ACBR_CMD_DIR, f"{base_nome}.txt")
    resp_path = os.path.join(ACBR_RSP_DIR, f"{base_nome}-resp.txt")

    for caminho in (cmd_path, resp_path):
        try:
            os.remove(caminho)
        except FileNotFoundError:
            pass

    with open(cmd_path, "w", encoding="utf-8", newline="") as arquivo:
        arquivo.write(conteudo.strip())
        if not conteudo.endswith("\r\n"):
            arquivo.write("\r\n")

    resposta_bruta = _aguardar_resposta(resp_path, timeout=timeout)
    if not resposta_bruta:
        raise RuntimeError("ACBr Monitor não retornou nenhuma resposta para o comando enviado.")

    return _interpretar_resposta(resposta_bruta)


def cancelar_nfe(chave: str, justificativa: str, protocolo: str, cnpj_emitente: str) -> Dict[str, str]:
    chave_limpa = _so_digitos(chave)
    if len(chave_limpa) != 44:
        raise ValueError("Informe uma chave de acesso válida (44 dígitos).")

    protocolo_limpo = _so_digitos(protocolo)
    if len(protocolo_limpo) < 10:
        raise ValueError("Informe o número de protocolo da SEFAZ (mínimo 10 dígitos).")

    cnpj_limpo = _so_digitos(cnpj_emitente)
    if len(cnpj_limpo) != 14:
        raise ValueError("Informe o CNPJ do emitente para cancelar a nota.")

    justificativa = _normalizar_justificativa(justificativa)
    comando = f'NFe.CancelarNFe("{chave_limpa}","{justificativa}","{cnpj_limpo}","{protocolo_limpo}")'
    return _executar_comando(comando, "cancelar")


def inutilizar_nfe(
    cnpj_emitente: str,
    justificativa: str,
    ano: str,
    modelo: str,
    serie: str,
    numero_inicial: str,
    numero_final: Optional[str] = None,
) -> Dict[str, str]:
    cnpj_limpo = _so_digitos(cnpj_emitente)
    if len(cnpj_limpo) != 14:
        raise ValueError("Informe o CNPJ do emitente (14 dígitos) para inutilizar a numeração.")

    justificativa = _normalizar_justificativa(justificativa)

    try:
        serie_int = int(str(serie).strip() or "1")
    except ValueError as erro:
        raise ValueError("Série inválida para a inutilização.") from erro

    try:
        modelo_int = int(str(modelo).strip() or "55")
    except ValueError as erro:
        raise ValueError("Modelo inválido para a inutilização.") from erro

    try:
        numero_ini = int(str(numero_inicial).strip())
    except ValueError as erro:
        raise ValueError("Número inicial inválido para a inutilização.") from erro

    if numero_final is None:
        numero_final = numero_ini
    try:
        numero_fim = int(str(numero_final).strip())
    except ValueError as erro:
        raise ValueError("Número final inválido para a inutilização.") from erro

    ano_str = str(ano).strip()
    if len(ano_str) >= 4:
        ano_str = ano_str[-2:]
    if len(ano_str) != 2:
        raise ValueError("Ano inválido para a inutilização (use os dois últimos dígitos).")

    comando = (
        'NFe.InutilizarNF('
        f'"{cnpj_limpo}",'
        f'"{justificativa}",'
        f'"{ano_str}",'
        f'"{modelo_int:02d}",'
        f'"{serie_int}",'
        f'"{numero_ini}",'
        f'"{numero_fim}")'
    )
    return _executar_comando(comando, "inutilizar")


__all__ = ["cancelar_nfe", "inutilizar_nfe"]