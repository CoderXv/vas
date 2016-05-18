__author__ = 'user'


# from PyQt4.QtCore import *
from PyQt4.QtGui import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk import *
from MraImageDisplayWindow import MraImageDisplayWindow
from VesselDisplayWindow import VesselDisplayWindow
from PlottingBoard import PlottingBoard
from SegmentationAnalyseWindow import SegmentationAnalyseWindow


class PatientImageViewer(QFrame):
    """
        ***************************************
            MraImgWin    *    vesselDisWin
        ***************************************
           plottingBoard *    segAnaWin
        ***************************************
    """
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.width = 0
        self.height = 0

        self.parent = parent

        self.analyseAreaLayout = QGridLayout(self)
        self.mraImageDisplayWindow = MraImageDisplayWindow()
        self.vesselDisplayWindow = VesselDisplayWindow()
        self.plottingBoard = PlottingBoard()
        self.segmentationAnalyseWindow = SegmentationAnalyseWindow(self)

        self.analyseAreaLayout.addWidget(self.mraImageDisplayWindow, 0, 0)
        self.analyseAreaLayout.addWidget(self.vesselDisplayWindow, 0, 1)
        self.analyseAreaLayout.addWidget(self.plottingBoard, 1, 0)
        self.analyseAreaLayout.addWidget(self.segmentationAnalyseWindow, 1, 1)
        self.analyseAreaLayout.setSpacing(0)
        self.analyseAreaLayout.setMargin(0)

        self.plottingBoard.setFixedHeight(440)
        self.segmentationAnalyseWindow.setFixedHeight(440)

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def update_vessel_img(self, index, status):
        self.vesselDisplayWindow.update_vessel_graph(index, status)

    def update_mri_image(self, img, flag, vessel_data_seq):
        self.mraImageDisplayWindow.set_mri_image(img, flag, vessel_data_seq)

    def update_vessel_ref_data(self, ref_data, flag):
        self.vesselDisplayWindow.load_ref_data(ref_data, flag)

    def update_vessel_point(self, point_path_seq, flag):
        self.segmentationAnalyseWindow.update_point_data(point_path_seq, flag)

    def pass_evaluated_vessel_to_renderer(self, path_dir):
        self.vesselDisplayWindow.update_evaluated_vessel_file(path_dir)

    def trans_ds_index_to_button(self, ds_index, ref_flag, ds_name):
        self.segmentationAnalyseWindow.update_ds_index(ds_index, ref_flag, ds_name)

    def interactor_initialization(self):
        self.mraImageDisplayWindow.interactor_initialization()
        self.vesselDisplayWindow.interactor_initialization()
        self.segmentationAnalyseWindow.sub_vtk_render_initialization()

    def pass_vessel_to_be_evaluated(self, single_path_dir, vessel_number):
        self.parent.pass_vessel_to_be_evaluated(single_path_dir, vessel_number)

    def store_vessel_to_be_evaluated(self, single_path_dir, ds_name, vessel_file_name, vessel_num):
        self.parent.store_vessel_to_be_evaluated(single_path_dir, ds_name, vessel_file_name, vessel_num)

    def update_info_board(self):
        self.parent.update_info_board()

    def load_vessel_to_be_evaluated(self, ds_name, vessel_num, file_name):
        return self.parent.load_vessel_to_be_evaluated(ds_name, vessel_num, file_name)

    def load_ref_data(self, ds_name, vessel_num):
        return self.parent.load_ref_data(ds_name, vessel_num)
        # return self.parent.get_the_ref_data_of_dataset_by_index(ds_name, vessel_num)
