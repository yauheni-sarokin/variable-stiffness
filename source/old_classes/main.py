import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QDialog
from PySide2.QtGui import QIcon
from PySide2.QtCore import QRegExp, Slot
from PySide2.QtGui import QRegExpValidator
from main_ui import Ui_MainWindow
from plot_dialog_ui import Ui_Dialog
import tools
import colorgradients
import os

#####################################################
#Class property container contains all the properties
#that were assigned within gui
#####################################################
class PropertyContainer():
	"""docstring for PropertyContainer"""
	def __init__(self, mainWindow):
		self.mainWindow = mainWindow
		

	def update(self):
		self.precision = mainWindow.get_precision()
		self.height = mainWindow.get_height()
		self.width = mainWindow.get_width()
		self.thickness = mainWindow.get_thickness()
		self.file = mainWindow.file
		self.entities = mainWindow.entities
		self.groups = mainWindow.groups

	def get_precision(self):
		return self.precision

	def get_height(self):
		return self.height

	def get_width(self):
		return self.width

	def get_thickness(self):
		return self.thickness

	def get_file(self):
		return self.file

	def get_entities(self):
		return self.entities

	#def update_groups(self):
		#self.groups = self.mainWindow.get_groups()

	def set_groups(self, groups):
		self.groups = groups

	def get_groups(self):
		return self.groups

	def set_checked_groups(self, groups):
		self.checked_groups = groups

	def get_checked_groups(self):
		return self.checked_groups


	def set_content(self, content):
		self.content = content

	def get_content(self):
		return self.content

	def set_entities(self, entities):
		self.entities = entities

	def get_entities(self):
		return self.entities


