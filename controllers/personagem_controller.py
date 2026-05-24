from direct.actor.Actor import Actor


def create_personagens(render, posicao, scale, asset_path):
    personagem = Actor(asset_path)
    personagem.reparentTo(render)
    personagem.setPos(*posicao)
    personagem.setScale(scale)
    personagem.setHpr(180, 0, 0)

    animacoes = personagem.getAnimNames()
    if animacoes:
        personagem.loop(animacoes[0])

    return personagem