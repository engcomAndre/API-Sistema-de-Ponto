from typing import List, Dict, Optional


def gen_mensagem(mensagem: str, conteudo: List[Dict[str, str]] = None) -> Dict[str, str]:
    res = {"mensagem": mensagem}
    res.update({"conteudo": conteudo} if conteudo else {})
    return res
