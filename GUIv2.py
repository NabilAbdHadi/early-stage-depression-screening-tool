from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pandas as pd
import sys, os, joblib
from win32api import GetSystemMetrics
import text_preprocessing as tp 
import text_classification as tc 


my_tp = tp.text_preprocessing()
my_tc = tc.text_classification()

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Depression Screening Tool")
        self.screenWidth = GetSystemMetrics(0)
        self.screenHeight = GetSystemMetrics(1)
        self.appWidth = 480
        self.appHeight = 480
        self.setGeometry((self.screenWidth-self.appWidth)/2, (self.screenHeight-self.appHeight)/2,self.appWidth,self.appHeight)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layout()

    def mainDesign(self):
        self.setStyleSheet("font-size:12pt;font-family:Arial;margin 10pt;padding:10pt;")
        self.mainTitle = QLabel("Early Stage of Depression Screening Tool")
        self.mainTitle.setStyleSheet("font-size:24pt;font-family:Arial Black")
        self.mainTitle.setAlignment(Qt.AlignCenter)
        self.mainTitle.setWordWrap(True)
        self.subtitle1 = QLabel("This system purpose is to predict the symptoms and risk factor of the depression from the User's text ")
        self.subtitle1.setStyleSheet("font-size:14pt")
        self.subtitle1.setAlignment(Qt.AlignCenter)
        self.subtitle1.setWordWrap(True)
        

        self.newInputBtn = QPushButton("Enter New Text")
        self.newInputBtn.setFixedSize(150,30)
        self.newInputBtn.clicked.connect(self.enterNewtext)
        self.importFileBtn = QPushButton("Import Text File")
        self.importFileBtn.setFixedSize(150,30)
        self.importFileBtn.clicked.connect(self.importExistingFile)

    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(50,20,50,20)
        #self.mainLayout.addSpacing(25)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.mainTitle)
        self.mainLayout.addSpacing(25)
        self.mainLayout.addWidget(self.subtitle1)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.newInputBtn,alignment=Qt.AlignHCenter)
        self.mainLayout.addWidget(self.importFileBtn,alignment=Qt.AlignHCenter)
        self.mainLayout.addStretch()
        
        self.setLayout(self.mainLayout)

    def enterNewtext(self):
        self.newWindow = questionWindow()
        self.close()

    def importExistingFile(self):
        global my_tp
        filename, ok = QFileDialog.getOpenFileName(self, "Import File","","*.txt")
        if ok:
            file = open(filename,"r+",encoding='utf-8')
            text = file.read()
            textlist = text.split(".")
            sentences = [my_tp.data_preparation(s) for s in textlist if s != ""]
            sentences = [s for s in sentences if len(s) > 0]
            #print(sentences)
            resultList = []
            predict = self.predicting_text(sentences)
            #print(df)
            for (s,p) in zip(textlist, predict):
                #print(s," : ",p)
                resultList.append([s,p])

            file.close()
            self.close()
            self.newWindow = resultWindow(resultList)

    def predicting_text(self,textList):
        global my_tc
        model = joblib.load(os.path.join('Depression_screening.model'))
        category = {
            0: 'no-deppressive',
            1: 'symptom' ,
            2: 'risk factor',
            3: 'medical history',}
        
        feature = my_tc.input_feature_extraction(textList)
        #testFile = feature * y
        predict = model.predict(feature)
        predict = [category[p] for p in predict]
        return predict


class questionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Depression Screening Tool")
        self.screenWidth = GetSystemMetrics(0)
        self.screenHeight = GetSystemMetrics(1)
        self.appWidth = 480
        self.appHeight = 640
        self.setGeometry((self.screenWidth-self.appWidth)/2, (self.screenHeight-self.appHeight)/2,self.appWidth,self.appHeight)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layout()

    def mainDesign(self):
        self.setStyleSheet("font-size:12pt;font-family:Arial;margin 10pt;padding:10pt;")
        self.question = QLabel("Tell us your story")
        self.question.setStyleSheet("font-size:14pt;")
        self.editor = QTextEdit()
        self.backBtn = QPushButton("Back")
        self.backBtn.setFixedSize(150,30)
        self.backBtn.clicked.connect(self.backEvent)
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.setFixedSize(150,30)
        self.submitBtn.clicked.connect(self.submitEvent)

    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(20,20,20,20)
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QHBoxLayout()

        self.mainLayout.addLayout(self.topLayout,80)
        self.mainLayout.addLayout(self.bottomLayout,20)
        self.topLayout.addWidget(self.question,20,alignment=Qt.AlignCenter)
        self.topLayout.addWidget(self.editor,80)
        self.bottomLayout.addWidget(self.backBtn)
        self.bottomLayout.addStretch
        self.bottomLayout.addWidget(self.submitBtn)

        self.setLayout(self.mainLayout)

    def backEvent(self):
        self.backwin = mainWindow()
        self.close()
        
    def submitEvent(self):
        text = self.editor.toPlainText()
        textlist = text.split(".")
        sentences = [my_tp.data_preparation(s) for s in textlist if s != ""]
        sentences = [s for s in sentences if len(s) > 0]
        predict = self.predicting_text(sentences)
        resultList=[]
        for (s,p) in zip(textlist, predict):
            #print(s," : ",p)
            resultList.append([s,p])

        self.newWindow = resultWindow(resultList)
        self.close()

    def predicting_text(self,textList):
        global my_tc
        model = joblib.load(os.path.join('Depression_screening.model'))
        category = {
            0: 'non-deppressive',
            1: 'symptom' ,
            2: 'risk factor',
            3: 'medical history',}
        
        feature = my_tc.input_feature_extraction(textList)
        #testFile = feature * y
        predict = model.predict(feature)
        predict = [category[p] for p in predict]
        return predict

class resultWindow(QWidget):
    def __init__(self,textlist):
        super().__init__()
        self.result = textlist
        self.setWindowTitle("Depression Screening Tool")
        self.screenWidth = GetSystemMetrics(0)
        self.screenHeight = GetSystemMetrics(1)
        self.appWidth = 480
        self.appHeight = 640
        self.setGeometry((self.screenWidth-self.appWidth)/2, (self.screenHeight-self.appHeight)/2,self.appWidth,self.appHeight)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layout()
        self.displayResult()

    def mainDesign(self):
        self.setStyleSheet("font-size:12pt;font-family:Arial;margin 10pt;padding:10pt;")
        self.question = QLabel("Result")
        self.question.setStyleSheet("font-size:24pt;font-family:Arial Bold")
        self.table = QTableWidget()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.verticalHeader().hide()
        self.newInputBtn = QPushButton("Export To CSV")
        self.newInputBtn.setFixedSize(150,30)
        self.newInputBtn.clicked.connect(self.export2csv)
        self.exitBtn = QPushButton("Main Manu")
        self.exitBtn.setFixedSize(150,30)
        self.exitBtn.clicked.connect(self.exitEvent)

    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(20,20,20,20)
        self.mainLayout.setStretch(0,1)
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QHBoxLayout()

        self.mainLayout.addLayout(self.topLayout,80)
        self.mainLayout.addLayout(self.bottomLayout,20)
        self.topLayout.addWidget(self.question,20,alignment=Qt.AlignCenter)
        self.topLayout.addWidget(self.table,80)
        self.bottomLayout.addWidget(self.newInputBtn)
        self.bottomLayout.addStretch()
        self.bottomLayout.addWidget(self.exitBtn)

        self.setLayout(self.mainLayout)

    def displayResult(self):
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderItem(0,QTableWidgetItem("Sentence"))
        self.table.setHorizontalHeaderItem(1,QTableWidgetItem("Category"))
        #print(len(self.result))
        self.table.setRowCount(len(self.result))
        for i in range(len(self.result)):
            self.table.setItem(i,0,QTableWidgetItem(self.result[i][0]))
            self.table.setItem(i,1,QTableWidgetItem(self.result[i][1]))
        
        self.table.resizeColumnsToContents()

    def export2csv(self):
        df = pd.DataFrame(self.result, columns=["Text","Label"])
        df.to_csv("output.csv")
        QMessageBox.information(self, "Success", "The result has been exported ")

    def exitEvent(self):
        self.exitWin = mainWindow()
        self.close()

def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()