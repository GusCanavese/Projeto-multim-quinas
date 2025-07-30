def acessar(dados, *caminho, default=""):
    for chave in caminho:
        if isinstance(dados, dict) and chave in dados:
            dados = dados[chave]
        else:
            return default
    if isinstance(dados, dict) and "#text" in dados:
        return dados["#text"]
    return dados if isinstance(dados, str) else default