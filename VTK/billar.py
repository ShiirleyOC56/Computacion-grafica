import vtk

#mesa - base -textura

def crearBase(x,y,z,textura,Xlength,Ylength,Zlength,rotacionX,rotacionY,rotacionZ):
    reader = vtk.vtkJPEGReader()
    reader.SetFileName(textura)

    texturebase=vtk.vtkTexture()
    if vtk.VTK_MAJOR_VERSION <= 5:
        texturebase.SetInput(reader.GetOutput())
    else:
        texturebase.SetInputConnection(reader.GetOutputPort())
    texturebase.InterpolateOn()

    #mesa - base - cubo

    base = vtk.vtkCubeSource()
    base.SetXLength(Xlength)
    base.SetYLength(Ylength)
    base.SetZLength(Zlength)
    base.Update()

    # Map texture coordinates
    map_to_plane = vtk.vtkTextureMapToPlane()
    if vtk.VTK_MAJOR_VERSION <= 5:
        map_to_plane.SetInput(base.GetOutput())
    else:
        map_to_plane.SetInputConnection(base.GetOutputPort())

    # Create mapper and set the mapped texture as input
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(map_to_plane.GetOutput())
    else:
        mapper.SetInputConnection(map_to_plane.GetOutputPort())

    #actor
    base_actor = vtk.vtkActor()
    base_actor.SetMapper(mapper)
    base_actor.SetPosition(x,y,z)
    base_actor.SetTexture(texturebase)
    base_actor.RotateX(rotacionX)
    base_actor.RotateY(rotacionY)
    base_actor.RotateZ(rotacionZ)
    return base_actor

def crear_patita(posx,posy,posz,textura,radio,height):
    reader = vtk.vtkJPEGReader()
    reader.SetFileName(textura)

    texturebase=vtk.vtkTexture()
    if vtk.VTK_MAJOR_VERSION <= 5:
        texturebase.SetInput(reader.GetOutput())
    else:
        texturebase.SetInputConnection(reader.GetOutputPort())
    texturebase.InterpolateOn()

    cono = vtk.vtkConeSource()
    cono.SetRadius(radio)
    cono.SetHeight(height)
    cono.SetResolution(4)
    cono.Update()

    # Map texture coordinates
    map_to_plane = vtk.vtkTextureMapToPlane()
    if vtk.VTK_MAJOR_VERSION <= 5:
        map_to_plane.SetInput(cono.GetOutput())
    else:
        map_to_plane.SetInputConnection(cono.GetOutputPort())
    
    # Create mapper and set the mapped texture as input
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(map_to_plane.GetOutput())
    else:
        mapper.SetInputConnection(map_to_plane.GetOutputPort())
    
    #actor
    cono_actor = vtk.vtkActor()
    cono_actor.SetMapper(mapper)
    cono_actor.SetTexture(texturebase)
    cono_actor.SetPosition(posx,posy,posz)
    cono_actor.RotateY(45.0)
    cono_actor.RotateZ(-90.0)
    return cono_actor

def crearPelota(pos,textura,radio,velocidad):
    reader = vtk.vtkJPEGReader()
    reader.SetFileName(textura)

    texturebase=vtk.vtkTexture()
    if vtk.VTK_MAJOR_VERSION <= 5:
        texturebase.SetInput(reader.GetOutput())
    else:
        texturebase.SetInputConnection(reader.GetOutputPort())
    texturebase.InterpolateOn()

    sphere= vtk.vtkSphereSource()
    sphere.SetThetaResolution(50)
    sphere.SetRadius(radio)
    sphere.Update()


    # Map texture coordinates
    map_to_plane = vtk.vtkTextureMapToPlane()
    if vtk.VTK_MAJOR_VERSION <= 5:
        map_to_plane.SetInput(cono.GetOutput())
    else:
        map_to_plane.SetInputConnection(sphere.GetOutputPort())

    # Create mapper and set the mapped texture as input
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(map_to_plane.GetOutput())
    else:
        mapper.SetInputConnection(map_to_plane.GetOutputPort())

    sphere_actor=vtk.vtkActor()
    sphere_actor.SetMapper(mapper)
    sphere_actor.SetTexture(texturebase)
    sphere_actor.SetPosition(pos[0],pos[1],pos[2])
    # sphere_actor.GetProperty().SetColor(0, 1, 0.0)
    return sphere_actor

def crear_camara(pos):
    camera = vtk.vtkCamera()
    # camera_actor=vtk.vtkCameraActor()
    # camera.SetFocalPoint(10,10,10)
    #camera.SetPosition(0,sphere.pos[1],sphere.pos[1]*2.7)
    camera.SetPosition(pos[0],pos[1],pos[2])
    # camera_actor.SetCamera(camera)

    return camera

textura_mesa = "texturas/texturamesa.jpg"
textura_piso = "texturas/texturapiso.jpg"
textura_borde1 = "texturas/madera.jpeg"
textura_borde2 = "texturas/madera.jpeg"
textura_borde3 = "texturas/madera.jpeg"
textura_borde4 = "texturas/madera.jpeg"
textura_bola= "texturas/ball_texture.jpg"
#------------------------------------------------------------#
mesa = crearBase(0,10,0,textura_mesa,50,50,2,90.0,0.0,0.0)
piso = crearBase(0,-6,0,textura_piso,100,100,4,90.0,0.0,0.0)
borde_adelante = crearBase(0,11,26,textura_borde1,50,4,2,0.0,0.0,0.0)
borde_atras = crearBase(0,11,-26,textura_borde1,50,4,2,0.0,0.0,0.0)
borde_izquierda = crearBase(-26,11,0,textura_borde1,54,4,2,0.0,90.0,0.0)
borde_derecha = crearBase(26,11,0,textura_borde1,54,4,2,0.0,90.0,0.0)
pata1 = crear_patita(21,1,21,textura_borde1,5,18)#derecha adelante
pata2 = crear_patita(-21,1,-21,textura_borde1,5,18)# izquierda atras
pata3 = crear_patita(21,1,-21,textura_borde1,5,18)#"derecha atras"
pata4 = crear_patita(-21,1,21,textura_borde1,5,18)#izquierda adelante
bola= crearPelota([0,12,0],textura_bola,1,[0,0,0])
camara= crear_camara([110,50,0])
#renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(mesa)
renderer.AddActor(piso)
renderer.AddActor(borde_adelante)
renderer.AddActor(borde_atras)
renderer.AddActor(borde_izquierda)
renderer.AddActor(borde_derecha)
renderer.AddActor(pata1)
renderer.AddActor(pata2)
renderer.AddActor(pata3)
renderer.AddActor(pata4)
renderer.AddActor(bola)
renderer.SetActiveCamera(camara)
#renderWindow
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Simple VTK scene")
render_window.SetSize(800, 800)
render_window.AddRenderer(renderer)

#interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()