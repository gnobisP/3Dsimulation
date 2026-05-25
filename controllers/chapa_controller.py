from panda3d.core import CardMaker, MovieTexture


def create_video_chapa(loader, render, video_path, position, scale):
    chapa_root = render.attachNewNode("video_chapa_root")
    chapa_root.setPos(*position)
    chapa_root.setScale(scale)

    chapa = loader.loadModel("assets/chapa.bam")
    chapa.reparentTo(chapa_root)
    chapa.setPos(0, 0, -1)
    chapa.setScale(5.0)

    video_texture = MovieTexture("tv_screen")
    if not video_texture.read(video_path):
        print(f"Não foi possível carregar o vídeo em {video_path}")
        return chapa_root

    video_texture.setLoop(True)
    video_texture.play()

    video_width = max(1, video_texture.getVideoWidth())
    video_height = max(1, video_texture.getVideoHeight())
    aspect = video_width / video_height

    card_maker = CardMaker("tv_screen_card")
    card_maker.setUvRange(video_texture)
    card_maker.setFrame(-1.0, 1.0, -1.0 / aspect, 1.0 / aspect)

    screen = chapa_root.attachNewNode(card_maker.generate())
    screen.setPos(0, 0, 0)
    screen.setHpr(-90, -90, -90)
    screen.setScale(6.8)
    screen.setTexture(video_texture, 1)

    return chapa_root