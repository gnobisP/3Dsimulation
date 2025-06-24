from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import AmbientLight, DirectionalLight, VBase4
from direct.actor.Actor import Actor
import sys
import random
from panda3d.core import Vec3
from panda3d.core import loadPrcFileData, WindowProperties, Vec3
from direct.showbase.ShowBase import ShowBase

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
        self.plataforma = self.loader.loadModel("models/Bus-Stop.obj")
        self.plataforma.reparentTo(self.render)
        self.plataforma.setPos(0, 0, 0)
        self.plataforma.setScale(1)

        # 🚶‍♂️ Gerar várias pessoas na cena
        self.pessoas = []

        for i in range(10):
            pessoa = Actor("models/man.egg")
            pessoa.reparentTo(self.render)

            # 🎲 Posicionamento aleatório na plataforma
            if(i==0):
                x = 0
                y = 0
                z = 279
            else:
                x = random.uniform(0, 9310.07)
                y = random.uniform(0, 4742.64)
                z = 279

            pessoa.setPos(x, y, z)
            pessoa.setScale(75)

            # 🔍 Obter a primeira animação disponível
            animacoes = pessoa.getAnimNames()
            print(len(animacoes))
            primeira = animacoes[0]

            # 🕒 Definir o tempo de loop (ex.: 1 segundo)
            tempo_inicio = 0
            tempo_fim = 1.2  # segundos (ajuste como quiser)

            # 🚧 Pega a duração total da animação (ajuste conforme sua animação)
            duracao_total = 8  # 🔧 exemplo, ajuste para sua animação

            # 📈 Pega número de frames
            total_frames = pessoa.getNumFrames(primeira)

            # 🔥 Função para fazer o loop parcial
            def loop_parcial(task, p=pessoa):
                tempo = task.time % (tempo_fim - tempo_inicio)
                t_normalizado = tempo / (tempo_fim - tempo_inicio)
                frame = int(t_normalizado * total_frames * (tempo_fim / duracao_total))
                frame = min(frame, total_frames - 1)
                p.pose(primeira, frame)
                return task.cont

            # 🚀 Iniciar o loop parcial
            self.taskMgr.add(loop_parcial, f"loop_parcial_{i}")
            # 🚀 Adicionar tarefa de movimento
            # 🚀 Adicionar tarefa de movimento
            self.taskMgr.add(self.mover, "mover")

            self.pessoas.append(pessoa)


        # 🎮 Controle de teclas
        self.key_map = {
            "forward": False, "backward": False,
            "left": False, "right": False,
            "up": False, "down": False,
            "p": False,
            "arrow-up": False, "arrow-down": False, "arrow-left": False, "arrow-right": False
        }

        # ⌨️ Mapear teclas
        self.accept("w", self.update_key, ["forward", True])
        self.accept("w-up", self.update_key, ["forward", False])

        self.accept("s", self.update_key, ["backward", True])
        self.accept("s-up", self.update_key, ["backward", False])

        self.accept("a", self.update_key, ["left", True])
        self.accept("a-up", self.update_key, ["left", False])

        self.accept("d", self.update_key, ["right", True])
        self.accept("d-up", self.update_key, ["right", False])

        self.accept("space", self.update_key, ["up", True])
        self.accept("space-up", self.update_key, ["up", False])

        self.accept("control", self.update_key, ["down", True])
        self.accept("control-up", self.update_key, ["down", False])

        self.accept("p", self.update_key, ["p", True])
        self.accept("p-up", self.update_key, ["p", False])

        self.accept("arrow_up", self.update_key, ["arrow-up", True])
        self.accept("arrow_up-up", self.update_key, ["arrow-up", False])

        self.accept("arrow_down", self.update_key, ["arrow-down", True])
        self.accept("arrow_down-up", self.update_key, ["arrow-down", False])

        self.accept("arrow_left", self.update_key, ["arrow-left", True])
        self.accept("arrow_left-up", self.update_key, ["arrow-left", False])

        self.accept("arrow_right", self.update_key, ["arrow-right", True])
        self.accept("arrow_right-up", self.update_key, ["arrow-right", False])


        # ⎋ Fechar
        self.accept("escape", sys.exit)

        # 🏃 Velocidade
        self.speed = 1500

        # 🖱️ Sensibilidade do mouse
        self.mouse_sensitivity = 0.05

        # 🎯 Centro da janela para resetar mouse
        self.center_x = int(self.win.getProperties().getXSize() / 2)
        self.center_y = int(self.win.getProperties().getYSize() / 2)

        self.last_mouse_x = self.center_x
        self.last_mouse_y = self.center_y

        # Centralizar mouse no começo
        self.win.movePointer(0, self.center_x, self.center_y)

        # 📦 Task para atualizar câmera
        self.taskMgr.add(self.update_camera, "update_camera")
        self.taskMgr.add(self.update_movement, "update_movement")


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

        if self.key_map["forward"]:
            direcao += quat.getForward()
        if self.key_map["backward"]:
            direcao -= quat.getForward()
        if self.key_map["left"]:
            direcao -= quat.getRight()
        if self.key_map["right"]:
            direcao += quat.getRight()
        if self.key_map["up"]:
            direcao += quat.getUp()
        if self.key_map["down"]:
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
        dt = globalClock.getDt()  # Tempo entre frames

        velocidade = 50  # unidades por segundo

        direcao = Vec3(0, 0, 0)

        if self.key_map["arrow-down"]:
            direcao += Vec3(0, 1, 0)
        if self.key_map["arrow-up"]:
            direcao += Vec3(0, -1, 0)
        if self.key_map["arrow-left"]:
           direcao += Vec3(1, 0, 0)
        if self.key_map["arrow-right"]:
           direcao += Vec3(-1, 0, 0)

        if direcao.length() > 0:
            direcao.normalize()
            pos = self.pessoas[0].getPos()
            nova_pos = pos + direcao * velocidade * dt
            self.pessoas[0].setPos(nova_pos)

            # 🔄 Rotacionar na direção do movimento (opcional)
            angulo = direcao.signedAngleDeg(Vec3(0, -1, 0), Vec3(0, 0, -1))
            self.pessoas[0].setH(angulo)

        return task.cont



app = MyApp()
app.run()
