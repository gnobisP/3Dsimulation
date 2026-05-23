from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import AmbientLight, DirectionalLight, VBase4
from direct.actor.Actor import Actor
import sys
import random
from panda3d.core import Vec3
from panda3d.core import loadPrcFileData, WindowProperties, Vec3
from direct.showbase.ShowBase import ShowBase
import time

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
        self.plataforma = self.loader.loadModel("assets/cenario0.obj")
        self.plataforma.reparentTo(self.render)
        self.plataforma.setPos(0, 0, 0)
        self.plataforma.setScale(1000)
        
        # Caregar tablet
        tablet = self.loader.loadModel("assets/tabletPronto.bam")
        tablet.reparentTo(self.render)
        tablet.setPos(0, 0, 0)
        tablet.setScale(1000)

        self.plataforma.setHpr(90,90,0)

        # 🚶‍♂️ Pessoas
        self.pessoas = []
        for i in range(100):
            pessoa = Actor("assets/push_up.bam")
            pessoa.reparentTo(self.render)

            if i == 0:
                x, y, z = 0, 0, 1500
            else:
                x = random.uniform(0, 9310.07)
                y = random.uniform(0, 4742.64)
                z = 1500

            pessoa.setPos(x, y, z)
            pessoa.setScale(1)

            animacoes = pessoa.getAnimNames()
            print(len(animacoes))
            if animacoes:
                pessoa.loop(animacoes[0])

            self.pessoas.append(pessoa)

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
        print(f"📍 Posição da câmera: X={pos.getX():.2f}, Y={pos.getY():.2f}, Z={pos.getZ():.2f}")
        print(f"🎯 Rotação da câmera: H={hpr.getX():.2f}, P={hpr.getY():.2f}, R={hpr.getZ():.2f}")

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

        pessoa = self.pessoas[0]
        nome_anim = pessoa.getAnimNames()[0] if pessoa.getAnimNames() else None

        if direcao.length() > 0:
            direcao.normalize()
            nova_pos = pessoa.getPos() + direcao * self.velocidade * dt
            pessoa.setPos(nova_pos)

            if nome_anim and not pessoa.getCurrentAnim():
                pessoa.loop(nome_anim)

            angulo = direcao.signedAngleDeg(Vec3(0, -1, 0), Vec3(0, 0, -1))
            pessoa.setH(angulo)

        else:
            if nome_anim and pessoa.getCurrentAnim():
                pessoa.stop()

        return task.cont




app = MyApp()
app.run() 
