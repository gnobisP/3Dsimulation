from panda3d.core import AmbientLight, DirectionalLight, VBase4, Vec3
from direct.actor.Actor import Actor
from panda3d.core import WindowProperties

class GameView:
    def __init__(self, base, render, loader):
        self.base = base
        self.render = render
        self.loader = loader
        self.players = []

        self.configure_window()

        self.setup_lighting()
        self.create_platform()
        self.create_players()

    def configure_window(self):
        
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_confined)
        self.base.win.requestProperties(props)

    def setup_lighting(self):
        ambient = AmbientLight("ambientLight")
        ambient.setColor(VBase4(0.3, 0.3, 0.3, 1))
        self.render.setLight(self.render.attachNewNode(ambient))

        directional = DirectionalLight("dirLight")
        directional.setColor(VBase4(1, 1, 1, 1))
        dir_node = self.render.attachNewNode(directional)
        dir_node.setHpr(45, -45, 0)
        self.render.setLight(dir_node)

    def create_platform(self):
        plataforma = self.loader.loadModel("assets/cenario0.obj")
        plataforma.reparentTo(self.render)
        plataforma.setPos(0, 0, 0)
        plataforma.setScale(1000)
        plataforma.setHpr(90, 90, 0)

    def create_players(self):
        for i in range(100):
            actor = Actor("assets/mod0_pessoa.egg")
            actor.reparentTo(self.render)
            actor.setScale(100)
            if i == 0:
                actor.setPos(0, 0, 1500)
            else:
                actor.setPos(i * 1000, i * 1000, 1500)

            if actor.getAnimNames():
                actor.loop(actor.getAnimNames()[0])

            self.players.append(actor)

    def update_player(self, player_model, actor):
        actor.setPos(player_model.position)
        actor.setH(player_model.rotation)
