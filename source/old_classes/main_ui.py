# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(400, 836)
        MainWindow.setMinimumSize(QSize(400, 0))
        MainWindow.setStyleSheet(u"QMainWindow\n"
"{\n"
"	background-color: #BDBDBD;\n"
"\n"
"}\n"
"QPushButton{\n"
"	color:#F5F5F5;\n"
"    background-color: #212121;\n"
"    /*border-style: outset;*/\n"
"\n"
"	border-radius: 10px;\n"
"	font: bold 14 px;\n"
"	padding: 6px;\n"
"	margin: 3px;\n"
"   	\n"
"\n"
"	\n"
"	font: 11pt \"FreeSans\";\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #757575;\n"
"    /*border-width: 2px;\n"
"	font-family: fantasy;\n"
"	*/\n"
"    \n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: #9E9E9E;\n"
"    \n"
"}\n"
"\n"
"QLabel\n"
"{\n"
"	color:#F5F5F5;\n"
"	text-align: right; /* align the text to the left */\n"
"	/*border: 1px solid green;\n"
"    border-radius: 4px;\n"
"    padding: 2px;\n"
"	*/\n"
"	border-radius: 10px;\n"
"	background-color: #9E9E9E;\n"
"	padding: 6px;\n"
"	margin: 3px;\n"
"	font: 11pt \"FreeSans\";\n"
"}\n"
"\n"
"QLineEdit{\n"
"	color:#F5F5F5;\n"
"	background-color: #757575;\n"
"    /*border-style: outset;*/\n"
"	border-radius: 10px;\n"
"	font: bold 14 px;\n"
"	min width: 10e"
                        "m;\n"
"	padding: 6px;\n"
"	margin: 3px;\n"
"	font: 11pt \"FreeSans\";\n"
"}\n"
"\n"
"\n"
"QComboBox\n"
"{\n"
"\n"
"	color:#F5F5F5;\n"
"	background-color: #757575;\n"
"	border-radius: 10px;\n"
"	font: bold 14 px;\n"
"	min width: 10em;\n"
"	padding: 6px;\n"
"	margin: 3px;\n"
"	font: 11pt \"FreeSans\";\n"
"}\n"
"\n"
"QComboBox QAbstractItemView{\n"
"background-color: #757575;\n"
" }\n"
"\n"
"#pushButton_close{\n"
"background-color: #c4001d;\n"
"}\n"
"\n"
"#pushButton_close:hover{\n"
"background-color: #ff1744;\n"
"}\n"
"#pushButton_close:pressed{\n"
"background-color: #ff616f;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setEnabled(True)
        self.widget.setAutoFillBackground(False)
        self.gridLayoutWidget = QWidget(self.widget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 0, 363, 711))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.label_groups_amount = QLabel(self.gridLayoutWidget)
        self.label_groups_amount.setObjectName(u"label_groups_amount")

        self.gridLayout.addWidget(self.label_groups_amount, 4, 2, 1, 1)

        self.lineEdit_thickness = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_thickness.setObjectName(u"lineEdit_thickness")
        self.lineEdit_thickness.setStyleSheet(u"")

        self.gridLayout.addWidget(self.lineEdit_thickness, 9, 2, 1, 1)

        self.lineEdit_height = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_height.setObjectName(u"lineEdit_height")

        self.gridLayout.addWidget(self.lineEdit_height, 7, 2, 1, 1)

        self.label_file_name = QLabel(self.gridLayoutWidget)
        self.label_file_name.setObjectName(u"label_file_name")

        self.gridLayout.addWidget(self.label_file_name, 1, 2, 1, 1)

        self.label_samples_geometry = QLabel(self.gridLayoutWidget)
        self.label_samples_geometry.setObjectName(u"label_samples_geometry")
        self.label_samples_geometry.setStyleSheet(u"height: 20px;")

        self.gridLayout.addWidget(self.label_samples_geometry, 5, 0, 1, 3)

        self.pushButton_plot = QPushButton(self.gridLayoutWidget)
        self.pushButton_plot.setObjectName(u"pushButton_plot")
        self.pushButton_plot.setStyleSheet(u"")

        self.gridLayout.addWidget(self.pushButton_plot, 11, 0, 1, 3)

        self.lineEdit_width = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_width.setObjectName(u"lineEdit_width")

        self.gridLayout.addWidget(self.lineEdit_width, 8, 2, 1, 1)

        self.label_entities = QLabel(self.gridLayoutWidget)
        self.label_entities.setObjectName(u"label_entities")

        self.gridLayout.addWidget(self.label_entities, 2, 0, 1, 1)

        self.lineEdit_precision = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_precision.setObjectName(u"lineEdit_precision")

        self.gridLayout.addWidget(self.lineEdit_precision, 6, 2, 1, 1)

        self.comboBox_gradients = QComboBox(self.gridLayoutWidget)
        self.comboBox_gradients.setObjectName(u"comboBox_gradients")
        self.comboBox_gradients.setEditable(False)
        self.comboBox_gradients.setIconSize(QSize(16, 16))

        self.gridLayout.addWidget(self.comboBox_gradients, 10, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 13, 0, 1, 3)

        self.pushButton_close = QPushButton(self.gridLayoutWidget)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setStyleSheet(u"")

        self.gridLayout.addWidget(self.pushButton_close, 12, 2, 1, 1)

        self.pushButton_open_file = QPushButton(self.gridLayoutWidget)
        self.pushButton_open_file.setObjectName(u"pushButton_open_file")

        self.gridLayout.addWidget(self.pushButton_open_file, 1, 0, 1, 1)

        self.label_entities_amount = QLabel(self.gridLayoutWidget)
        self.label_entities_amount.setObjectName(u"label_entities_amount")

        self.gridLayout.addWidget(self.label_entities_amount, 2, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 1, 1, 1)

        self.label_precision = QLabel(self.gridLayoutWidget)
        self.label_precision.setObjectName(u"label_precision")

        self.gridLayout.addWidget(self.label_precision, 6, 0, 1, 1)

        self.label_height = QLabel(self.gridLayoutWidget)
        self.label_height.setObjectName(u"label_height")

        self.gridLayout.addWidget(self.label_height, 7, 0, 1, 1)

        self.label_width = QLabel(self.gridLayoutWidget)
        self.label_width.setObjectName(u"label_width")

        self.gridLayout.addWidget(self.label_width, 8, 0, 1, 1)

        self.label_thickness = QLabel(self.gridLayoutWidget)
        self.label_thickness.setObjectName(u"label_thickness")
        self.label_thickness.setStyleSheet(u"")

        self.gridLayout.addWidget(self.label_thickness, 9, 0, 1, 1)

        self.label_gradients = QLabel(self.gridLayoutWidget)
        self.label_gradients.setObjectName(u"label_gradients")
        self.label_gradients.setStyleSheet(u"")

        self.gridLayout.addWidget(self.label_gradients, 10, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 12, 0, 1, 2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 6, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 7, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 8, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 9, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_8, 10, 1, 1, 1)

        self.label_select_file = QLabel(self.gridLayoutWidget)
        self.label_select_file.setObjectName(u"label_select_file")
        self.label_select_file.setMinimumSize(QSize(0, 0))
        self.label_select_file.setStyleSheet(u"")

        self.gridLayout.addWidget(self.label_select_file, 0, 0, 1, 3)

        self.pushButton_divide = QPushButton(self.gridLayoutWidget)
        self.pushButton_divide.setObjectName(u"pushButton_divide")

        self.gridLayout.addWidget(self.pushButton_divide, 3, 0, 1, 3)

        self.label_groups = QLabel(self.gridLayoutWidget)
        self.label_groups.setObjectName(u"label_groups")

        self.gridLayout.addWidget(self.label_groups, 4, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_test = QPushButton(self.gridLayoutWidget)
        self.pushButton_test.setObjectName(u"pushButton_test")

        self.verticalLayout_3.addWidget(self.pushButton_test)

        self.pushButton_test_2 = QPushButton(self.gridLayoutWidget)
        self.pushButton_test_2.setObjectName(u"pushButton_test_2")

        self.verticalLayout_3.addWidget(self.pushButton_test_2)


        self.gridLayout.addLayout(self.verticalLayout_3, 14, 0, 1, 3)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_9, 4, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 400, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.pushButton_open_file, self.lineEdit_height)
        QWidget.setTabOrder(self.lineEdit_height, self.lineEdit_width)
        QWidget.setTabOrder(self.lineEdit_width, self.lineEdit_thickness)
        QWidget.setTabOrder(self.lineEdit_thickness, self.pushButton_plot)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_groups_amount.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.lineEdit_thickness.setText(QCoreApplication.translate("MainWindow", u"1,0000", None))
        self.lineEdit_height.setText(QCoreApplication.translate("MainWindow", u"1,0000", None))
        self.label_file_name.setText(QCoreApplication.translate("MainWindow", u"No file", None))
        self.label_samples_geometry.setText(QCoreApplication.translate("MainWindow", u"Samples geometry", None))
        self.pushButton_plot.setText(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.lineEdit_width.setText(QCoreApplication.translate("MainWindow", u"1,0000", None))
        self.label_entities.setText(QCoreApplication.translate("MainWindow", u"Entities", None))
        self.lineEdit_precision.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.pushButton_close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.pushButton_open_file.setText(QCoreApplication.translate("MainWindow", u"Open file", None))
        self.label_entities_amount.setText(QCoreApplication.translate("MainWindow", u"Entities", None))
        self.label_precision.setText(QCoreApplication.translate("MainWindow", u"Precision", None))
        self.label_height.setText(QCoreApplication.translate("MainWindow", u"Height, mm", None))
        self.label_width.setText(QCoreApplication.translate("MainWindow", u"Width, mm", None))
        self.label_thickness.setText(QCoreApplication.translate("MainWindow", u"Thickness, mm", None))
        self.label_gradients.setText(QCoreApplication.translate("MainWindow", u"Gradients", None))
#if QT_CONFIG(accessibility)
        self.label_select_file.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.label_select_file.setText(QCoreApplication.translate("MainWindow", u"Select data file", None))
        self.label_select_file.setProperty("class", QCoreApplication.translate("MainWindow", u"asd", None))
        self.pushButton_divide.setText(QCoreApplication.translate("MainWindow", u"Divide by groups", None))
        self.label_groups.setText(QCoreApplication.translate("MainWindow", u"Groups", None))
        self.pushButton_test.setText(QCoreApplication.translate("MainWindow", u"Test 1", None))
        self.pushButton_test_2.setText(QCoreApplication.translate("MainWindow", u"Test 2", None))
    # retranslateUi

