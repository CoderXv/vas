#!/usr/bin/env python
from PyQt4 import QtCore

__author__ = 'xuhaoshen'
from PyQt4 import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4.QtCore import *

class ScoreBoardWindow(QFrame):
    """
        This class is used for display the grade of the evaluation.
        ========================
        Target Vessel | combobox
        ========================

                 Grade

        ========================
    """
    def __init__(self, parent=None):
        super(QFrame, self).__init__(parent)

        self.parent = parent
        self.vesselNumber = 0  # default
        self.vesselLoaded = False # whether is loaded
        # -- set the background color.
        self.setStyleSheet("background-color:transparent")

        # -- init the windows component.
        self.scoreBoard = QWidget()
        self.scoreBoardHeader = QLabel()
        # new
        self.vesselSelectBox = QComboBox()
        self.scoreDisplayWindow = QTableWidget()

        # set the score header
        self.scoreBoardHeader.setText("Target Vessel")
        self.scoreBoardHeader.setFixedHeight(30)
        self.scoreBoardHeader.setAlignment(QtCore.Qt.AlignCenter)

        # set the vessel select combobox
        self.vesselSelectBox.setFixedHeight(30)
        self.vesselSelectBox.addItems(["Ready to Select", "vessel0", "vessel1", "vessel2", "vessel3"])
        self.vesselSelectBox.setCurrentIndex(0)
        self.connect(self.vesselSelectBox, SIGNAL("currentIndexChanged(int)"), self.update_target_vessel)

        # set QFont of the header
        header_font = QFont("Times")
        header_font.setBold(True)
        header_font.setPointSize(13)
        self.scoreBoardHeader.setFont(header_font)
        self.vesselSelectBox.setFont(header_font)

        # set the color of the grid line.
        self.scoreDisplayWindow.setStyleSheet("gridline-color:rgb(192,198,204)")   # alice blue

        # set the score table.
        self.scoreDisplayWindow.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.scoreDisplayWindow.verticalHeader().setResizeMode(QHeaderView.Stretch)
        self.scoreDisplayWindow.setColumnCount(2)
        self.scoreDisplayWindow.setRowCount(6)
        self.verticalView = self.scoreDisplayWindow.verticalHeader()
        self.verticalView.setHidden(True)
        self.horizonView = self.scoreDisplayWindow.horizontalHeader()
        self.horizonView.setHidden(True)
        self.verticalView.setClickable(False)

        # set the content in the table as read-only.
        self.scoreDisplayWindow.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # set the title in the table.
        self.init_titles()

        self.Header = QWidget()
        self.HeaderLayout = QHBoxLayout(self.Header)
        self.HeaderLayout.addWidget(self.scoreBoardHeader)
        self.HeaderLayout.addWidget(self.vesselSelectBox)

        self.BoardLayout = QVBoxLayout(self)
        self.BoardLayout.addWidget(self.Header)
        self.BoardLayout.addWidget(self.scoreDisplayWindow)

        self.BoardLayout.setSpacing(0)
        self.BoardLayout.setMargin(6)

        self.show()

    def init_titles(self):
        string_list = ["OV score", "OF score", "OT score", "AD score", "AI score", "AT score"]
        # set the Grid-line color of the table.
        score_font = QFont("Times")
        # score_font.setBold(True) # it's too ugly if we set bold
        score_font.setPointSize(11)
        for row in range(6):
            item = QTableWidgetItem("%s" % (string_list[row]))
            item.setFont(score_font)
            item.textAlignment()
            self.scoreDisplayWindow.setItem(row, 0, item)

    def update_score(self, score_list):
        column = 0
        for score in score_list:
            item = QTableWidgetItem("%d" % score)
            self.scoreDisplayWindow.setItem(0, column, item)

    def update_target_vessel(self):
        self.vesselNumber = self.vesselSelectBox.currentIndex()
        if self.vesselNumber > 0:
            self.vesselLoaded = True
        else:
            self.vesselLoaded = False

        print self.vesselLoaded

    def get_status(self):
        return self.vesselLoaded

    def get_selected_vessel(self):
        return self.vesselNumber

    def reset_selected_vessel(self):
        self.vesselNumber = 0
















