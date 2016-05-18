# coding=utf-8


from AnalyserIHM.ObjectEventService import ObjectEventService

__author__ = 'xuhaoshen'
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from ctypes.wintypes import RECT
# from AnalyserIHM.AnalyserMenuBar import AnalyserMenuBar
from ctypes import *


class AnalyserTitleBar(QWidget):
    """
    This class represent the title bar of the main window of the vas, which include the
    the name of the application at the right side.
    and four push button to control the main window. the click & move of the mouse's left button trigger the moving
    of the main window.
    Attributes:
        - principal components of the title bar
        --------------------------------------------------------------------------------------------------
        | AnalyserTitle |              | minimizeWindowButton | maximizeWindowButton | closeWindowButton |
        --------------------------------------------------------------------------------------------------
    """

    def __init__(self, parent=None):
        super(AnalyserTitleBar, self).__init__(parent)
        self.parent = parent

        # -----------------------------------------------
        # attributes initialization
        # -----------------------------------------------
        self.analyserMediator = None
        self.mousePointerMove = None
        self.mousePosition = None
        self.mouseLeftButtonPressed = False
        self.m_bMaxWin = False
        self.toolbarPickUp = False
        self.m_rectRestoreWindow = self.parent.geometry()
        button_size = QSize(15, 15)
        self.width = 0
        self.height = 0

        # ------------------------------------------------
        # configure the appearance and the setting of the title bar
        # ------------------------------------------------
        self.setFixedHeight(30)
        self.setMouseTracking(True)

        # ------------------------------------------------
        # component of the title bar
        # ------------------------------------------------
        # -- the name of the app
        self.analyserTitle = QLabel(self)
        self.analyserTitle.setFixedHeight(30)
        self.analyserTitle.setText("VAS")
        self.analyserTitle.setStyleSheet("margin-left:6px; color:Blue")
        self.analyserTitle.setCursor(Qt.PointingHandCursor)
        self.analyserTitle.setFont(QFont("Helvetica", 8, QFont.AnyStyle, True))
        self.analyserTitle.move(0, 0)

        # -- button to close the main window
        self.closeMainWindowButton = QPushButton()
        self.closeMainWindowButton.setFixedSize(button_size)
        # self.closeMainWindowButton.setText("x")
        self.closeMainWindowButton.setIcon(QIcon(":/close_window.png"))
        self.closeMainWindowButton.setFlat(True)

        # -- button to maximize the main window
        self.maximizeWindowButton = QPushButton()
        self.maximizeWindowButton.setFixedSize(button_size)
        # self.maximizeWindowButton.setText("+")
        self.maximizeWindowButton.setIcon(QIcon(":/max_window.png"))
        self.maximizeWindowButton.setFlat(True)

        # -- button to minimize the main window
        self.minimizeWindowButton = QPushButton()
        self.minimizeWindowButton.setFixedSize(button_size)
        # self.minimizeWindowButton.setText("-")
        self.minimizeWindowButton.setIcon(QIcon(":/mini_window.png"))
        self.minimizeWindowButton.setFlat(True)

        # -- button to pick up and pull down the tool bar
        self.pickToolbarButton = QPushButton()
        self.pickToolbarButton.setFixedSize(button_size)
        self.pickToolbarButton.setIcon(QIcon(";/arrow_down.png"))
        self.pickToolbarButton.setFlat(True)

        # -- container of these buttons
        self.buttonsNecessaryLabel = QLabel(self)
        self.buttonsNecessaryLabel.setFixedSize(80, 30)
        self.buttonsNecessaryLabel.setCursor(Qt.CustomCursor)
        self.buttonsNecessaryLabel.move(self.parent.width() - 80, 0)

        buttons_necessary_layout = QHBoxLayout(self.buttonsNecessaryLabel)
        buttons_necessary_layout.addWidget(self.pickToolbarButton)
        buttons_necessary_layout.addWidget(self.minimizeWindowButton)
        buttons_necessary_layout.addWidget(self.maximizeWindowButton)
        buttons_necessary_layout.addWidget(self.closeMainWindowButton)
        buttons_necessary_layout.setMargin(0)  # outer
        buttons_necessary_layout.setSpacing(5)  # inner

        # ------------------------------------------------
        # connect the signal and slot with buttons.
        # ------------------------------------------------
        self.connect(self.minimizeWindowButton, SIGNAL("clicked()"), self.minimize_window)
        self.connect(self.maximizeWindowButton, SIGNAL("clicked()"), self.maximize_window_button)
        self.connect(self.closeMainWindowButton, SIGNAL("clicked()"), self.close_window)

        self.show()

    def set_size(self, width, height):
        self.width = width
        self.height = height

    # -- mouse event --
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if (event.y() < 5) or (event.x() < 5):
                event.ignore()
                return
            self.mousePosition = event.globalPos()
            self.mouseLeftButtonPressed = True

    def mouseMoveEvent(self, event):
        if self.mouseLeftButtonPressed:
            self.mousePointerMove = event.globalPos()
            self.parent.move(self.parent.pos() + self.mousePointerMove - self.mousePosition)
            self.mousePosition = self.mousePointerMove
        event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseLeftButtonPressed = False
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.m_bMaxWin:
                self.m_rectRestoreWindow = self.parent.geometry()
                self.parent.setGeometry(QApplication.desktop().availableGeometry())
            else:
                self.parent.setGeometry(self.m_rectRestoreWindow)
        self.m_bMaxWin = not self.m_bMaxWin
        self.parent.set_window_maximize_size()
        self.parent.draw_background()

    def resizeEvent(self, event):
        self.buttonsNecessaryLabel.move(self.parent.width() - 80, 0)

    # -- max min and close the main window.

    def minimize_window(self):
        # -- minimize the main window
        self.parent.showMinimized()

    def maximize_window(self):
        # -- maximize the main window
        self.parent.setGeometry(QApplication.desktop().availableGeometry())
        self.m_bMaxWin = True
        self.parent.set_window_maximize_size()
        self.parent.draw_background()
        self.buttonsNecessaryLabel.move(self.parent.width() - 80, 0)

    def close_window(self):
        # -- close the main window
        reply = QMessageBox.question(None, "WARNING", "Decide to Quit?", QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return
        elif reply == QMessageBox.Yes:
            self.parent.close()

    # -- if it's the normal size, click the maximize button, then the widget will be maxmized;
    # -- if it's the maximize button, then the widget will be rezised to it's normal size.
    def maximize_window_button(self):
        if not self.m_bMaxWin:
            self.parent.setGeometry(QApplication.desktop().availableGeometry())
            self.m_bMaxWin = True
            self.parent.set_window_maximize_size()
            self.parent.draw_background()
            self.buttonsNecessaryLabel.move(self.parent.width() - 80, 0)
        else:
            self.parent.setGeometry(self.m_rectRestoreWindow)
            self.m_bMaxWin = False
            self.parent.set_window_normal_size()
            self.parent.draw_background()
            self.buttonsNecessaryLabel.move(self.parent.width() - 80, 0)
