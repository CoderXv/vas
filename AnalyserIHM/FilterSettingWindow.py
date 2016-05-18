__author__ = 'user'
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class FilterSettingWindow(QDialog):
    """
    This class is the widget used for setting automatic evaluating
    """
    def __init__(self, item=None, position=None, scene=None, parent=None):
        super(QDialog, self).__init__(parent)
        self.item = item
        self.position = position

        self.OV = 0
        self.OF = 0
        self.OT = 0
        self.AD = 0
        self.AI = 0
        self.AT = 0

        self.OV_editor = QTextEdit()
        self.OV_editor.setFixedWidth(100)
        self.OV_editor.setFixedHeight(25)
        self.OF_editor = QTextEdit()
        self.OF_editor.setFixedWidth(100)
        self.OF_editor.setFixedHeight(25)
        self.OT_editor = QTextEdit()
        self.OT_editor.setFixedWidth(100)
        self.OT_editor.setFixedHeight(25)
        self.AD_editor = QTextEdit()
        self.AD_editor.setFixedWidth(100)
        self.AD_editor.setFixedHeight(25)
        self.AI_editor = QTextEdit()
        self.AI_editor.setFixedWidth(100)
        self.AI_editor.setFixedHeight(25)
        self.AT_editor = QTextEdit()
        self.AT_editor.setFixedWidth(100)
        self.AT_editor.setFixedHeight(25)

        self.OV_editor_label = QLabel()
        self.OV_editor_label.setText("OV Score")
        self.OF_editor_label = QLabel()
        self.OF_editor_label.setText("OF Score")
        self.OT_editor_label = QLabel()
        self.OT_editor_label.setText("OT Score")
        self.AD_editor_label = QLabel()
        self.AD_editor_label.setText("AD Score")
        self.AI_editor_label = QLabel()
        self.AI_editor_label.setText("AI Score")
        self.AT_editor_label = QLabel()
        self.AT_editor_label.setText("AT Score")

        self.Accept_button = QPushButton()
        self.Accept_button.setText("Accept")
        self.Cancel_button = QPushButton()
        self.Cancel_button.setText("Cancel")

        self.button_box = QWidget()
        self.button_box_layout = QVBoxLayout(self.button_box)
        self.button_box_layout.addWidget(self.Accept_button)
        self.button_box_layout.addWidget(self.Cancel_button)

        self.SettingPanel = QWidget()
        self.SettingPanelLayout = QGridLayout(self.SettingPanel)
        self.SettingPanelLayout.addWidget(self.OV_editor_label, 0, 0)
        self.SettingPanelLayout.addWidget(self.OF_editor_label, 0, 1)
        self.SettingPanelLayout.addWidget(self.OT_editor_label, 0, 2)
        self.SettingPanelLayout.addWidget(self.AD_editor_label, 0, 3)
        self.SettingPanelLayout.addWidget(self.AT_editor_label, 0, 4)
        self.SettingPanelLayout.addWidget(self.AI_editor_label, 0, 5)
        self.SettingPanelLayout.addWidget(self.OV_editor, 1, 0)
        self.SettingPanelLayout.addWidget(self.OF_editor, 1, 1)
        self.SettingPanelLayout.addWidget(self.OT_editor, 1, 2)
        self.SettingPanelLayout.addWidget(self.AD_editor, 1, 3)
        self.SettingPanelLayout.addWidget(self.AT_editor, 1, 4)
        self.SettingPanelLayout.addWidget(self.AI_editor, 1, 5)

        self.FilterSettingBox = QHBoxLayout(self)
        self.FilterSettingBox.addWidget(self.SettingPanel)
        self.FilterSettingBox.addWidget(self.button_box)
        self.FilterSettingBox.setSpacing(3)
        self.FilterSettingBox.setMargin(6)



        # lable_Text = ["&OV", "&OF", "&OT", "&AD", "&AI", "&AT"]

    def create_label(self, text):
        label = QLabel(text)
        
