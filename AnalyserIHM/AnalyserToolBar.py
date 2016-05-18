__author__ = 'xuhaoshen'

import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from AnalyserIHM.ObjectEventService import ObjectEventService
import time

class AnalyserToolBar(QWidget):
    """ToolBarOfAnalyser
    This class represent the tool bar of the main window of the VAS, which include a number of push button below

    Attributes:
        - principal component of the title bar
            -------------------------------------------------------------------------------------------------------------------------------------------------------------
            | button1(ready for design)| button2 |                     | button3 | ...          | organizationLabel |
            -------------------------------------------------------------------------------------------------------------------------------------------------------------
    """
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setFixedHeight(40)

        # -------------------------------------------------------------
        # Attributes initialization
        # -------------------------------------------------------------
        self.filepathList = []
        self.pickInformationBoardButtonClicked = False
        self.myButtonList = []
        self.myButtonString = ["fileList", "fileopen", "addPageButton",
                               "analyser_configuration", "analyser_save"]
        self.buttonSize = QSize(40, 40)
        self.screenGrabActivated = False
        self.coordinate = [1, 1, 1, 1]

        # -------------------------------------------------------------
        # Push buttons on the tool bar.
        # -------------------------------------------------------------
        self.pickInformationBoardButton = QPushButton(self)
        self.pickInformationBoardButton.move(0, 0)
        self.importFileButton = QPushButton(self)
        self.importFileButton.move(40, 0)
        self.addPageButton = QPushButton(self)
        self.addPageButton.move(80, 0)
        self.analyserConfigurationButton = QPushButton(self)
        self.analyserConfigurationButton.move(120, 0)
        self.analyserSaveButton = QPushButton(self)
        self.analyserSaveButton.move(160, 0)

        self.myButtonList.append(self.pickInformationBoardButton)
        self.myButtonList.append(self.importFileButton)
        self.myButtonList.append(self.addPageButton)
        self.myButtonList.append(self.analyserConfigurationButton)
        self.myButtonList.append(self.analyserSaveButton)

        self.create_wideget()

        self.show()

    def create_wideget(self):
        """
            -- set the property of the pushbutton.
        """
        for i in range(0, len(self.myButtonList)):
                self.myButtonList[i].setIcon(QIcon(":/%s.png"% self.myButtonString[i]))
                self.myButtonList[i].setMouseTracking(True)
                self.myButtonList[i].setFixedSize(self.buttonSize)
                self.myButtonList[i].setFlat(True)


