from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import center
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
import sys
from numpy.lib.function_base import select
from win32api import GetSystemMetrics   #pip install pywin32
import pandas as pd
import text_preprocessing as tp
import text_classification as tc
import joblib
import os
import numpy as np


class my_window(QMainWindow):
    def __init__(self):
        super(my_window, self).__init__()
        """ initialize nlp class """
        self.my_tp = tp.text_preprocessing()
        self.my_tc = tc.text_classification()
        
        # set size
        self.screenWidth = GetSystemMetrics(0)
        self.screenHeight = GetSystemMetrics(1)
        self.appWidth = 480
        self.appHeight = 480
        self.setContentsMargins(20,20,20,20)
        
        
        # setting app
        self.setGeometry((self.screenWidth - self.appWidth) / 2,
                         (self.screenHeight - self.appHeight) / 2,
                         self.appWidth, self.appHeight)

        self.setWindowTitle("Early Stage of Depression Screening Tool")
     
        """ initialize all buttons and labels """

        """ all label initialization and setting """
        self.TitleLabel = QtWidgets.QLabel("Early Stage of Depression Screening Tool",self)
        self.TitleLabel.setWordWrap(True)
        self.TitleLabel.setFixedWidth(self.appWidth-20)
        self.TitleLabel.setMinimumHeight(100)
        self.TitleLabel.setFont(QFont('Arial', pointSize=24))
        self.TitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TitleLabel.setGeometry(int((self.appWidth-self.TitleLabel.width())/2), 50, 100, 100)
        self.TitleLabel.wordWrap()
        self.TitleLabel.hide()

        subtitle = "This tool is used to find the symptoms and risk factors from your story.\nThen, the depression will be consider based on the predicted symptoms "
        
        self.subLabel1 = QtWidgets.QLabel(subtitle,self)
        self.subLabel1.setWordWrap(True)
        self.subLabel1.setFixedWidth(self.appWidth-100)
        self.subLabel1.setMinimumHeight(50)
        self.subLabel1.setFont(QFont('Arial', pointSize=12))
        self.subLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.subLabel1.setGeometry(int((self.appWidth-self.subLabel1.width())/2), 200, 100, 200)
        self.subLabel1.wordWrap()
        self.subLabel1.hide()

        subtitle1 = "Please insert new text or your existing text file."
        self.subLabel2 = QtWidgets.QLabel(subtitle1,self)

        self.subLabel2.setWordWrap(True)
        self.subLabel2.setFixedWidth(self.appWidth-100)
        self.subLabel2.setMinimumHeight(50)
        self.subLabel2.setFont(QFont('Arial', pointSize=12))
        self.subLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.subLabel2.setGeometry(int((self.appWidth-self.subLabel2.width())/2), 200, 100, 100)
        self.subLabel2.wordWrap()
        
        self.subLabel2.hide()

        """ all Button initialization and setting """
        self.button3 = QtWidgets.QPushButton('Submit',self)
        self.button2 = QtWidgets.QPushButton('Import text file',self)
        self.button1 = QtWidgets.QPushButton('Enter new text',self)

        self.button3.setFont(QFont('Arial', pointSize=12))
        self.button2.setFont(QFont('Arial', pointSize=12))
        self.button1.setFont(QFont('Arial', pointSize=12))
        
        self.button3.setMinimumWidth(150)
        self.button2.setMinimumWidth(150)
        self.button1.setMinimumWidth(150)

        self.button2.move((self.appWidth - self.button2.width()) / 2 , self.appHeight - 150)
        self.button1.move((self.appWidth - self.button2.width()) / 2 , self.appHeight - 190)

        
        
        self.button3.hide()
        self.button2.hide()
        self.button1.hide()

        """ textedit """
        self.answerText = QtWidgets.QTextEdit(self)
        self.answerText.setFont(QFont('Arial', pointSize=11))
        self.answerText.lineWrapMode()
        self.answerText.setAcceptRichText(True)
        self.answerText.setGeometry(20, 100, self.appWidth - 40, self.appHeight-40)
        self.answerText.hide()        


        """ tablewidget """
        self.tablewidget = QTableWidget()
        self.tablewidget.setColumnCount(2)
        self.tablewidget.setGeometry(int((self.appWidth-self.TitleLabel.width())/2), 50, 100, 100)
        self.tablewidget.hide()
        # call other function
        self.initUI()
    

    def startUI(self):
        """ resize the app """
        self.appHeight = 480
        self.setGeometry((self.screenWidth - self.appWidth) / 2,
                         (self.screenHeight - self.appHeight) / 2,
                         self.appWidth, self.appHeight)

        """ show all need buttons and label """
        self.TitleLabel.show()
        self.subLabel1.show()
        self.subLabel2.show()
        self.button1.show()
        self.button2.show()
        self.answerText.hide()   
        
        """ all setting for the button and label """
        self.button2.setText("Import text file")
        self.button1.setText("Enter new text")
        self.subLabel1.setGeometry(int((self.appWidth-self.subLabel1.width())/2), 150, 100, 100)
        self.subLabel2.setGeometry(int((self.appWidth-self.subLabel1.width())/2), 240, 100, 100)

        subtitle = "This tool is used to find the symptoms and risk factors from your story.\n\nThe depression will be consider based on the predicted symptoms "
        self.subLabel1.setText(subtitle)
        self.subLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.button2.move((self.appWidth - self.button2.width()) / 2 , self.appHeight - 100)
        self.button1.move((self.appWidth - self.button2.width()) / 2 , self.appHeight - 140)
        self.button2.clicked.connect(self.import_file)
        self.button1.clicked.connect(self.questionUI)

    def initUI(self):  # setting labels and button
        self.startUI()

        #self.nextBtn()

    def questionUI(self):
        """ hide unnecessary labels and button and resize the app's width """

        self.TitleLabel.hide()
        self.subLabel2.hide()
        

        """ resize the app """

        self.appHeight = 640
        self.setGeometry((self.screenWidth - self.appWidth) / 2,
                         (self.screenHeight - self.appHeight) / 2,
                         self.appWidth, self.appHeight)

        """ rewrite the text  """

        self.subLabel1.setText("tell us your story")
        self.subLabel1.setGeometry(int((self.appWidth-self.TitleLabel.width())/2)+10, 50, 100, 100)
        self.subLabel1.setAlignment(QtCore.Qt.AlignLeft)

        self.answerText.setText(None)
        self.answerText.show()

        self.button1.move(30  , self.appHeight - 80)
        self.button1.setText("Back")
        self.button1.clicked.connect(self.startUI)
        self.button3.show()
        self.button3.move((self.appWidth - self.button2.width())-30  , self.appHeight - 80)
        self.button3.setText("Submit")
        
        if len(self.answerText.toPlainText()) is not None:
            self.button3.clicked.connect(self.submitButton)

    

    def submitButton(self):
        try:
            text = self.answerText.toPlainText()
            textlist = text.split(".")
            sentences = [self.my_tp.data_preparation(s) for s in textlist]
            sentences = [s for s in sentences if len(s) > 0]

            predict = self.predicting_text(sentences)
            for (s,p) in zip(textlist, predict):
                    print(s," : ",p)

            print("\n\n")
        except ValueError:
            pass

    def import_file(self):
        self.filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', "E:\StudyAtUM\Sem 9\FYP 2" , '*.txt')
        try:
            
            file = open(self.filePath, "r+", encoding="utf-8") 
            text = file.read()
            textlist = text.split(".")
            sentences = [self.my_tp.data_preparation(s) for s in textlist]
            sentences = [s for s in sentences if len(s) > 0]
            #print(sentences)
            predict = self.predicting_text(sentences)
            #print(df)
            for (s,p) in zip(textlist, predict):
                print(s," : ",p)

            print("\n*****************\n")
            file.close()
            #self.resultUI(textlist,predict)
            
        except FileNotFoundError:
            pass
        

    def predicting_text(self,textList):
        print("*****************\n")
        model = joblib.load(os.path.join('Depression_screening.model'))
        category = {
            0: 'no-deppressive',
            1: 'symptom' ,
            2: 'risk factor',
            3: 'medical history',}
        
        feature = self.my_tc.input_feature_extraction(textList)
        #testFile = feature * y
        predict = model.predict(feature)
        predict = [category[p] for p in predict]
        return predict
            
    def resultUI(self, textlist, predictlist):
        self.appHeight = 640
        self.appWidth = 800
        self.setGeometry((self.screenWidth - self.appWidth) / 2,
                         (self.screenHeight - self.appHeight) / 2,
                         self.appWidth, self.appHeight)


        self.TitleLabel.hide()
        #self.subLabel1.hide()
        #self.subLabel2.hide()
        self.button1.hide()
        self.button2.hide()
        self.subLabel1.setText("\n".join(textlist))
        self.subLabel1.setAlignment(QtCore.Qt.AlignLeft)
        self.subLabel1.move(50, 50)
        self.subLabel1.setFixedWidth(590)
        self.subLabel1.setFixedHeight(600)
        self.subLabel1.setWordWrap(False)

        self.subLabel2.setText("\n".join(predictlist))
        self.subLabel2.setAlignment(QtCore.Qt.AlignLeft)
        self.subLabel2.move(610, 50)
        self.subLabel2.setFixedWidth(150)
        self.subLabel2.setFixedHeight(600)
        #self.tablewidget.show()

def window():
    # initilize app
    app = QApplication(sys.argv)
    win = my_window()
    win.show()
    sys.exit(app.exec_())


window()
