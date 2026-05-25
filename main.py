from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import AmbientLight, DirectionalLight, VBase4
from direct.showbase.ShowBaseGlobal import globalClock
import sys
import random
from panda3d.core import Vec3
from panda3d.core import loadPrcFileData, WindowProperties, Vec3
from direct.showbase.ShowBase import ShowBase
import time
from controllers.personagem_controller import create_personagens
from controllers.tablet_controller import create_suporte_and_tablet_video
from controllers.chapa_controller import create_video_chapa
# 🎯 Configurações iniciais
loadPrcFileData('', 'win-size 1280 720')
loadPrcFileData('', 'window-title Movimento Livre 3D')
loadPrcFileData('', 'show-frame-rate-meter 1')

class MyApp(ShowBase):
    def __init__(self):
        super().__init__()

        # 🎥 Desativar o controle padrão da câmera
        self.disableMouse()

        self.center_x = int(self.win.getProperties().getXSize() / 2)
        self.center_y = int(self.win.getProperties().getYSize() / 2)
        self.last_mouse_x = self.center_x
        self.last_mouse_y = self.center_y
        self.win.movePointer(0, self.center_x, self.center_y)

        # 🎯 Configurar janela
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_confined)
        self.win.requestProperties(props)
        
        # 🎇 Adicionar luz
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(VBase4(0.3, 0.3, 0.3, 1))
        self.render.setLight(self.render.attachNewNode(ambientLight))

        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setColor(VBase4(1, 1, 1, 1))
        dlnp = self.render.attachNewNode(directionalLight)
        dlnp.setHpr(45, -45, 0)
        self.render.setLight(dlnp)

        # 🚌 Carregar modelo
        self.plataforma = self.loader.loadModel("assets/room.obj")
        self.plataforma.reparentTo(self.render)
        self.plataforma.setPos(750, 00, 0)
        self.plataforma.setScale(1000,1000,1500)
        self.plataforma.setHpr(90,90,0)

        # 🚌 Carregar tapete
        self.plataforma = self.loader.loadModel("assets/tapete.dae")
        self.plataforma.reparentTo(self.render)
        self.plataforma.setPos(-950, 2700, 215)
        self.plataforma.setScale(100)
        self.plataforma.setSx(120)
        self.plataforma.setHpr(90,90,0)
        self.plataforma.setTextureOff(1)
        self.plataforma.setMaterialOff(1)
        self.plataforma.setColorScale(0, 0, 0, 1)
        self.plataforma.setLightOff()

        # 🚌 Carregar tapete
        self.plataforma = self.loader.loadModel("assets/tapete.dae")
        self.plataforma.reparentTo(self.render)
        self.plataforma.setPos(1250, 2700, 215)
        self.plataforma.setScale(100)
        self.plataforma.setSx(120)
        self.plataforma.setHpr(90,90,0)
        self.plataforma.setTextureOff(1)
        self.plataforma.setMaterialOff(1)
        self.plataforma.setColorScale(0, 0, 0, 1)
        self.plataforma.setLightOff()

        # 🚌 Carregar tapete
        self.plataforma = self.loader.loadModel("assets/tapete.dae")
        self.plataforma.reparentTo(self.render)
        self.plataforma.setPos(3450, 2700, 215)
        self.plataforma.setScale(100)
        self.plataforma.setSx(120)
        self.plataforma.setHpr(90,90,0)
        self.plataforma.setTextureOff(1)
        self.plataforma.setMaterialOff(1)
        self.plataforma.setColorScale(0, 0, 0, 1)
        self.plataforma.setLightOff()

        self.plataforma = create_video_chapa(
            loader=self.loader,
            render=self.render,
            video_path="assets/videos/flexao_tapete2.mp4",
            position=(-1325, 2600, 260),
            scale=90
        )

        self.plataforma = create_video_chapa(
            loader=self.loader,
            render=self.render,
            video_path="assets/videos/polichinelo_corretoSempre.mp4",
            position=(875, 2700, 260),
            scale=90
        )

        self.plataforma = create_video_chapa(
            loader=self.loader,
            render=self.render,
            video_path="assets/videos/agachamento_tapete.mp4",
            position=(3075, 2700, 260),
            scale=90
        )

        # Carregar suporte tablet + video tablet
        self.plataforma = create_suporte_and_tablet_video(
            loader=self.loader,
            render=self.render,
            video_path="assets/videos/flexao.mp4",
            position=(-1600, 2950, 0),
            scale=0.5,
            suporte_scale_z=500,
            tablet_position_z=250,
        )
        # Carregar suporte tablet + video tablet
        self.plataforma = create_suporte_and_tablet_video(
            loader=self.loader,
            render=self.render,
            video_path="assets/videos/polichinelo.mp4",
            position=(600, 2950, 0),
            scale=0.5,
            suporte_scale_z=1300,
            tablet_position_z=750,
        )
        # Carregar suporte tablet + video tablet
        self.plataforma = create_suporte_and_tablet_video(
            loader=self.loader,
            render=self.render,
            video_path="assets/videos/agachamento.mp4",
            position=(2800, 2950, 0),
            scale=0.5,
            suporte_scale_z=1300,
            tablet_position_z=750,
        )


        # 🚶‍♂️ Pessoas
        self.personagem1 = create_personagens(
            self.render,
            (-1480, 2750, 250),
            6,
            "assets/push_up.bam",
        )

        self.personagem2 = create_personagens(
            self.render,
            (920, 2700, 250),
            600,
         
            "assets/jumping_jacks.bam",
        )
        
        self.personagem3 = create_personagens(
            self.render,
            (3025, 2700, 250),
            600,
            "assets/agachamento.bam",
        )




        #####################




        # 🎮 Controle de teclas
        self.key_map = {
            "w": False, "s": False,
            "a": False, "d": False,
            "space": False, "control": False,
            "p": False,
            "arrow-up": False, "arrow-down": False, "arrow-left": False, "arrow-right": False
        }

        # ⌨️ Mapear teclas
        for key in ["w","s","a","d","space", "control", "p", "arrow_up", "arrow_down", "arrow_left", "arrow_right"]:
            self.accept(key, self.update_key, [key.replace("_", "-"), True])
            self.accept(f"{key}-up", self.update_key, [key.replace("_", "-"), False])    

      

        # ⎋ Fechar
        self.accept("escape", sys.exit)

        # 🚀 Parâmetros
        self.speed = 1500
        self.velocidade = 500
        self.mouse_sensitivity = 0.05

        # 🎯 Centro da janela para resetar mouse
        self.center_x = int(self.win.getProperties().getXSize() / 2)
        self.center_y = int(self.win.getProperties().getYSize() / 2)

        self.last_mouse_x = self.center_x
        self.last_mouse_y = self.center_y

        # Centralizar mouse no começo
        self.win.movePointer(0, self.center_x, self.center_y)

        # ⏱️ Timer para calcular dt corretamente
        self.last_time = time.perf_counter()

        # 📦 Task para atualizar câmera
        self.taskMgr.add(self.update_camera, "update_camera")
        self.taskMgr.add(self.update_movement, "update_movement")
        self.taskMgr.add(self.mover, "mover")


    def update_key(self, key, value):
        self.key_map[key] = value


    def update_camera(self, task):
        if self.mouseWatcherNode.hasMouse():
            md = self.win.getPointer(0)
            x = md.getX()
            y = md.getY()

            # 🧠 Calcula delta do mouse
            dx = x - self.last_mouse_x
            dy = y - self.last_mouse_y

            # 🔄 Atualiza rotação da câmera
            self.camera.setH(self.camera.getH() - dx * self.mouse_sensitivity)
            self.camera.setP(self.camera.getP() - dy * self.mouse_sensitivity)

            # 🔥 Limita o pitch para não virar de cabeça pra baixo (opcional)
            self.camera.setP(max(-90, min(90, self.camera.getP())))

        self.win.movePointer(0, self.center_x, self.center_y)
        self.last_mouse_x = self.center_x
        self.last_mouse_y = self.center_y

        return task.cont

    def update_movement(self, task):
        dt = globalClock.getDt()

        direcao = Vec3(0, 0, 0)
        quat = self.camera.getQuat()

        if self.key_map["w"]:
            direcao += quat.getForward()
        if self.key_map["s"]:
            direcao -= quat.getForward()
        if self.key_map["a"]:
            direcao -= quat.getRight()
        if self.key_map["d"]:
            direcao += quat.getRight()
        if self.key_map["space"]:
            direcao += quat.getUp()
        if self.key_map["control"]:
            direcao -= quat.getUp()

        if direcao.length() > 0:
            direcao.normalize()
            self.camera.setPos(self.camera.getPos() + direcao * self.speed * dt)

        return task.cont

    
    def print_camera_position(self):
        pos = self.camera.getPos()
        hpr = self.camera.getHpr()
        #print(f"📍 Posição da câmera: X={pos.getX():.2f}, Y={pos.getY():.2f}, Z={pos.getZ():.2f}")
        #print(f"🎯 Rotação da câmera: H={hpr.getX():.2f}, P={hpr.getY():.2f}, R={hpr.getZ():.2f}")

    def mover(self, task):
        # ⏱️ Calcular dt baseado no tempo real
        current_time = time.perf_counter()
        dt = current_time - self.last_time
        self.last_time = current_time

        # Evitar saltos gigantes em caso de travamento
        dt = min(dt, 0.05)  # 50 ms no máximo (~20 FPS mínimo)

        direcao = Vec3(0, 0, 0)
        if self.key_map["arrow-down"]:
            direcao += Vec3(0, 1, 0)
        if self.key_map["arrow-up"]:
            direcao += Vec3(0, -1, 0)
        if self.key_map["arrow-left"]:
            direcao += Vec3(1, 0, 0)
        if self.key_map["arrow-right"]:
                direcao += Vec3(-1, 0, 0)

        pessoa = self.personagem1
        nome_anim = pessoa.getAnimNames()[0] if pessoa.getAnimNames() else None

        if direcao.length() > 0:
            direcao.normalize()
            nova_pos = pessoa.getPos() + direcao * self.velocidade * dt
            pessoa.setPos(nova_pos)

            if nome_anim and not pessoa.getCurrentAnim():
                pessoa.loop(nome_anim)

            angulo = direcao.signedAngleDeg(Vec3(0, -1, 0), Vec3(0, 0, -1))
            pessoa.setH(angulo)

        #else:
            #if nome_anim and pessoa.getCurrentAnim():
                #pessoa.stop()

        return task.cont




app = MyApp()
app.run()
