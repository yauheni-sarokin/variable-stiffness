# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_dialog.ui'
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

#####################################################
#READ WHY YOU CANT PASS ANY PARAMETERS
#https://stackoverflow.com/questions/24719368/syntaxerror-non-default-argument-follows-default-argument/39942121
#####################################################
class Ui_Dialog(QDialog):
    def setupUi(self, Dialog):
        
        
        #####################################################
        #self.dialog = Dialog SET IT TO CLOSE QDIALOG
        #####################################################
        self.dialog = Dialog
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 600)
        Dialog.setStyleSheet(u"QDialog\n"
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
"	min width: 10em;\n"
""
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
        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 381, 550))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)
        #Add 10 checkboxes per 1 vert layout

        #groups from property container
        groups = self.property_container.get_groups()

        #contain check boxes
        self.plot_check_boxes = []
        #contain vertical layouts
        self.plot_vertical_layouts = []
        #add mock checkboxes
        _amount_of_cb = len(groups) #MOCK DATA
        #max cb per v layout
        _cb_per_v_layout = 10 
        #amount of vertical layouts
        _amount_of_v_layouts = _amount_of_cb//_cb_per_v_layout + 1 
        # checkboxes per layout
        cb_per_layout = []

        #All vertical layouts with checkboxes are inside one horizontal 
        self.horizontalLayout_cb = QHBoxLayout()
        self.horizontalLayout_cb.setObjectName(u"horizontalLayout_cb")

        self.verticalLayout.addLayout(self.horizontalLayout_cb)
        
        for i in range(_amount_of_v_layouts):
            if i + 1 < _amount_of_v_layouts:
                cb_per_layout.append(_cb_per_v_layout)
            else:
                number = _amount_of_cb - (i * _cb_per_v_layout)
                cb_per_layout.append(number)


        for v_layout in range(_amount_of_v_layouts):
            verticalLayout_cb = QVBoxLayout()
            #verticalLayout_cb.setObjectName("verticalLayout_cb_{}".format(str(v_layout)))
            v_l_object_name = "verticalLayout_cb_{}".format(str(v_layout))
            verticalLayout_cb.setObjectName(v_l_object_name)

            self.plot_vertical_layouts.append(verticalLayout_cb)
            self.horizontalLayout_cb.addLayout(verticalLayout_cb)

            for cb_i in range(cb_per_layout[v_layout]):
                #####################################################
                #Create check box here, but have to iterate something
                #####################################################
                checkBox = QCheckBox()
                checkBox.setObjectName("checkBox_{}".format(str(cb_i)))

                self.plot_check_boxes.append(checkBox)
                verticalLayout_cb.addWidget(checkBox)

                #####################################################
                #Increase group index
                #####################################################


            #Add spacer to comtress check boxes inside one lay out
            verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            verticalLayout_cb.addItem(verticalSpacer)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_check_all = QPushButton(self.verticalLayoutWidget)
        self.pushButton_check_all.setObjectName(u"pushButton_check_all")

        self.horizontalLayout.addWidget(self.pushButton_check_all)

        self.pushButton_uncheck_all = QPushButton(self.verticalLayoutWidget)
        self.pushButton_uncheck_all.setObjectName(u"pushButton_uncheck_all")

        self.horizontalLayout.addWidget(self.pushButton_uncheck_all)

        self.verticalLayout.addLayout(self.horizontalLayout)


        self.plot_button = QPushButton(self.verticalLayoutWidget)
        self.plot_button.setObjectName(u"plot_button")

        self.verticalLayout.addWidget(self.plot_button)

        #####################################################
        #Push button stress - strain
        #####################################################
        self.plot_button_modulus_displacement = QPushButton(self.verticalLayoutWidget)
        self.plot_button_modulus_displacement.setObjectName(u"plot_button_stress_strain")

        self.verticalLayout.addWidget(self.plot_button_modulus_displacement)
        #####################################################
        #Label with explanations
        #####################################################
        self.label_explain = QLabel(self.verticalLayoutWidget)
        self.label_explain.setObjectName(u"label_explain")

        self.verticalLayout.addWidget(self.label_explain)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
        #self.plot_button.clicked.connect(Dialog.accept)
        self.plot_button.clicked.connect(self.push_plot_button)
        self.plot_button_modulus_displacement.clicked.connect(self.push_plot_modulus_displacement_button)
        self.pushButton_check_all.clicked.connect(self.push_check_all_button)
        self.pushButton_uncheck_all.clicked.connect(self.push_uncheck_all_button)
    # setupUi

    def set_property_container(self, property_container):
        self.property_container = property_container

    def push_plot_modulus_displacement_button(self):
        #####################################################
        #Collect checked groups
        #####################################################
        checked_groups = []
        for check_box, group in zip (self.plot_check_boxes, self.property_container.get_groups()):
            if check_box.isChecked():
                checked_groups.append(group)

        self.property_container.set_checked_groups(checked_groups)

        #####################################################
        #If we push plot stress strain -> send signal 3
        #####################################################
        self.dialog.done(3)

    def push_plot_button(self):
        #####################################################
        #Collect checked groups
        #####################################################
        checked_groups = []
        for check_box, group in zip (self.plot_check_boxes, self.property_container.get_groups()):
            if check_box.isChecked():
                checked_groups.append(group)
        #####################################################
        #Send set of checked groups to properties container
        #####################################################

        self.property_container.set_checked_groups(checked_groups)

        #self.dialog.accept()
        #####################################################
        #If we push plot force displacement -> send signal 2
        #####################################################
        self.dialog.done(2)
        #self.dialog.close()
        
    def push_check_all_button(self):
        for i in self.plot_check_boxes:
            i.setCheckState(Qt.CheckState.Checked)

    def push_uncheck_all_button(self):
        for i in self.plot_check_boxes:
            #i.setCheckState(Qt.CheckState.PartiallyChecked)
            i.setCheckState(Qt.CheckState.Unchecked)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Groups to plot", None))
        
        for check_box, group in zip (self.plot_check_boxes, self.property_container.get_groups()):
            group_voltage = group.get_voltage()
            entities_amount = len(group.get_entities())
            check_box.setText(
                "{} V, s: {}".format(str(group_voltage), str(entities_amount)))

        self.pushButton_check_all.setText(QCoreApplication.translate("Dialog", u"Check all", None))
        self.pushButton_uncheck_all.setText(QCoreApplication.translate("Dialog", u"Unheck all", None))
        self.plot_button.setText(QCoreApplication.translate("Dialog", u"Plot force-displacement", None))
        self.plot_button_modulus_displacement.setText(QCoreApplication.translate("Dialog", u"Plot modulus-displacement", None))
        self.label_explain.setText(QCoreApplication.translate("Dialog", u"*s - amount of samples", None))
    # retranslateUi

