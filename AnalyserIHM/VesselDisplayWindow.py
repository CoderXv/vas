__author__ = 'xuhaoshen'
import vtk
import sys
# from PyQt4.QtCore import *
from PyQt4.QtGui import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt4.QtCore import *
from AnalyserContext.VesselFileReader import VesselFileReader


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
    if sys.hexversion == 34015728:
        mapper.SetInput(grid)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor


class VesselDisplayWindow(QFrame):
    """
        This class is used for reading the vessel coordinates and then display it in the widget by vtk kit.
    """
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.ref_data_seq = None  # store the four ref data ( vessel file reader)
        self.actor_dict = {}
        self.vesselDisplayWindowLayout = QVBoxLayout(self)
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.vesselDisplayWindowLayout.addWidget(self.vtkWidget)
        self.vesselDisplayWindowLayout.setSpacing(0)
        self.vesselDisplayWindowLayout.setMargin(0)

        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(122.0/255, 140.0/255, 153.0/255)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.show()

    def interactor_initialization(self):
        self.iren.Initialize()

    def load_ref_data(self, ref_data_seq, flag):
        self.ren.RemoveAllViewProps()
        ref_available = flag
        if ref_available:
            self.ref_data_seq = ref_data_seq
            actor_seq = []

            for ref_data in ref_data_seq:
                print ref_data
                # init the reader ,store the data.
                actor = create_vessel_actor(ref_data)
                actor.GetProperty().SetColor(255, 0, 0)  # red for reference vessels.
                actor_seq.append(actor)

            self.actor_dict["vessel0"] = actor_seq[0]
            self.actor_dict["vessel1"] = actor_seq[1]
            self.actor_dict["vessel2"] = actor_seq[2]
            self.actor_dict["vessel3"] = actor_seq[3]

            for actor in actor_seq:
                self.ren.AddActor(actor)
        else:
            pass

        self.ren.ResetCamera()
        self.iren.Initialize()

    def update_evaluated_vessel_file(self, path_dir):
        path_dir = path_dir
        actor_seq = []
        for evaluated_path in path_dir:
            vessel_file_reader = VesselFileReader()
            vessel_file_reader. parse_vessel_file(evaluated_path)
            vessel_file_reader.do_parse_vessel_file()
            actor = create_vessel_actor(vessel_file_reader)
            actor.GetProperty().SetColor(255, 250, 250)  # snow vessel in evaluated files.
            actor_seq.append(actor)
        for actor in actor_seq:
            self.ren.AddActor(actor)

    def update_vessel_graph(self, index, status):
        index = index
        status = status

        if status == Qt.Checked:
            self.add_vessel(index)
        else:
            self.delete_vessel(index)

        return

    def add_vessel(self, index):
        self.ren.RemoveAllViewProps()
        actor = create_vessel_actor(self.ref_data_seq[index - 1])

        if index == 1:
            actor.GetProperty().SetColor(250, 0, 0)
            self.actor_dict["vessel0"] = actor
        elif index == 2:
            actor.GetProperty().SetColor(255, 0, 0)
            self.actor_dict["vessel1"] = actor
        elif index == 3:
            actor.GetProperty().SetColor(255, 0, 0)
            self.actor_dict["vessel2"] = actor
        elif index == 4:
            actor.GetProperty().SetColor(255, 0, 0)
            self.actor_dict["vessel3"] = actor

        for actor_name in self.actor_dict:
            self.ren.AddActor(self.actor_dict[actor_name])

        self.ren.ResetCamera()
        self.iren.Initialize()

        print "add vessel%d" % (index - 1)
        return

    def delete_vessel(self, index):
        self.ren.RemoveAllViewProps()

        if index == 1:
            del self.actor_dict["vessel0"]
        elif index == 2:
            del self.actor_dict["vessel1"]
        elif index == 3:
            del self.actor_dict["vessel2"]
        elif index == 4:
            del self.actor_dict["vessel3"]

        for actor_name in self.actor_dict:
            self.ren.AddActor(self.actor_dict[actor_name])

        self.ren.ResetCamera()
        self.iren.Initialize()

        print "del vessel%d" % (index - 1)
        return
