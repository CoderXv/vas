from PyQt4.QtGui import *
from PyQt4.QtCore import *
from AnalyserIHM.ScoreBoardWindow import ScoreBoardWindow
from AnalyserIHM.EvaluatingVesselDisplayWindow import EvaluatingVesselDisplayWindow
import sys
__author__ = 'xuhaoshen'


class SegmentationAnalyseWindow(QFrame):
    """
        This class display the table containing vessel select checkbox, as well as showing the a, b, e, and s point
        co-ordinate, the score board displaying the score of the evaluating result, the widget to containing buttons
        to trigger the evaluating, and the widget to showing the result the evaluation as well as display the evaluated
        vessel-image.

        The view of segmentation analyse window is as follows:
        ============================================


                Vessel File Data Checkbox Table


        =============================================
        |                   |
        |                   |
        |                   |
        |   Scoring Board   |      EvaVesselDisWin
        |                   |
        |                   |
        =============================================
    """
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        super(QFrame, self).__init__(parent)
        self.parent = parent
        self.SegmentationAnalyseBox = QWidget()
        self.vesselsTableWidget = QTableWidget()
        self.vesselsTableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.vesselsTableWidget.verticalHeader().setResizeMode(QHeaderView.Stretch)
        self.points_path_seq = None
        # self.pos = QCursor()
        self.vesselsTableWidget.setColumnCount(6)
        self.vesselsTableWidget.setRowCount(5)
        self.verticalView = self.vesselsTableWidget.verticalHeader()
        self.setStyleSheet("background-color:transparent; border: 0px solid grey")

        # hidden the column/row's number and header.
        self.vesselsTableWidget.setStyleSheet("gridline-color:rgb(192,198,204)")  # alice blue
        self.verticalView.setHidden(True)
        self.verticalView.setClickable(False)
        self.horizonView = self.vesselsTableWidget.horizontalHeader()
        self.horizonView.setHidden(True)
        self.verticalView.setClickable(False)
        # self.vesselsTableWidget.setMouseTracking(True)
        # self.vesselsTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.vesselsTableWidget.setCursor(self.pos)

        # set the context in the table as read-only.
        self.vesselsTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.vesselsTableWidgetLayout = QVBoxLayout(self.vesselsTableWidget)
        self.vesselsTableWidgetLayout.setMargin(6)
        self.vesselsTableWidgetLayout.setSpacing(6)

        # remember all of the Gui in Qt can be handled in QWidget and BoxLayout.
        self.ScoreBoardWindow = ScoreBoardWindow(self)
        self.ScoreBoardWindow.setFixedHeight(280)
        self.ScoreBoardWindow.setFixedWidth(300)

        self.EvaluateVesselDisplayWindow = EvaluatingVesselDisplayWindow(self)
        self.EvaluateVesselDisplayWindow.setFixedHeight(280)

        self.SegAnaBoxLayout = QGridLayout(self)
        self.SegAnaBoxLayout.addWidget(self.vesselsTableWidget, 0, 0, 1, 0)
        self.SegAnaBoxLayout.addWidget(self.ScoreBoardWindow, 1, 0)
        self.SegAnaBoxLayout.addWidget(self.EvaluateVesselDisplayWindow, 1, 1)

        self.SegAnaBoxLayout.setSpacing(0)
        self.SegAnaBoxLayout.setMargin(5)

        self.ref_flag = None
        self.preVessel0Status = None
        self.preVessel1Status = None
        self.preVessel2Status = None
        self.preVessel3Status = None

        # reconstruct button
        self.buttonList = []
        self.construct_reconstruct_button(5)

        # set buttons' signal and slot settings.
        self.connect(self.buttonList[0], SIGNAL("clicked()"), self.reconstruct0)
        self.connect(self.buttonList[1], SIGNAL("clicked()"), self.reconstruct1)
        self.connect(self.buttonList[2], SIGNAL("clicked()"), self.reconstruct2)
        self.connect(self.buttonList[3], SIGNAL("clicked()"), self.reconstruct3)

    def construct_reconstruct_button(self, num):
        for i in xrange(num):
            button = QPushButton()
            button.setText("Reconstruct")
            self.buttonList.append(button)

    def construct_point_and_vessel(self, flag):
        column = 1
        row = 1
        point_seq = ["PointA", "PointB", "PointE", "PointS"]

        vessel_header_font = QFont("Helvetica", 11, QFont.AnyStyle, True)
        vessel_header_font.setBold(True)

        point_header_font = QFont("Helvetica", 11)
        point_header_font.setBold(True)
        # vertically, the vessel x.
        if flag:
            while row < 5:
                item = QTableWidgetItem("vessel %d" % (row-1))
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Checked)
                item.setFont(vessel_header_font)
                self.vesselsTableWidget.setItem(row, 0, item)
                row += 1

            # horizontally, the point a, b, e, s
            while column < 5:
                item = QTableWidgetItem("%s" % point_seq[column-1])
                item.setFont(point_header_font)
                self.vesselsTableWidget.setItem(0, column, item)
                column += 1

            # if checkboxes has been clicked, we call its function.
            self.vesselsTableWidget.itemClicked.connect(self.handle_item_clicked)
            # init the point status.
            self.ref_flag = True
            self.preVessel0Status = Qt.Checked
            self.preVessel1Status = Qt.Checked
            self.preVessel2Status = Qt.Checked
            self.preVessel3Status = Qt.Checked

            row = 1
            column = 5
            while row < 5:
                # button.setFlat(True)
                # print button.width()
                # print button.height()
                self.vesselsTableWidget.setCellWidget(row, column, self.buttonList[row-1])
                # self.connect(button, SIGNAL("triggered()"), self.reconstruct)
                row += 1
        else:
            while row < 5:
                item = QTableWidgetItem("vessel %d" % (row-1))
                self.vesselsTableWidget.setItem(row, 0, item)
                row += 1
            while column < 5:
                item = QTableWidgetItem("%s" % point_seq[column-1])
                self.vesselsTableWidget.setItem(0, column, item)
                column += 1
            self.ref_flag = False

    def update_ds_index(self, ds_index, ref_flag, ds_name):
        self.EvaluateVesselDisplayWindow.update_ds_index(ds_index, ref_flag, ds_name)

    def update_point_data(self, points_path_seq, flag):
        self.points_path_seq = points_path_seq
        # construct the layout of the table
        self.construct_point_and_vessel(flag)

        # it's list which elements are dict with keywords: point a,b,e,s.

        for each_vessel_point_path_seq in self.points_path_seq:
            # path_seq is an dict
            point_path_in_each_vessel = [each_vessel_point_path_seq["pointA"], each_vessel_point_path_seq["pointB"],
                                         each_vessel_point_path_seq["pointE"], each_vessel_point_path_seq["pointS"]]
            # four points in a sequence in order.
            # point_path_in_each_vessel
            row = 1
            # start from the first row.
            for each_path in point_path_in_each_vessel:
                content = open(each_path)
                cor = content.read().splitlines()
                # var content here is a file-object thing, use .read() to get the coordinate in the text file.
                # splitlines used for removing \r\n symbol from read() content.
                cor_seq = cor[0].split(' ')
                # now cor_seq format is ['x', 'y', 'z']
                while row in range(1, 5):
                    column = 1
                    while column in range(1, 5):
                        item = QTableWidgetItem("(%r, %r, %r)" % (cor_seq[0], cor_seq[1], cor_seq[2]))
                        font = QFont()
                        font.setPointSize(7)
                        item.setFont(font)
                        self.vesselsTableWidget.setItem(row, column, item)
                        column += 1
                    row += 1
            # set all of the vessel x item uncheckable.
        return
    # problem: how can we insure that once we click the checkbox, the reaction function can react properly.

    def handle_item_clicked(self, item):
        row = item.row()
        column = item.column()

        if row in range(1, 5) and column == 0:
            if row == 1:
                if item.checkState() != self.preVessel0Status:
                    self.refresh_vtk_actor_from_iren(item)
                    self.preVessel0Status = item.checkState()
            elif row == 2:
                if item.checkState() != self.preVessel1Status:
                    self.refresh_vtk_actor_from_iren(item)
                    self.preVessel1Status = item.checkState()
            elif row == 3:
                if item.checkState() != self.preVessel2Status:
                    self.refresh_vtk_actor_from_iren(item)
                    self.preVessel2Status = item.checkState()
            elif row == 4:
                if item.checkState() != self.preVessel3Status:
                    self.refresh_vtk_actor_from_iren(item)
                    self.preVessel3Status = item.checkState()
        return

    def refresh_vtk_actor_from_iren(self, item):
        row = item.row()
        self.parent.update_vessel_img(row, item.checkState())
        return

    def sub_vtk_render_initialization(self):
        self.EvaluateVesselDisplayWindow.interactor_initialization()

    def pass_evaluated_vessel_to_renderer(self, path_dir):
        self.parent.pass_evaluated_vessel_to_renderer(path_dir)

    def get_board_check_status(self):
        return self.ScoreBoardWindow.get_status()

    def get_vessel_to_be_evaluated_from_board(self):
        return self.ScoreBoardWindow.get_selected_vessel()

    def pass_vessel_to_be_evaluated(self, single_path_dir, vessel_number):
        self.parent.pass_vessel_to_be_evaluated(single_path_dir, vessel_number)

    def store_vessel_to_be_evaluated(self, single_path_dir, ds_name, file_name, vessel_num):
        self.parent.store_vessel_to_be_evaluated(single_path_dir, ds_name, file_name, vessel_num)

    def update_info_board(self):
        self.parent.update_info_board()

    def reset_selected_vessel(self):
        self.ScoreBoardWindow.reset_selected_vessel()

    def load_vessel_to_be_evaluated(self, ds_name, vessel_num, file_name):
        return self.parent.load_vessel_to_be_evaluated(ds_name, vessel_num, file_name)

    def load_ref_data(self, ds_name, vessel_num):
        return self.parent.load_ref_data(ds_name, vessel_num)

    def reconstruct0(self):
        if self.ref_flag is True and self.preVessel0Status == Qt.Checked:
                print "ready to reconstruct vessel 0"

    def reconstruct1(self):
        if self.ref_flag is True and self.preVessel1Status == Qt.Checked:
                print "ready to reconstruct vessel 1"

    def reconstruct2(self):
        if self.ref_flag is True and self.preVessel2Status == Qt.Checked:
                print "ready to reconstruct vessel 2"

    def reconstruct3(self):
        if self.ref_flag is True and self.preVessel3Status == Qt.Checked:
                print "ready to reconstruct vessel 3"

    #def reconstruct_vessel(self,  )

