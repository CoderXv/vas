# !/usr/bin/env python
import os
import sys
import threading
from PyQt4.QtGui import *
from AnalyserContext.SystemDataBase import SystemDataBase
from AnalyserIHM.AnalyserMainWindow import AnalyserMainWindow
from Controller import Controller
from qrc_resources import *
# cmd for convert png files to resource code: pyrcc4.exe -o qrc_resources.py resource.qrc


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("siat")
    app.setApplicationName("vas")
    app.setWindowIcon(QIcon(":/icon.png"))
    app.setStyle("cleanlooks")  # important, if not, icon can't adapt the size of button

    username = os.environ['USERNAME']
    workspace_path = 'C:\Users\\' + username + '\Documents\CoronaryData_CTA\\'

    if not os.path.exists(workspace_path):
        os.mkdir(workspace_path)

    system_database = SystemDataBase(workspace_path)
    system_database.do_parse_data_sets()

    controller = Controller(system_database)

    analyserMainWindow = AnalyserMainWindow(controller)
    analyserMainWindow.find_data_set_existed()

    analyserMainWindow.show()

    sys.exit(app.exec_())
