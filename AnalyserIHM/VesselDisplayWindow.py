import vtk
import sys
from PyQt4.QtGui import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt4.QtCore import *
from AnalyserContext.VesselFileReader import VesselFileReader
import math
import time
import threading


class VesselDisplayWindow(QFrame):
    """
        This class is used for reading the vessel coordinates and then display it in the widget by vtk kit.
    """
    Signal_NoParameters = pyqtSignal()

    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.ref_data_seq = None  # store the four ref data ( vessel file reader)
        self.actor_dict = {}
        self.vesselDisplayWindowLayout = QVBoxLayout(self)
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.vesselDisplayWindowLayout.addWidget(self.vtkWidget)
        self.vesselDisplayWindowLayout.setSpacing(0)
        self.vesselDisplayWindowLayout.setMargin(0)

        # change mm to voxel
        self.xVoxelNum = 0.363281011581
        self.yVoxelNum = 0.363281011581
        self.zVoxelNum = 0.40000000596

        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(122.0 / 255, 140.0 / 255, 153.0 / 255)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.vessel_index = -1
        self.offset = 0
        self.vessel_image = None
        self.Signal_NoParameters.connect(self.update_renderer, Qt.QueuedConnection)

    @pyqtSlot()
    def update_renderer(self):
        print "update"
        self.render_volume_data(self.vessel_image)

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
                actor = self.create_vessel_actor(ref_data)
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
            vessel_file_reader.parse_vessel_file(evaluated_path)
            vessel_file_reader.do_parse_vessel_file()
            actor = self.create_vessel_actor(vessel_file_reader)
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
        actor = self.create_vessel_actor(self.ref_data_seq[index - 1])

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

    def create_vessel_actor(self, ref_data):
        vessel_ref_data = ref_data

        points = vtk.vtkPoints()

        # insert each properties of points into obj.
        for i in range(vessel_ref_data.get_len_of_vassel_value()):
            x = vessel_ref_data.get_abscissa_value_at(i) / self.xVoxelNum
            y = vessel_ref_data.get_ordinate_value_at(i) / self.yVoxelNum
            z = vessel_ref_data.get_iso_value_at(i) / self.zVoxelNum
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

    def do_reconstruct(self):
        # print vessel_index
        vessel_data = self.ref_data_seq[self.vessel_index]
        # init the coordinate cube : 512*512*272
        m_grid = []
        for i in range(512):
            row = []
            for j in range(512):
                col = []
                for k in range(272):
                    col.append(0)
                row.append(col)
            m_grid.append(row)
        print "start computing, please wait"

        for i in range(vessel_data.get_len_of_vassel_value()):
            # get the cordinate of ref_centerline and change it into voxel
            center_x = vessel_data.get_abscissa_value_at(i) / self.xVoxelNum
            center_y = vessel_data.get_ordinate_value_at(i) / self.yVoxelNum
            center_z = vessel_data.get_iso_value_at(i) / self.zVoxelNum
            center_radius = vessel_data.get_radius_value_at(i) / ((self.xVoxelNum + self.yVoxelNum + self.zVoxelNum) / 3)

            x_left_range = max(0, int(center_x - self.offset))
            x_right_range = min(512, int(center_x + self.offset))
            y_left_range = max(0, int(center_y - self.offset))
            y_right_range = min(512, int(center_y + self.offset))
            z_left_range = max(0, int(center_z - self.offset))
            z_right_range = min(272, int(center_z + self.offset))

            sigma = center_radius / 2

            # compute the reconstruct grid
            for x in xrange(x_left_range, x_right_range):
                for y in xrange(y_left_range, y_right_range):
                    for z in xrange(z_left_range, z_right_range):
                        distance = (x - center_x) ** 2 + (y - center_y) ** 2 + (z - center_z) ** 2
                        cal_radius = 2 * sigma ** 2

                        grey_scale_value = math.exp(-(distance / cal_radius)) * 1000

                        m_grid[x][y][z] = max(grey_scale_value, m_grid[x][y][z])

                        # then call the process function to show it
        print "end computing, start rendering"
        self.volume_data_process(m_grid)

    def reconstruct(self, vessel_index, offset=10):
        self.vessel_index = vessel_index
        self.offset = offset
        task = threading.Thread(None, self.do_reconstruct)
        task.start()

    def volume_data_process(self, m_grid):
        vessel_image = vtk.vtkImageData()
        vessel_image.SetDimensions(len(m_grid), len(m_grid[0]), len(m_grid[0][0]))
        # set the type of input
        if vtk.VTK_MAJOR_VERSION <= 5:
            vessel_image.SetNumberOfScalarComponents(1)
            vessel_image.SetScalarTypeToUnsignedChar()
        else:
            imageData.AllocateScalars(vtk.VTK_DOUBLE, 1)
        dims = vessel_image.GetDimensions()
        start_time = time.time()

        for x in range(dims[0]):
            for y in range(dims[1]):
                for z in range(dims[2]):
                    vessel_image.SetScalarComponentFromFloat(x, y, z, 0, m_grid[x][y][z])
        end_time = time.time()
        print "computing time:", (end_time - start_time)
        self.vessel_image = vessel_image
        self.Signal_NoParameters.emit()



    def render_volume_data(self, vtk_img_data):
        # Create transfer mapping scalar value to opacity
        opacity_transfer_function = vtk.vtkPiecewiseFunction()
        opacity_transfer_function.AddPoint(0, 0.0)
        opacity_transfer_function.AddPoint(50, 0.0)
        opacity_transfer_function.AddPoint(100, 0.8)
        opacity_transfer_function.AddPoint(1200, 0.8)

        # Create transfer mapping scalar value to color
        color_transfer_function = vtk.vtkColorTransferFunction()
        color_transfer_function.AddRGBPoint(0, 0.0, 0.0, 0.0)
        color_transfer_function.AddRGBPoint(50, 0.0, 0.0, 0.0)
        color_transfer_function.AddRGBPoint(100, 1.0, 0.0, 0.0)
        color_transfer_function.AddRGBPoint(1200, 1.0, 0.0, 0.0)

        # The property describes how the data will look
        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetColor(color_transfer_function)
        volume_property.SetScalarOpacity(opacity_transfer_function)
        volume_property.ShadeOff()
        volume_property.SetInterpolationTypeToLinear()

        # The mapper / ray cast function know how to render the data
        compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
        volume_mapper = vtk.vtkVolumeRayCastMapper()
        volume_mapper.SetVolumeRayCastFunction(compositeFunction)
        if vtk.VTK_MAJOR_VERSION <= 5:
            volume_mapper.SetInput(vtk_img_data)
        else:
            volume_mapper.SetInputData(vtk_img_data)
        volume_mapper.SetBlendModeToMaximumIntensity()

        # The volume holds the mapper and the property and
        # can be used to position/orient the volume
        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)

        self.ren.AddVolume(volume)
        self.ren.ResetCamera()
        self.iren.Initialize()