#####################################################
#Main logic of file reading
#First open txt file, contain str lines with data co-
#lums
#content = get_content_from_file(file)
#
#Second. read entities from content
#entities = get_entities_from_content(content)
#groups =
# get_groups_by_displacements_by_voltages(entities)
#####################################################

 
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	#docstring for Ui_MainWindow"QtWidgets.QMainWindow, Ui_MainWindow
	def __init__(self):
		#Create new form and UI
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.show()
		self.setIcon()
		#####################################################
		#Set initial variables
		#####################################################
		self.file = 'No file'
		self.entities = 0
		self.groups = 0

		#####################################################
		#Write initial variables to gui
		#####################################################
		self.write_label_entities(str(self.entities))
		self.write_label_groups(str(self.groups))
		self.write_label_file_name(self.file)
		self.pushButton_plot.setEnabled(False)

		#####################################################
		#Set validator for fields
		#Validator for precision foelds, only numbers
		#####################################################
		precision_rx = QRegExp("-?\\d{1,4}")
		precision_validator = QRegExpValidator(precision_rx, self)
		self.lineEdit_precision.setValidator(precision_validator)
		#####################################################
		#Validator for thickness, height, width
		#####################################################
		th_he_wi_rx = QRegExp("\\d{1}\\,\\d{1,4}")
		th_he_wi_validator = QRegExpValidator(th_he_wi_rx, self)
		self.lineEdit_height.setValidator(th_he_wi_validator)
		self.lineEdit_width.setValidator(th_he_wi_validator)
		self.lineEdit_thickness.setValidator(th_he_wi_validator)
		#####################################################
		#Load color gradients
		#Take gradients from colorgradients and insert dicti-
		#onary keys into combo box
		#####################################################
		list_of_gradients = []
		for i in colorgradients.color_gradients.keys():
			list_of_gradients.append(i)
		self.comboBox_gradients.addItems(list_of_gradients)
		#####################################################
		#Connect gui buttons to their function in buttons ui
		#####################################################
		self.pushButton_open_file.clicked.connect(self.open_file)
		self.pushButton_plot.clicked.connect(self.plot)
		self.pushButton_close.clicked.connect(self.close)
		self.pushButton_test.clicked.connect(self.test)
		self.pushButton_divide.clicked.connect(self.divide)


	#####################################################
	#main window getters
	#####################################################
	def get_height(self):
		return self.lineEdit_height.text()

	def get_width(self):
		return self.lineEdit_width.text()

	def get_thickness(self):
		return self.lineEdit_thickness.text()

	def get_precision(self):
		return self.lineEdit_precision.text()

	def get_groups(self):
		return self.lineEdit_precision.text()

	def get_entities(self):
		return self.lineEdit_precision.text()

	def get_content(self):
		return self.lineEdit_precision.text()

	#####################################################
	#Set app icon
	#####################################################
	def setIcon(self):
		appIcon = QIcon('program/resources/logo.png')
		self.setWindowIcon(appIcon)

	#####################################################
	#Set to main gui class property container that are
	#stored from the gui
	#####################################################
	def set_property_container(self, property_container):
		self.property_container = property_container

	#####################################################
	#Click button functions, substitute somehow!
	#transfer to other file if possible
	#####################################################
	def open_file(self):
		#open dialog and try to open file
		file_path, file_name = self.open_file_and_return_path_and_name()
		#is thyere file or not
		is_file = self.enable_plot_button(file_name)
		#write file name to label
		self.write_label_file_name(file_name)
		#get how many entities are there
		if is_file:
			self.content = self.open_file_and_read_content(file_path)
			self.entities = self.open_content_and_read_entities(self.content)
			self.write_label_entities(str(len(self.entities)))



		# self.path_To_File = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "All (*.*)")
		# file_name = self.path_To_File[0].split('/')[-1]
		# if file_name == '': 
		# 	file_name = 'No file'
		# 	self.pushButton_plot.setEnabled(False)
		# else:
		# 	self.pushButton_plot.setEnabled(True)

		# self.label_file_name.setText(file_name)
		# self.file = file_name

	#####################################################
	#Plot button hook logic
	#####################################################
	def plot(self):
		#####################################################
		#Create dialog
		#####################################################
		plot_dialog = QtWidgets.QDialog()
		ui = Ui_Dialog()
		#####################################################
		#Set property container, class that contains 
		#all the possible gui properties
		#####################################################
		ui.set_property_container(self.property_container)
		#####################################################
		#Setup ui
		#####################################################
		ui.setupUi(plot_dialog)

		plot_dialog.show()
		#execute - run the window. this line is obligatory
		#to run dialog within application
		accepted = plot_dialog.exec_()

		#####################################################
        #If we push plot force displacement -> send signal 2
        #####################################################
		if accepted == 2:
			checked_groups = self.property_container.get_checked_groups()

			gradient = self.comboBox_gradients.currentText()
			precision = int(self.lineEdit_precision.text())
			tools.plot_force_displacement(checked_groups, gradient, precision)
			#tools.plot_displacement_groups(checked_groups)
		#####################################################
        #If we push plot stress strain -> send signal 3
        #####################################################
		elif accepted == 3:
			checked_groups = self.property_container.get_checked_groups()

			gradient = self.comboBox_gradients.currentText()
			precision = int(self.lineEdit_precision.text())

			#b in mm
			width_text = self.lineEdit_width.text()
			width = float(width_text.replace(',','.'))
			#l in mm
			height_text = self.lineEdit_height.text()
			height = float(height_text.replace(',','.'))
			#h in mm
			thickness_text = self.lineEdit_thickness.text()
			thickness = float(thickness_text.replace(',','.'))

			tools.plot_modulus_displacement_mock(checked_groups, 
				height, width, thickness,
				gradient, precision)


	#####################################################
	#Close button hook logic
	#####################################################
	def close(self):
		QtCore.QCoreApplication.quit()
	#####################################################
	#Divide button hook logic
	#####################################################
	def divide(self):
		#####################################################
		#Now this function only devides into voltage groups
		#with different displacements
		#####################################################
		#self.groups = model.get_groups_by_displacements_by_voltages(self.entities)
		#####################################################
		#Mock logic
		#####################################################
		#self.groups = tools.get_entities_groups_by_voltage(self.entities)
		self.groups = tools.get_entities_groups_by_voltage_by_displacement_from_entities(self.entities)
		'''for group in self.groups:
									print(group.get_voltage())'''
		#print(len(self.groups_2))
		#####################################################
		#Mock logic
		#####################################################
		self.write_label_groups(str(len(self.groups)))
		self.property_container.set_groups(self.groups)

	#####################################################
	#Test button
	#####################################################
	def test(self):
		gradient = self.comboBox_gradients.currentText()
		precision = int(self.lineEdit_precision.text())
		print(gradient)
		print(str(precision))

	#####################################################
	#auxiliary functions
	#####################################################
	#####################################################
	#Open file and return name if any
	#####################################################
	def open_file_and_return_path_and_name(self):
		self.path_To_File = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "All (*.*)")
		file_name = self.path_To_File[0].split('/')[-1]
		if file_name == '': 
			file_name = 'No file'
		return self.path_To_File[0], file_name
	#####################################################
	#if any file return tru and make plot button enabled
	#####################################################
	def enable_plot_button(self, file_name):
		if file_name == '':
			self.pushButton_plot.setEnabled(False)
			return False
		else:
			self.pushButton_plot.setEnabled(True)
			return True
	#####################################################
	#Open file an read content
	#####################################################
	def open_file_and_read_content(self, file):
		return tools.get_content_from_file(file)
	#####################################################
	#Open content and read entities
	#####################################################
	def open_content_and_read_entities(self, content):
		return tools.get_entities_from_content(content)

	#####################################################
	#UI environment functions
	#to write or read UI
	#####################################################

	#####################################################
	#write entities label
	#####################################################
	def write_label_entities(self, text):
		self.label_entities_amount.setText(text)
	#####################################################
	#write entities label
	#####################################################
	def write_label_groups(self, text):
		self.label_groups_amount.setText(text)
	#####################################################
	#write file name label
	#####################################################
	def write_label_file_name(self, text):
		self.label_file_name.setText(text)





if __name__ == '__main__':
	#Create new QApplication
	app = QtWidgets.QApplication(sys.argv)
	

	#Class with logic
	mainWin = MainWindow()
	#####################################################
	#Insert here property container class that will store 
	#GUI properties and will transfer them into other
	#####################################################
	properties = PropertyContainer(mainWin)
	mainWin.set_property_container(properties)

	#Do not change
	ret = app.exec_()
	sys.exit() 