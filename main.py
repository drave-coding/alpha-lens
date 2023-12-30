from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon

# #imports
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import cv2

#models and maps
TF_MODEL_URL = 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_asia_V1/1'
LABEL_MAP_URL = './label_map/landmarks_classifier_asia_V1_label_map.csv'
# LABEL_MAP_URL = 'https://www.gstatic.com/aihub/tfhub/labelmaps/landmarks_classifier_asia_V1_label_map.csv'
IMAGE_SHAPE = (321, 321)

#reading csv file
df=pd.read_csv(LABEL_MAP_URL)


# Creating Identifier
identifier=tf.keras.Sequential([hub.KerasLayer(
    TF_MODEL_URL, 
    input_shape=IMAGE_SHAPE +(3,),
    output_key="predictions:logits"
 )])

# creating label map i.e. a dictionary 
label_map=dict(zip(df.id, df.name))

# photo editing and classification function

def classifyimg(RGBimg):
    RGBimg=np.array(RGBimg)/255
    RGBimg=np.reshape(RGBimg, (1,321,321,3))
    prediction=identifier.predict(RGBimg)
    return label_map[np.argmax(prediction)]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(409, 723)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 411, 731))
        self.graphicsView.setStyleSheet("image:url(:/newPrefix/logo.png)")
        self.graphicsView.setObjectName("graphicsView")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 30, 201, 71))
        font = QtGui.QFont()
        font.setFamily("Cooper Black")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 500, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(".QPushButton{\n"
"    background-color: #4A494A;\n"
"    border-radius: 12px;\n"
"    \n"
"    color: white;\n"
"    border: 2px solid #f44336\n"
"}\n"
"\n"
".QPushButton:hover{\n"
"    background-color: white;\n"
"    color:black\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-20, 90, 451, 411))
        self.label.setStyleSheet("image:url(logo.png)")
        self.label.setText("")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Alpha Lens"))
        MainWindow.setWindowIcon(QIcon('Brandlogo_new.png'))
        self.label_2.setText(_translate("MainWindow", "Alpha Lens"))
        self.pushButton.setText(_translate("MainWindow", "Get an Image"))
        self.pushButton.clicked.connect(self.upload_img)
        
    # Creating Image Function
    def upload_img(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        path = str(path)
        img=cv2.imread(path)
        BGRimg=cv2.resize(img,(640,480))
        RGBimg=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        RGBimg=cv2.resize(RGBimg,(321,321))
        result=classifyimg(RGBimg)
        print(result)

        
        # output page
        cv2.rectangle(BGRimg, (0, 480), (640, 425),(61, 61, 61), -2)
        cv2.putText(BGRimg, 'Result: {}'.format(str(result)), (20,460), cv2.FONT_HERSHEY_DUPLEX, 
                   1, (255,255,255), 1, cv2.LINE_AA)
        cv2.imshow("The Image",BGRimg)
        cv2.waitKey(0)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
