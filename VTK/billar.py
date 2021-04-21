import vtk

#mesa - base -textura
reader = vtk.vtkJPEGReader()
reader.SetFileName("texturas/texturabase.jpg")

texturebase=vtk.vtkTexture()
if vtk.VTK_MAJOR_VERSION <= 5:
    texturebase.SetInput(reader.GetOutput())
else:
    texturebase.SetInputConnection(reader.GetOutputPort())
texturebase.InterpolateOn()

#mesa - base - cubo

base = vtk.vtkCubeSource()
base.SetXLength(20)
base.SetYLength(1)
base.SetZLength(20)
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
#sphere_actor.GetProperty().SetColor(0, 1, 0.0)
base_actor.SetTexture(texturebase)

#renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(base_actor)


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
