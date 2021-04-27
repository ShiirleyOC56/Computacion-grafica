import vtk

class CubeObject:
    def __init__(self,pos,textura,medidas,rotaciones):
        self.pos=pos
        self.textura=textura
        self.medidas=medidas
        self.rotaciones=rotaciones
        self.actor=None
    
    def crearMesa(self):
        reader = vtk.vtkJPEGReader()
        reader.SetFileName(self.textura)

        texturebase=vtk.vtkTexture()
        if vtk.VTK_MAJOR_VERSION <= 5:
            texturebase.SetInput(reader.GetOutput())
        else:
            texturebase.SetInputConnection(reader.GetOutputPort())
        texturebase.InterpolateOn()

        cube = vtk.vtkCubeSource()
        cube.SetXLength(self.medidas[0])
        cube.SetYLength(self.medidas[1])
        cube.SetZLength(self.medidas[2])
        cube.Update()

        # Map texture coordinates
        map_to_plane = vtk.vtkTextureMapToPlane()
        if vtk.VTK_MAJOR_VERSION <= 5:
            map_to_plane.SetInput(cube.GetOutput())
        else:
            map_to_plane.SetInputConnection(cube.GetOutputPort())

        # Create mapper and set the mapped texture as input
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(map_to_plane.GetOutput())
        else:
            mapper.SetInputConnection(map_to_plane.GetOutputPort())

        #actor
        base_actor = vtk.vtkActor()
        base_actor.SetMapper(mapper)
        base_actor.SetPosition(self.pos[0],self.pos[1],self.pos[2])
        base_actor.SetTexture(texturebase)
        base_actor.RotateX(self.rotaciones[0])
        base_actor.RotateY(self.rotaciones[1])
        base_actor.RotateZ(self.rotaciones[2])
        return base_actor

class ConoObject:
    def __init__(self,pos,textura,radio,height):
        self.pos=pos
        self.textura=textura
        self.radio=radio
        self.height=height
        self.actor=None
    
    def crearPata(self):
        reader = vtk.vtkJPEGReader()
        reader.SetFileName(self.textura)

        texturebase=vtk.vtkTexture()
        if vtk.VTK_MAJOR_VERSION <= 5:
            texturebase.SetInput(reader.GetOutput())
        else:
            texturebase.SetInputConnection(reader.GetOutputPort())
        texturebase.InterpolateOn()

        cono = vtk.vtkConeSource()
        cono.SetRadius(self.radio)
        cono.SetHeight(self.height)
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
        cono_actor.SetPosition(self.pos[0],self.pos[1],self.pos[2])
        cono_actor.RotateY(45.0)
        cono_actor.RotateZ(-90.0)
        return cono_actor

class SphereObject:
    def __init__(self,pos,radio,velocidad,masa,aceleracion,texturas):
        self.pos=pos
        self.radio=radio
        self.velocidad=velocidad
        self.u_velocidad=velocidad
        self.actor=None
        self.textura=texturas
        self.masa=masa
        self.aceleracion=aceleracion

    def crearPelota(self):
        reader = vtk.vtkJPEGReader()
        reader.SetFileName(self.textura)

        texturebase=vtk.vtkTexture()
        if vtk.VTK_MAJOR_VERSION <= 5:
            texturebase.SetInput(reader.GetOutput())
        else:
            texturebase.SetInputConnection(reader.GetOutputPort())
        texturebase.InterpolateOn()

        sphere= vtk.vtkSphereSource()
        sphere.SetThetaResolution(50)
        sphere.SetRadius(self.radio)
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
        sphere_actor.SetPosition(self.pos[0],self.pos[1],self.pos[2])
        # sphere_actor.GetProperty().SetColor(0, 1, 0.0)
        return sphere_actor

def CoeFriccion(pos):
    r = mt.sqrt(pos[0]**2 + pos[1]**2 +pos[2]**2)
    coef= mt.acos(pos[0]/r)
    result= mt.sin(coef)/mt.cos(coef)
    return result

