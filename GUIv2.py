from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pandas as pd
import sys, os, joblib
from nltk.tokenize import sent_tokenize
from win32api import GetSystemMetrics
from text_preprocessing import TEXT_PREPROCESSING
from text_classification import TEXT_CLASSIFICATION
from text_classification import RISK_FACTOR_BoW
from text_classification import SYMPTOM_MODEL

my_tp = TEXT_PREPROCESSING()
my_tc = TEXT_CLASSIFICATION()

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
            textlist = sent_tokenize(text)
            sentences = [my_tp.data_preparation(s) for s in textlist if s != "" or s == None]
            sentences = [s for s in sentences if len(s) > 0]
            resultList = []
            predict = self.predicting_text(sentences)
            for (t,s,p) in zip(textlist,sentences, predict):
                resultList.append([t,s,p])

            file.close()
            self.close()
            self.newWindow = resultWindow(resultList)

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
        if text == None or text == "" or len(text) == 0:
            QMessageBox.information(self, 
                                    "Warning", "No text was inserted\n"+
                                    "The system cannot be process\n"+
                                    "Please insert the text")
        elif len(text) <= 20:
             QMessageBox.information(self, "Warning", "The text is too short\n"+
                                            "Please insert more word so the system can process properly")
        else:
            textlist = sent_tokenize(text)
            sentences = [my_tp.data_preparation(s) for s in textlist if s != ""]
            sentences = [s for s in sentences if len(s) > 0]
            predict = self.predicting_text(sentences)
            resultList=[]
            for (t,s,p) in zip(textlist,sentences, predict):
                    resultList.append([t,s,p])

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
        self.result = textlist#[i for i in textlist if i[2] != 'non-deppressive']
        self.setWindowTitle("Depression Screening Tool")
        self.screenWidth = GetSystemMetrics(0)
        self.screenHeight = GetSystemMetrics(1)
        self.appWidth = 960
        self.appHeight = 720
        self.setGeometry((self.screenWidth-self.appWidth)/2, 
                            (self.screenHeight-self.appHeight)/2,
                            self.appWidth,self.appHeight)

        self.symptom = {
                        'dep' : 'depressed mood',
                        'int' : 'loss of interest or pleasure',
                        'wac' : 'change in weight or appetite',
                        'cis' : 'change in sleep',
                        'par' : 'psychomotor agitation or retardation',
                        'fat' : 'fatigue or loss of energy',
                        'gui' : 'feeling guilt or worthless',
                        'con' : 'concentration problem',
                        'sui' : 'suicidal thought',
                        }

        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layout()
        self.displayResult()

    def mainDesign(self):
        self.setStyleSheet("font-size:12pt;font-family:Arial;margin 10pt;padding:10pt;")
        self.main_title = QLabel("Result")
        self.main_title.setStyleSheet("font-size:24pt;font-family:Arial Bold")
        self.subtitle = QLabel("The list of risk factor(s) and symptom(s) that existed in the user's text\n"+
                                "*To see the list of warning words, double click the text")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.table = QTableWidget()
        self.table.verticalHeader().hide()
        self.table.setWordWrap(False)
        self.table.resizeRowsToContents()

        self.exportBtn = QPushButton("Export To CSV")
        self.exportBtn.setFixedSize(150,30)
        self.exportBtn.clicked.connect(self.export2csv)

        self.sumBtn = QPushButton("Summary")
        self.sumBtn.setFixedSize(150,30)
        self.sumBtn.clicked.connect(self.summaryEvent)

    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(20,20,20,20)
        self.mainLayout.setStretch(0,1)
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QHBoxLayout()

        self.mainLayout.addLayout(self.topLayout,80)
        self.mainLayout.addLayout(self.bottomLayout,20)
        self.topLayout.addWidget(self.main_title,10,alignment=Qt.AlignCenter)
        self.topLayout.addWidget(self.subtitle,10,alignment=Qt.AlignCenter)
        self.topLayout.addWidget(self.table,80)
        self.bottomLayout.addWidget(self.exportBtn)
        self.bottomLayout.addStretch()
        self.bottomLayout.addWidget(self.sumBtn)

        self.setLayout(self.mainLayout)

    def displayResult(self):
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderItem(0,QTableWidgetItem("Sentence"))
        self.table.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.table.setHorizontalHeaderItem(1,QTableWidgetItem("Category"))
        self.table.setColumnWidth(1,150)
        self.table.setRowCount(len(self.result))
        
        for i in range(len(self.result)):
            self.table.setItem(i,0,QTableWidgetItem(self.result[i][0]))
            self.table.setItem(i,1,QTableWidgetItem(self.result[i][2]))
        
        
        self.table.doubleClicked.connect(self.doubleClickedEvent)

    def doubleClickedEvent(self):
        """
        docstring
        """
        risk = RISK_FACTOR_BoW()
        symptom = SYMPTOM_MODEL()
        row = self.table.currentItem().row()
        row_ele = self.result[row]

        r = risk.getBag_of_word(" ".join(row_ele[1]))
        r = ", ".join(r)

        s = symptom.get_symptom_BoW(row_ele[1])
        all, main = symptom.get_symptom(row_ele[1])
        all = [self.symptom[i] for i in all]
        all = ", ".join(all)
        main = self.symptom[main[0]]
        s = ", ".join(s)
        if row_ele[2] == 'risk factor':
            QMessageBox.information(self, 
                                    "Risk Factor", 
                                    "list of warning words:-\n{}".format(r))
        elif row_ele[2] == 'symptom':
            QMessageBox.information(self, 
                                    "Symptom found", 
                                    "Main Symptom : \t{}\n".format(main)+
                                    "Others Symptom : \n{}\n\n".format(all)+
                                    "list of warning words:-\n{}".format(s))
            
    def export2csv(self):
        df = pd.DataFrame(self.result, columns=["Text","Preprocessed","Label"])
        df.to_csv("output.csv")
        QMessageBox.information(self, "Success", "The result has been exported ")

    def summaryEvent(self):
        self.sumWin = summaryWindow(self.result)
        self.close()


