__author__ = 'user'
import vtk
# from PyQt4.QtCore import *
from PyQt4.QtGui import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk import *
# from AnalyserContext.VesselFileReader import VesselFileReader
import sys


def create_vessel_actor(ref_data):
    vessel_ref_data = ref_data
    points = vtk.vtkPoints()

    # insert each properties of points into obj.
    for i in range(vessel_ref_data.get_len_of_vassel_value()):
        x = vessel_ref_data.get_abscissa_value_at(i)
        y = vessel_ref_data.get_ordinate_value_at(i)
        z = vessel_ref_data.get_iso_value_at(i)
        points.InsertPoint(i, x, y, z)

    poly = vtk.vtkPolyVertex()
    poly.GetPointIds().SetNumberOfIds(vessel_ref_data.get_len_of_vassel_value())

    cont = 0
    while cont < vessel_ref_data.get_len_of_vassel_value():
        poly.GetPointIds().SetId(cont, cont)
        cont += 1

    grid = vtk.vtkUnstructuredGrid()
    grid.SetPoints(points)
    grid.InsertNextCell(poly.GetCellType(), poly.GetPointIds())

    mapper = vtk.vtkDataSetMapper()
    if sys.hexversion == 34015984:
        mapper.SetInputData(grid)
    elif sys.hexversion == 34015728:
        mapper.SetInput(grid)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor


def update_evaluated_vessel_file(path_data_seq):
    path_data_seq = path_data_seq
    actor_seq = []
    for ref_cl_data in path_data_seq:
        actor = create_vessel_actor(ref_cl_data)
        actor.GetProperty().SetColor(255, 0, 0)  # snow vessel in evaluated files.
        actor_seq.append(actor)
    return actor_seq


class MraImageDisplayWindow(QFrame):
    """
        This class is used for reading the selected mhd file and display it on the widget by vtk kit.
    """
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.opacityTransferFunction = vtkPiecewiseFunction()
        self.opacityTransferFunction.AddPoint(0, 0.0)
        self.opacityTransferFunction.AddPoint(1200, 0.0)
        self.opacityTransferFunction.AddPoint(1600, 0.7)
        self.opacityTransferFunction.AddPoint(2400, 0.7)


        self.colorTransferFunction = vtkColorTransferFunction()
        self.colorTransferFunction.AddRGBPoint(0, 0.0, 0.0, 1.0)
        self.colorTransferFunction.AddRGBPoint(800, 1.0, 0.0, 0.0)
        self.colorTransferFunction.AddRGBPoint(1200, 1.0, 1.0, 1.0)
        self.colorTransferFunction.AddRGBPoint(2000, 1.0, 1.0, 1.0)

        self.gradientTransferFunction = vtkPiecewiseFunction()
        self.gradientTransferFunction.AddPoint(0, 2.0)
        self.gradientTransferFunction.AddPoint(500, 2.0)
        self.gradientTransferFunction.AddSegment(600, 0.73, 900, 0.9)
        self.gradientTransferFunction.AddPoint(1300, 0.1)

        self.compositeFunction = vtkVolumeRayCastCompositeFunction()

        self.volumeProperty = vtkVolumeProperty()
        self.volumeProperty.SetColor(self.colorTransferFunction)
        self.volumeProperty.SetScalarOpacity(self.opacityTransferFunction)
        self.volumeProperty.SetGradientOpacity(self.gradientTransferFunction)

        self.volumeMapper = vtkVolumeRayCastMapper()
        self.volumeMapper.SetVolumeRayCastFunction(self.compositeFunction)

        self.volume = vtkVolume()

        self.mraImageDisplayWindowLayout = QVBoxLayout(self)
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.mraImageDisplayWindowLayout.addWidget(self.vtkWidget)
        self.mraImageDisplayWindowLayout.setSpacing(0)
        self.mraImageDisplayWindowLayout.setMargin(0)

        self.ren = vtkRenderer()
        self.ren.SetBackground(122.0 / 255, 140.0 / 255, 153.0 / 255)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

    def interactor_initialization(self):
        self.iren.Initialize()

    def set_mri_image(self, img, flag, vessel_data_seq):
        self.ren.RemoveAllViewProps()

        if vtk.VTK_MAJOR_VERSION <= 5:
            self.volumeMapper.SetInput(img)
        else:
            self.volumeMapper.SetInputData(img)

        self.volume.SetMapper(self.volumeMapper)
        self.volume.SetProperty(self.volumeProperty)

        if flag:
            actor_seq = update_evaluated_vessel_file(vessel_data_seq)
            for actor in actor_seq:
                self.ren.AddActor(actor)

        self.ren.AddVolume(self.volume)

        self.ren.ResetCamera()
        self.iren.Initialize()
