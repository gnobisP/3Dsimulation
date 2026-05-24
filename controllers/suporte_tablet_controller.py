def create_suporte_tablet(loader, render, position, scale):
    suporte = loader.loadModel("assets/suporteTablet.bam")
    suporte.reparentTo(render)
    suporte.setPos(*position)
    suporte.setScale(scale)
    suporte.setTextureOff(1)
    suporte.setMaterialOff(1)
    suporte.setColorScale(0, 0, 0, 1)
    suporte.setLightOff()
    return suporte