import vtk

#mesa - base -textura

def crearBase(x,y,z,textura,Xlength,Ylength,Zlength):
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
    return base_actor

textura_mesa = "texturas/texturamesa.jpg"
textura_piso = "texturas/texturapiso.jpg"
mesa = crearBase(0,50,0,textura_mesa,20,1,20)
piso = crearBase(0,-50,0,textura_piso,50,1,50)
#renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(mesa)
renderer.AddActor(piso)

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
