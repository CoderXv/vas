__author__ = 'XuHaoshen'import platformfrom PatientImageViewer import PatientImageViewerfrom PyQt4.QtGui import *from PatientInformationBoard import PatientInformationBoardfrom PyQt4.QtCore import *from AnalyserTitleBar import AnalyserTitleBarfrom AnalyserStatusBar import AnalyserStatusBarfrom AnalyserToolBar import AnalyserToolBarclass AnalyserMainWindow(QFrame):    """    -Attributes:        -        *************************************************        *               analyserTitleBar                *        *************************************************        *               analyserToolBar                 *        *************************************************        *                  *                            *        *                  *                            *        * PatientInfoBoard *      PatientImgViewer      *        *                  *                            *        *                  *                            *        *************************************************        *            analyserStatusBar(preparing)       *        *************************************************    """    def __init__(self, controller):        QMainWindow.__init__(self)        # ----------------------------------------------------------        # positioning the Graphical tool in the middle of the screen        # ----------------------------------------------------------        self.mouseRelased = False        self.mousePressed = False        self.desktop = QApplication.desktop()        width = self.desktop.width()        height = self.desktop.height()        self.appWidth = 0.85 * width        self.appHeight = 0.85 * height        self.setMinimumWidth(self.appWidth)        self.setMinimumHeight(self.appHeight)        self.setGeometry((width - self.appWidth) / 2, (height - self.appHeight) / 2, self.appWidth, self.appHeight)        self.normalSize = True        self.mouseStat = True        # ----------------------------------------------------------        # configure the appearance of the graphic tool        # ----------------------------------------------------------        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)        self.setWindowOpacity(1.0)        self.setMouseTracking(True)        self.draw_background()        # ---------------------------------------------------------        # init the principal components of the main window.        # ---------------------------------------------------------        self.connector = controller        self.analyserTitleBar = AnalyserTitleBar(self)        self.analyserToolBar = AnalyserToolBar(self)        self.patientImageViewer = PatientImageViewer(self)        self.patientImageViewer.set_size(self.appWidth, self.appHeight)        self.patientInformationBoard = PatientInformationBoard(self, self.connector)        self.analyserStatusBar = AnalyserStatusBar(self)        # ---------------------------------------------------------        # construct IHM        # ---------------------------------------------------------        self.analyserWorkspace = QWidget()        central_layout = QHBoxLayout(self.analyserWorkspace)        central_layout.addWidget(self.patientInformationBoard)        central_layout.addWidget(self.patientImageViewer)        central_layout.setSpacing(0)        central_layout.setMargin(0)        self.analyserMainLayout = QVBoxLayout(self)        self.analyserMainLayout.addWidget(self.analyserTitleBar)        self.analyserMainLayout.addWidget(self.analyserToolBar)        self.analyserMainLayout.addWidget(self.analyserWorkspace)        self.analyserMainLayout.addWidget(self.analyserStatusBar)        self.analyserMainLayout.setSpacing(0)        self.analyserMainLayout.setMargin(0)        self.patientImageViewer.interactor_initialization()    def find_data_set_existed(self):        self.patientInformationBoard.find_data_set_existed()    def set_window_normal_size(self):        self.normalSize = True    def set_window_maximize_size(self):        self.normalSize = False    def get_app_width(self):        return self.appWidth    def get_app_height(self):        return self.appHeight    def get_analyser_title_bar(self):        return self.analyserTitleBar    def get_img_viewer(self):        return self.patientImageViewer    def get_info_board(self):        return self.patientInformationBoard    def set_table_content(self, points_path_seq, flag):        self.patientImageViewer.update_vessel_point(points_path_seq, flag)    def get_analyser_status_bar(self):        return self.analyserStatusBar    def get_mouse_stat(self):        return self.mouseStat    def trans_ds_index_to_button(self, ds_index, ref_flag, ds_name):        self.patientImageViewer.trans_ds_index_to_button(ds_index, ref_flag, ds_name)    def reset(self):        self.mouseRelased = False        self.mousePressed = False        pass    def pass_vessel_to_be_evaluated(self, single_path_dir, vessel_number):        self.patientInformationBoard.pass_vessel_to_patient_info_board(single_path_dir, vessel_number)    def store_vessel_to_be_evaluated(self, single_path_dir, ds_name, file_name, vessel_num):        self.connector.store_vessel_to_be_evaluated(single_path_dir, ds_name, file_name, vessel_num)    def update_info_board(self):        self.patientInformationBoard.update_info_board()    def load_vessel_to_be_evaluated(self, ds_name, vessel_num, file_name):        return self.connector.load_vessel_to_be_evaluated(ds_name, vessel_num, file_name)    def load_ref_data(self, ds_name, vessel_num):        return self.connector.get_the_ref_data_of_dataset_by_index(ds_name, vessel_num)    def draw_background(self):        # -- configure the background and the size of the graphical tool        pixmap = QPixmap(":/background.png")        palette = self.palette()        if self.normalSize:            palette.setBrush(QPalette.Background, QBrush(                pixmap.scaled(QSize(self.appWidth, self.appHeight), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))        else:            palette.setBrush(QPalette.Background, QBrush(                pixmap.scaled(QSize(self.desktop.width(), self.desktop.height()), Qt.IgnoreAspectRatio,                              Qt.SmoothTransformation)))        self.setPalette(palette)        self.setMask(pixmap.mask())        self.setAutoFillBackground(True)