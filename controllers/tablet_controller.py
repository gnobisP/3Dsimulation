from panda3d.core import CardMaker, MovieTexture
from controllers.suporte_tablet_controller import create_suporte_tablet


def create_video_tablet(loader, render, video_path, position, scale):
    tablet_root = render.attachNewNode("video_tablet_root")
    tablet_root.setPos(*position)
    tablet_root.setScale(scale)

    tablet = loader.loadModel("assets/tabletPronto.bam")
    tablet.reparentTo(tablet_root)
    tablet.setPos(0, 0, 0)
    tablet.setScale(5.0)

    video_texture = MovieTexture("tv_screen")
    if not video_texture.read(video_path):
        print(f"Não foi possível carregar o vídeo em {video_path}")
        return tablet_root

    video_texture.setLoop(True)
    video_texture.play()

    video_width = max(1, video_texture.getVideoWidth())
    video_height = max(1, video_texture.getVideoHeight())
    aspect = video_width / video_height

    card_maker = CardMaker("tv_screen_card")
    card_maker.setUvRange(video_texture)
    card_maker.setFrame(-1.0, 1.0, -1.0 / aspect, 1.0 / aspect)

    screen = tablet_root.attachNewNode(card_maker.generate())
    screen.setPos(11.5, -0.5, 18.0)
    screen.setHpr(0, 0, 0)
    screen.setScale(9.8)
    screen.setTexture(video_texture, 1)

    return tablet_root


def create_suporte_and_tablet_video(
    loader,
    render,
    video_path,
    position=(0, 0, 0),
    scale=1,
    suporte_scale_z=1000,
    tablet_position_z=0,
):
    support_root = render.attachNewNode("support_and_tablet_root")
    support_root.setPos(*position)
    support_root.setScale(scale)

    suporte = create_suporte_tablet(
        loader=loader,
        render=support_root,
        position=(77, 1335, 200),
        scale=1,
    )
    suporte.setScale(1000, 1000, suporte_scale_z)
    suporte.setHpr(270, 0, 0)

    tablet_root = support_root.attachNewNode("video_tablet_root")
    tablet_position_z_local = tablet_position_z / scale if scale not in (0, 0.0) else tablet_position_z
    tablet_root.setPos(100, 1100, tablet_position_z_local)
    tablet_root.setScale(40)

    tablet = loader.loadModel("assets/tabletPronto.bam")
    tablet.reparentTo(tablet_root)
    tablet.setPos(0, 0, 0)
    tablet.setScale(5.0)

    video_texture = MovieTexture("tv_screen")
    if not video_texture.read(video_path):
        print(f"Não foi possível carregar o vídeo em {video_path}")
        return support_root

    video_texture.setLoop(True)
    video_texture.play()

    video_width = max(1, video_texture.getVideoWidth())
    video_height = max(1, video_texture.getVideoHeight())
    aspect = video_width / video_height

    card_maker = CardMaker("tv_screen_card")
    card_maker.setUvRange(video_texture)
    card_maker.setFrame(-1.0, 1.0, -1.0 / aspect, 1.0 / aspect)

    screen = tablet_root.attachNewNode(card_maker.generate())
    screen.setPos(11.5, -0.5, 18.0)
    screen.setHpr(0, 0, 0)
    screen.setScale(9.8)
    screen.setTexture(video_texture, 1)

    return support_root