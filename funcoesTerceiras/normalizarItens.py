import ast
import json


def normalizar_itens_pedido(raw):
    itens = raw or []

    if isinstance(itens, (bytes, bytearray)):
        itens = itens.decode("utf-8", errors="ignore")

    if isinstance(itens, str):
        tentativas = 0
        while isinstance(itens, str) and tentativas < 3:
            if not itens.strip():
                return []
            try:
                itens = json.loads(itens)
            except Exception:
                try:
                    itens = ast.literal_eval(itens)
                except Exception:
                    return []
            tentativas += 1

    if isinstance(itens, dict):
        if any(chave in itens for chave in ("descricao", "quantidade", "preco", "valor")):
            return [itens]
        itens_aninhados = itens.get("itens") or itens.get("items")
        if itens_aninhados is not None:
            itens = itens_aninhados
        else:
            itens = list(itens.values())

    if isinstance(itens, tuple):
        itens = list(itens)

    if isinstance(itens, list):
        if len(itens) == 1 and isinstance(itens[0], list):
            itens = itens[0]
        if len(itens) == 1 and isinstance(itens[0], dict):
            nested = itens[0].get("itens") or itens[0].get("items")
            if nested is not None:
                itens = nested
    else:
        return []

    return itens or []
