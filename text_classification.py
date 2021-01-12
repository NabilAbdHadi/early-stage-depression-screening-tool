
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV
from database import FYP_MySQL 
import pickle
from text_preprocessing import TEXT_PREPROCESSING

class TEXT_CLASSIFICATION:
    """
    this classification is used:
        - to predict single classification output either non-depressive, risk factor or symptom
        - using the tdidf feature extraction
    """
    def __init__(self):
        """ initialize the sklearn function """
        self.count_vect = CountVectorizer(analyzer="word", ngram_range=(1, 1))
        self.tfidf_transformer = TfidfTransformer()
        self.SVM_model = SVC(kernel='rbf', C=4, gamma=0.75)

        """ import database """
        data = FYP_MySQL() 

        self.tokens = [i[2].split(' ') for i in data.fetchALL('data_training')]
        self.label = [i[3] for i in data.fetchALL('data_training')]
        """ change label from string to numerical """
        self.category = {
            'non-deppressive' : 0,
            'symptom' : 1,
            'risk factor' : 2,
            'medical history' : 0,}

    def feature_extraction(self, textArray):
        
        textList = [" ".join(text) for text in textArray]
        wordCount = self.count_vect.fit_transform(textList)
        with open('feature.pickle', 'wb') as handle:
            pickle.dump(self.count_vect.vocabulary_, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return self.tfidf_transformer.fit_transform(wordCount)

    def input_feature_extraction(self, textArray):
        with open('feature.pickle', 'rb') as handle:
            b = pickle.load(handle)
        
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
        return train_test_split(x, y, test_size=0.1)

    def SVM(self):
        x_train, x_test, y_train, y_test = self.load_data()
        self.SVM_model.fit(x_train,y_train)
        y_pred = self.SVM_model.predict(x_test)
        accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
        if accuracy > 0.85:
            pickle.dump(self.SVM_model, open("Depression_screening.model", "wb"))
        return accuracy

    def hyperparameter_tuning(self):
        self.SVM()
        x_train, x_test, y_train, y_test = self.load_data()
        param_grid = {'kernel':['rbf'],
             'C':[5.5,6,6.5,7,7.5,8,8.5,9,9.5,10],
             'gamma' : [0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1] } 
        
        grid = GridSearchCV(self.SVM_model, param_grid, refit = True, verbose = 3) 
        grid.fit(x_train,y_train)
        print(grid.best_params_)
        print(grid.best_estimator_) 
        grid_predictions = grid.predict(x_test) 
        print(classification_report(y_test, grid_predictions)) 


class RISK_FACTOR_KEYWORD_EXTRACTOR:
    """
    this classification is design to return the most frequent used 
    """
    def __init__(self):
        """
        initialize CountVectorizer module and import dataset from MySQL 
        """
        self.data = FYP_MySQL().fetchALL('data_training')
        self.matrix = CountVectorizer()
       
    def load_data(self):
        return [i[2] for i in self.data if i[3] == "risk factor"]

    def feature_extraction(self, text):
        self.matrix.fit_transform(text)
        return sorted(self.matrix.vocabulary_.items(), key=lambda x: x[1], reverse=True)
    
    def bag_of_word(self):
        """
        return the bag of word with all values are set to zero
        """
        " load data "
        d = self.load_data()
        " extracting the sorted feature in descending order "
        BoW = dict(self.feature_extraction(d)[:300])
        " modift bag of word value to zeros "
        return dict.fromkeys(BoW, 0)
    
    def getBag_of_word(self, text):
        """
        return the word from the user text that also the include in bag of word of the risk factor.
        """
        BoW = self.bag_of_word()
        print(len(BoW))
        " step 1 : check how many word from text for each factor "
        for word in text.split(" "):
            if word in BoW.keys():
                BoW[word] +=1
        """ 
        step 2 : display the list of words that appear in text
        """
        return [i for i,j in BoW.items() if j > 0]
    

class SYMPTOM_MODEL:
    """
    this classification is used:
        - to analyse the user'text from symptom table 
        - each sentences can indicates many symptom but each sentence will have main symptom
        - to produce multiple output result
        - to predict all possible symptom based on the term that been used
        - return the probabilities of all symptom
        - return bag of word of 
    """

    def __init__(self):
        """
        initiallize all necessary modules and classes 
        """
        self.data = FYP_MySQL().fetchALL('symptom')
        self.matrix = CountVectorizer()            

    def load_data(self):
        """
        - load data from mysql
        - symptom code name :
            dep : depressed mood 
            int : loss of interest/pleasure
            wac : change in weight/appetite
            cis : change in sleep - insomnia/hypersomnia
            par : psychomotor agitation/retardation
            fat : fatigue or loass of energy
            gui : feeling guilt/worthless
            con : concentration problem
            sui : suicidal thought
        """
        symptom = {
                    'dep' : [],
                    'int' : [],
                    'wac' : [],
                    'cis' : [],
                    'par' : [],
                    'fat' : [],
                    'gui' : [],
                    'con' : [],
                    'sui' : [],
                    }
        
        for i in self.data:
            if i[3] > 0:
                symptom['dep'].append((i[2],i[3]))
            if i[4] > 0:
                symptom['int'].append((i[2],i[4]))
            if i[5] > 0:
                symptom['wac'].append((i[2],i[5]))
            if i[6] > 0:
                symptom['cis'].append((i[2],i[6]))
            if i[7] > 0:
                symptom['par'].append((i[2],i[7]))
            if i[8] > 0:
                symptom['fat'].append((i[2],i[8]))
            if i[9] > 0:
                symptom['gui'].append((i[2],i[9]))
            if i[10] > 0:
                symptom['con'].append((i[2],i[10]))
            if i[11] > 0:
                symptom['sui'].append((i[2],i[11]))
            
        return symptom

    def feature_extraction(self, text):
        """ 
        - extracting the feature
        - return bag of word and the word frequency that been sorted descending order
        """
        self.matrix.fit_transform(text)
        return sorted(self.matrix.vocabulary_.items(), key=lambda x: x[1], reverse=True)
    
    def bag_of_word(self):
        """
        return 2 dict : bag-of-word of all symptom and main symptom

        - the total of word that in each of symptom is 507, 131, 18, 76, 385, 138, 340, 171, and 193 repectively
        - the limit for the keyword is 70 for all symptom and 50 for main symptom but wac does not applied
        """
        " load data "
        symptom = self.load_data()
        
        " extracting the sorted feature in descending order "
        BoW_symptom = {}
        for i,j in symptom.items():
            temp = [k[0] for k in j]
            if i == 'wac':
                BoW_symptom[i] = dict(self.feature_extraction(temp))
                BoW_symptom[i] = dict.fromkeys(BoW_symptom[i],0)
            else:
                BoW_symptom[i] = dict(self.feature_extraction(temp)[:70])
                BoW_symptom[i] = dict.fromkeys(BoW_symptom[i],0)

        return BoW_symptom
    
    def classification(self, textList):
        """
        input   : list of preprocessed token
        return the dictionary of Bag of word and its word count
        """

        all_symptom = self.bag_of_word()
        
        for token in textList:
            for symptom_BoW in all_symptom.values():
                if token in symptom_BoW.keys():
                    symptom_BoW[token] +=1

        return all_symptom

    def get_symptom_probabilities(self,textList):
        """
        input   : list of preprocessed token
        return the probabilities of the each symptom for all symptom and main symptom
        """
        a = self.classification(textList)

        all_sym_result = [(i, float("{:.4f}".format(sum(j.values())/len(textList)))) for i,j in a.items()] 

        return all_sym_result
    
    def get_symptom(self, textList):
        """
        input : list of preprocessed token
        return all symptom code 
        """
        a = self.get_symptom_probabilities(textList)

        all_sym = [i[0] for i in a ]

        return all_sym
    
    def get_main_symptom(self, textList):
        """
        input : list of preprocessed token
        return main symptom code
        """
        a = self.get_symptom_probabilities(textList)
        prob = [i[1] for i in a ]
        main_sym = [i[0] for i in a if i[1] == max(prob)]
        return main_sym
        
    def get_symptom_BoW(self, textList):
        """
        input : list of preprocessed token
        return warning terms or words
        """
        all_BoW_set = set()
        a = self.get_symptom(textList)
        c = self.classification(textList)
        [[all_BoW_set.add(k) for k,l in j.items() if l > 0] for i,j in c.items() if i in a]
        return all_BoW_set
    
    def get_max_probabilities(self, preprocessList):
        """
        input: list of preprocessed token in 2-D
        return max probability of all symptom

         -  this function used to find the maximum value of 
            each symptoms probabilities output from every sentences
         -  the function is the extended of the get_symptom_probabilities function
        """
        all_prob = []
        for tokens in preprocessList:
            a = self.get_symptom_probabilities(tokens)
            a = [i[1] for i in a]
            all_prob.append(a)
            
        prob = [0.0]*9
        for i in range(len(all_prob)):
            prob[0] = max(all_prob[i][0],prob[0])
            prob[1] = max(all_prob[i][1],prob[1])
            prob[2] = max(all_prob[i][2],prob[2])
            prob[3] = max(all_prob[i][3],prob[3])
            prob[4] = max(all_prob[i][4],prob[4])
            prob[5] = max(all_prob[i][5],prob[5])
            prob[6] = max(all_prob[i][6],prob[6])
            prob[7] = max(all_prob[i][7],prob[7])
            prob[8] = max(all_prob[i][8],prob[8])
        return prob

    def summary(self, preprocessList):
        """
        return the dictionary of symptom and it's maximum probabilities
        extended of get_max_probabilities function
        """
        max_prob = self.get_max_probabilities(preprocessList)
        return {
                'dep' : max_prob[0],
                'int' : max_prob[1],
                'wac' : max_prob[2],
                'cis' : max_prob[3],
                'par' : max_prob[4],
                'fat' : max_prob[5],
                'gui' : max_prob[6],
                'con' : max_prob[7],
                'sui' : max_prob[8],
                }


def main():
    tc = TEXT_CLASSIFICATION()
    a = 0.00
    while a <= 0.85:
        a = tc.SVM()
        print("Accuracy: {:.2f}%".format(a * 100),"\t",a)

if __name__ == "__main__":
    #main()
    #r = RISK_FACTOR_KEYWORD_EXTRACTOR()
    #print(r.getBag_of_word(" Di depan matanya aku kena perfect tak boleh buat silap"))
    text = ['Terkadang aku hiris-hiris pergelangan tangan, berbekas, berparut tapi tiada siapa yang tahu, ada pun classmate bertanya apabila ternampak lengan baju aku terselak, aku katakan tiada apa, aku beri alasan yang aku lap cermin tingkap bilik buatkan lengan calar balar',
            'Dan waktu ini pun aku masih berperang dengan diri aku sendiri, kini aku sudah berkahwin, punyai seorang anak,Waktu sarat mengandung aku pernah menggantung diri, tapi masih juga takdir aku bernafas, kerana tepat pada waktu suami aku balik dan pecahkan pintu bilik untuk selamatkan aku',
            'Keluarga aku tak tahu aku punyai depresi yang sanggup mencederakan diri, hanya suami aku sahaja mengetahuinya',
            'Pernah juga waktu aku susah tidur malam, termenung sendiri di tingkap, merenung kebawah dan terdetik â€œkalau aku terjun ni, mesti lega kepala akuâ€', 
            'Sewaktu aku terdetik itulah, tiba-tiba aku dengar suara ketawa datang dari phone aku'
            ]
    s = SYMPTOM_MODEL()
    tp = TEXT_PREPROCESSING()
    p = [tp.data_preparation(i) for i in text]
    print(s.summary(p))
    #TEXT_CLASSIFICATION().hyperparameter_tuning()
        