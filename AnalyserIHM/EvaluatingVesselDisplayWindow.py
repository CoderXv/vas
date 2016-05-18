#!/usr/bin/env python
import shutil

__author__ = 'xuhaoshen'

from PyQt4 import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk import *
import os
from AnalyserContext.VesselFileReader import VesselFileReader
from FilterSettingWindow import FilterSettingWindow


class EvaluatingVesselDisplayWindow(QFrame):
    """
        This class is used for displaying the vessel which is selected to be compared with the reference data.
        ============================
                        | buttton 1|
          vtkrenderer   | button  2|
                        |    ...   |
        ============================
    """
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        super(QFrame, self).__init__(parent)
        self.parent = parent
        self.buttonSize = QSize(40, 40)

        # -- init the component of the class.
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.vesselButtonPanel = QWidget()
        self.vesselLoadButton = QPushButton(self)
        self.startScoringButton = QPushButton(self)
        self.deleteButton = QPushButton(self)
        self.resetRendererButton = QPushButton(self)
        self.refAvailable = False
        self.targetVesselSelectedFlag = False  # TODO... temp change
        self.ds_name = None

        # -- set Icon of the qpushbutton
        button_size = QSize(40, 40)
        self.vesselLoadButton.setIcon(QIcon(":/open_vessel.png"))
        # self.vesselLoadButton.setFixedSize(40, 40)
        self.vesselLoadButton.setIconSize(button_size)
        self.vesselLoadButton.setFlat(True)
        self.vesselLoadButton.setShortcut('Ctrl+O')

        self.startScoringButton.setIcon(QIcon(":/start_scoring.png"))
        self.startScoringButton.setIconSize(button_size)
        self.startScoringButton.setFlat(True)

        self.deleteButton.setIcon(QIcon(":/delete.png"))
        self.deleteButton.setIconSize(button_size)
        self.deleteButton.setFlat(True)

        self.resetRendererButton.setIcon(QIcon(":/reset_renderer.png"))
        self.resetRendererButton.setIconSize(button_size)
        self.resetRendererButton.setFlat(True)

        # -- init the vtk render.
        self.ren = vtkRenderer()
        self.ren.SetBackground(122.0 / 255, 140.0 / 255, 153.0 / 255)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        # self.iren.Initialize()

        # -- ds_index
        self.ds_index = None

        # -- set the layout of the button panel.
        self.buttonPanelLayout = QGridLayout(self.vesselButtonPanel)
        self.buttonPanelLayout.addWidget(self.vesselLoadButton, 0, 0)
        self.buttonPanelLayout.addWidget(self.startScoringButton, 1, 0)
        self.buttonPanelLayout.addWidget(self.deleteButton, 2, 0)
        self.buttonPanelLayout.addWidget(self.resetRendererButton, 3, 0)
        self.vesselButtonPanel.setFixedWidth(45)

        # -- set the layout of the whole window.
        self.EvaluatingVesselWindowLayout = QHBoxLayout(self)
        self.EvaluatingVesselWindowLayout.addWidget(self.vtkWidget)
        self.EvaluatingVesselWindowLayout.addWidget(self.vesselButtonPanel)
        self.EvaluatingVesselWindowLayout.setSpacing(3)
        self.EvaluatingVesselWindowLayout.setMargin(6)

        self.connect(self.vesselLoadButton, SIGNAL("clicked()"), self.button_load_vessel_to_be_evaluated)
        self.connect(self.startScoringButton, SIGNAL("clicked()"), self.start_vessel_evaluate)
        self.connect(self.deleteButton, SIGNAL("clicked()"), self.auto_evaluate)
        self.connect(self.resetRendererButton, SIGNAL("clicked()"), self.remove_all_images)

        # self.show()

    def interactor_initialization(self):
        self.iren.Initialize()


    def update_ds_index(self, ds_index, ref_flag, ds_name):
        if self.ds_index != ds_index:
            self.ren.RemoveAllViewProps()
        self.ds_name = ds_name
        self.ds_index = ds_index

        self.refAvailable = ref_flag

    # -- By Now we just load all the txt files in the img00 folder for example.
    def button_load_vessel_to_be_evaluated(self):
        """
        pass the path of file to be evaluated to the program, then copy and save it into the certain dir.
        """
        if not self.refAvailable:
            reply = QMessageBox.question(None, "ERROR", "Load Vessel First Or Select Right Dataset!", QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return
        f_name = QFileDialog.getOpenFileName(self, 'Open File', '/home')
        self.update_evaluated_vessel_file(f_name)
        # self.load_vessel_to_be_evaluated

    def update_evaluated_vessel_file(self, single_path_dir):
        single_path_dir = single_path_dir
        self.targetVesselSelectedFlag = self.parent.get_board_check_status()
        if not self.targetVesselSelectedFlag:
            reply = QMessageBox.question(None, "ERROR", "Please Select Target Vessel First!", QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return
        vessel_number = self.parent.get_vessel_to_be_evaluated_from_board() - 1
        split_path = single_path_dir.split("/")
        filename = split_path[-1]
        username = os.environ['USERNAME']
        workspace_path = 'C:\Users\\' + username + '\Documents\CoronaryData_CTA\\'
        current_path = workspace_path + "\\" + self.ds_name + "\\" + "vessel" + str(vessel_number) + "\\" + filename
        single_path_dir.replace("/", "\\")
        shutil.copyfile(single_path_dir, current_path)
        # self.parent.pass_vessel_to_be_evaluated(single_path_dir, vessel_number)
        self.parent.store_vessel_to_be_evaluated(single_path_dir, self.ds_name, filename, vessel_number)
        self.parent.update_info_board()
        self.load_ref_data_and_evaluated_data(self.ds_name, vessel_number, filename)

    def remove_all_images(self):
        self.ren.RemoveAllViewProps()
        self.iren.Initialize()

    def auto_evaluate(self):
        dialog = FilterSettingWindow(self)
        dialog.exec_()

    def start_vessel_evaluate(self):
        if not self.refAvailable:
            reply = QMessageBox.question(None, "WARNING", "Please Load a dataset First!", QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                return
        if not self.targetVesselSelectedFlag:
            reply = QMessageBox.question(None, "ERROR", "Please Select Target Vessel First!", QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return
        print "evaluate start"
        # after evaluating the vessel, reset the flag
        self.reset_all()
        return

    def load_ref_data_and_evaluated_data(self, ds_name, vessel_num, file_name):
        vessel_to_be_evaluated_data = self.load_vessel_to_be_evaluated(ds_name, vessel_num, file_name)
        ref_data = self.load_ref_vessel_data(ds_name, vessel_num)
        vessel_actor = self.create_vessel_actor(vessel_to_be_evaluated_data)
        vessel_actor.GetProperty().SetColor(255, 0, 0)
        ref_actor = self.create_vessel_actor(ref_data)
        ref_actor.GetProperty().SetColor(0, 255, 127)
        self.ren.AddActor(vessel_actor)
        self.ren.AddActor(ref_actor)
        self.ren.ResetCamera()
        self.iren.Initialize()

    def reset_all(self):
        self.targetVesselSelectedFlag = None
        self.parent.reset_selected_vessel()

    def load_vessel_to_be_evaluated(self, ds_name, vessel_num, file_name):
        return self.parent.load_vessel_to_be_evaluated(ds_name, vessel_num, file_name)

    def load_ref_vessel_data(self, ds_name, vessel_num):
        return self.parent.load_ref_data(ds_name, vessel_num)

    @staticmethod
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