def movement(caller,time_event):
    global time
    global velocidadBola
    if(time< 0.15):            
        esfera.u_velocidad[0] = esfera.velocidad[0]
        esfera.u_velocidad[2] = esfera.velocidad[2]
        ####la velocidad se guarda para cada eje en funcion
        esfera.pos[0]= esfera.pos[0] + esfera.velocidad[0]*time
        esfera.pos[2]= esfera.pos[2] + esfera.velocidad[2]*time
        ###se mueve la pelotita 
        co=0
        if(esfera.velocidad[0]<=0 or esfera.velocidad[2]<=0):
            co=-0.1
            ###si la pelota choca y va para abajo el co es negativo
        else:
            co=0.1
            ###si la pelota choca y va para arriba el co es positivo
        if (esfera.pos[0] <24) and (esfera.pos[0] > -24 ):
            ### si la pelota no ah chocado con los bordes de ancho de la mesa
            esfera.velocidad[0]=esfera.velocidad[0] - time*co
            #### se reduce la velocidad en x
        else: 
            esfera.velocidad[0]=- esfera.velocidad[0]
            ###si la pelota ha chocado se cambia de signo la velocidad, si va para arriba se vuelve positivo y si va para abajo negativo
            if(esfera.velocidad[0]<=0):
                ###si va para abajo se le reduce 0.5
                esfera.velocidad[0] += 0.5
            else:
                
                esfera.velocidad[0]-=0.5
                ###si va para arriba se le reduce 0.5
        if (esfera.pos[2] <24) and (esfera.pos[2] > -24 ):
             ### si la pelota no ah chocado con los bordes del laargo de la mesa
            esfera.velocidad[2]=esfera.velocidad[2]-time*co
            #### se reduce la velocidad en x
        else:
            esfera.velocidad[2]=-esfera.velocidad[2]
            if(esfera.velocidad[2]<=0):
                esfera.velocidad[2] += 0.5
            else:
                esfera.velocidad[2]-=0.5
        ###es lo mismo de arriba solo que en el eje z o velocidad[2]


        if(round(esfera.velocidad[0])==0 ):
            esfera.velocidad[0]=0
        if( round(esfera.velocidad[2])==0):
            esfera.velocidad[2]=0
        ###redondeara las velocidades

        esfera.actor.SetPosition(esfera.pos[0], esfera.pos[1], esfera.pos[2])   
    
        time += 0.0001
    else:
        interactor.DestroyTimer()

    render_window.Render()


def crear_camara(pos):
    camera = vtk.vtkCamera()
    # camera_actor=vtk.vtkCameraActor()
    # camera.SetFocalPoint(10,10,10)
    #camera.SetPosition(0,sphere.pos[1],sphere.pos[1]*2.7)
    camera.SetPosition(pos[0],pos[1],pos[2])
    # camera_actor.SetCamera(camera)

    return camera

#------------------------------------------------------------------------------------------------------------------
texturas=["texturas/texturamesa.jpg","texturas/texturapiso.jpg","texturas/madera.jpeg","texturas/ball_texture.jpg"]
piso = CubeObject([0,-6,0],texturas[1],[100,100,4],[90.0,0.0,0.0])
piso.actor=piso.crearMesa()
mesa = CubeObject([0,10,0],texturas[0],[50,50,2],[90.0,0.0,0.0])
mesa.actor=mesa.crearMesa()
#BORDES
bordeDelante = CubeObject([0,11,26],texturas[2],[50,4,2],[0.0,0.0,0.0])
bordeDelante.actor=bordeDelante.crearMesa()
bordeAtras = CubeObject([0,11,-26],texturas[2],[50,4,2],[0.0,0.0,0.0])
bordeAtras.actor=bordeAtras.crearMesa()
bordeIzquierda = CubeObject([-26,11,0],texturas[2],[54,4,2],[0.0,90.0,0.0])
bordeIzquierda.actor=bordeIzquierda.crearMesa()
bordeDerecha = CubeObject([26,11,0],texturas[2],[54,4,2],[0.0,90.0,0.0])
bordeDerecha.actor=bordeDerecha.crearMesa()
#PATAS
pata1 = ConoObject([21,1,21],texturas[2],5,18)
pata1.actor=pata1.crearPata()
pata2 = ConoObject([-21,1,-21],texturas[2],5,18)
pata2.actor=pata2.crearPata()
pata3 = ConoObject([21,1,-21],texturas[2],5,18)
pata3.actor=pata3.crearPata()
pata4 = ConoObject([-21,1,21],texturas[2],5,18)
pata4.actor=pata4.crearPata()
#BOLA
esfera=SphereObject([0,12,0],1,[0,0,0],5,10,texturas[3])
esfera.actor=esfera.crearPelota()
time=0
coef = 0.1
velocidadBola=[30,20]
esfera.velocidad[0]=velocidadBola[0]
esfera.velocidad[2]=velocidadBola[1]
camara= crear_camara([110,50,0])
#----------------------------------------------------------------

renderer = vtk.vtkRenderer()
renderer.SetBackground(0.0,0.0,0.0)
renderer.AddActor(piso.actor)
renderer.AddActor(mesa.actor)
renderer.AddActor(bordeDelante.actor)
renderer.AddActor(bordeAtras.actor)
renderer.AddActor(bordeIzquierda.actor)
renderer.AddActor(bordeDerecha.actor)
renderer.AddActor(pata1.actor)
renderer.AddActor(pata2.actor)
renderer.AddActor(pata3.actor)
renderer.AddActor(pata4.actor)
renderer.AddActor(esfera.actor)
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
interactor.CreateRepeatingTimer(1)
# print(od)

interactor.AddObserver("TimerEvent", movement)
interactor.Start()
