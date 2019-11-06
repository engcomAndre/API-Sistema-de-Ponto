def gen_mensagem(mensagem: str, conteudo: dict = None):
    res = {"mensagem": mensagem}
    res.update({"conteudo": conteudo} if conteudo else {})
    return res
