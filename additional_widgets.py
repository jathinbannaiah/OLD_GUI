from OpenGL import GL, GLU, GLUT

from PyQt5 import QtCore, QtWidgets, uic

import traceback, sys, os, shutil

import cli_convertor

class mutableint():

    def __init__(self, value = 0):

        self.value = value

class workersignals(QtCore.QObject):

    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)
 
class worker(QtCore.QRunnable):
    
    def __init__(self, function, *args):
        
        super(worker, self).__init__()

        self.function = function
        self.args = args
        self.signals = workersignals()

    @QtCore.pyqtSlot()
    def run(self):
        try:
            result = self.function(*self.args)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  
        finally:
            self.signals.finished.emit()

class openGLDisplay(QtWidgets.QOpenGLWidget):

    def __init__(self, *args):

        super(openGLDisplay, self).__init__(*args)
        self.zoom = 1
        self.drawflag = 0
        self.prev_x = 0
        self.prev_y = 0
        self.x = 0.0
        self.y = 0.0
        self.updateflag = 1
    
    def paintGL(self):
        self.loadScene()
        GLUT.glutInit()
        GL.glClearColor(0.7, 0.7, 0.7, 0)		
        GL.glClearDepth(1)

        GL.glColor3f(0.0, 0.0, 0.0)   

        GL.glBegin(GL.GL_LINE_LOOP)
        GL.glVertex3f(4, 4, 0)
        GL.glVertex3f(4, -4, 0)
        GL.glVertex3f(-4, -4, 0)
        GL.glVertex3f(-4, 4, 0)
        GL.glEnd()

        scale_factor = 7700 / 4.0
        
        if (self.drawflag):

            if (self.currentlayer.polylinecount):
                GL.glColor3f(0.2, 0.2, 0.2)
                GL.glBegin(GL.GL_LINES)
                
                prev_polyline = self.currentlayer.polylines[0]
                for polyline in self.currentlayer.polylines:
                    if (polyline[2]):
                        GL.glVertex3f(prev_polyline[0] / scale_factor, prev_polyline[1] / scale_factor, 0)
                        GL.glVertex3f(polyline[0] / scale_factor, polyline[1] / scale_factor, 0)
                    prev_polyline = polyline
                
                GL.glEnd()

            if (self.currentlayer.hatchcount):
                GL.glColor3f(0.4, 0.4, 0.4)
                GL.glBegin(GL.GL_LINES)
                
                for hatch in self.currentlayer.hatches:
                    GL.glVertex3f(hatch[0] / scale_factor, hatch[1] / scale_factor, 0)
                    GL.glVertex3f(hatch[2] / scale_factor, hatch[3] / scale_factor, 0)

                GL.glEnd()

    def initializeGL(self):
        print("\033[4;30;102m INITIALIZE GL\033[0m")
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def loadScene(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        _, _, width, height = GL.glGetDoublev(GL.GL_VIEWPORT)
        GLU.gluPerspective(
            45,
            width / float(height or 1), 
            .25, 
            200, 
        )

        GLU.gluLookAt(self.x, self.y, 10 * self.zoom, self.x, self.y, 0, 0, 1, 0)

    def mousePressEvent(self, event):
        self.prev_x = event.x()
        self.prev_y = event.y()

    def mouseMoveEvent(self, event):
        self.x += (self.prev_x - event.x()) * 8 * self.zoom / 950
        self.y += (event.y() - self.prev_y) * 8 * self.zoom / 950
        self.updateflag = 1

        if (self.x > 4):
            self.x = 4
        elif (self.x < -4):
            self.x = -4
        
        if (self.y > 4):
            self.y = 4
        elif (self.y < -4):
            self.y = -4
        
        self.prev_x = event.x()
        self.prev_y = event.y()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        zoom = self.zoom - (delta / 2400.0)
        self.updateflag = 1

        if (zoom > 2):
            self.zoom = 2
        elif (zoom < 0.05):
            self.zoom = 0.05
        else:
            self.zoom = zoom

class ErrorWindow(QtWidgets.QMainWindow):          

    def __init__(self, *args):

        super(ErrorWindow, self).__init__()
        uic.loadUi('ErrorGUI.ui', self)
        self.setWindowTitle("Error")

        self.Exitbutton = self.findChild(QtWidgets.QPushButton, 'Exitbutton')
        self.Errorbox = self.findChild(QtWidgets.QLineEdit, 'Errorbox')
        self.Tracebackbox = self.findChild(QtWidgets.QTextEdit, 'Tracebackbox')
        self.Exitbutton.clicked.connect(self.Exitbuttonclicked)

        self.Errorbox.setText(args[0])
        self.Tracebackbox.setText(args[1])

    def Exitbuttonclicked(self):
        self.close()
