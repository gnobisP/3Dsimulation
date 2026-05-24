from panda3d.core import CardMaker


def create_image_chapa(loader, render, image_path, position, scale):
    chapa_root = render.attachNewNode("image_chapa_root")
    chapa_root.setPos(*position)
    chapa_root.setScale(scale)

    chapa = loader.loadModel("assets/chapa.bam")
    chapa.reparentTo(chapa_root)
    chapa.setPos(0, 0, 0)
    chapa.setScale(1.0)

    # Carrega a imagem como textura
    image_texture = loader.loadTexture(image_path)

    if not image_texture:
        print(f"Não foi possível carregar a imagem em {image_path}")
        return chapa_root

    # Obtém dimensões da imagem
    image_width = max(1, image_texture.getXSize())
    image_height = max(1, image_texture.getYSize())
    aspect = image_width / image_height

    # Cria a "tela" do chapa
    card_maker = CardMaker("chapa_screen_card")
    card_maker.setFrame(-1.0, 1.0, -1.0 / aspect, 1.0 / aspect)

    screen = chapa_root.attachNewNode(card_maker.generate())
    screen.setPos(0, 0, 0)
    screen.setHpr(0, 0, 0)
    screen.setScale(1.0)

    # Aplica a textura
    screen.setTexture(image_texture, 1)

    return chapa_root