from panda3d.core import WindowProperties
from panda3d.core import Vec3

class CameraController:
    def __init__(self, base, key_map, speed=1500, mouse_sensitivity=0.05):
        self.base = base
        self.camera = base.camera
        self.mouse_sensitivity = mouse_sensitivity
        self.key_map = key_map
        self.speed = speed 

        # Centraliza o mouse
        props = base.win.getProperties()
        self.center_x = int(props.getXSize() / 2)
        self.center_y = int(props.getYSize() / 2)
        base.win.movePointer(0, self.center_x, self.center_y)

        self.last_mouse_x = self.center_x
        self.last_mouse_y = self.center_y

        # Configurações iniciais da janela
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_confined)
        base.win.requestProperties(props)

    def update(self, dt):
        if self.base.mouseWatcherNode.hasMouse():
            md = self.base.win.getPointer(0)
            x = md.getX()
            y = md.getY()

            dx = x - self.last_mouse_x
            dy = y - self.last_mouse_y

            # Atualiza a rotação da câmera
            self.camera.setH(self.camera.getH() - dx * self.mouse_sensitivity)
            self.camera.setP(self.camera.getP() - dy * self.mouse_sensitivity)
            self.camera.setP(max(-90, min(90, self.camera.getP())))

            # Centraliza novamente o mouse
            self.base.win.movePointer(0, self.center_x, self.center_y)
            self.last_mouse_x = self.center_x
            self.last_mouse_y = self.center_y

        self.update_movement(dt)

    def update_movement(self, dt):
        direcao = Vec3(0, 0, 0)
        quat = self.camera.getQuat()

        if self.key_map.get("w"):
            direcao += quat.getForward()
        if self.key_map.get("s"):
            direcao -= quat.getForward()
        if self.key_map.get("a"):
            direcao -= quat.getRight()
        if self.key_map.get("d"):
            direcao += quat.getRight()
        if self.key_map.get("space"):
            direcao += quat.getUp()
        if self.key_map.get("control"):
            direcao -= quat.getUp()

        if direcao.length() > 0:
            direcao.normalize()
            self.camera.setPos(self.camera.getPos() + direcao * self.speed * dt)

