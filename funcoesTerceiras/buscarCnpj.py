import requests


def buscar_cnpj(cnpj):
    cnpj_limpo = "".join(filter(str.isdigit, str(cnpj or "")))
    if len(cnpj_limpo) != 14:
        raise ValueError("CNPJ inválido. Informe 14 dígitos.")

    url = f"https://publica.cnpj.ws/cnpj/{cnpj_limpo}"
    resposta = requests.get(url, timeout=10)
    if resposta.status_code != 200:
        raise ValueError("Não foi possível consultar o CNPJ informado.")

    dados = resposta.json() or {}
    estabelecimento = dados.get("estabelecimento", {}) or {}
    cidade = estabelecimento.get("cidade", {}) or {}
    estado = estabelecimento.get("estado", {}) or {}

    telefone = estabelecimento.get("telefone1") or estabelecimento.get("telefone2") or ""
    if estabelecimento.get("ddd1") and telefone:
        telefone = f"({estabelecimento.get('ddd1')}) {telefone}"

    return {
        "nome": dados.get("razao_social") or estabelecimento.get("nome_fantasia") or "",
        "cep": (estabelecimento.get("cep") or "").replace("-", ""),
        "rua": estabelecimento.get("logradouro") or "",
        "numero": estabelecimento.get("numero") or "",
        "bairro": estabelecimento.get("bairro") or "",
        "cidade": cidade.get("nome") or "",
        "estado": estado.get("sigla") or "",
        "telefone": telefone,
    }