class summaryWindow(QWidget):
    def __init__(self,textlist):
        super().__init__()
        self.sym_model = SYMPTOM_MODEL()
        self.result = [i[1] for i in textlist if i[2] == 'symptom']

        self.symptom = {
                        'dep' : 'Depressed mood',
                        'int' : 'Loss of interest or pleasure',
                        'wac' : 'Change in weight or appetite',
                        'cis' : 'Change in sleep',
                        'par' : 'Psychomotor agitation or retardation',
                        'fat' : 'Fatigue or loss of energy',
                        'gui' : 'Feeling guilt or worthless',
                        'con' : 'Concentration problem',
                        'sui' : 'Suicidal thought',
                        }
        self.user_symptom = self.sym_model.summary(self.result)
        


        self.setWindowTitle("Depression Screening Tool")
        self.screenWidth = GetSystemMetrics(0)
        self.screenHeight = GetSystemMetrics(1)
        self.appWidth = 480
        self.appHeight = 600
        self.setGeometry((self.screenWidth-self.appWidth)/2, 
                            (self.screenHeight-self.appHeight)/2,
                            self.appWidth,self.appHeight)
        
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layout()
        self.displaySymptomList()
    
    def mainDesign(self):
        self.setStyleSheet("font-size:12pt;font-family:Arial;margin 10pt;padding:10pt;")
        self.main_title = QLabel("Summary")
        self.main_title.setStyleSheet("font-size:24pt;font-family:Arial Bold")
        self.subtitle = QLabel()
        self.subtitle.setAlignment(Qt.AlignCenter)
        
        self.symptom_list = QListWidget()
        self.symptom_list.setStyleSheet("font-size:14pt")
        
        self.symptom_prob_list = QListWidget()
        self.symptom_prob_list.setStyleSheet("font-size:14pt")
        

        self.newBtn = QPushButton("Main Menu")
        self.newBtn.setFixedSize(150,30)
        self.newBtn.clicked.connect(self.newInputEvent)
        self.exitBtn = QPushButton("Exit")
        self.exitBtn.setFixedSize(150,30)
        self.exitBtn.clicked.connect(self.close)

    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(20,20,20,20)
        self.mainLayout.setStretch(0,1)
        self.topLayout = QVBoxLayout()
        self.topBottomLayout = QHBoxLayout()
        self.topBottomLayout.setContentsMargins(0,0,0,0)
        self.bottomLayout = QHBoxLayout()

        self.mainLayout.addLayout(self.topLayout,80)
        self.mainLayout.addLayout(self.bottomLayout,20)
        self.topLayout.addWidget(self.main_title,10, alignment=Qt.AlignCenter)
        self.topLayout.addWidget(self.subtitle,10, alignment=Qt.AlignCenter)
        self.topLayout.addLayout(self.topBottomLayout,60)
        self.topBottomLayout.addWidget(self.symptom_list,60)
        self.topBottomLayout.addWidget(self.symptom_prob_list,30)
        self.bottomLayout.addWidget(self.newBtn)
        self.bottomLayout.addStretch()
        self.bottomLayout.addWidget(self.exitBtn)

        self.setLayout(self.mainLayout)

    def displaySymptomList(self):
        self.symptom_list.addItem("Symptom")
        self.symptom_prob_list.addItem("Probability")
        numOfSym = 0
        for i,j in self.user_symptom.items():
            self.symptom_list.addItem(self.symptom[i])
            self.symptom_prob_list.addItem("{} %".format(j*100))
            if j > 0.5:
                numOfSym +=1
        if numOfSym > 5:
            self.subtitle.setText("There are {} symptom(s) that have high probabilities existed in the User.\nUser might already in depression".format(numOfSym))
        elif numOfSym > 0:
            self.subtitle.setText("There are {} symptom(s) that have high probabilities existed in the User.\nPlease be careful and take care for yourself".format(numOfSym))
        else:
            self.subtitle.setText("There is none symptom exists in the User")


    def newInputEvent(self):
        self.newWin = mainWindow()
        self.close()


def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()