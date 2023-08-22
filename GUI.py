#from OpenGL import GL, GLU, GLUT

from PyQt5 import QtCore, QtWidgets, uic

import qdarkstyle

import traceback, sys, os, shutil

import cli_convertor, additional_widgets

class mainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):

        super(mainWindow, self).__init__()
        uic.loadUi('QtGUI.ui', self)
        self.threadpool = QtCore.QThreadPool()

        #Menu bar
        self.Menufile = self.findChild(QtWidgets.QMenu, 'Menufilebar')
        self.Menuopenfile = self.findChild(QtWidgets.QAction, 'Menuopenfile')
        self.Menuopenfile.triggered.connect(self.Menuopenfileclicked)
        self.Menuquit = self.findChild(QtWidgets.QAction, 'Menuquit')
        self.Menuquit.triggered.connect(self.Menuquitclicked)

        #Tabs
        self.Tabs = self.findChild(QtWidgets.QTabWidget, 'Configuretabs')
        self.Tabs.setCurrentIndex(1)
        self.Tabs.setTabEnabled(0, False)

        #Parameter file
        self.Parametervalues = self.findChild(QtWidgets.QGroupBox, 'Parametervalues')
        self.Beamcurrentbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Beamcurrentbox')
        self.Lenscurrentbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Lenscurrentbox')
        self.Focuscurrentbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Focuscurrentbox')
        self.Parameter4box = self.findChild(QtWidgets.QDoubleSpinBox, 'Parameter4box')
        self.Parameter5box = self.findChild(QtWidgets.QDoubleSpinBox, 'Parameter5box')
        self.Changeparamindexbutton = self.findChild(QtWidgets.QPushButton, 'Changeparamindexbutton')
        self.Changeparamindexbutton.clicked.connect(self.Changeparamindexbuttonclicked)
        self.Selectindexbox = self.findChild(QtWidgets.QSpinBox, 'Selectindexbox')
        self.Selectindexbox.valueChanged.connect(self.Selectindexboxchanged)

        #Save parameter file
        self.Saveparamtext = self.findChild(QtWidgets.QLineEdit, 'Saveparamtext')
        self.Saveparambutton = self.findChild(QtWidgets.QPushButton, 'Saveparambutton')
        self.Saveparambutton.clicked.connect(self.Saveparambuttonclicked)

        #Preheat bottom
        self.Preheatbottomcountbox = self.findChild(QtWidgets.QSpinBox, 'Preheatbottomcountbox')
        self.Preheatbottomcountbutton = self.findChild(QtWidgets.QPushButton, 'Preheatbottomcountbutton')
        self.Preheatbottomcountbutton.clicked.connect(self.Preheatbottomcountbuttonclicked)
        self.Preheatbottomindexbox = self.findChild(QtWidgets.QSpinBox, 'Preheatbottomindexbox')       
        self.Preheatbottomindexbox.valueChanged.connect(self.Preheatbottomindexboxchanged)
        self.Preheatbottomhatchcountbox = self.findChild(QtWidgets.QLineEdit, 'Preheatbottomhatchcountbox')
        self.Preheatbottomtimebox = self.findChild(QtWidgets.QLineEdit, 'Preheatbottomtimebox')
        self.Preheatbottomrunbox = self.findChild(QtWidgets.QSpinBox, 'Preheatbottomrunbox')
        self.Preheatbottomdistbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Preheatbottomdistbox')
        self.Preheatbottomvelocitybox = self.findChild(QtWidgets.QDoubleSpinBox, 'Preheatbottomvelocitybox')
        self.Preheatbottombeambox = self.findChild(QtWidgets.QDoubleSpinBox, 'Preheatbottombeambox')
        self.Preheatbottomlensbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Preheatbottomlensbox')
        self.Preheatbottomfocusbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Preheatbottomfocusbox')
        self.Displaypreheatbottombutton = self.findChild(QtWidgets.QPushButton, 'Displaypreheatbottombutton')
        self.Modifypreheatbottombutton = self.findChild(QtWidgets.QPushButton, 'Modifypreheatbottombutton')
        self.Modifypreheatbottombutton.clicked.connect(self.Modifypreheatbottombuttonclicked)
        self.Displaypreheatbottombutton.clicked.connect(self.Displaypreheatbottombuttonclicked)
        self.Preheatbottomrunbox.setDisabled(True)
        self.Preheatbottomdistbox.setDisabled(True)
        self.Preheatbottomvelocitybox.setDisabled(True)
        self.Preheatbottombeambox.setDisabled(True)
        self.Preheatbottomlensbox.setDisabled(True)
        self.Preheatbottomfocusbox.setDisabled(True)
        self.Displaypreheatbottombutton.setDisabled(True)
        self.Modifypreheatbottombutton.setDisabled(True)

        #Preheat layer
        self.Preheatlayercountbox = self.findChild(QtWidgets.QSpinBox, 'Preheatlayercountbox')
        self.Preheatlayercountbutton = self.findChild(QtWidgets.QPushButton, 'Preheatlayercountbutton')
        self.Preheatlayercountbutton.clicked.connect(self.Preheatlayercountbuttonclicked)
        self.Preheatlayerindexbox = self.findChild(QtWidgets.QSpinBox, 'Preheatlayerindexbox')       
        self.Preheatlayerindexbox.valueChanged.connect(self.Preheatlayerindexboxchanged)
        self.Preheatlayerhatchcountbox = self.findChild(QtWidgets.QLineEdit, 'Preheatlayerhatchcountbox')
        self.Preheatlayertimebox = self.findChild(QtWidgets.QLineEdit, 'Preheatlayertimebox')
        self.Preheatlayerrunbox = self.findChild(QtWidgets.QSpinBox, 'Preheatlayerrunbox')
        self.Preheatlayerdistbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Preheatlayerdistbox')
        self.Preheatlayervelocitybox = self.findChild(QtWidgets.QDoubleSpinBox, 'Preheatlayervelocitybox')
        self.Preheatlayerbeambox = self.findChild(QtWidgets.QDoubleSpinBox, 'Preheatlayerbeambox')
        self.Preheatlayerlensbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Preheatlayerlensbox')
        self.Preheatlayerfocusbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Preheatlayerfocusbox')
        self.Displaypreheatlayerbutton = self.findChild(QtWidgets.QPushButton, 'Displaypreheatlayerbutton')
        self.Modifypreheatlayerbutton = self.findChild(QtWidgets.QPushButton, 'Modifypreheatlayerbutton')
        self.Modifypreheatlayerbutton.clicked.connect(self.Modifypreheatlayerbuttonclicked)
        self.Displaypreheatlayerbutton.clicked.connect(self.Displaypreheatlayerbuttonclicked)
        self.Preheatlayerrunbox.setDisabled(True)
        self.Preheatlayerdistbox.setDisabled(True)
        self.Preheatlayervelocitybox.setDisabled(True)
        self.Preheatlayerbeambox.setDisabled(True)
        self.Preheatlayerlensbox.setDisabled(True)
        self.Preheatlayerfocusbox.setDisabled(True)
        self.Displaypreheatlayerbutton.setDisabled(True)
        self.Modifypreheatlayerbutton.setDisabled(True)

        #File information
        self.Filetext = self.findChild(QtWidgets.QLineEdit, 'Filetext')
        self.Fileinformationbox = self.findChild(QtWidgets.QGroupBox, 'Fileinformation')
        self.Fileinformationbox.setDisabled(True)
        self.Filenamebox = self.findChild(QtWidgets.QLineEdit, 'Filenamebox')
        self.Layercountbox = self.findChild(QtWidgets.QLineEdit,'Layercountbox')
        self.Datebox = self.findChild(QtWidgets.QLineEdit,'Datebox')
        self.Versionbox = self.findChild(QtWidgets.QLineEdit,'Versionbox')
        self.Parsebutton = self.findChild(QtWidgets.QPushButton, 'Parsebutton')
        self.Parsebutton.clicked.connect(self.Parsebuttonclicked)
        self.Parseprogress = self.findChild(QtWidgets.QProgressBar, 'Parseprogress')
        self.Parseprogressvalue = additional_widgets.mutableint(0)

        #Layer Parse
        self.Layerparsebox = self.findChild(QtWidgets.QGroupBox, 'Layerparse')
        self.Layerparsebox.setDisabled(True)
        self.Polylinevelocitybox = self.findChild(QtWidgets.QDoubleSpinBox, 'Polylinevelocitybox')
        self.Polylineruncountbox = self.findChild(QtWidgets.QSpinBox, 'Polylineruncountbox')
        self.Polylinebeambox = self.findChild(QtWidgets.QDoubleSpinBox, 'Polylinebeambox')
        self.Polylinelensbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Polylinelensbox')
        self.Polylinefocusbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Polylinefocusbox')
        
        self.Hatchvelocitybox = self.findChild(QtWidgets.QDoubleSpinBox, 'Hatchvelocitybox')
        self.Hatchruncountbox = self.findChild(QtWidgets.QSpinBox, 'Hatchruncountbox')
        self.Hatchbeambox = self.findChild(QtWidgets.QDoubleSpinBox, 'Hatchbeambox')
        self.Hatchlensbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Hatchlensbox')
        self.Hatchfocusbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Hatchfocusbox')

        self.Selectlayersbox = self.findChild(QtWidgets.QLineEdit, 'Selectlayersbox')
        self.Modifyparambutton = self.findChild(QtWidgets.QPushButton, 'Modifyparambutton')
        self.Modifyparambutton.clicked.connect(self.Modifyparambuttonclicked)
        self.Selectlayerbox = self.findChild(QtWidgets.QSpinBox, 'Selectlayerbox')
        self.Selectlayerbox.valueChanged.connect(self.Selectlayerboxchanged)
        self.Modifyprogress = self.findChild(QtWidgets.QProgressBar, 'Modifyprogress')
        self.Modifyprogressvalue = additional_widgets.mutableint(0)

        #Layer information
        self.Layerinformationbox = self.findChild(QtWidgets.QGroupBox, 'Layerinformation')
        self.Layerinformationbox.setDisabled(True)
        self.Polylinecountbox = self.findChild(QtWidgets.QLineEdit, 'Polylinecountbox')
        self.Hatchcountbox = self.findChild(QtWidgets.QLineEdit, 'Hatchcountbox')
        self.Selectlayerinfobox = self.findChild(QtWidgets.QSpinBox, 'Selectlayerinfobox')
        self.Selectlayerinfoslider = self.findChild(QtWidgets.QSlider, 'Selectlayerinfoslider')
        self.Layerheightbox = self.findChild(QtWidgets.QLineEdit, 'Layerheightbox')
        self.Polylinetimebox = self.findChild(QtWidgets.QLineEdit, 'Polylinetimebox')
        self.Hatchtimebox = self.findChild(QtWidgets.QLineEdit, 'Hatchtimebox')
        self.Selectlayerinfobox.valueChanged.connect(self.Displaylayerchange)
        self.Selectlayerinfoslider.valueChanged.connect(self.Displaylayerchangeslider)

        #Save file
        self.Savebox = self.findChild(QtWidgets.QGroupBox, 'Savefile')
        self.Savebox.setDisabled(True)
        self.Savetext = self.findChild(QtWidgets.QLineEdit, 'Savefiletext')
        self.Savebutton = self.findChild(QtWidgets.QPushButton, 'Savebutton')
        self.Savebutton.clicked.connect(self.Savebuttonclicked)
        self.Savebuttonstatic = self.findChild(QtWidgets.QPushButton, 'Savebuttonstatic')
        self.Savebuttonstatic.clicked.connect(self.Savebuttonstaticclicked)
        self.Saveprogress = self.findChild(QtWidgets.QProgressBar, 'Saveprogress')
        self.Saveprogressvalue = additional_widgets.mutableint(0)

        #Cross calibrate
        self.Crosshatchfactorbox = self.findChild(QtWidgets.QSpinBox, 'Crosshatchfactorbox')
        self.Crosshatchvelocitybox = self.findChild(QtWidgets.QDoubleSpinBox, 'Crosshatchvelocitybox')
        self.Crosstimebox = self.findChild(QtWidgets.QLineEdit, 'Crosstimebox')

        self.Crossmodifybutton = self.findChild(QtWidgets.QPushButton, 'Crossmodifybutton')
        self.Crossdisplaybutton = self.findChild(QtWidgets.QPushButton, 'Crossdisplaybutton')
        self.Crosssavebutton = self.findChild(QtWidgets.QPushButton, 'Crosssavebutton')
        self.Crossmodifybutton.clicked.connect(self.Crossmodifybuttonclicked)
        self.Crossdisplaybutton.clicked.connect(self.Crossdisplaybuttonclicked)
        self.Crosssavebutton.clicked.connect(self.Crosssavebuttonclicked)
        self.Crossdisplaybutton.setDisabled(True)
        self.Crosssavebutton.setDisabled(True)

        #Square calibrate
        self.Squaregapbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Squaregapbox')
        self.Squaredotspacingbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Squaredotspacingbox')
        self.Squaretimebox = self.findChild(QtWidgets.QLineEdit, 'Squaretimebox')

        self.Squaremodifybutton = self.findChild(QtWidgets.QPushButton, 'Squaremodifybutton')
        self.Squaredisplaybutton = self.findChild(QtWidgets.QPushButton, 'Squaredisplaybutton')
        self.Squaresavebutton = self.findChild(QtWidgets.QPushButton, 'Squaresavebutton')
        self.Squaremodifybutton.clicked.connect(self.Squaremodifybuttonclicked)
        self.Squaredisplaybutton.clicked.connect(self.Squaredisplaybuttonclicked)
        self.Squaresavebutton.clicked.connect(self.Squaresavebuttonclicked)
        self.Squaredisplaybutton.setDisabled(True)
        self.Squaresavebutton.setDisabled(True)

        #Dot calibrate
        self.Dotgapbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Dotgapbox')
        self.Dotspacingbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Dotspacingbox')
        self.Dotholdbox = self.findChild(QtWidgets.QSpinBox, 'Dotholdbox')
        self.Dottimebox = self.findChild(QtWidgets.QLineEdit, 'Dottimebox')

        self.Dotmodifybutton = self.findChild(QtWidgets.QPushButton, 'Dotmodifybutton')
        self.Dotdisplaybutton = self.findChild(QtWidgets.QPushButton, 'Dotdisplaybutton')
        self.Dotsavebutton = self.findChild(QtWidgets.QPushButton, 'Dotsavebutton')
        self.Dotmodifybutton.clicked.connect(self.Dotmodifybuttonclicked)
        self.Dotdisplaybutton.clicked.connect(self.Dotdisplaybuttonclicked)
        self.Dotsavebutton.clicked.connect(self.Dotsavebuttonclicked)
        self.Dotdisplaybutton.setDisabled(True)
        self.Dotsavebutton.setDisabled(True)

        #Numeral calibrate
        self.Numeralxbox = self.findChild(QtWidgets.QSpinBox, 'Numeralxbox')
        self.Numeralybox = self.findChild(QtWidgets.QSpinBox, 'Numeralybox')
        self.Numeralheightbox = self.findChild(QtWidgets.QSpinBox, 'Numeralheightbox')
        self.Numeralwidthbox = self.findChild(QtWidgets.QSpinBox, 'Numeralwidthbox')
        self.Numeralvelocitybox = self.findChild(QtWidgets.QDoubleSpinBox, 'Numeralvelocitybox')
        self.Numeraltimebox = self.findChild(QtWidgets.QLineEdit, 'Numeraltimebox')
        self.Numerallettersbox = self.findChild(QtWidgets.QSpinBox, 'Numerallettersbox')
     
        self.Numeralmodifybutton = self.findChild(QtWidgets.QPushButton, 'Numeralmodifybutton')
        self.Numeraldisplaybutton = self.findChild(QtWidgets.QPushButton, 'Numeraldisplaybutton')
        self.Numeralsavebutton = self.findChild(QtWidgets.QPushButton, 'Numeralsavebutton')
        self.Numeralmodifybutton.clicked.connect(self.Numeralmodifybuttonclicked)
        self.Numeraldisplaybutton.clicked.connect(self.Numeraldisplaybuttonclicked)
        self.Numeralsavebutton.clicked.connect(self.Numeralsavebuttonclicked)
        self.Numeraldisplaybutton.setDisabled(True)
        self.Numeralsavebutton.setDisabled(True)

    def setupUI(self):
        print("\033[1;101m SETUP UI \033[0m")

        self.parameterslist = cli_convertor.Parameterfile()
        self.preheatbottom = []
        self.preheatbottomcount = 0
        self.preheatlayer = []
        self.preheatlayercount = 0

        self.openGLWidget = additional_widgets.openGLDisplay(self.centralwidget)
        self.openGLWidget.setGeometry(QtCore.QRect(0, 0, 950, 950))
        self.openGLWidget.setObjectName("openGLWidget1")

        self.windowsHeight = self.openGLWidget.height()
        self.windowsWidth = self.openGLWidget.width()
        self.openGLWidget.resizeGL(self.windowsWidth, self.windowsHeight)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateopenGLWidget)
        self.timer.start(17)

    def updateopenGLWidget(self):
        self.Parseprogress.setValue(self.Parseprogressvalue.value)
        self.Modifyprogress.setValue(self.Modifyprogressvalue.value)
        self.Saveprogress.setValue(self.Saveprogressvalue.value)

        if(self.openGLWidget.updateflag):
            self.openGLWidget.updateflag = 0
            self.openGLWidget.update()

    def Menuquitclicked(self):
        sys.exit()

    def Selectindexboxchanged(self):
        self.Beamcurrentbox.setValue(self.parameterslist.parameters[self.Selectindexbox.value() + 1][0])
        self.Lenscurrentbox.setValue(self.parameterslist.parameters[self.Selectindexbox.value() + 1][1])
        self.Focuscurrentbox.setValue(self.parameterslist.parameters[self.Selectindexbox.value() + 1][2])
        self.Parameter4box.setValue(self.parameterslist.parameters[self.Selectindexbox.value() + 1][3])
        self.Parameter5box.setValue(self.parameterslist.parameters[self.Selectindexbox.value() + 1][4])

    def Changeparamindexbuttonclicked(self):
        self.parameterslist.change_parameters(self.Selectindexbox.value(), self.Beamcurrentbox.value(), self.Lenscurrentbox.value(), \
            self.Focuscurrentbox.value(), self.Parameter4box.value(), self.Parameter5box.value())

    def Saveparambuttonclicked(self):
        self.saveparamfilepath = str(QtWidgets.QFileDialog.getExistingDirectory(self,"Select Directory to save"))
        if(self.saveparamfilepath == ""):
            return

        self.saveparamfilepath = self.saveparamfilepath + '/'
        self.Saveparamtext.setText(self.saveparamfilepath)
        self.parameterslist.write_parameters(self.saveparamfilepath)

    def Preheatbottomcountbuttonclicked(self):
        self.preheatbottomcount = self.Preheatbottomcountbox.value()
        self.preheatbottom = []

        if(self.preheatbottomcount):
            self.Preheatbottomrunbox.setDisabled(False)
            self.Preheatbottomdistbox.setDisabled(False)
            self.Preheatbottomvelocitybox.setDisabled(False)
            self.Preheatbottombeambox.setDisabled(False)
            self.Preheatbottomlensbox.setDisabled(False)
            self.Preheatbottomfocusbox.setDisabled(False)
            self.openGLWidget.drawflag = 0
            self.openGLWidget.x = 0
            self.openGLWidget.y = 0
            self.openGLWidget.zoom = 1.0
            self.openGLWidget.updateflag = 1
            
            for _ in range(self.preheatbottomcount):
                self.preheatbottom.append(cli_convertor.Preheat())

            self.Displaypreheatbottombutton.setDisabled(False)
            self.Modifypreheatbottombutton.setDisabled(False)
            self.Preheatbottomindexbox.setMaximum(self.preheatbottomcount - 1)
            self.Preheatbottomindexbox.setValue(0)

        else:
            self.Displaypreheatbottombutton.setDisabled(True)
            self.Modifypreheatbottombutton.setDisabled(True)
            self.Preheatbottomindexbox.setMaximum(0)
            self.Preheatbottomindexbox.setValue(0)

        self.Preheatbottomindexboxchanged()

    def Preheatbottomindexboxchanged(self):
        if(self.preheatbottomcount):    
            value = self.Preheatbottomindexbox.value()
            self.Preheatbottomrunbox.setValue(self.preheatbottom[value].hatch_runcount)
            self.Preheatbottomvelocitybox.setValue(16.25 / self.preheatbottom[value].hatch_velocity)
            self.Preheatbottomdistbox.setValue(self.preheatbottom[value].hatch_distance)
            self.Preheatbottomhatchcountbox.setText(str(self.preheatbottom[value].hatchcount))
            self.Preheatbottomtimebox.setText(str(self.preheatbottom[value].time))
            self.Preheatbottombeambox.setValue(self.preheatbottom[value].hatch_beam_current)
            self.Preheatbottomlensbox.setValue(self.preheatbottom[value].hatch_lens_current)
            self.Preheatbottomfocusbox.setValue(self.preheatbottom[value].hatch_focus_current)

        else:
            self.Preheatbottomrunbox.setValue(1)
            self.Preheatbottomvelocitybox.setValue(325)
            self.Preheatbottomdistbox.setValue(0.1)
            self.Preheatbottomhatchcountbox.setText("")
            self.Preheatbottomtimebox.setText("")
            self.Preheatbottombeambox.setValue(0.5)
            self.Preheatbottomlensbox.setValue(0.5)
            self.Preheatbottomfocusbox.setValue(0.5)

    def Modifypreheatbottombuttonclicked(self):
        value = self.Preheatbottomindexbox.value()
        self.preheatbottom[value].modify_pattern(16.25 / self.Preheatbottomvelocitybox.value(), self.Preheatbottomdistbox.value(), \
            self.Preheatbottomrunbox.value(), self.Preheatbottombeambox.value(), self.Preheatbottomlensbox.value(), self.Preheatbottomfocusbox.value())

        self.Preheatbottomindexboxchanged()

    def Displaypreheatbottombuttonclicked(self):
        self.openGLWidget.currentlayer = self.preheatbottom[self.Preheatbottomindexbox.value()]
        self.openGLWidget.drawflag = 1
        self.openGLWidget.updateflag = 1

    def Preheatlayercountbuttonclicked(self):
        self.preheatlayercount = self.Preheatlayercountbox.value()
        self.preheatlayer = []

        if(self.preheatlayercount):
            self.Preheatlayerrunbox.setDisabled(False)
            self.Preheatlayerdistbox.setDisabled(False)
            self.Preheatlayervelocitybox.setDisabled(False)
            self.Preheatlayerbeambox.setDisabled(False)
            self.Preheatlayerlensbox.setDisabled(False)
            self.Preheatlayerfocusbox.setDisabled(False)
            self.Displaypreheatlayerbutton.setDisabled(False)
            self.openGLWidget.drawflag = 0
            self.openGLWidget.x = 0
            self.openGLWidget.y = 0
            self.openGLWidget.zoom = 1.0
            self.openGLWidget.updateflag = 1

            for _ in range(self.preheatlayercount):
                self.preheatlayer.append(cli_convertor.Preheat())

            self.Displaypreheatlayerbutton.setDisabled(False)
            self.Modifypreheatlayerbutton.setDisabled(False)
            self.Preheatlayerindexbox.setMaximum(self.preheatlayercount - 1)
            self.Preheatlayerindexbox.setValue(0)

        else:
            self.Displaypreheatlayerbutton.setDisabled(True)
            self.Modifypreheatlayerbutton.setDisabled(True)
            self.Preheatlayerindexbox.setMaximum(0)
            self.Preheatlayerindexbox.setValue(0)

        self.Preheatlayerindexboxchanged()

    def Preheatlayerindexboxchanged(self):
        if(self.preheatlayercount):    
            value = self.Preheatlayerindexbox.value()
            self.Preheatlayerrunbox.setValue(self.preheatlayer[value].hatch_runcount)
            self.Preheatlayervelocitybox.setValue(16.25 / self.preheatlayer[value].hatch_velocity)
            self.Preheatlayerdistbox.setValue(self.preheatlayer[value].hatch_distance)
            self.Preheatlayerhatchcountbox.setText(str(self.preheatlayer[value].hatchcount))
            self.Preheatlayertimebox.setText(str(self.preheatlayer[value].time))
            self.Preheatlayerbeambox.setValue(self.preheatlayer[value].hatch_beam_current)
            self.Preheatlayerlensbox.setValue(self.preheatlayer[value].hatch_lens_current)
            self.Preheatlayerfocusbox.setValue(self.preheatlayer[value].hatch_focus_current)

        else:
            self.Preheatlayerrunbox.setValue(1)
            self.Preheatlayervelocitybox.setValue(325)
            self.Preheatlayerdistbox.setValue(0.1)
            self.Preheatlayerhatchcountbox.setText("")
            self.Preheatlayertimebox.setText("")
            self.Preheatlayerbeambox.setValue(0.5)
            self.Preheatlayerlensbox.setValue(0.5)
            self.Preheatlayerfocusbox.setValue(0.5)

    def Modifypreheatlayerbuttonclicked(self):
        value = self.Preheatlayerindexbox.value()
        self.preheatlayer[value].modify_pattern(16.25 / self.Preheatlayervelocitybox.value(), self.Preheatlayerdistbox.value(), \
            self.Preheatlayerrunbox.value(), self.Preheatlayerbeambox.value(), self.Preheatlayerlensbox.value(), self.Preheatlayerfocusbox.value())

        self.Preheatlayerindexboxchanged()

    def Displaypreheatlayerbuttonclicked(self):
        self.openGLWidget.currentlayer = self.preheatlayer[self.Preheatlayerindexbox.value()]
        self.openGLWidget.drawflag = 1
        self.openGLWidget.updateflag = 1

    def Menuopenfileclicked(self):
        self.filepath = QtWidgets.QFileDialog.getOpenFileName(self,'CLI File',os.getcwd(),filter="Cli Files(*.cli)")
        if(self.filepath[0] != ""):
            self.filename = self.filepath[0]
            while('/' in self.filename):
                end = self.filename.find('/')
                self.filename = self.filename[(end + 1):]
                
            self.filename = self.filename[0:len(self.filename) - 4]
            self.Filenamebox.setText(self.filename)
            self.Filetext.setText(self.filepath[0])
            self.Parsebutton.setDisabled(True)
            self.Layerinformationbox.setDisabled(True)

            workerthread = additional_widgets.worker(cli_convertor.CLIFile, self.Filetext.text())
            workerthread.signals.result.connect(self.Fileimportcomplete)
            workerthread.signals.finished.connect(self.Enablebuttons)
            workerthread.signals.error.connect(self.Error)

            self.threadpool.start(workerthread)       

    def Fileimportcomplete(self, clifile):
        self.clifile = clifile

        try:
            self.clifile.count_layers()
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.Error((exctype, value, traceback.format_exc()))
            return

        self.openGLWidget.drawflag = 0
        self.openGLWidget.x = 0
        self.openGLWidget.y = 0
        self.openGLWidget.zoom = 1.0
        self.openGLWidget.updateflag = 1

        self.Tabs.setCurrentIndex(2)
        self.Fileinformationbox.setDisabled(False)
        self.Layerinformationbox.setDisabled(True)
        self.Savebox.setDisabled(True)
        self.Layerparsebox.setDisabled(True)
        self.Layercountbox.setText(str(self.clifile.layercount))
        self.Versionbox.setText(str(self.clifile.version))
        self.Datebox.setText(self.clifile.date)

    def Parsebuttonclicked(self):
        self.Parsebutton.setDisabled(True)
        self.Modifyparambutton.setDisabled(True)
        self.Savebutton.setDisabled(True)
        self.Selectlayerinfobox.setDisabled(True)
        self.Selectlayerinfoslider.setDisabled(True)
        self.Parseprogressvalue.value = 0

        workerthread = additional_widgets.worker(self.clifile.parse_layers, self.Parseprogressvalue)
        workerthread.signals.result.connect(self.Parsecomplete)
        workerthread.signals.finished.connect(self.Enablebuttons)
        workerthread.signals.error.connect(self.Error)

        self.threadpool.start(workerthread)

    def Parsecomplete(self, result):
        print("Parse successful")
        self.Parseprogressvalue.value = 100
        self.Layerinformationbox.setDisabled(False)
        self.Savebox.setDisabled(False)
        self.Layerparsebox.setDisabled(False)
        self.Selectlayerinfoslider.setMinimum(0)
        self.Selectlayerinfoslider.setMaximum(self.clifile.layercount - 1)
        self.Selectlayerinfobox.setMinimum(0)
        self.Selectlayerinfobox.setMaximum(self.clifile.layercount - 1)
        self.Selectlayerbox.setMinimum(0)
        self.Selectlayerbox.setMaximum(self.clifile.layercount - 1)
        print(len(self.clifile.layers))
        self.Selectlayerinfobox.setValue(0)
        self.Selectlayerboxchanged()
        self.Selectlayerbox.setValue(0)
        self.Selectlayerinfoslider.setValue(0)
        self.Displaylayerchange()

    def Selectlayerboxchanged(self):
        layer = self.clifile.layers[self.Selectlayerbox.value()]

        self.Polylinevelocitybox.setValue(16.25 / layer.polyline_velocity)
        self.Polylineruncountbox.setValue(layer.poly_runcount)
        self.Polylinebeambox.setValue(layer.polyline_beam_current)
        self.Polylinelensbox.setValue(layer.polyline_lens_current)
        self.Polylinefocusbox.setValue(layer.polyline_focus_current)

        self.Hatchvelocitybox.setValue(16.25 / layer.hatch_velocity)
        self.Hatchruncountbox.setValue(layer.hatch_runcount)
        self.Hatchbeambox.setValue(layer.hatch_beam_current)
        self.Hatchlensbox.setValue(layer.hatch_lens_current)
        self.Hatchfocusbox.setValue(layer.hatch_focus_current)

    def Modifyparambuttonclicked(self):
        text = self.Selectlayersbox.text()
        if (text == ""):
            return
        text = text.replace(" ", "")

        values = []
        flag = True
        errorflag = 0
        while(flag):
            if (',' in text):
                end = text.find(',')
                substring = text[:end]
                text = text[(end + 1):]

            else :
                substring = text
                flag = False

            if ('-' in substring):
                end = substring.find('-')

                substring1 = substring[:end]
                substring2 = substring[(end+1):]
                if('-' in substring2):
                    errorflag = 1
                    break

                if(substring1.isnumeric()):
                    value1 = int(substring1)
                else :
                    errorflag = 1
                    break

                if(substring2.isnumeric()):
                    value2 = int(substring2)
                else :
                    errorflag = 1
                    break

                if(value1 > value2):
                    value1, value2 = value2, value1 
                    break

                value = list(range(value1,value2 + 1))
                values += value

            else :
                if(substring.isnumeric()):
                    value = int(substring)
                    values.append(value)
                else :
                    errorflag = 1
                    break

        for i in values:
            if(i > self.clifile.layercount):
                errorflag = 2

        if(errorflag != 0):
            errorwindow = QtWidgets.QErrorMessage(self)
            errorwindow.setWindowModality(QtCore.Qt.WindowModal)
            if (errorflag == 1):
                errorwindow.showMessage("Unknown character")
            elif (errorflag == 2):
                errorwindow.showMessage("Layer index out of bounds")
            return

        self.Parsebutton.setDisabled(True)
        self.Savebutton.setDisabled(True)
        self.Savebuttonstatic.setDisabled(True)
        self.Modifyparambutton.setDisabled(True)
        self.Selectlayerinfobox.setDisabled(True)
        self.Selectlayerinfoslider.setDisabled(True)
        self.Modifyprogressvalue.value = 0

        workerthread = additional_widgets.worker(self.Modifyparameters, values)
        workerthread.signals.result.connect(self.Modifyparameterscomplete)
        workerthread.signals.finished.connect(self.Enablebuttons)
        workerthread.signals.error.connect(self.Error)

        self.threadpool.start(workerthread)

    def Modifyparameters(self, values):
        for i in values:
            if(i < self.clifile.layercount):
                self.clifile.setlayer_parameters(i, 16.25 / self.Polylinevelocitybox.value(), 16.25 / self.Hatchvelocitybox.value(), \
                    self.Polylineruncountbox.value(), self.Hatchruncountbox.value(), self.Polylinebeambox.value(), self.Hatchbeambox.value(), \
                        self.Polylinelensbox.value(), self.Hatchlensbox.value(), self.Polylinefocusbox.value(), self.Hatchfocusbox.value())
            
            self.Modifyprogressvalue.value = int(100*i/len(values))

    def Modifyparameterscomplete(self):
        print("Modify complete")
        self.Modifyprogressvalue.value = 100
        self.Displaylayerchange()
        self.Selectlayerboxchanged()

    def Displaylayerchange(self):
        self.currentlayer = self.clifile.layers[self.Selectlayerinfobox.value()]
        self.Selectlayerinfoslider.setValue(self.Selectlayerinfobox.value())
        self.openGLWidget.currentlayer = self.currentlayer
        self.Polylinecountbox.setText(str(self.currentlayer.polylinecount))
        self.Hatchcountbox.setText(str(self.currentlayer.hatchcount))
        self.Layerheightbox.setText(str(self.currentlayer.height))
        self.Polylinetimebox.setText(str(self.currentlayer.poly_time))
        self.Hatchtimebox.setText(str(self.currentlayer.hatch_time))
        self.openGLWidget.drawflag = 1
        self.openGLWidget.updateflag = 1

    def Displaylayerchangeslider(self):
        self.Selectlayerinfobox.setValue(self.Selectlayerinfoslider.value())

    def Savebuttonclicked(self):
        self.savefilepath = str(QtWidgets.QFileDialog.getExistingDirectory(self,"Select Directory to save"))
        if(self.savefilepath == ""):
            return
            
        self.savefilepath += "/" + self.filename
        self.Savetext.setText(self.savefilepath)

        self.clifile.preheat_bottom = self.preheatbottom
        self.clifile.preheat_bottom_count = self.preheatbottomcount
        self.Preheatbottomcountbutton.setDisabled(True)
        self.Modifypreheatbottombutton.setDisabled(True)
        
        self.clifile.preheat_layers = self.preheatlayer
        self.clifile.preheat_layers_count = self.preheatlayercount
        self.Preheatlayercountbutton.setDisabled(True)
        self.Modifypreheatlayerbutton.setDisabled(True)

        self.Saveprogressvalue.value = 0

        try:
            shutil.rmtree(self.savefilepath)
        except OSError:
            pass

        try:
            os.mkdir(self.savefilepath)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.Error((exctype, value, traceback.format_exc()))
            return

        self.Parsebutton.setDisabled(True)
        self.Savebutton.setDisabled(True)        
        self.Savebuttonstatic.setDisabled(True)
        self.Modifyparambutton.setDisabled(True)

        workerthread = additional_widgets.worker(self.clifile.write_layers, self.savefilepath, self.Saveprogressvalue, self.preheatlayercount)
        workerthread.signals.result.connect(self.Savecomplete)
        workerthread.signals.finished.connect(self.Enablebuttons)
        workerthread.signals.error.connect(self.Error)

        self.threadpool.start(workerthread)

    def Savebuttonstaticclicked(self):
        self.savefilepath = "/home/sahil/Documents/M3DP/AMCOE/testsave/static"

        self.Savetext.setText(self.savefilepath)

        self.clifile.preheat_bottom = self.preheatbottom
        self.clifile.preheat_bottom_count = self.preheatbottomcount
        self.Preheatbottomcountbutton.setDisabled(True)
        self.Modifypreheatbottombutton.setDisabled(True)
        
        self.clifile.preheat_layers = self.preheatlayer
        self.clifile.preheat_layers_count = self.preheatlayercount
        self.Preheatlayercountbutton.setDisabled(True)
        self.Modifypreheatlayerbutton.setDisabled(True)

        self.Saveprogressvalue.value = 0

        try:
            if(os.listdir(self.savefilepath)):
                buttonReply = QtWidgets.QMessageBox.question(self, 'Save files', "Overwrite Files",\
                     QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                if buttonReply == QtWidgets.QMessageBox.Cancel:
                    return
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.Error((exctype, value, traceback.format_exc()))
            return
            
        for filename in os.listdir(self.savefilepath):
            file_path = os.path.join(self.savefilepath, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.Error((exctype, value, traceback.format_exc()))
                return

        self.Parsebutton.setDisabled(True)
        self.Savebutton.setDisabled(True)
        self.Savebuttonstatic.setDisabled(True)
        self.Modifyparambutton.setDisabled(True)

        workerthread = additional_widgets.worker(self.clifile.write_layers, self.savefilepath, self.Saveprogressvalue, self.preheatlayercount)
        workerthread.signals.result.connect(self.Savecomplete)
        workerthread.signals.finished.connect(self.Enablebuttons)
        workerthread.signals.error.connect(self.Error)

        self.threadpool.start(workerthread)

    def Savecomplete(self):
        print("Save complete")
        self.Saveprogressvalue.value = 100

    def Crossmodifybuttonclicked(self):
        self.crosscalibrate = cli_convertor.Crosscalibrate(self.Crosshatchfactorbox.value(), self.Crosshatchvelocitybox.value())
        self.Crosstimebox.setText(str(self.crosscalibrate.time))
        self.Crossdisplaybutton.setDisabled(False)
        self.Crosssavebutton.setDisabled(False)

    def Crossdisplaybuttonclicked(self):
        self.openGLWidget.currentlayer = self.crosscalibrate
        self.openGLWidget.drawflag = 1
        self.openGLWidget.updateflag = 1

    def Crosssavebuttonclicked(self):
        crosssavefilepath = str(QtWidgets.QFileDialog.getExistingDirectory(self,"Select Directory to save"))
        self.crosscalibrate.write_pattern(crosssavefilepath)

    def Squaremodifybuttonclicked(self):
        self.squarecalibrate = cli_convertor.Squarecalibrate(self.Squaregapbox.value(), self.Squaredotspacingbox.value())
        self.Squaretimebox.setText(str(self.squarecalibrate.time))
        self.Squaredisplaybutton.setDisabled(False)
        self.Squaresavebutton.setDisabled(False)

    def Squaredisplaybuttonclicked(self):
        self.openGLWidget.currentlayer = self.squarecalibrate
        self.openGLWidget.drawflag = 1
        self.openGLWidget.updateflag = 1

    def Squaresavebuttonclicked(self):
        squaresavefilepath = str(QtWidgets.QFileDialog.getExistingDirectory(self,"Select Directory to save"))
        self.squarecalibrate.write_pattern(squaresavefilepath)

    def Dotmodifybuttonclicked(self):
        self.dotcalibrate = cli_convertor.Dotcalibrate(self.Dotgapbox.value(), self.Dotspacingbox.value(), self.Dotholdbox.value())
        self.Dottimebox.setText(str(self.dotcalibrate.time))
        self.Dotdisplaybutton.setDisabled(False)
        self.Dotsavebutton.setDisabled(False)

    def Dotdisplaybuttonclicked(self):
        self.openGLWidget.currentlayer = self.dotcalibrate
        self.openGLWidget.drawflag = 1
        self.openGLWidget.updateflag = 1

    def Dotsavebuttonclicked(self):
        dotsavefilepath = str(QtWidgets.QFileDialog.getExistingDirectory(self,"Select Directory to save"))
        self.dotcalibrate.write_pattern(dotsavefilepath)

    def Numeralmodifybuttonclicked(self):
        self.numeralcalibrate = cli_convertor.Numbercalibrate(self.Numeralheightbox.value(), self.Numeralwidthbox.value(), \
            self.Numeralxbox.value(), self.Numeralybox.value(), self.Numeralvelocitybox.value(), self.Numerallettersbox.value())
        self.Numeraltimebox.setText(str(self.numeralcalibrate.time))
        self.Numeraldisplaybutton.setDisabled(False)
        self.Numeralsavebutton.setDisabled(False)

    def Numeraldisplaybuttonclicked(self):
        self.openGLWidget.currentlayer = self.numeralcalibrate
        self.openGLWidget.drawflag = 1
        self.openGLWidget.updateflag = 1

    def Numeralsavebuttonclicked(self):
        numeralsavefilepath = str(QtWidgets.QFileDialog.getExistingDirectory(self,"Select Directory to save"))
        self.numeralcalibrate.write_pattern(numeralsavefilepath + "/numerals")

    def Enablebuttons(self):

        self.Parsebutton.setDisabled(False)
        if(self.Savebox.isEnabled):
            self.Savebutton.setDisabled(False)
            self.Savebuttonstatic.setDisabled(False)
        if(self.Layerparsebox.isEnabled):
            self.Modifyparambutton.setDisabled(False)
        if(self.Layerinformationbox.isEnabled):
            self.Selectlayerinfobox.setDisabled(False)
            self.Selectlayerinfoslider.setDisabled(False)

        self.Preheatbottomcountbutton.setDisabled(False)
        if(self.preheatbottomcount):
            self.Modifypreheatbottombutton.setDisabled(False)

        self.Preheatlayercountbutton.setDisabled(False)
        if(self.preheatlayercount):
            self.Modifypreheatlayerbutton.setDisabled(False)

    def Error(self, error):
        self.Errorbox = additional_widgets.ErrorWindow(str(error[0]), str(error[2]))
        self.Errorbox.show()


app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
window = mainWindow()
window.setupUI()
window.show()
window.showMaximized()
sys.exit(app.exec_())
