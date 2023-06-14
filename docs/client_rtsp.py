from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QTimer
import sys
import cv2
import os
import time
from ui_rtsp import *

class AnaPencere(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        
        super(AnaPencere, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        self.ui.pushButtonOk.clicked.connect(self.rtspAdres)
        self.dur =False
        self.ui.pushButtonPlay.clicked.connect(self.controlTimer)
        self.ui.pushButtonStop.clicked.connect(self.stop)

    def rtspAdres(self):
        self.adress = self.ui.lineEdit_ipAdress.text()
    
    def stop(self):
        if self.timer.isActive():
            self.timer.stop()
            # release video capture
            self.cap.release()

    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture("rtsp://"+self.adress+":8554/video_stream")
            # start timer
            self.timer.start(1)

    def viewCam(self):
        start_time = time.time()
        ret, image = self.cap.read()

        sum = 0
        N = 100
        for i in range(0,N):
            for j in range(0,N):
                sum +=1
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (640,480))

        adres = os.getcwd()
        self.frame_cascade = cv2.CascadeClassifier(adres+"/haarcascade_frontalface_default.xml")
        self.frame_rect = self.frame_cascade.detectMultiScale(image, minNeighbors = 5)

        for (x,y,w,h) in self.frame_rect:
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,150), 7)

        height, width, channel = image.shape
        step = channel * width
        time.sleep(0.15)
        fps = 1.0 / (time.time() - start_time)
        fps = int(fps)
        cv2.putText(image, "FPS: "+str(fps), (25,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), 2)

        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.ui.labelCam.setPixmap(QPixmap.fromImage(qImg))
               

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = AnaPencere()
    mainWindow.show()
    sys.exit(app.exec_())
