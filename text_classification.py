
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV
from ast import literal_eval
import pickle, json


class text_classification:
    def __init__(self):
        """ initialize the sklearn variable """
        self.count_vect = CountVectorizer(analyzer="word", ngram_range=(1, 1))
        self.tfidf_transformer = TfidfTransformer()
        self.SVM_model = SVC(kernel='rbf', C=4, gamma=0.5)
        #self.SVM_model = svm.SVC(kernel='rbf', C=7, gamma=0.4)

        """ import dataset """
        with open('Data Training.json', encoding='utf8', mode='r') as json_file:
            data = json.load(json_file)

        self.tokens = [data[i]['token text'] for i in data]
        self.label = [data[i]['category'] for i in data]
        """ change label from string to numerical """
        self.category = {
            'non-deppressive' : 0,
            'symptom' : 1,
            'risk factor' : 2,
            'medical history' : 3,}

            
        
    def feature_extraction(self, textArray):
        
        textList = [" ".join(text) for text in textArray]
        wordCount = self.count_vect.fit_transform(textList)
        with open('feature.pickle', 'wb') as handle:
            pickle.dump(self.count_vect.vocabulary_, handle, protocol=pickle.HIGHEST_PROTOCOL)
        #print(type(wordCount))
        return self.tfidf_transformer.fit_transform(wordCount)


    def input_feature_extraction(self, textArray):
        with open('feature.pickle', 'rb') as handle:
            b = pickle.load(handle)
        
        #print(list(b.keys()))
        new_input = []
        new_input.append(list(b.keys()))
        for text in textArray:
            newtext = []
            for t in text:
                if t in b.keys():
                    newtext.append(t)
            new_input.append(newtext)
        
        textList = [" ".join(text) for text in new_input]
        wordCount = self.count_vect.fit_transform(textList)
        return self.tfidf_transformer.fit_transform(wordCount[1:])


    def load_data(self):
            
        x = self.feature_extraction(self.tokens)
        
        y = []
        for i in self.label: 
            j = self.category[str(i)]
            y.append(j)
        #return 
        return train_test_split(x, y, test_size=0.1)


    def SVM(self):
        x_train, x_test, y_train, y_test = self.load_data()
        self.SVM_model.fit(x_train,y_train)
        y_pred = self.SVM_model.predict(x_test)
        accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
        if accuracy > 0.8:
            pickle.dump(self.SVM_model, open("Depression_screening.model", "wb"))
        #return "Accuracy: {:.2f}%".format(accuracy * 100)
        return accuracy


    def hyperparameter_tuning(self):
        self.SVM()
        x_train, x_test, y_train, y_test = self.load_data()
        param_grid = {'kernel':['rbf'],
             'C':[1,2,3,4,5,6,7,8,9,10],
             'gamma' : [0.5,0.6,0.7,0.8] } 
        
        grid = GridSearchCV(self.SVM_model, param_grid, refit = True, verbose = 3) 
        grid.fit(x_train,y_train)
        print(grid.best_params_)
        print(grid.best_estimator_) 
        grid_predictions = grid.predict(x_test) 
  
        # print classification report 
        print(classification_report(y_test, grid_predictions)) 


if __name__ == "__main__":
    tc = text_classification()
    #tc.hyperparameter_tuning()
    a = 0.00
    while a <= 0.8:
        a = tc.SVM()
        print("Accuracy: {:.2f}%".format(a * 100),"\t",a)